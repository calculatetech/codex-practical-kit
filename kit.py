#!/usr/bin/env python3
"""Install and remove the Codex Practical Kit without owning a new runtime."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

KIT_ID = "codex-practical-kit"
KIT_VERSION = "0.3.0"
ROOT = Path(__file__).resolve().parent
AGENTS_START = "<!-- codex-practical-kit:start -->"
AGENTS_END = "<!-- codex-practical-kit:end -->"
REPOWISE_START = "# >>> codex-practical-kit:repowise >>>"
REPOWISE_END = "# <<< codex-practical-kit:repowise <<<"
HOOK_HANDLER_BASENAMES = {"session_start.py", "stop_gate.py", "stop_docs.py", "session_end.py"}
INSTALLED_HOOK_BASENAMES = {"session_start.py", "stop_gate.py", "session_end.py"}
CUSTOM_SKILLS = (
    "docs-maintainer",
    "roadmap-maintainer",
    "research-first",
    "task-brief",
    "design-preflight",
    "adversarial-review",
)
UPSTREAM_SKILLS = ("ponytail", "simple-english")
ALL_SKILLS = (*UPSTREAM_SKILLS, *CUSTOM_SKILLS)


class KitError(RuntimeError):
    """A safe, user-actionable failure."""


@dataclass(frozen=True)
class InstallPaths:
    home: Path
    codex_home: Path
    skills_home: Path
    install_root: Path

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "InstallPaths":
        home = Path(args.home).expanduser().resolve() if getattr(args, "home", None) else Path.home()
        codex_home = (
            Path(args.codex_home).expanduser().resolve()
            if getattr(args, "codex_home", None)
            else Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser().resolve()
        )
        skills_home = (
            Path(args.skills_home).expanduser().resolve()
            if getattr(args, "skills_home", None)
            else (home / ".agents" / "skills").resolve()
        )
        data_base = Path(os.environ.get("XDG_DATA_HOME", home / ".local" / "share")).expanduser()
        install_root = (
            Path(args.install_root).expanduser().absolute()
            if getattr(args, "install_root", None)
            else (data_base / KIT_ID).absolute()
        )
        return cls(
            home=home,
            codex_home=codex_home,
            skills_home=skills_home,
            install_root=install_root,
        )


# ---------- generic helpers ----------


def write_file(path: Path, data: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, bytes):
        path.write_bytes(data)
    else:
        path.write_text(data, encoding="utf-8", newline="")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise KitError(f"Command not found: {command[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise KitError(f"Command timed out: {shlex.join(command)}") from exc
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise KitError(f"Command failed ({result.returncode}): {shlex.join(command)}\n{detail}")
    return result


def command_version(command: list[str]) -> str | None:
    try:
        result = run(command, check=False, timeout=20)
    except KitError:
        return None
    text = (result.stdout or result.stderr).strip()
    return text.splitlines()[0] if text else None


def json_load(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise KitError(f"Invalid JSON. Fix this file before installation: {path}\n{exc}") from exc


def marker_block(text: str, start: str, end: str, body: str) -> str:
    block = f"{start}\n{body.rstrip()}\n{end}"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(block, text, count=1).rstrip() + "\n"
    prefix = text.rstrip()
    return ((prefix + "\n\n") if prefix else "") + block + "\n"


def remove_marker_block(text: str, start: str, end: str) -> str:
    pattern = re.compile(r"\n?" + re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.DOTALL)
    result = pattern.sub("\n", text, count=1)
    result = re.sub(r"\n{3,}", "\n\n", result).strip()
    return result + ("\n" if result else "")


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def relative_or_absolute(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


# ---------- upstream skill material ----------


def load_lock() -> dict[str, Any]:
    value = json.loads((ROOT / "upstream.lock.json").read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise KitError("Unsupported upstream.lock.json schema")
    return value


def raw_github_url(repository: str, commit: str, source_path: str) -> str:
    match = re.fullmatch(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?", repository.rstrip("/"))
    if not match:
        raise KitError(f"Unsupported repository URL: {repository}")
    owner, repo = match.groups()
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{source_path}"


def download_file(url: str, expected_blob: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": f"{KIT_ID}/{KIT_VERSION}"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise KitError(f"Could not download pinned upstream file:\n{url}\n{exc}") from exc
    actual = git_blob_sha1(data)
    if actual != expected_blob:
        raise KitError(
            "Downloaded upstream file did not match the pinned Git blob. "
            f"Expected {expected_blob}, got {actual}: {url}"
        )
    return data


def stage_upstream_skills(destination: Path) -> dict[str, dict[str, Any]]:
    lock = load_lock()
    records: dict[str, dict[str, Any]] = {}
    for skill_name, skill in lock["skills"].items():
        repo = skill["repository"]
        commit = skill["commit"]
        skill_root = destination / skill_name
        for item in skill["files"]:
            data = download_file(raw_github_url(repo, commit, item["path"]), item["git_blob_sha1"])
            target = destination / item["destination"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        records[skill_name] = {
            "repository": repo,
            "commit": commit,
            "license": skill["license"],
        }
    return records


# ---------- skills ----------


def copy_custom_skills(destination: Path) -> None:
    source = ROOT / "assets" / "skills"
    for name in CUSTOM_SKILLS:
        shutil.copytree(source / name, destination / name, dirs_exist_ok=True)


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def install_skills(
    paths: InstallPaths, source_root: Path, owned_names: set[str]
) -> list[dict[str, str]]:
    paths.skills_home.mkdir(parents=True, exist_ok=True)
    for name in ALL_SKILLS:
        destination = paths.skills_home / name
        if name in owned_names:
            remove_path(destination)
        shutil.copytree(source_root / name, destination)
    return [{"name": name} for name in ALL_SKILLS]


# ---------- AGENTS.md ----------


def install_global_agents(paths: InstallPaths) -> None:
    agents = paths.codex_home / "AGENTS.md"
    body = (ROOT / "assets" / "AGENTS.block.md").read_text(encoding="utf-8").rstrip()
    updated = marker_block(read_text(agents), AGENTS_START, AGENTS_END, body)
    write_file(agents, updated)


def uninstall_global_agents(paths: InstallPaths) -> None:
    agents = paths.codex_home / "AGENTS.md"
    if not agents.exists():
        return
    updated = remove_marker_block(read_text(agents), AGENTS_START, AGENTS_END)
    if updated:
        write_file(agents, updated)
    else:
        agents.unlink()


# ---------- hooks ----------


def hook_command(python: Path, script: Path) -> tuple[str, str]:
    posix = f"{shlex.quote(str(python))} {shlex.quote(str(script))}"
    windows = subprocess.list2cmdline([str(python), str(script)])
    return posix, windows


def handler_is_ours(handler: Any, hook_root: Path) -> bool:
    if not isinstance(handler, dict):
        return False
    commands = (
        (str(handler.get("command") or ""), True),
        (str(handler.get("commandWindows") or ""), False),
    )
    for command, posix in commands:
        try:
            parts = shlex.split(command, posix=posix)
        except ValueError:
            continue
        if len(parts) == 2 and parts[1].strip('"') in {
            str(hook_root / name) for name in HOOK_HANDLER_BASENAMES
        }:
            return True
    return False


def remove_our_hooks(data: dict[str, Any], hook_root: Path) -> dict[str, Any]:
    hooks = data.get("hooks")
    if not isinstance(hooks, dict):
        return data
    for event in list(hooks):
        groups = hooks.get(event)
        if not isinstance(groups, list):
            continue
        kept_groups = []
        for group in groups:
            if not isinstance(group, dict):
                kept_groups.append(group)
                continue
            handlers = group.get("hooks")
            if not isinstance(handlers, list):
                kept_groups.append(group)
                continue
            kept_handlers = [
                handler for handler in handlers if not handler_is_ours(handler, hook_root)
            ]
            if kept_handlers:
                copy = dict(group)
                copy["hooks"] = kept_handlers
                kept_groups.append(copy)
        if kept_groups:
            hooks[event] = kept_groups
        else:
            hooks.pop(event, None)
    if not hooks:
        data.pop("hooks", None)
    return data


def load_hooks_config(paths: InstallPaths) -> dict[str, Any]:
    hooks_path = paths.codex_home / "hooks.json"
    data = json_load(hooks_path, {})
    if not isinstance(data, dict):
        raise KitError(f"Expected a JSON object in {hooks_path}")
    hooks = data.get("hooks")
    if hooks is not None and not isinstance(hooks, dict):
        raise KitError(f"Expected `hooks` to be an object in {hooks_path}")
    if isinstance(hooks, dict):
        for event in ("SessionStart", "Stop", "SessionEnd"):
            if event in hooks and not isinstance(hooks[event], list):
                raise KitError(f"Expected hooks.{event} to be a list in {hooks_path}")
    return data


def install_hooks(paths: InstallPaths) -> None:
    hooks_path = paths.codex_home / "hooks.json"
    data = load_hooks_config(paths)
    hook_root = paths.install_root / "hooks"
    data = remove_our_hooks(data, hook_root)
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise KitError(f"Expected `hooks` to be an object in {hooks_path}")

    py = Path(sys.executable).resolve()
    definitions = (
        (
            "SessionStart",
            {
                "matcher": "startup|resume|clear|compact",
                "hooks": [
                    {
                        "type": "command",
                        "command": hook_command(py, hook_root / "session_start.py")[0],
                        "commandWindows": hook_command(py, hook_root / "session_start.py")[1],
                        "timeout": 10,
                        "statusMessage": "Loading practical defaults",
                        "additionalContextLimit": 1200,
                    }
                ],
            },
        ),
        (
            "Stop",
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": hook_command(py, hook_root / "stop_gate.py")[0],
                        "commandWindows": hook_command(py, hook_root / "stop_gate.py")[1],
                        "timeout": 20,
                        "statusMessage": "Checking review and documentation evidence",
                    }
                ]
            },
        ),
        (
            "SessionEnd",
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": hook_command(py, hook_root / "session_end.py")[0],
                        "commandWindows": hook_command(py, hook_root / "session_end.py")[1],
                        "timeout": 3,
                    }
                ]
            },
        ),
    )
    for event, group in definitions:
        current = hooks.setdefault(event, [])
        if not isinstance(current, list):
            raise KitError(f"Expected hooks.{event} to be a list in {hooks_path}")
        current.append(group)
    write_file(hooks_path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def uninstall_hooks(paths: InstallPaths) -> None:
    hooks_path = paths.codex_home / "hooks.json"
    if not hooks_path.exists():
        return
    data = json_load(hooks_path, {})
    if not isinstance(data, dict):
        raise KitError(f"Expected a JSON object in {hooks_path}")
    data = remove_our_hooks(data, paths.install_root / "hooks")
    if data:
        write_file(hooks_path, json.dumps(data, indent=2, sort_keys=True) + "\n")
    else:
        hooks_path.unlink()


# ---------- core install lifecycle ----------


def manifest_path(paths: InstallPaths) -> Path:
    return paths.install_root / "install-manifest.json"


def install_core(args: argparse.Namespace, paths: InstallPaths) -> None:
    paths.install_root.parent.mkdir(parents=True, exist_ok=True)
    paths.install_root.mkdir(parents=True, exist_ok=True)
    previous_manifest = json_load(manifest_path(paths), {})
    previous_records = (
        previous_manifest.get("skills", [])
        if isinstance(previous_manifest, dict)
        and previous_manifest.get("skills_home") == str(paths.skills_home)
        else []
    )
    owned_names = {
        str(item.get("name"))
        for item in previous_records
        if isinstance(item, dict) and item.get("name") in ALL_SKILLS
    }
    staging = Path(tempfile.mkdtemp(prefix="stage-", dir=paths.install_root.parent))
    try:
        skill_stage = staging / "skills"
        skill_stage.mkdir(parents=True)
        upstream_records = stage_upstream_skills(skill_stage)
        copy_custom_skills(skill_stage)
        conflicts = [
            paths.skills_home / name
            for name in ALL_SKILLS
            if (paths.skills_home / name).exists() and name not in owned_names
        ]
        if conflicts:
            raise KitError(
                "These skill directories already exist and are not owned by this kit:\n- "
                + "\n- ".join(map(str, conflicts))
            )
        load_hooks_config(paths)

        shutil.copytree(ROOT / "assets" / "hooks", paths.install_root / "hooks", dirs_exist_ok=True)
        obsolete_hook = paths.install_root / "hooks" / "stop_docs.py"
        if obsolete_hook.exists():
            obsolete_hook.unlink()
        shutil.copy2(ROOT / "upstream.lock.json", paths.install_root / "upstream.lock.json")
        shutil.copy2(ROOT / "LICENSE", paths.install_root / "LICENSE")

        records = install_skills(paths, skill_stage, owned_names)
        remove_path(paths.install_root / "skills")
        install_global_agents(paths)
        install_hooks(paths)
        manifest = {
            "schema_version": 1,
            "kit_version": KIT_VERSION,
            "installed_at": int(time.time()),
            "codex_home": str(paths.codex_home),
            "skills_home": str(paths.skills_home),
            "install_root": str(paths.install_root),
            "skills": records,
            "upstream": upstream_records,
        }
        write_file(manifest_path(paths), json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def uninstall_skills(paths: InstallPaths) -> None:
    path = manifest_path(paths)
    manifest = json_load(path, {})
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise KitError(f"Unsupported install manifest: {path}")
    records = manifest.get("skills")
    if not isinstance(records, list):
        raise KitError("Expected `skills` to be a list in the install manifest.")
    names: list[str] = []
    for item in records:
        name = item.get("name") if isinstance(item, dict) else None
        if name not in ALL_SKILLS or name in names:
            raise KitError("Found an invalid skill record in the install manifest.")
        names.append(name)
    for name in names:
        remove_path(paths.skills_home / name)


def uninstall_core(args: argparse.Namespace, paths: InstallPaths) -> bool:
    path = manifest_path(paths)
    if not path.exists():
        return False
    manifest = json_load(path, {})
    codex_home = manifest.get("codex_home") if isinstance(manifest, dict) else None
    skills_home = manifest.get("skills_home") if isinstance(manifest, dict) else None
    if not isinstance(codex_home, str) or not isinstance(skills_home, str):
        raise KitError(f"Install manifest is missing recorded destinations: {path}")
    installed = InstallPaths(paths.home, Path(codex_home), Path(skills_home), paths.install_root)
    uninstall_skills(installed)
    uninstall_global_agents(installed)
    uninstall_hooks(installed)
    path.unlink()
    if args.purge and paths.install_root.exists():
        shutil.rmtree(paths.install_root)
    return True


# ---------- RepoWise project integration ----------


def resolve_git_root(path: Path) -> Path:
    result = run(["git", "rev-parse", "--show-toplevel"], cwd=path, timeout=20)
    value = result.stdout.strip()
    if not value:
        raise KitError(f"Not inside a Git repository: {path}")
    return Path(value).resolve()


def repowise_config_block(root: Path, uvx: str) -> str:
    return "\n".join(
        [
            "[mcp_servers.repowise]",
            f"command = {toml_string(uvx)}",
            'args = ["--from", "repowise==0.41.0", "repowise", "mcp"]',
            f"cwd = {toml_string(str(root))}",
            "startup_timeout_sec = 30",
        ]
    )


def repowise_agents_block() -> str:
    return """## RepoWise index

- This repository has a local RepoWise index in `.repowise`.
- Use RepoWise MCP tools for repository overview, symbol context, callers, change risk, decision history, code health, dead code, and affected tests.
- Read source before you treat an inferred relationship or generated page as authoritative.
- If RepoWise is unavailable or stale, continue with native tools. Do not stop the task.
- Refresh the index with `uvx --from repowise==0.41.0 repowise update --no-agents`."""


def ensure_no_external_repowise_table(text: str) -> None:
    stripped = remove_marker_block(text, REPOWISE_START, REPOWISE_END)
    if re.search(r"(?m)^\s*\[mcp_servers\.repowise\]\s*$", stripped):
        raise KitError(
            "A RepoWise MCP table already exists outside this kit's managed block. "
            "Remove or rename that table before setup so there is one owner."
        )


def repowise_command(root: Path, *args: str, timeout: int = 1800) -> subprocess.CompletedProcess[str]:
    uvx = shutil.which("uvx")
    if not uvx:
        raise KitError(
            "RepoWise setup needs `uvx`. Install uv, then rerun this command. "
            "The core Ponytail, SimpleEnglish, docs, and research kit does not need uv."
        )
    return run([uvx, "--from", "repowise==0.41.0", "repowise", *args], cwd=root, timeout=timeout)


def setup_repo(args: argparse.Namespace) -> None:
    root = resolve_git_root(Path(args.repo).expanduser().resolve())
    config = root / ".codex" / "config.toml"
    agents = root / "AGENTS.md"
    config_before = read_text(config)
    agents_before = read_text(agents)
    ensure_no_external_repowise_table(config_before)

    if not (root / ".repowise").exists():
        init_args = [
            "init",
            "--yes",
            "--no-codex",
            "--no-agents",
            "--no-editor-setup",
            "--no-distill-hook",
            "--no-claude-md",
        ]
        if args.prose:
            init_args.extend(["--prose", "--provider", "codex_cli"])
        else:
            init_args.append("--no-prose")
        repowise_command(root, *init_args)

    uvx = shutil.which("uvx")
    assert uvx is not None
    config_after = marker_block(
        config_before,
        REPOWISE_START,
        REPOWISE_END,
        repowise_config_block(root, uvx),
    )
    agents_after = marker_block(
        agents_before,
        AGENTS_START + ":repowise",
        AGENTS_END + ":repowise",
        repowise_agents_block(),
    )
    write_file(config, config_after)
    write_file(agents, agents_after)
    remove_path(root / ".codex-practical-kit")


def remove_repo(args: argparse.Namespace) -> None:
    root = resolve_git_root(Path(args.repo).expanduser().resolve())
    config = root / ".codex" / "config.toml"
    agents = root / "AGENTS.md"
    if config.exists():
        updated = remove_marker_block(read_text(config), REPOWISE_START, REPOWISE_END)
        if updated:
            write_file(config, updated)
        else:
            config.unlink()
    if agents.exists():
        updated = remove_marker_block(
            read_text(agents),
            AGENTS_START + ":repowise",
            AGENTS_END + ":repowise",
        )
        if updated:
            write_file(agents, updated)
        else:
            agents.unlink()
    if args.delete_index and (root / ".repowise").exists():
        shutil.rmtree(root / ".repowise")
    remove_path(root / ".codex-practical-kit")


def update_repowise(args: argparse.Namespace) -> None:
    root = resolve_git_root(Path(args.repo).expanduser().resolve())
    if not (root / ".repowise").exists():
        raise KitError(f"RepoWise is not initialized in {root}")
    repowise_command(root, "update", "--no-agents")


# ---------- diagnostics ----------


def check(condition: bool, label: str, detail: str = "") -> bool:
    mark = "OK" if condition else "FAIL"
    print(f"[{mark}] {label}{(': ' + detail) if detail else ''}")
    return condition


def doctor(args: argparse.Namespace, paths: InstallPaths) -> int:
    ok = True
    manifest = json_load(manifest_path(paths), {})
    ok &= check(isinstance(manifest, dict) and bool(manifest), "core install manifest", str(manifest_path(paths)))
    installed_version = manifest.get("kit_version") if isinstance(manifest, dict) else None
    ok &= check(installed_version == KIT_VERSION, "kit version", str(installed_version or "unknown"))
    for name in ALL_SKILLS:
        dest = paths.skills_home / name
        ok &= check(dest.exists(), f"skill {name}", str(dest))
    agents = paths.codex_home / "AGENTS.md"
    ok &= check(agents.exists() and AGENTS_START in read_text(agents), "global AGENTS block", str(agents))
    hooks_path = paths.codex_home / "hooks.json"
    try:
        hooks_data = json_load(hooks_path, {})
        serialized = json.dumps(hooks_data)
        hooks_ok = all(name in serialized for name in INSTALLED_HOOK_BASENAMES)
    except KitError:
        hooks_ok = False
    ok &= check(hooks_ok, "Codex hooks", str(hooks_path))

    codex_version = command_version(["codex", "--version"])
    ok &= check(bool(codex_version), "Codex CLI", codex_version or "not found")
    if codex_version:
        login = run(["codex", "login", "status"], check=False, timeout=30)
        login_text = (login.stdout or login.stderr).strip().replace("\n", " ")
        ok &= check(login.returncode == 0, "Codex login", login_text[:240])

    if args.repo:
        try:
            root = resolve_git_root(Path(args.repo).expanduser().resolve())
        except KitError as exc:
            ok &= check(False, "repository", str(exc))
        else:
            ok &= check((root / ".repowise").is_dir(), "RepoWise index", str(root / ".repowise"))
            config = read_text(root / ".codex" / "config.toml")
            ok &= check(REPOWISE_START in config, "RepoWise MCP config", str(root / ".codex" / "config.toml"))
            uvx = shutil.which("uvx")
            ok &= check(bool(uvx), "uvx", uvx or "not found")
            if uvx:
                version = command_version([uvx, "--from", "repowise==0.41.0", "repowise", "--version"])
                ok &= check(bool(version and "0.41.0" in version), "RepoWise 0.41.0", version or "unavailable")
    print("\nResult:", "ready" if ok else "needs attention")
    return 0 if ok else 1


# ---------- command line ----------


def add_path_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--home", help="Override the home directory (mainly for testing).")
    parser.add_argument("--codex-home", help="Override CODEX_HOME.")
    parser.add_argument("--skills-home", help="Override the Agent Skills directory.")
    parser.add_argument("--install-root", help="Override the kit data directory.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install minimal coding, design preflight, adversarial review, docs, research, and optional RepoWise skills for Codex."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    install = sub.add_parser("install", help="Install the Codex-native core kit.")
    add_path_options(install)
    install.add_argument("--repo", help="Also configure the given repository with RepoWise.")
    install.add_argument("--repowise-prose", action="store_true", help="Use the Codex subscription to generate RepoWise prose during setup.")

    uninstall = sub.add_parser("uninstall", help="Remove only material owned by this kit.")
    add_path_options(uninstall)
    uninstall.add_argument("--purge", action="store_true", help="Delete the kit data directory after removing integrations.")

    repo = sub.add_parser("setup-repo", help="Add a pinned, keyless RepoWise index and Codex MCP entry.")
    repo.add_argument("repo", nargs="?", default=".")
    repo.add_argument("--prose", action="store_true", help="Generate RepoWise prose through the authenticated Codex CLI subscription.")

    remove = sub.add_parser("remove-repo", help="Remove the managed RepoWise Codex integration.")
    remove.add_argument("repo", nargs="?", default=".")
    remove.add_argument("--delete-index", action="store_true", help="Also delete the local .repowise index.")

    update = sub.add_parser("repowise-update", help="Refresh the pinned RepoWise index.")
    update.add_argument("repo", nargs="?", default=".")

    diag = sub.add_parser("doctor", help="Check the core kit and optional repository integration.")
    add_path_options(diag)
    diag.add_argument("--repo", help="Also check RepoWise in this repository.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "setup-repo":
            setup_repo(args)
            print("RepoWise is ready for this repository.")
            print("Start a new Codex session, review the project hooks/config trust prompt, then run `codex mcp list`.")
            return 0
        if args.command == "remove-repo":
            remove_repo(args)
            print("Removed the managed RepoWise Codex integration.")
            if not args.delete_index:
                print("Kept the .repowise index. Use --delete-index to remove it.")
            return 0
        if args.command == "repowise-update":
            update_repowise(args)
            print("RepoWise index updated.")
            return 0

        paths = InstallPaths.from_args(args)
        if args.command == "install":
            install_core(args, paths)
            print("Core kit installed.")
            print(f"Skills: {paths.skills_home}")
            print(f"Global instructions: {paths.codex_home / 'AGENTS.md'}")
            print(f"Hooks: {paths.codex_home / 'hooks.json'}")
            print("Open a new Codex session and use `/hooks` to review and trust the new command hooks.")
            if args.repo:
                repo_args = argparse.Namespace(repo=args.repo, prose=args.repowise_prose)
                setup_repo(repo_args)
                print(f"RepoWise configured for {resolve_git_root(Path(args.repo).expanduser().resolve())}.")
            return 0
        if args.command == "uninstall":
            if not uninstall_core(args, paths):
                print("Core kit is not installed. Nothing changed.")
                return 0
            print("Core kit integration removed.")
            if not args.purge:
                print(f"Kept toolkit files at {paths.install_root}.")
            return 0
        if args.command == "doctor":
            return doctor(args, paths)
        parser.error("unknown command")
    except (KitError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

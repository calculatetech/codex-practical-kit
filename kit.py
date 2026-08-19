#!/usr/bin/env python3
"""Install and remove the Codex Practical Kit."""

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
import tomllib
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

KIT_ID = "codex-practical-kit"
KIT_VERSION = "0.18.0"
REPOWISE_VERSION = "0.41.0"
UV_VERSION = "0.12.4"
UV_INSTALLER_URL = f"https://astral.sh/uv/{UV_VERSION}/install.sh"
UV_INSTALLER_SHA256 = "f1ee4a249799525a330df57643335120150c9102db7483b1d37546cc43af3a16"
ROOT = Path(__file__).resolve().parent
AGENTS_START = "<!-- codex-practical-kit:start -->"
AGENTS_END = "<!-- codex-practical-kit:end -->"
REPOWISE_START = "# >>> codex-practical-kit:repowise >>>"
REPOWISE_END = "# <<< codex-practical-kit:repowise <<<"

REPOWISE_WATCH_PATCH = (
    "from repowise.cli.commands import watch_cmd as w;"
    "original=w._event_paths;"
    "w._event_paths=lambda event,root:set() if getattr(event,'event_type','') in "
    "{'opened','closed','closed_no_write'} else original(event,root);"
    "w.watch_command.main(args=__import__('sys').argv[1:],standalone_mode=False)"
)
HOOKS_START = "# >>> codex-practical-kit:hooks >>>"
HOOKS_END = "# <<< codex-practical-kit:hooks <<<"
INSTALLED_HOOK_BASENAMES = {"session_start.py"}
MANAGED_HOOK_EVENTS = ("SessionStart", "UserPromptSubmit", "Stop")
CUSTOM_SKILLS = (
    "delivery-lifecycle",
    "repository-knowledge",
    "docs-maintainer",
    "roadmap-maintainer",
    "research-first",
    "design-preflight",
    "adversarial-review",
    "defect-diagnostic",
    "publication",
    "toolkit-maintainer",
    "plan-history",
)
OBSOLETE_SKILLS = ("task-brief", "codex-practical-kit-rules")
UPSTREAM_SKILLS = ("ponytail", "simple-english", "neuroarxiv")
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
    env: dict[str, str] | None = None,
    input_text: str | None = None,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            input=input_text,
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
        return pattern.sub(lambda _match: block, text, count=1).rstrip() + "\n"
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


def download_sha256(url: str, expected_sha256: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": f"{KIT_ID}/{KIT_VERSION}"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise KitError(f"Could not download pinned upstream file:\n{url}\n{exc}") from exc
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected_sha256:
        raise KitError(
            "Downloaded upstream file did not match the pinned SHA-256. "
            f"Expected {expected_sha256}, got {actual}: {url}"
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


def global_agents_body(paths: InstallPaths) -> str:
    body = (ROOT / "assets" / "AGENTS.block.md").read_text(encoding="utf-8").rstrip()
    replacements = {
        "{{SKILLS_HOME}}": paths.skills_home.as_posix(),
        "{{PLANS_FILE}}": plans_path(paths).as_posix(),
    }
    for token, value in replacements.items():
        body = body.replace(token, value)
    if re.search(r"{{[A-Z_]+}}", body):
        raise KitError("Global AGENTS template contains an unknown path token.")
    return body


def install_global_agents(paths: InstallPaths) -> None:
    agents = paths.codex_home / "AGENTS.md"
    updated = marker_block(read_text(agents), AGENTS_START, AGENTS_END, global_agents_body(paths))
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


def plans_path(paths: InstallPaths) -> Path:
    return paths.codex_home / "PLANS.md"


def install_global_plans(paths: InstallPaths) -> None:
    write_file(plans_path(paths), read_text(ROOT / ".agent" / "PLANS.md"))


def uninstall_global_plans(paths: InstallPaths, manifest: dict[str, Any]) -> None:
    recorded = manifest.get("plans_file")
    if recorded is None:
        return
    expected = plans_path(paths)
    if recorded != str(expected):
        raise KitError(f"Install manifest has an invalid plans file: {recorded}")
    remove_path(expected)


# ---------- hooks ----------


def hook_command(python: Path, script: Path) -> tuple[str, str]:
    posix = f"{shlex.quote(str(python))} {shlex.quote(str(script))}"
    windows = subprocess.list2cmdline([str(python), str(script)])
    return posix, windows


def hooks_config_block(
    paths: InstallPaths, events: tuple[str, ...] = MANAGED_HOOK_EVENTS
) -> str:
    command, command_windows = hook_command(
        Path(sys.executable).resolve(),
        paths.install_root / "hooks" / "session_start.py",
    )
    blocks = []
    for event in events:
        lines = [f"[[hooks.{event}]]"]
        if event == "SessionStart":
            lines.append('matcher = "startup|resume|clear|compact"')
        lines.extend([
            "",
            f"[[hooks.{event}.hooks]]",
            'type = "command"',
            f"command = {toml_string(command)}",
            f"commandWindows = {toml_string(command_windows)}",
            'statusMessage = "Loading practical defaults"',
            "timeout = 10",
            "additionalContextLimit = 1200",
        ])
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def configured_hook_events(paths: InstallPaths, text: str) -> set[str]:
    if not text.strip():
        return set()
    try:
        config = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        path = paths.codex_home / "config.toml"
        raise KitError(f"Invalid TOML. Fix this file before installation: {path}\n{exc}") from exc
    command, command_windows = hook_command(
        Path(sys.executable).resolve(),
        paths.install_root / "hooks" / "session_start.py",
    )
    expected = {
        "type": "command",
        "command": command,
        "commandWindows": command_windows,
        "statusMessage": "Loading practical defaults",
        "timeout": 10,
        "additionalContextLimit": 1200,
    }
    hooks = config.get("hooks", {})
    return {
        event
        for event in MANAGED_HOOK_EVENTS
        if any(
            all(handler.get(key) == value for key, value in expected.items())
            for group in hooks.get(event, [])
            for handler in group.get("hooks", [])
        )
    }


def install_hooks(paths: InstallPaths) -> None:
    config = paths.codex_home / "config.toml"
    text = read_text(config)
    unmanaged = (
        remove_marker_block(text, HOOKS_START, HOOKS_END)
        if HOOKS_START in text
        else text
    )
    configured = configured_hook_events(paths, unmanaged)
    missing = tuple(event for event in MANAGED_HOOK_EVENTS if event not in configured)
    if not missing and HOOKS_START in text:
        write_file(config, unmanaged)
    elif missing:
        write_file(
            config,
            marker_block(text, HOOKS_START, HOOKS_END, hooks_config_block(paths, missing)),
        )


def uninstall_hooks(paths: InstallPaths) -> None:
    config = paths.codex_home / "config.toml"
    if not config.exists():
        return
    text = read_text(config)
    if HOOKS_START not in text:
        return
    updated = remove_marker_block(text, HOOKS_START, HOOKS_END)
    if updated:
        write_file(config, updated)
    else:
        config.unlink()


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
    obsolete_names = {
        str(item.get("name"))
        for item in previous_records
        if isinstance(item, dict) and item.get("name") in OBSOLETE_SKILLS
    }
    plan = plans_path(paths)
    plan_owned = (
        isinstance(previous_manifest, dict)
        and previous_manifest.get("plans_file") == str(plan)
    )
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
        if plan.exists() and not plan_owned:
            raise KitError(f"This plans file already exists and is not owned by this kit: {plan}")
        validate_global_repowise_config(paths)
        uv, repowise = ensure_repowise_runtime(paths)

        hook_root = paths.install_root / "hooks"
        remove_path(hook_root)
        hook_root.mkdir()
        shutil.copy2(ROOT / "assets" / "hooks" / "session_start.py", hook_root)
        shutil.copy2(ROOT / "upstream.lock.json", paths.install_root / "upstream.lock.json")
        shutil.copy2(ROOT / "LICENSE", paths.install_root / "LICENSE")

        records = install_skills(paths, skill_stage, owned_names)
        for name in obsolete_names:
            remove_path(paths.skills_home / name)
        remove_path(paths.install_root / "skills")
        install_global_agents(paths)
        install_global_plans(paths)
        install_hooks(paths)
        install_global_repowise(paths, repowise)
        manifest = {
            "schema_version": 1,
            "kit_version": KIT_VERSION,
            "installed_at": int(time.time()),
            "codex_home": str(paths.codex_home),
            "skills_home": str(paths.skills_home),
            "install_root": str(paths.install_root),
            "plans_file": str(plan),
            "uv": uv,
            "repowise": repowise,
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
        if name not in (*ALL_SKILLS, *OBSOLETE_SKILLS) or name in names:
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
    uninstall_global_plans(installed, manifest)
    uninstall_global_agents(installed)
    uninstall_hooks(installed)
    uninstall_global_repowise(installed)
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


def user_bin(paths: InstallPaths) -> Path:
    return paths.home / ".local" / "bin"


def find_runtime_command(paths: InstallPaths, name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    candidate = user_bin(paths) / name
    if candidate.is_file():
        return str(candidate)
    manifest = json_load(manifest_path(paths), {})
    recorded = manifest.get(name) if isinstance(manifest, dict) else None
    return recorded if isinstance(recorded, str) and Path(recorded).is_file() else None


def ensure_uv(paths: InstallPaths) -> str:
    uv = find_runtime_command(paths, "uv")
    if uv:
        return uv

    script = download_sha256(UV_INSTALLER_URL, UV_INSTALLER_SHA256).decode("utf-8")
    destination = user_bin(paths)
    env = os.environ.copy()
    env["HOME"] = str(paths.home)
    env["UV_INSTALL_DIR"] = str(destination)
    env.pop("UV_UNMANAGED_INSTALL", None)
    run(["sh"], env=env, input_text=script, timeout=300)
    uv = destination / "uv"
    if not uv.is_file():
        raise KitError(f"uv {UV_VERSION} installation did not create {uv}")
    return str(uv)


def ensure_repowise(paths: InstallPaths, uv: str) -> str:
    repowise = find_runtime_command(paths, "repowise")
    if repowise:
        version = command_version([repowise, "--version"])
        if version and REPOWISE_VERSION in version:
            return repowise
        raise KitError(
            f"Found a different RepoWise command at {repowise}: {version or 'unknown version'}. "
            f"Install RepoWise {REPOWISE_VERSION} or remove that command before retrying."
        )

    destination = user_bin(paths)
    env = os.environ.copy()
    env["HOME"] = str(paths.home)
    env["UV_TOOL_BIN_DIR"] = str(destination)
    env["UV_TOOL_DIR"] = str(paths.home / ".local" / "share" / "uv" / "tools")
    run([uv, "tool", "install", f"repowise=={REPOWISE_VERSION}"], env=env, timeout=1800)
    run([uv, "tool", "update-shell"], env=env, timeout=60)
    repowise = destination / "repowise"
    if not repowise.is_file():
        raise KitError(f"RepoWise {REPOWISE_VERSION} installation did not create {repowise}")
    return str(repowise)


def ensure_repowise_runtime(paths: InstallPaths) -> tuple[str, str]:
    uv = ensure_uv(paths)
    return uv, ensure_repowise(paths, uv)


def repowise_init_args(prose: bool) -> list[str]:
    args = [
        "init",
        "--yes",
        "--no-codex",
        "--no-agents",
        "--no-editor-setup",
        "--no-distill-hook",
        "--no-claude-md",
        "--no-workspace",
    ]
    if prose:
        args.extend(["--prose", "--provider", "codex_cli"])
    else:
        args.append("--no-prose")
    return args


def repowise_watch_command(repowise: str) -> list[str]:
    launcher = Path(repowise).resolve()
    try:
        first_line = launcher.read_bytes().splitlines()[0].decode("utf-8").strip()
    except (IndexError, OSError, UnicodeDecodeError) as exc:
        raise KitError(f"Cannot read the RepoWise launcher at {launcher}: {exc}") from exc
    if not first_line.startswith("#!"):
        raise KitError(f"RepoWise launcher has no Python shebang: {launcher}")
    words = shlex.split(first_line[2:])
    if not words:
        raise KitError(f"RepoWise launcher has an empty shebang: {launcher}")
    if Path(words[0]).name == "env":
        interpreter = shutil.which(words[-1])
    else:
        interpreter = words[0]
    if not interpreter or not Path(interpreter).is_file():
        raise KitError(f"Cannot resolve the RepoWise Python interpreter: {first_line[2:]}")
    return [interpreter, "-c", REPOWISE_WATCH_PATCH]


def repowise_bootstrap(repowise: str, watcher: list[str] | None = None) -> str:
    command = shlex.quote(repowise)
    init = " ".join(
        [command, *map(shlex.quote, repowise_init_args(False)), '"$ROOT"']
    )
    update = " ".join(
        [
            command,
            "update",
            "--index-only",
            "--no-agents",
            "--no-workspace",
            '"$ROOT"',
        ]
    )
    watch = " ".join(
        [
            *map(shlex.quote, watcher or repowise_watch_command(repowise)),
            "--index-only",
            "--no-workspace",
            '"$ROOT"',
        ]
    )
    return "\n".join(
        [
            "set -eu",
            'if ! ROOT=$(git rev-parse --show-toplevel 2>/dev/null); then',
            '  if [ -n "$(ls -A)" ]; then',
            f"    exec {command} mcp",
            "  fi",
            "  git init --quiet 1>&2",
            "  ROOT=$(git rev-parse --show-toplevel)",
            "fi",
            'if [ ! -d "$ROOT/.repowise" ]; then',
            f"  {init} 1>&2",
            "fi",
            f'{command} hook install "$ROOT" --no-workspace 1>&2',
            "if git rev-parse --verify HEAD >/dev/null 2>&1; then",
            f"  {update} 1>&2",
            "fi",
            'LOG="$ROOT/.repowise/.update.log"',
            f'{watch} >> "$LOG" 2>&1 &',
            "WATCH_PID=$!",
            "sleep 1",
            'if ! kill -0 "$WATCH_PID" 2>/dev/null; then',
            '  wait "$WATCH_PID"',
            "  exit 1",
            "fi",
            "cleanup() {",
            '  kill "$WATCH_PID" 2>/dev/null || true',
            '  wait "$WATCH_PID" 2>/dev/null || true',
            "}",
            "trap cleanup EXIT",
            "trap 'exit 129' HUP",
            "trap 'exit 130' INT",
            "trap 'exit 143' TERM",
            f'{command} mcp "$ROOT"',
        ]
    )


def repowise_config_block(
    repowise: str,
    root: Path | None = None,
    watcher: list[str] | None = None,
) -> str:
    lines = [
        "[mcp_servers.repowise]",
        'command = "/bin/sh"',
        f"args = [\"-c\", {toml_string(repowise_bootstrap(repowise, watcher))}]",
        'default_tools_approval_mode = "approve"',
        "required = true",
        "startup_timeout_sec = 1800",
    ]
    if root is not None:
        lines.append(f"cwd = {toml_string(str(root))}")
    return "\n".join(lines)


def ensure_no_external_repowise_table(text: str) -> None:
    stripped = remove_marker_block(text, REPOWISE_START, REPOWISE_END)
    if re.search(r"(?m)^\s*\[mcp_servers\.repowise\]\s*$", stripped):
        raise KitError(
            "A RepoWise MCP table already exists outside this kit's managed block. "
            "Remove or rename that table before setup so there is one owner."
        )


def global_repowise_config(paths: InstallPaths) -> Path:
    return paths.codex_home / "config.toml"


def validate_global_repowise_config(paths: InstallPaths) -> None:
    ensure_no_external_repowise_table(read_text(global_repowise_config(paths)))


def install_global_repowise(paths: InstallPaths, repowise: str) -> None:
    config = global_repowise_config(paths)
    updated = marker_block(
        read_text(config),
        REPOWISE_START,
        REPOWISE_END,
        repowise_config_block(repowise),
    )
    write_file(config, updated)


def uninstall_global_repowise(paths: InstallPaths) -> None:
    config = global_repowise_config(paths)
    if not config.exists():
        return
    updated = remove_marker_block(read_text(config), REPOWISE_START, REPOWISE_END)
    if updated:
        write_file(config, updated)
    else:
        config.unlink()


def repowise_command(
    root: Path,
    *args: str,
    paths: InstallPaths,
    repowise: str | None = None,
    timeout: int = 1800,
) -> subprocess.CompletedProcess[str]:
    if repowise is None:
        _, repowise = ensure_repowise_runtime(paths)
    return run([repowise, *args], cwd=root, timeout=timeout)


def setup_repo(args: argparse.Namespace, paths: InstallPaths) -> None:
    root = resolve_git_root(Path(args.repo).expanduser().resolve())
    config = root / ".codex" / "config.toml"
    agents = root / "AGENTS.md"
    config_before = read_text(config)
    agents_before = read_text(agents)
    ensure_no_external_repowise_table(config_before)
    _, repowise = ensure_repowise_runtime(paths)

    if not (root / ".repowise").exists():
        repowise_command(
            root,
            *repowise_init_args(args.prose),
            paths=paths,
            repowise=repowise,
        )
    repowise_command(
        root,
        "hook",
        "install",
        str(root),
        "--no-workspace",
        paths=paths,
        repowise=repowise,
    )
    if (
        run(["git", "rev-parse", "--verify", "HEAD"], cwd=root, check=False).returncode
        == 0
    ):
        repowise_command(
            root,
            "update",
            "--index-only",
            "--no-agents",
            "--no-workspace",
            str(root),
            paths=paths,
            repowise=repowise,
        )

    config_after = marker_block(
        config_before,
        REPOWISE_START,
        REPOWISE_END,
        repowise_config_block(repowise, root),
    )
    write_file(config, config_after)
    agents_after = remove_marker_block(
        agents_before,
        AGENTS_START + ":repowise",
        AGENTS_END + ":repowise",
    )
    if agents_after != agents_before:
        if agents_after:
            write_file(agents, agents_after)
        else:
            agents.unlink()
    remove_path(root / ".codex-practical-kit")


def remove_repo(args: argparse.Namespace, paths: InstallPaths) -> None:
    root = resolve_git_root(Path(args.repo).expanduser().resolve())
    config = root / ".codex" / "config.toml"
    agents = root / "AGENTS.md"
    config_before = read_text(config)
    ensure_no_external_repowise_table(config_before)
    _, repowise = ensure_repowise_runtime(paths)
    repowise_command(
        root,
        "hook",
        "uninstall",
        str(root),
        "--no-workspace",
        paths=paths,
        repowise=repowise,
    )
    write_file(
        config,
        marker_block(
            config_before,
            REPOWISE_START,
            REPOWISE_END,
            "[mcp_servers.repowise]\nenabled = false",
        ),
    )
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


def update_repowise(args: argparse.Namespace, paths: InstallPaths) -> None:
    root = resolve_git_root(Path(args.repo).expanduser().resolve())
    if not (root / ".repowise").exists():
        raise KitError(f"RepoWise is not initialized in {root}")
    repowise_command(root, "update", "--no-agents", paths=paths)


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
    agents_text = read_text(agents)
    ok &= check(
        agents.exists()
        and AGENTS_START in agents_text
        and global_agents_body(paths) in agents_text,
        "global AGENTS block",
        str(agents),
    )
    plan = plans_path(paths)
    expected_plan = read_text(ROOT / ".agent" / "PLANS.md")
    plan_recorded = manifest.get("plans_file") if isinstance(manifest, dict) else None
    ok &= check(
        plan_recorded == str(plan) and read_text(plan) == expected_plan,
        "global PLANS file",
        str(plan),
    )
    hooks_path = paths.codex_home / "config.toml"
    hooks_text = read_text(hooks_path)
    hook_root = paths.install_root / "hooks"
    installed_files = {path.name for path in hook_root.iterdir()} if hook_root.is_dir() else set()
    try:
        hooks_ok = configured_hook_events(paths, hooks_text) == set(MANAGED_HOOK_EVENTS)
    except KitError:
        hooks_ok = False
    hooks_ok = hooks_ok and installed_files == INSTALLED_HOOK_BASENAMES
    ok &= check(hooks_ok, "Codex hooks", str(hooks_path))

    global_config = global_repowise_config(paths)
    global_text = read_text(global_config)
    ok &= check(
        REPOWISE_START in global_text
        and 'default_tools_approval_mode = "approve"' in global_text
        and "required = true" in global_text
        and "startup_timeout_sec = 1800" in global_text,
        "global RepoWise MCP config",
        str(global_config),
    )
    uv = find_runtime_command(paths, "uv")
    ok &= check(bool(uv), "uv", uv or "not found")
    repowise = find_runtime_command(paths, "repowise")
    ok &= check(bool(repowise), "RepoWise command", repowise or "not found")
    if repowise:
        version = command_version([repowise, "--version"])
        ok &= check(
            bool(version and REPOWISE_VERSION in version),
            f"RepoWise {REPOWISE_VERSION}",
            version or "unavailable",
        )

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
            disabled = bool(
                REPOWISE_START in config
                and re.search(r"(?m)^enabled\s*=\s*false\s*$", config)
            )
            ok &= check(
                not disabled,
                "repository RepoWise opt-out",
                "disabled" if disabled else "enabled",
            )
            hook = read_text(root / ".git" / "hooks" / "post-commit")
            ok &= check(
                "# repowise-hook-start" in hook and "# repowise-hook-end" in hook,
                "RepoWise post-commit hook",
                str(root / ".git" / "hooks" / "post-commit"),
            )
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
        description="Install minimal coding, ExecPlan, design preflight, adversarial review, docs, research, and RepoWise support for Codex."
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

    diag = sub.add_parser("doctor", help="Check the core kit and repository integration.")
    add_path_options(diag)
    diag.add_argument("--repo", help="Also check RepoWise in this repository.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    paths = InstallPaths.from_args(args)
    try:
        if args.command == "setup-repo":
            setup_repo(args, paths)
            print("RepoWise is ready for this repository.")
            print("Start a new Codex session, then run `codex mcp list`.")
            return 0
        if args.command == "remove-repo":
            remove_repo(args, paths)
            print("Removed the managed RepoWise Codex integration.")
            if not args.delete_index:
                print("Kept the .repowise index. Use --delete-index to remove it.")
            return 0
        if args.command == "repowise-update":
            update_repowise(args, paths)
            print("RepoWise index updated.")
            return 0

        if args.command == "install":
            install_core(args, paths)
            print("Core kit installed.")
            print(f"Skills: {paths.skills_home}")
            print(f"Global instructions: {paths.codex_home / 'AGENTS.md'}")
            print(f"Global ExecPlan rules: {plans_path(paths)}")
            print(f"Hooks: {paths.codex_home / 'config.toml'}")
            print("Open a new Codex session and use `/hooks` to review and trust the Session Start hook.")
            if args.repo:
                repo_args = argparse.Namespace(repo=args.repo, prose=args.repowise_prose)
                setup_repo(repo_args, paths)
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

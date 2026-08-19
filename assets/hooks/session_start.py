#!/usr/bin/env python3
"""Add practical context and preserve completed Plan Mode responses."""

import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PLAN_MARKER = re.compile(r"^<!-- cpk-plan-spec: ([^\r\n]+) -->$", re.MULTILINE)
PATCH_FILE = re.compile(r"^\*\*\* (?:Add|Update) File: (.+)$", re.MULTILINE)
ROADMAP_PATH = Path("docs/roadmap.md")
ROADMAP_VIEW_PATH = Path(".codex/roadmap-view.md")
ROADMAP_VIEW_MARKER = "<!-- codex-practical-kit:roadmap-view -->"
ROADMAP_EXCLUDE_START = "# >>> codex-practical-kit:roadmap-view >>>"
ROADMAP_EXCLUDE_END = "# <<< codex-practical-kit:roadmap-view <<<"
ROADMAP_EXCLUDE_PATH = "/.codex/roadmap-view.md"


def repository_root(cwd: Path) -> Path | None:
    for candidate in (cwd, *cwd.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def roadmap_target(event: dict[str, object]) -> tuple[Path, Path] | None:
    tool_input = event.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str):
        return None
    cwd = Path(str(event.get("cwd") or Path.cwd())).resolve()
    for value in PATCH_FILE.findall(command):
        path = Path(value.strip())
        candidate = path if path.is_absolute() else cwd / path
        candidate = candidate.resolve()
        root = repository_root(candidate.parent)
        if root is not None and candidate == (root / ROADMAP_PATH).resolve():
            roadmap = candidate
            return root, roadmap
    return None


def roadmap_state_file(event: dict[str, object]) -> Path | None:
    session = event.get("session_id")
    tool_use = event.get("tool_use_id")
    if not isinstance(session, str) or not isinstance(tool_use, str):
        return None
    key = hashlib.sha256(f"{session}\0{tool_use}".encode()).hexdigest()
    return Path(tempfile.gettempdir()) / "codex-practical-kit-roadmap" / f"{key}.json"


def fingerprint(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except FileNotFoundError:
        return None


def save_roadmap_state(event: dict[str, object]) -> None:
    target = roadmap_target(event)
    state = roadmap_state_file(event)
    if target is None or state is None:
        return
    _, roadmap = target
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(
        json.dumps({"path": str(roadmap), "fingerprint": fingerprint(roadmap)}),
        encoding="utf-8",
    )


def git_common_directory(root: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError((result.stderr or "cannot resolve the shared Git directory").strip())
    common = Path(result.stdout.strip()).resolve()
    if common.name != ".git" or not common.is_dir():
        raise RuntimeError("the repository does not use a supported primary checkout")
    return common


def exclude_roadmap_view(common: Path) -> None:
    path = common / "info" / "exclude"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if ROADMAP_EXCLUDE_START in text or ROADMAP_EXCLUDE_PATH in text.splitlines():
        return
    block = (
        f"{ROADMAP_EXCLUDE_START}\n{ROADMAP_EXCLUDE_PATH}\n"
        f"{ROADMAP_EXCLUDE_END}\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text((text.rstrip() + "\n\n" if text.strip() else "") + block, encoding="utf-8")


def write_roadmap_view(common: Path, roadmap: Path) -> None:
    view = common.parent / ROADMAP_VIEW_PATH
    if view.parent.exists() and not view.parent.is_dir():
        raise RuntimeError(f"preserved user-owned path at {view.parent}")
    if view.exists():
        if not view.is_file() or not view.read_text(encoding="utf-8").startswith(
            ROADMAP_VIEW_MARKER + "\n"
        ):
            raise RuntimeError(f"preserved user-owned file at {view}")
    exclude_roadmap_view(common)
    source = roadmap.read_text(encoding="utf-8")
    content = (
        f"{ROADMAP_VIEW_MARKER}\n"
        "> Generated view. Edit `docs/roadmap.md` in the active task worktree.\n\n"
        + source
    )
    view.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=view.parent, delete=False
        ) as output:
            temporary = Path(output.name)
            output.write(content)
        os.replace(temporary, view)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def refresh_roadmap_view(event: dict[str, object]) -> None:
    target = roadmap_target(event)
    state = roadmap_state_file(event)
    if target is None or state is None or not state.exists():
        return
    root, roadmap = target
    try:
        before = json.loads(state.read_text(encoding="utf-8"))
    finally:
        state.unlink(missing_ok=True)
    if before.get("path") != str(roadmap) or before.get("fingerprint") == fingerprint(roadmap):
        return
    if not roadmap.is_file():
        raise RuntimeError("the changed roadmap is not a regular file")
    write_roadmap_view(git_common_directory(root), roadmap)


def roadmap_warning(exc: Exception) -> None:
    print(json.dumps({
        "systemMessage": f"Codex Practical Kit: roadmap view was not refreshed: {exc}"
    }, separators=(",", ":")))


def completed_plan(message: str) -> bool:
    stripped = message.strip()
    return (
        stripped.startswith("<proposed_plan>\n")
        and stripped.endswith("\n</proposed_plan>")
        and stripped.count("<proposed_plan>") == 1
        and stripped.count("</proposed_plan>") == 1
    )


def event_key(event: dict[str, object]) -> str:
    identity = f"{event.get('session_id', '')}\0{event.get('turn_id', '')}"
    return hashlib.sha256(identity.encode()).hexdigest()


def write_record(
    directory: Path, prefix: str, timestamp: str, key: str, content: bytes
) -> bool:
    directory.mkdir(parents=True, exist_ok=True)
    escaped_prefix = glob.escape(prefix)
    existing = sorted(directory.glob(f"{escaped_prefix}.*.{key}.md"))
    if any(path.read_bytes() == content for path in existing):
        return False
    if existing:
        digest = hashlib.sha256(content).hexdigest()
        collisions = sorted(directory.glob(f"{escaped_prefix}.*.{key}.{digest}.md"))
        if any(path.read_bytes() == content for path in collisions):
            return False
        name = f"{prefix}.{timestamp}.{key}.{digest}.md"
    else:
        name = f"{prefix}.{timestamp}.{key}.md"
    with (directory / name).open("xb") as output:
        output.write(content)
    return bool(existing)


def plan_targets(root: Path | None, markers: list[str]) -> tuple[list[Path], list[str]]:
    targets: list[Path] = []
    failures: list[str] = []
    if not markers:
        return targets, ["the plan has no cpk-plan-spec marker"]
    if markers == ["none"]:
        return targets, failures
    for marker in markers:
        if marker == "none":
            failures.append("none cannot appear with a specification path")
            continue
        relative = Path(marker)
        if root is None or relative.is_absolute() or relative.suffix.lower() != ".md":
            failures.append(marker)
            continue
        target = (root / relative).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            failures.append(marker)
            continue
        if target not in targets:
            targets.append(target)
    return targets, failures


def save_plan(event: dict[str, object]) -> list[str]:
    message = event.get("last_assistant_message")
    if not isinstance(message, str) or not message:
        return ["Codex did not provide the completed Plan Mode response"]
    if not completed_plan(message):
        return []

    cwd = Path(str(event.get("cwd") or Path.cwd())).resolve()
    root = repository_root(cwd)
    markers = [value.strip() for value in PLAN_MARKER.findall(message)]
    targets, failures = plan_targets(root, markers)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    key = event_key(event)
    content = message.encode("utf-8")
    collisions = False

    for target in targets:
        collisions |= write_record(
            target.parent,
            f"{target.stem}.plan-summary",
            timestamp,
            key,
            content,
        )

    if not targets or failures:
        if root is not None:
            history = root / ".agent" / "plan-history"
        else:
            codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
            cwd_key = hashlib.sha256(str(cwd).encode()).hexdigest()
            history = codex_home / "plan-history" / cwd_key
        collisions |= write_record(history, "plan-summary", timestamp, key, content)

    warnings = []
    if failures:
        warnings.append("Plan history used unlinked storage: " + ", ".join(failures))
    if collisions:
        warnings.append("Plan history preserved different content for the same event identity")
    return warnings

event = json.load(sys.stdin)

if event.get("hook_event_name") == "PreToolUse":
    try:
        save_roadmap_state(event)
    except Exception as exc:
        roadmap_warning(exc)
elif event.get("hook_event_name") == "PostToolUse":
    try:
        refresh_roadmap_view(event)
    except Exception as exc:
        roadmap_warning(exc)
elif event.get("hook_event_name") == "Stop":
    warnings = save_plan(event) if event.get("permission_mode") == "plan" else []
    output = (
        {"systemMessage": "Codex Practical Kit: " + "; ".join(warnings)}
        if warnings
        else {}
    )
    print(json.dumps(output, separators=(",", ":")))
elif event.get("hook_event_name") == "UserPromptSubmit":
    if event.get("permission_mode") == "plan":
        print("normal mode\nUse plan-history before planning. Read and reconcile all applicable Plan history records.")
elif event.get("hook_event_name") == "SessionStart":
    context = "Codex Practical Kit is active. Read the managed AGENTS.md links that apply to this task."
    if event.get("source") == "compact":
        context += " Apply repository-knowledge before the next repository lookup. Keep it active until the task ends. Before later planning, use plan-history and reconcile all applicable records."
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }, separators=(",", ":")))

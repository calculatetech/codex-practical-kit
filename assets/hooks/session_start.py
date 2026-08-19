#!/usr/bin/env python3
"""Add practical context and preserve completed Plan Mode responses."""

import glob
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


PLAN_MARKER = re.compile(r"^<!-- cpk-plan-spec: ([^\r\n]+) -->$", re.MULTILINE)


def repository_root(cwd: Path) -> Path | None:
    for candidate in (cwd, *cwd.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


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

if event.get("hook_event_name") == "Stop":
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

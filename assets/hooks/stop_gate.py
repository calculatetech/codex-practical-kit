#!/usr/bin/env python3
"""Request review and documentation markers when Git status changes."""

from __future__ import annotations

import subprocess
from pathlib import Path

from hook_common import (
    advance_baseline,
    git_status,
    has_docs_status,
    is_documentation,
    is_forbidden_docs_file,
    load_baseline,
    read_payload,
    review_status,
    status_paths,
    write_json,
)


def block(reason: str) -> None:
    write_json({"decision": "block", "reason": reason})
    raise SystemExit(0)


payload = read_payload()

# Plan Mode is read-only. Never replace its response with a continuation.
if payload.get("permission_mode") == "plan":
    write_json({})
    raise SystemExit(0)

baseline = load_baseline(payload)
if baseline is None or not baseline.get("git_root"):
    write_json({})
    raise SystemExit(0)

root = Path(baseline["git_root"])
try:
    current = git_status(root)
except (OSError, subprocess.SubprocessError) as exc:
    block(f"The toolkit could not read Git status: {exc}")

if current == baseline["status"]:
    write_json({})
    raise SystemExit(0)

paths = status_paths(current)
forbidden = [
    path for path in paths
    if (root / path).exists() and is_forbidden_docs_file(path)
]
if forbidden:
    block(
        "Repository-root docs/ is documentation-only: " + ", ".join(forbidden[:10])
    )

message = payload.get("last_assistant_message")
docs_done = has_docs_status(message)
review = review_status(message)
code_changed = not paths or any(not is_documentation(path) for path in paths)

if review == "stopped":
    write_json({})
    raise SystemExit(0)

accepted = docs_done and (not code_changed or review in {"clean", "clean_after_fixes"})
if accepted:
    try:
        advance_baseline(payload, root, current)
    except OSError as exc:
        block(f"The toolkit could not save Git status: {exc}")
    write_json({})
    raise SystemExit(0)

if payload.get("stop_hook_active") is True:
    write_json({})
    raise SystemExit(0)

if code_changed:
    block(
        "Git status changed. Finish documentation first. Then run one supported-model "
        "adversarial review. End with current Review and Docs status lines."
    )

block(
    "Documentation changed. Run docs-maintainer and end with a current Docs status line."
)

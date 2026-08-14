"""Shared helpers for Codex Practical Kit hooks."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

KIT_ID = "codex-practical-kit"
_SAFE_ID = re.compile(r"[^A-Za-z0-9_.-]+")
_DOC_EXTENSIONS = {
    ".adoc", ".asciidoc", ".avif", ".css", ".gif", ".htm", ".html",
    ".ico", ".jpeg", ".jpg", ".md", ".mdx", ".pdf", ".png", ".rst",
    ".svg", ".txt", ".webp",
}
_DOC_NAMES = {
    "agents.md", "changelog.md", "contributing.md", "license", "readme",
    "readme.md", "security.md",
}


def read_payload() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def write_json(value: object) -> None:
    sys.stdout.write(json.dumps(value, separators=(",", ":")) + "\n")


def state_root() -> Path:
    base = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    root = base / KIT_ID / "sessions"
    root.mkdir(parents=True, exist_ok=True)
    return root


def session_id(payload: dict[str, Any]) -> str:
    raw = str(payload.get("session_id") or payload.get("thread_id") or "unknown")
    safe = _SAFE_ID.sub("_", raw).strip("._")
    return safe[:160] or "unknown"


def state_file(payload: dict[str, Any]) -> Path:
    return state_root() / f"{session_id(payload)}.json"


def git_root(cwd: str | os.PathLike[str] | None) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=Path(cwd or os.getcwd()).expanduser(),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    value = result.stdout.strip()
    return Path(value).resolve() if value else None


def git_status(root: Path) -> str:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
        timeout=10,
    )
    return result.stdout


def baseline_value(payload: dict[str, Any]) -> dict[str, Any]:
    root = git_root(payload.get("cwd"))
    return {
        "schema_version": 1,
        "created_at": int(time.time()),
        "git_root": str(root) if root else None,
        "status": git_status(root) if root else "",
    }


def save_baseline(payload: dict[str, Any]) -> None:
    path = state_file(payload)
    if not path.exists():
        path.write_text(
            json.dumps(baseline_value(payload), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def load_baseline(payload: dict[str, Any]) -> dict[str, Any] | None:
    try:
        value = json.loads(state_file(payload).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if not isinstance(value, dict):
        return None
    if not isinstance(value.get("status"), str):
        return None
    root = value.get("git_root")
    return value if root is None or isinstance(root, str) else None


def advance_baseline(payload: dict[str, Any], root: Path, status: str) -> None:
    value = {
        "schema_version": 1,
        "created_at": int(time.time()),
        "git_root": str(root),
        "status": status,
    }
    state_file(payload).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def remove_baseline(payload: dict[str, Any]) -> None:
    try:
        state_file(payload).unlink()
    except FileNotFoundError:
        pass


def status_paths(status: str) -> list[str]:
    paths = []
    for line in status.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        paths.append(path.strip('"'))
    return paths


def is_documentation(path: str) -> bool:
    item = Path(path)
    name = item.name.lower()
    return item.suffix.lower() in _DOC_EXTENSIONS or name in _DOC_NAMES


def is_forbidden_docs_file(path: str) -> bool:
    item = Path(path)
    return bool(item.parts) and item.parts[0].lower() == "docs" and not is_documentation(path)


def has_docs_status(message: Any) -> bool:
    return isinstance(message, str) and (
        "Docs: updated" in message or "Docs: no change needed" in message
    )


def review_status(message: Any) -> str | None:
    if not isinstance(message, str):
        return None
    if "Review: stopped" in message:
        return "stopped"
    if "Review: clean after fixes" in message:
        return "clean_after_fixes"
    if "Review: clean" in message:
        return "clean"
    return None

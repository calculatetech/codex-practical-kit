#!/usr/bin/env python3
"""Add the practical context for supported Codex hook events."""

import json
import sys

event = json.load(sys.stdin)

if event.get("hook_event_name") == "UserPromptSubmit":
    if event.get("permission_mode") == "plan":
        print("normal mode")
elif event.get("hook_event_name") == "SessionStart":
    context = "Codex Practical Kit is active. Read the managed AGENTS.md links that apply to this task."
    if event.get("source") == "compact":
        context += " Apply repository-knowledge before the next repository lookup. Keep it active until the task ends."
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }, separators=(",", ":")))

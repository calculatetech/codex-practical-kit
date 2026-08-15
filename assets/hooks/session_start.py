#!/usr/bin/env python3
"""Tell Codex that the managed rule router is active."""

import json

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "Codex Practical Kit is active. Read the managed AGENTS.md links that apply to this task.",
    }
}, separators=(",", ":")))

#!/usr/bin/env python3
"""Save a Git baseline and inject a compact working agreement."""

from __future__ import annotations

from hook_common import read_payload, save_baseline, write_json

payload = read_payload()
save_baseline(payload)

context = """Codex Practical Kit is active.
- Use Ponytail full for coding: understand first, reuse existing code, fix the root cause, and keep the correct diff small.
- Use deterministic least effort: true or false checks, one attempt, and stop on failure.
- Ignore I/O faults, permissions, links, concurrency, interruption, retry, recovery, submodules, and outside influence unless the task includes them.
- Use Simple English for user-facing prose: answer first, short sentences, define technical terms, and keep commands exact.
- Use RepoWise before broad exploration when its MCP tools are available and current. Fall back to native tools when it is unavailable.
- Before non-trivial implementation, use design-preflight to define the normal-use floor, scope ceiling, owner, and exact checks.
- Use one ExecPlan for complex features, multi-file changes, and significant refactors.
- On `main`, allow only bounded documentation, comments, formatting, and roadmap updates. Use a task branch for one writable implementation stream.
- Use a worktree for independent writable streams, multiple implementation agents, or a main checkout that cannot switch safely.
- For toolkit releases, features increment the minor version. Fixes and published same-feature checkpoints increment the patch version.
- Local checkpoint commits do not change the version. Use prerelease suffixes only for planned public testing.
- Use research only for unfamiliar, current, high-impact, or hard-to-reverse choices.
- When docs/roadmap.md exists, use roadmap-maintainer before implementation and at each task transition.
- Finalize documentation and the roadmap before adversarial-review and commit.
- Use one fresh supported-model correctness reviewer. Never make a post-commit documentation change.
- End with one `Review:` line and one `Docs:` line.
"""

write_json({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context,
    }
})

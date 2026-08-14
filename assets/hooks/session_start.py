#!/usr/bin/env python3
"""Save a Git baseline and inject a compact working agreement."""

import json

context = """Codex Practical Kit is active.
- Use Ponytail full for coding: understand first, reuse existing code, fix the root cause, and keep the correct diff small.
- Use deterministic least effort: true or false checks, one attempt, and stop on failure.
- Ignore I/O faults, permissions, links, concurrency, interruption, retry, recovery, submodules, and outside influence unless the task includes them.
- Use Simple English for user-facing prose: answer first, short sentences, define technical terms, and keep commands exact.
- Material decisions use `Decision`, optional `Term`, `Trigger`, `Likelihood`, `Current exposure`, `Options`, `Recommendation`, then `Question`.
- Investigate first. Skip the full handoff for routine inputs. State option effects, use qualitative likelihood, and prefer the smallest reversible choice that meets the requirement.
- Use RepoWise before broad exploration when its MCP tools are available and current. Fall back to native tools when it is unavailable.
- Before non-trivial implementation, use design-preflight to define the normal-use floor, scope ceiling, owner, and exact checks.
- Use one ExecPlan for complex features, multi-file changes, and significant refactors.
- On `main`, allow only bounded documentation, comments, formatting, and roadmap updates. Use a task branch for one writable implementation stream.
- Use a worktree for independent writable streams, multiple implementation agents, or a main checkout that cannot switch safely.
- PR mode requires protected `main`, required CI checks, resolved conversations, and workflows that supply those checks. Otherwise, use direct integration.
- In PR mode, `publish` authorizes the path through squash merge. Require current CI, a current Codex thumbs-up, no requested changes, and resolved conversations. Each push resets the gates. Cleanup stays separate.
- For toolkit releases, features increment the minor version. Fixes and published same-feature checkpoints increment the patch version.
- Local checkpoint commits do not change the version. Use prerelease suffixes only for planned public testing.
- Use research only for unfamiliar, current, high-impact, or hard-to-reverse choices.
- When docs/roadmap.md exists, use roadmap-maintainer before implementation and at each task transition.
- Finalize documentation and the roadmap before adversarial-review and commit.
- Use one fresh supported-model correctness reviewer. Never make a post-commit documentation change.
- End with one `Review:` line and one `Docs:` line.
"""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context,
    }
}, separators=(",", ":")))

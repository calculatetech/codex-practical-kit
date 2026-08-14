# Prompt for Codex

Run this from the extracted `codex-practical-kit` directory.

```text
Install the Codex Practical Kit safely.

First read README.md, docs/REMOVE-CBM.md, docs/REVIEW.md, kit.py, and the tests. Inspect my current global and repository Codex configuration. Do not remove or overwrite unrelated hooks, MCP servers, skills, plugins, prompts, or AGENTS instructions.

If a broken CBM integration is still configured, remove only CBM-owned references before installing this kit. Attempt each operation once. Stop and report the first failure. Do not run CBM's own uninstall routine if it cannot start. Verify that `codex mcp list` no longer contains CBM.

Run `./run-tests.sh`. Then run `./install.sh`. Review the resulting changes in `~/.codex/AGENTS.md`, `~/.codex/PLANS.md`, `~/.codex/config.toml`, and `~/.codex/hooks.json`. Confirm that the Stop hook points to `stop_gate.py`, not the old `stop_docs.py`. Confirm that the installed kit reports version 0.7.0 or newer. Confirm that the `roadmap-maintainer` skill and its template are installed. Confirm that the obsolete `task-brief` skill is absent. Confirm that the managed RepoWise MCP table has `default_tools_approval_mode = "approve"`. Do not trust the Codex hooks on my behalf. Tell me to open `/hooks` in a new Codex session. If version 0.2.0 was active, tell me not to resume that old session because it can retain the stale continuation that version 0.2.1 corrected.

The installer must reuse `uv` when present or install pinned uv when absent. It must install pinned RepoWise as a persistent uv tool when absent. If I am in a Git repository, run `./setup-repo.sh .`. Do not enable model-written RepoWise prose unless I explicitly say yes. Confirm that `.git/hooks/post-commit` contains RepoWise's managed block.

Do not install Spec Kit, Compound Engineering, Superpowers, Trail of Bits skills, ADHD, or NeuroArxiv during this task. They are optional. The core kit already contains the small design-preflight and adversarial-review skills.

Finish by running `./doctor.sh` and, when you are in a Git repository, `./doctor.sh --repo .`. Report exact files changed, commands run, and any manual step that remains.
```

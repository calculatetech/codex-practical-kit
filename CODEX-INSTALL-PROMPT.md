# Prompt for Codex

Run this from the extracted `codex-practical-kit` directory.

## Operating model

<!-- cpk-rule-route-only: supported-model -->
[Supported model](assets/skills/design-preflight/references/supported-model.md)

## Prompt

```text
Install the Codex Practical Kit safely.

First read README.md, docs/REMOVE-CBM.md, docs/REVIEW.md, assets/skills/design-preflight/references/supported-model.md, kit.py, and the tests. Inspect my current global and repository Codex configuration. Do not remove or overwrite unrelated hooks, MCP servers, skills, plugins, prompts, or AGENTS instructions.

If a broken CBM integration is still configured, remove only CBM-owned references before installing this kit. Apply the supported-model rules. Do not run CBM's own uninstall routine if it cannot start. Verify that `codex mcp list` no longer contains CBM.

Run `./run-tests.sh`. Then run `./install.sh`. Review the resulting changes in `~/.codex/AGENTS.md`, `~/.codex/PLANS.md`, and `~/.codex/config.toml`. Confirm that AGENTS names the focused lifecycle skills. Confirm that the toolkit installs `session_start.py` but not `stop_gate.py`, `stop_docs.py`, or `session_end.py`. Confirm that `config.toml` contains the managed `SessionStart` and `UserPromptSubmit` hooks. Confirm that `./doctor.sh` reports the version from source. Confirm that `delivery-lifecycle`, `neuroarxiv`, `publication`, `repository-knowledge`, `roadmap-maintainer`, and `toolkit-maintainer` are installed. Confirm that obsolete `codex-practical-kit-rules` and `task-brief` skills are absent. Confirm that the managed RepoWise MCP table has `default_tools_approval_mode = "approve"`, `required = true`, and `startup_timeout_sec = 1800`. Do not trust the Codex hook on my behalf. Tell me to open `/hooks` in a new Codex session. If version 0.2.0 was active, tell me not to resume that old session because it can retain the stale continuation that version 0.2.1 corrected.

The installer must reuse `uv` when present or install pinned uv when absent. It must install pinned RepoWise as a persistent uv tool when absent. If I am in a Git repository, run `./setup-repo.sh .`. Do not enable model-written RepoWise prose unless I explicitly say yes. Confirm that `.git/hooks/post-commit` contains RepoWise's managed block.

Do not install Spec Kit, Compound Engineering, Superpowers, Trail of Bits skills, or ADHD during this task. They are not core components. The core kit installs NeuroArxiv and the small design-preflight, adversarial-review, and defect-diagnostic skills. Leave any user-managed ADHD installation unchanged.

Finish by running `./doctor.sh` and, when you are in a Git repository, `./doctor.sh --repo .`. Report exact files changed, commands run, and any manual step that remains.
```

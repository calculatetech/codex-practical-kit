# Codex Practical Kit

Codex Practical Kit installs a small working agreement for personal repositories. It favors direct code, clear documentation, and bounded review.

The managed `AGENTS.md` is a small skill router. Skill descriptions keep unrelated rules out of task context.

## Included components

The kit installs these task skills:

- `ponytail`
- `simple-english`
- `neuroarxiv`
- `design-preflight`
- `delivery-lifecycle`
- `repository-knowledge`
- `research-first`
- `docs-maintainer`
- `roadmap-maintainer`
- `adversarial-review`
- `defect-diagnostic`
- `publication`
- `toolkit-maintainer`
- `plan-history`

Each lifecycle skill contains its focused rule owners or links to the one skill that owns a shared rule.

## Install

On macOS or Linux, run:

```bash
./run-tests.sh
./install.sh
./doctor.sh
```

On Windows, install PowerShell 7 and Python 3.11 or later. Then run:

```powershell
pwsh -File .\run-tests.ps1
pwsh -File .\install.ps1
pwsh -File .\doctor.ps1
```

The installer copies managed skills to `~/.agents/skills/`. Do not edit installed copies.

The installer writes a managed block in `~/.codex/AGENTS.md`. It renders the absolute PLANS path and names installed skills.

The installer also writes `$CODEX_HOME/PLANS.md` and managed Codex hooks. Session Start announces the AGENTS router.

Prompt submission selects normal mode before Plan-mode prompts. The passive Stop hook saves completed Plan Mode responses without continuing the turn.

The edit hooks update `<primary-checkout>/.codex/roadmap-view.md` after an agent changes `docs/roadmap.md`. Keep this generated file open to follow worktree progress. Edit only `docs/roadmap.md`.

The `plan-history` skill puts immutable summaries beside related specifications. It uses `.agent/plan-history/` when no specification exists. Later planning sessions read and reconcile these records.

An unrecorded destination skill is a conflict. The installer stops before it changes that directory.

Open a new Codex session after installation. Use `/hooks` to review and trust the managed command.

## Rule owners

An applicable skill selects only the rules needed for its task:

- [Rule ownership](assets/skills/toolkit-maintainer/SKILL.md)
- [Coordination](assets/skills/delivery-lifecycle/references/coordination.md)
- [Supported model](assets/skills/design-preflight/references/supported-model.md)
- [Scope boundaries](assets/skills/design-preflight/references/scope-boundaries.md)
- [Decision handoffs](assets/skills/delivery-lifecycle/references/decision-handoffs.md)
- [Repository knowledge](assets/skills/repository-knowledge/SKILL.md)
- [Research First](assets/skills/research-first/SKILL.md)
- [Delivery lifecycle](assets/skills/delivery-lifecycle/references/delivery-lifecycle.md)
- [Implementation modes](assets/skills/delivery-lifecycle/references/implementation-modes.md)
- [Git isolation](assets/skills/delivery-lifecycle/references/git-isolation.md)
- [Plan history](assets/skills/plan-history/SKILL.md)
- [Full-set results](assets/skills/design-preflight/references/full-set-results.md)
- [Owner composition](assets/skills/design-preflight/references/owner-composition.md)
- [Scenario discrimination](assets/skills/design-preflight/references/scenario-discrimination.md)
- [Review closure](assets/skills/adversarial-review/references/review-closure.md)
- [Publication](assets/skills/publication/references/publication.md)
- [Versioning](assets/skills/publication/references/versioning.md)

Skill-specific procedures remain in each skill. [ExecPlan rules](.agent/PLANS.md) remain focused on executable plans.

## RepoWise

The core install provides pinned `uv` and RepoWise when they are absent. It configures one required user-level RepoWise MCP server.

In a Git repository, the first MCP start creates the index and installs RepoWise's `post-commit` hook. Each MCP session catches up the index and watches working-tree edits without model calls. A completely empty folder becomes a Git repository. A non-empty, non-Git folder remains unchanged.

On macOS or Linux, run eager setup when you need the index before the next Codex session:

```bash
./setup-repo.sh /path/to/repository
./doctor.sh --repo /path/to/repository
```

On Windows, run:

```powershell
pwsh -File .\setup-repo.ps1 C:\path\to\repository
pwsh -File .\doctor.ps1 --repo C:\path\to\repository
```

See [RepoWise notes](docs/REPOWISE.md) for setup, refresh, opt-out, and trust-boundary details.

## Uninstall

On macOS or Linux, remove managed integrations and copied skills:

```bash
./uninstall.sh
```

Also remove toolkit files:

```bash
./uninstall.sh --purge
```

On Windows, run:

```powershell
pwsh -File .\uninstall.ps1
pwsh -File .\uninstall.ps1 --purge
```

Core uninstall leaves `uv` and RepoWise installed. Other repositories and tools can use them.

Uninstall also leaves all Plan history records in their project or fallback locations.

Core uninstall leaves generated roadmap views because it does not track repository locations. Remove owned view files before core uninstall.

On macOS or Linux, run:

```bash
python3 kit.py remove-repo <repository>
```

On Windows, run:

```powershell
python kit.py remove-repo <repository>
```

## Verification

On macOS or Linux, run:

```bash
./run-tests.sh
sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
git diff --check
sha256sum --check MANIFEST.sha256
```

On Windows, run:

```powershell
pwsh -File .\run-tests.ps1
git diff --check
```

`MANIFEST.sha256` covers distributed files. Regenerate it after code and documentation are final.

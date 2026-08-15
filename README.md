# Codex Practical Kit

Codex Practical Kit installs a small working agreement for personal repositories. It favors direct code, clear documentation, and bounded review.

The managed `AGENTS.md` is a router. It links focused rule owners instead of loading the complete policy for every task.

## Included components

The kit installs these task skills:

- `ponytail`
- `simple-english`
- `design-preflight`
- `research-first`
- `docs-maintainer`
- `roadmap-maintainer`
- `adversarial-review`
- `defect-diagnostic`

It also installs `codex-practical-kit-rules`. This package contains the focused rule files that AGENTS links.

## Install

Run:

```bash
./run-tests.sh
./install.sh
./doctor.sh
```

The installer copies managed skills to `~/.agents/skills/`. Do not edit installed copies.

The installer writes a managed block in `~/.codex/AGENTS.md`. It renders absolute links for the configured skills and PLANS paths.

The installer also writes `$CODEX_HOME/PLANS.md` and a managed Session Start hook. The hook only announces that the AGENTS router is active.

An unrecorded destination skill is a conflict. The installer stops before it changes that directory.

Open a new Codex session after installation. Use `/hooks` to review and trust the Session Start command.

## Rule owners

Read only the rule that applies to the task:

- [Rule ownership](assets/skills/codex-practical-kit-rules/references/rule-ownership.md)
- [Coordination](assets/skills/codex-practical-kit-rules/references/coordination.md)
- [Supported model](assets/skills/codex-practical-kit-rules/references/supported-model.md)
- [Decision handoffs](assets/skills/codex-practical-kit-rules/references/decision-handoffs.md)
- [Repository knowledge](assets/skills/codex-practical-kit-rules/references/repository-knowledge.md)
- [Delivery lifecycle](assets/skills/codex-practical-kit-rules/references/delivery-lifecycle.md)
- [Git isolation](assets/skills/codex-practical-kit-rules/references/git-isolation.md)
- [Full-set results](assets/skills/codex-practical-kit-rules/references/full-set-results.md)
- [Owner composition](assets/skills/codex-practical-kit-rules/references/owner-composition.md)
- [Review closure](assets/skills/codex-practical-kit-rules/references/review-closure.md)
- [Publication](assets/skills/codex-practical-kit-rules/references/publication.md)
- [Versioning](assets/skills/codex-practical-kit-rules/references/versioning.md)

Skill-specific procedures remain in each skill. [ExecPlan rules](.agent/PLANS.md) remain focused on executable plans.

## RepoWise

The core install provides pinned `uv` and RepoWise when they are absent. It configures one required user-level RepoWise MCP server.

In a Git repository, the first MCP start creates the index and installs RepoWise's `post-commit` hook. A completely empty folder becomes a Git repository. A non-empty, non-Git folder remains unchanged.

Run eager setup when you need the index before the next Codex session:

```bash
./setup-repo.sh /path/to/repository
./doctor.sh --repo /path/to/repository
```

See [RepoWise notes](docs/REPOWISE.md) for setup, refresh, opt-out, and trust-boundary details.

## Uninstall

Remove managed integrations and copied skills:

```bash
./uninstall.sh
```

Also remove toolkit files:

```bash
./uninstall.sh --purge
```

Core uninstall leaves `uv` and RepoWise installed. Other repositories and tools can use them.

## Verification

Run:

```bash
./run-tests.sh
sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
git diff --check
sha256sum --check MANIFEST.sha256
```

`MANIFEST.sha256` covers distributed files. Regenerate it after code and documentation are final.

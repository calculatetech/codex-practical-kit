# Optional Spec Kit

Spec Kit is an optional behavior source. The [ExecPlan rules](../.agent/PLANS.md) remain authoritative for implementation plans.

Use the managed AGENTS routes for Design Preflight and other task procedures.

Add Spec Kit when the task needs more behavior detail. Good signals include:

- A new application.
- A feature with several user stories.
- Several teams or reviewers.
- A long implementation with durable plan and task artifacts.
- A need for repeatable specification commands across many repositories.

## Install

Use the current official installation guide. A typical Codex skills-mode setup is:

```bash
uv tool install specify-cli
specify init --here --integration codex --integration-options="--skills"
```

Run `specify integration list` first when the installed release changes its integration names or options.

## Ownership

Apply [Rule ownership](../assets/skills/toolkit-maintainer/SKILL.md).

When Spec Kit supplies the behavior specification:

- Its specification is the durable behavior source.
- Plan Mode summaries remain as immutable repository records and specification siblings for later reconciliation.
- The task ExecPlan records stable implementation decisions. Apply [Delivery lifecycle](../assets/skills/delivery-lifecycle/references/delivery-lifecycle.md) for operational progress and lifecycle state.
- Applicable managed skills link from AGENTS.

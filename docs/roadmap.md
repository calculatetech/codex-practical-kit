# Codex Practical Kit Roadmap

This is the source of truth for toolkit work. Task identifiers are permanent. Once assigned, a `CPK-###` number is never reused or changed. Move tasks between sections as their status changes. Never mark more than one task active.

Status legend:

- 🎯 **Active** — implementation or required review is in progress
- ⏭ **Planned next** — accepted and ordered for near-term delivery
- ◻ **Planned later** — accepted but not yet scheduled
- ⚠️ **Accepted residual risk** — bounded work is complete, but a documented limitation remains accepted
- ❌ **Declined** — considered and intentionally not supported
- ✅ **Completed** — implemented and validated

## Active

No task is active.

## Planned next

No task is planned next.

## Planned later

No task is planned later.

## Accepted residual risk

No residual risk is accepted.

## Declined

- ❌ **CPK-009 — Make complete installation transactional.** The toolkit intentionally stops and reports an operation error. It does not recover partial installation work.

## Completed

- ✅ **Minimal implementation discipline.** Ponytail, Simple English, repository-first inspection, and focused validation rules are installed.
- ✅ **Design and planning foundation.** Design Preflight, Spec Kit guidance, and ExecPlan rules are available.
- ✅ **Review and documentation foundation.** Clean-context adversarial review, the three-pass breaker, and documentation maintenance are available.
- ✅ **CPK-001 — Make roadmap state authoritative.** The Roadmap Maintainer, template, and lifecycle rules make `docs/roadmap.md` the human source of truth.
- ✅ **CPK-003 — Reconcile adversarial review.** One fresh reviewer per pass applies the supported-model true or false gate before commit.
- ✅ **CPK-004 — Define Git task isolation.** Branches isolate one implementation stream. Worktrees isolate independent writers. Main remains available for bounded documentation work.
- ✅ **CPK-005 — Define version increments.** Initial development starts at 0.1.0. Features increment minor versions. Fixes and published same-feature checkpoints increment patch versions.
- ✅ **CPK-006 — Define PR publication.** Repositories use PR mode only after CI and protected `main` enforce its gates. One `publish` request then authorizes the path through verified squash merge.
- ✅ **CPK-007 — Close PR conversations.** Delivered through CPK-006. Current CI, a current Codex clean signal, and resolved conversations gate merge.
- ✅ **CPK-010 — Restore deterministic least effort.** Copy-only installation with manifest-scoped ownership, one-attempt failure handling, plain Git status, and bounded review replace speculative recovery and proof machinery.
- ✅ **CPK-002 — Make ExecPlan the durable task model.** The kit installs one global ExecPlan fallback, preserves repository overrides, and removes Task Brief as a competing owner.
- ✅ **CPK-011 — Make RepoWise self-starting and self-updating.** The kit installs missing runtime tools, initializes Git repositories from Codex, enables RepoWise MCP calls, and maintains the wiki after commits.
- ✅ **CPK-012 — Prevent self-invalidating review closure.** Material changes invalidate review. Review-result, roadmap, publication, checksum, and ignored test-record updates close a clean review without recursion.
- ✅ **CPK-008 — Make decision handoffs operator-readable.** Material choices now use a compact handoff with the trigger, likelihood, exposure, option effects, recommendation, and exact question.
- ✅ **CPK-013 — Bootstrap empty project folders.** Empty workspaces now initialize Git and RepoWise. Non-empty, non-Git folders remain unchanged.
- ✅ **CPK-014 — Remove the Stop hook.** The toolkit installs only Session Start. Reinstallation removes old Stop and Session End hooks while it preserves unrelated handlers. Agent instructions remain the review authority.
- ✅ **CPK-015 — Install Codex hooks in config.toml.** The installer checks parsed Session Start handler entries in the documented Codex configuration file. It leaves existing matching entries unchanged and creates no legacy JSON file.
- ✅ **CPK-016 — Require the RepoWise code graph.** Codex waits for automatic RepoWise initialization and does not continue without the required graph.

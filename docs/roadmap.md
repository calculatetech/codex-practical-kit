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

- ⏭ **CPK-004 — Define Git task isolation.** Set branch, worktree, checkpoint commit, authorization, cleanup, and dirty-tree rules.
- ⏭ **CPK-005 — Define version increments.** Formalize feature increments to the second digit and bug-fix increments to the third. Set timing, synchronized files, failed-release handling, and release boundaries.
- ⏭ **CPK-006 — Define PR publication.** State when work needs a pull request, when drafts become ready, and which checks gate publication.
- ⏭ **CPK-007 — Close PR conversations.** Monitor CI and Codex review, detect approval reactions or findings, respond, and resolve all threads.

## Planned later

- ◻ **CPK-008 — Make decision handoffs operator-readable.** Explain unfamiliar terms, the concrete trigger, likelihood in the supported operating model, current exposure, options, effects, and a recommendation before requesting direction.

## Accepted residual risk

No residual risk is accepted.

## Declined

- ❌ **CPK-009 — Make complete installation transactional.** The toolkit intentionally stops and reports an operation error. It does not recover partial installation work.

## Completed

- ✅ **Minimal implementation discipline.** Ponytail, Simple English, repository-first inspection, and focused validation rules are installed.
- ✅ **Design and planning foundation.** Design Preflight, Spec Kit guidance, and ExecPlan rules are available.
- ✅ **Review and documentation foundation.** Clean-context adversarial review, the three-pass breaker, documentation maintenance, and Git-status reminders are available.
- ✅ **CPK-001 — Make roadmap state authoritative.** The Roadmap Maintainer, template, and lifecycle rules make `docs/roadmap.md` the human source of truth.
- ✅ **CPK-003 — Reconcile adversarial review.** One fresh reviewer per pass applies the supported-model true or false gate before commit.
- ✅ **CPK-010 — Restore deterministic least effort.** Copy-only installation with manifest-scoped ownership, one-attempt failure handling, plain Git status, and bounded review replace speculative recovery and proof machinery.
- ✅ **CPK-002 — Make ExecPlan the durable task model.** The kit installs one global ExecPlan fallback, preserves repository overrides, and removes Task Brief as a competing owner.
- ✅ **CPK-011 — Make RepoWise self-starting and self-updating.** The kit installs missing runtime tools, initializes Git repositories from Codex, enables RepoWise MCP calls, and maintains the wiki after commits.
- ✅ **CPK-012 — Prevent self-invalidating review closure.** Material changes invalidate review. Review-result, roadmap, publication, checksum, and ignored test-record updates close a clean review without recursion.

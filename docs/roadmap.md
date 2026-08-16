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

- ✅ **CPK-031 — Freeze tracked task status before delivery.** Tracked task records contain their final durable state before commit, CI, push, pull request, merge, or publication.
- ✅ **CPK-030 — Make RepoWise index-first and self-refreshing.** Exact lookups use indexed selectors, model synthesis remains optional, and active Codex sessions keep working-tree edits indexed without model calls.
- ✅ **CPK-029 — Activate normal mode when Plan mode starts.** The managed prompt hook selects Ponytail normal mode before each Plan-mode prompt. Other modes keep their selected implementation mode.
- ✅ **CPK-028 — Scope minimalism by lifecycle phase.** Planning, research, test-scope definition, and read-only review use normal mode. Implementation uses Ponytail after scenario obligations are fixed, and each retained runtime scenario maps to one production path, oracle, runnable check, and result.
- ✅ **CPK-027 — Move rules into lifecycle skills.** AGENTS now routes tasks to lifecycle skills. Each shared rule remains in one focused owner, and upgrades remove the obsolete general package.
- ✅ **CPK-026 — Add content-addressed review checkpoints.** Later correctness passes review only fix deltas and direct impact. One final coherence pass checks the complete task after fixes.
- ✅ **CPK-025 — Verify the live toolkit before publication.** Toolkit publication now requires live installation and a ready Doctor result from the reviewed candidate.
- ✅ **CPK-024 — Bind reviews to documented product scope.** One scope owner now limits planning and review to documented product use cases and task-relevant owners.
- ✅ **CPK-023 — Enforce single rule ownership.** Focused rule files are authoritative. AGENTS routes by task, and validation rejects duplicate owners and invalid routes.
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
- ✅ **CPK-017 — Count only implementation defects toward the review breaker.** Documentation and review-housekeeping findings remain actionable but do not advance or reset the three-defect count.
- ✅ **CPK-018 — Compact the global agent profile.** The managed policy is below 100 lines and defines safe coordinator, subagent, and reviewer roles.
- ✅ **CPK-019 — Make direct publication integrate final work.** In direct mode, one `publish` request now authorizes the path through verified integration into `main`. Tags, releases, and cleanup remain separate.
- ✅ **CPK-020 — Protect full-set invariants from bounded samples.** Implementation policy, Design Preflight, and correctness review now reject success derived from bounded raw-input samples.
- ✅ **CPK-021 — Diagnose severe defects at review stop gates.** Each stop finding gets a separate decision handoff. The same final response includes the complete diagnostic before the human halt.
- ✅ **CPK-022 — Derive runtime scenarios before implementation.** Design Preflight now derives independent input, path, transition, and collection scenarios, preserves contract gaps, and stores accepted proof in one ExecPlan.

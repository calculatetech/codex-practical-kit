# Repair worktree handoffs, preflight, and publication

This ExecPlan is the durable CPK-047 implementation specification. Maintain it according to `.agent/PLANS.md`.

## Purpose

Plan History can leave an applicable untracked record in the worktree that accepted a Plan after implementation moves to another worktree. That redundant file can later block a fast-forward of local `main`.

Design Preflight can give its challenger a source surface that is broader than the accepted task. Publication can also confuse local native review with GitHub PR review or finish while local `main` remains stale.

Release these corrections as version `0.23.2` on branch `cpk-047-bounded-preflight-publication` from commit `94a23813a5337b1716cc43de69b8571bec24c2aa`.

## Product boundary

[Plan History](../../assets/skills/plan-history/SKILL.md) owns applicable record discovery, immutable content, and cross-worktree handoff. [Coordination](../../assets/skills/delivery-lifecycle/references/coordination.md) owns delegated-task liveness. [Design Preflight](../../assets/skills/design-preflight/SKILL.md) owns challenger scope and its two phases. [Publication](../../assets/skills/publication/references/publication.md) owns PR sequencing and integration completion.

Adversarial Review retains local review and finding authority. Supported Model retains one-attempt error handling. Git Isolation retains task-start divergence rules. The task adds no hook behavior, helper, parser, daemon, database, dependency, or runtime state machine.

## Decisions

- Relocate an applicable untracked Plan record by copying it to the task worktree, comparing bytes, and removing only the redundant source copy.
- Keep central and specification-sibling records in the task worktree because they have different discovery roles.
- Bound preflight by the accepted outcome. Permit source expansion only through authoritative product evidence or a direct composing relationship.
- Keep one challenger identity for both phases. Elapsed time does not authorize a duplicate task.
- Treat local native review and GitHub PR review as separate cumulative gates.
- After a remote squash merge, fast-forward local `main` to `origin/main` before publication completes.
- Preserve unrelated untracked files. Stop only for tracked changes, divergence, or an actual overwrite conflict.

## Checkpoints

### CP1 — Transfer pending Plan History

Update the Plan History owner and its deterministic owner test. Require discovery across worktrees in the same Git repository. Copy applicable untracked records to the same task-worktree path. Remove a source copy only after exact byte equality. Retain unique, tracked, unrelated, or different-content records.

Run the focused Plan History checks, one checkpoint native review, and one local checkpoint commit.

### CP2 — Bound preflight

Add a task-bound source packet and an evidence-backed `source_scope` result. Keep one challenger for both phases. Route generic liveness to Coordination and one-attempt errors to Supported Model.

Run the focused preflight checks, one checkpoint native review, and one local checkpoint commit.

### CP3 — Reconcile publication

Require Plan History handoff before publication classifies worktree state. Require exact local, remote-branch, and PR-head identity. Keep local and GitHub review gates separate. After squash merge, fetch `origin`, fast-forward the clean local-main worktree, prove integration, and monitor post-merge CI.

Run the focused publication checks, one checkpoint native review, and one local checkpoint commit. Then run one final native review of the complete candidate.

## Validation

- Prove safe Plan record relocation, collision retention, tracked-record protection, and repeatable partial-copy handling.
- Prove bounded preflight sources, supported expansion, one live challenger, and no automatic restart.
- Prove separate review gates, exact current-head review, local-main fast-forward, and safe stops.
- Run the complete Python suite, skill validation, link checks, shell and PowerShell checks, manifest validation, and `git diff --check`.
- Install the final reviewed candidate and require Doctor to report `Result: ready`.

## Prior Plan reconciliation

Record: `.agent/plan-history/plan-summary.20260825T172626414955Z.9eaf7888a286b18f69d5a94869ee99522214d23dd715a553664a2041108fced3.md`

Status: superseded

Reason: The publication checkpoint did not first relocate pending Plan History records from the `main` worktree.

Replacement: Add CP1 relocation before preflight and publication. Apply that owner before publication classifies worktree state.

Scope: unfinished subtasks CP1 and CP2.

Record: `.agent/plan-history/plan-summary.20260825T173129857080Z.a3ee26a1802fb85c5a0a100ccb3c33c1a6fff358bd20b65636adc61f8d0de377.md`

Status: carried

Reason: This record is the accepted CPK-047 implementation contract.

The completed CPK-035, CPK-042, CPK-043, CPK-044, and final CPK-046 decisions remain carried.

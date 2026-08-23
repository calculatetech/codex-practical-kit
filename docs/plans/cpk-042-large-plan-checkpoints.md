# Split large plans into reviewed checkpoints

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose

Plan Mode must divide large work at independently verifiable boundaries. One ExecPlan keeps stable, ordered subtasks. Each completed subtask receives focused validation, review, and a local checkpoint commit. One final coherence review covers the complete task.

## Progress

- [x] (2026-08-23) Reconciled the accepted CPK-042 Plan with CPK-040 and CPK-041.
- [x] (2026-08-23) Created branch `cpk-042-large-plan-checkpoints` from `0013a3c0d3c777514e9315ae46b7bd17f471962e`.
- [x] (2026-08-23) Made CPK-042 the only Active roadmap task.
- [x] (2026-08-23) CP1: Added checkpoint review and delivery rules. Validation and the correction delta review passed.
- [ ] CP2: Add semantic plan splitting and safe replanning, validate them, review them, run final coherence, and create a local commit.

## Prior Plan Reconciliation

Record: `.agent/plan-history/plan-summary.20260822T050100617085Z.fd7dfe4c94e461a1824112794d31e1372d316ccf79eed8a3937d2754c1157e40.md`

Status: carried

Reason: CPK-040 preserves distinct accepted Plan responses and links them to one ExecPlan.

Record: `.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md`

Status: carried

Reason: CPK-041 remains authoritative for source-backed material decisions.

Record: `.agent/plan-history/plan-summary.20260823T052048899607Z.c539b46a7e5fa56092a382fef046fd00d4271c42c4fda8e0f0e2216ce94df122.md`

Status: carried

Reason: This record is the accepted CPK-042 implementation contract.

## Product Boundary

The ExecPlan owner defines semantic subtask boundaries. Adversarial Review owns checkpoint and coherence review behavior. Delivery Lifecycle owns local commit eligibility. Plan History owns replan reconciliation.

The task changes installed instructions and their contract tests. It does not add runtime state, child plans, a task database, an action counter, a dependency service, or a new skill. Plan capture remains unchanged.

## Normal-Use Behavior Floor

A large Plan contains stable subtasks when its outcomes can be implemented and proved separately. Each subtask names its outcome, owner boundary, dependencies, implementation result, validation oracle, review boundary, and local commit boundary.

A clean checkpoint review covers only the current subtask delta and its direct interaction with completed checkpoints. It does not close the task. One final coherence review covers the complete feature before roadmap completion.

When Plan Mode replans unfinished work, it preserves completed identifiers, outcomes, contracts, and commits. A change to completed behavior becomes a new corrective subtask.

## Scope Ceiling

Use semantic boundaries only. Do not add a numeric action ceiling. Do not split one atomic migration or stateful sequence that needs one proof boundary. Do not create child ExecPlans or mutable task infrastructure.

## Subtasks

### CP1 — Reviewed-subtask delivery

Observable outcome: A completed subtask can receive a scope-bound checkpoint review and local commit without closing the task.

Primary owner and change boundary: Adversarial Review owns `checkpoint` mode and its packet. Delivery Lifecycle only consumes the clean checkpoint result to allow a local commit.

Dependencies: Existing `full`, `delta`, and `coherence` review modes; existing task-wide production-defect accounting.

Implementation result: Adversarial Review now defines `checkpoint` mode. Its packet records the subtask and previous accepted checkpoint. Delivery Lifecycle permits the reviewed local commit without closing the task.

Validation and oracle: The focused checkpoint-rule test passed. All 80 default Python checks passed, with one native Windows skip. Shell syntax and `git diff --check` passed.

Review result: Pass 1 found that a corrected checkpoint had no commit path after its clean delta review. The correction makes that delta the clean checkpoint result. The focused delta review was clean.

Checkpoint boundary: Review the staged CP1 tree with the existing full-review workflow. Commit locally only after a clean result.

### CP2 — Semantic splitting and safe replanning

Observable outcome: Plan Mode produces one ExecPlan with stable semantic subtasks and preserves completed checkpoints during replanning.

Primary owner and change boundary: `.agent/PLANS.md` owns subtask structure. Plan History owns replan reconciliation. Tests and version metadata prove installation.

Dependencies: CP1 checkpoint review and commit rules.

Implementation result: Pending.

Validation and oracle: Run focused plan-rule and history tests, the complete suite, compilation, shell syntax, owner, route, manifest, and diff checks. Install the toolkit, require Doctor `Result: ready`, then run one clean planning smoke and one completed-checkpoint replan smoke.

Checkpoint boundary: Review CP2 against the accepted CP1 commit. After it passes, run one cumulative coherence review from the task base. Close the task and commit locally only after both reviews pass.

## Validation and Acceptance

Keep detailed output in one ignored CPK-042 test-result file. Finalize substantive documentation before each review. Keep the roadmap Active after CP1. Move it to Completed only after final coherence passes.

## Interfaces and Dependencies

The review mode enum gains `checkpoint`. Its packet gains the subtask identifier and previous accepted checkpoint. The toolkit version becomes `0.21.0`. No dependency changes.

## Outcome

Pending.

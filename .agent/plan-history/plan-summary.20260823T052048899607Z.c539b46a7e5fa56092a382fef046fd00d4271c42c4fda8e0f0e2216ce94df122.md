<proposed_plan>
# CPK-042 — Split Large Plans into Reviewed Checkpoints

## Summary

Plan Mode will divide large work by semantic boundaries, not arbitrary point counts.

One ExecPlan will contain stable, ordered subtasks. Each subtask must produce one independently verifiable outcome.

Each subtask will receive focused validation and adversarial review before its checkpoint commit. One final coherence review will check the complete feature.

Release this feature as version `0.21.0`. This design follows OpenAI’s guidance for independent milestones and frequent commits. [Official OpenAI ExecPlan guidance](https://developers.openai.com/cookbook/articles/codex_exec_plans/)

## Implementation Changes

### Checkpoint 1: Add reviewed-subtask delivery

Extend Adversarial Review with a `checkpoint` mode.

- Compare the staged subtask with the previous accepted checkpoint.
- Review the new subtask, its direct dependencies, and its interaction with completed checkpoints.
- Do not reopen unchanged checkpoint code.
- Use existing delta reviews for corrections to the current checkpoint.
- Keep production-defect accounting active across the complete task.
- Delay review closure and roadmap completion until final coherence passes.

Update Delivery Lifecycle to permit a local checkpoint commit only after that subtask has a final clean review result.

Keep the task Active after intermediate commits. Do not authorize a push, merge, tag, release, or publication.

Run focused checks and full validation. Review this checkpoint with the existing full-review workflow, then create its local checkpoint commit.

### Checkpoint 2: Add semantic plan splitting and replanning

Extend the ExecPlan owner in `.agent/PLANS.md`.

Require multiple subtasks when work contains separately verifiable:

- User-visible outcomes.
- Primary code owners.
- Foundation and consumer stages.
- Migrations and later adoption.
- Interfaces that can remain valid before later work starts.

Do not use a numeric action limit. Do not create artificial splits when one stateful sequence or atomic migration requires one proof boundary.

Use one stable subtask identifier for each checkpoint. Do not renumber completed subtasks.

Each subtask must state:

- Its observable outcome.
- Its primary owner and allowed change boundary.
- Its dependencies on earlier subtasks.
- Its implementation result.
- Its exact validation command and required oracle.
- Its checkpoint review and local commit boundary.

Extend Plan History for checkpoint replanning.

- Read the current ExecPlan, applicable Plan records, and completed checkpoint history.
- Keep completed subtask outcomes and accepted contracts unchanged.
- Permit splits, merges, and reordering only for unfinished subtasks.
- Record scoped supersession when a new Plan replaces unfinished work.
- Add a corrective subtask when a new requirement changes completed behavior.
- Never amend or rewrite a completed checkpoint commit.

Update version `0.20.0` to `0.21.0`, focused tests, task documentation, roadmap state, and checksums.

Review this checkpoint against the first checkpoint commit. Then run one cumulative coherence review before review closure and the final local commit.

## Interfaces and Ownership

The review-result schema gains `checkpoint` as a review mode. Its packet gains the subtask identifier and previous accepted checkpoint.

The ExecPlan remains the only durable implementation plan. No child ExecPlans, parent index, task database, action counter, dependency service, or new skill will exist.

The Plan capture runtime remains unchanged. It already stores distinct accepted replans beside the same ExecPlan without overwriting earlier records.

## Test Plan

- Prove that semantic split triggers exist and no numeric ceiling exists.
- Prove that each subtask contains one outcome, dependencies, owner boundary, proof, review gate, and commit boundary.
- Prove that checkpoint review excludes unchanged completed checkpoints.
- Prove that final coherence covers all checkpoint interactions exactly once.
- Prove that review closure cannot occur after an intermediate checkpoint.
- Prove that two accepted Plans for one ExecPlan create distinct immutable history records.
- Prove that a replan preserves completed subtasks and changes only the unfinished tail.
- Prove that changing completed behavior creates a new corrective subtask.
- Run the complete Python suite, compilation, shell syntax, owner, route, manifest, and diff checks.
- Install the reviewed toolkit and require Doctor to report `Result: ready`.
- Run a clean Plan Mode smoke with several independent outcomes. Confirm that it produces one checkpointed ExecPlan.
- Run a second clean Plan Mode smoke after one simulated checkpoint. Confirm that replanning preserves the completed checkpoint.

## Assumptions and Boundaries

Use branch `cpk-042-large-plan-checkpoints` from synchronized commit `0013a3c`.

Use one implementation stream. A worktree and multiple implementation agents are unnecessary.

Checkpoint commits remain local until the user requests publication.

The existing hook runtime, Git CLI, choice widget, roadmap format, and publication policy remain opaque and unchanged.

## Prior Plan Reconciliation

Record: `.agent/plan-history/plan-summary.20260822T050100617085Z.fd7dfe4c94e461a1824112794d31e1372d316ccf79eed8a3937d2754c1157e40.md`  
Status: carried  
Reason: CPK-040 already preserves multiple accepted Plan responses and links them to one ExecPlan.

Record: `.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md`  
Status: carried  
Reason: CPK-041 remains authoritative for source-backed material decisions and the choices made during this plan.

Preflight: ready — reuse one ExecPlan, semantic subtask boundaries, reviewed checkpoint commits, and final coherence.

<!-- cpk-plan-spec: docs/plans/cpk-042-large-plan-checkpoints.md -->
</proposed_plan>
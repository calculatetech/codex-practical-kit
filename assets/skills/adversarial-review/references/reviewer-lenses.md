# Native review targets

Native Codex review independently inspects the selected commit, repository, dependencies, and tests for actionable defects introduced by the candidate. Do not preload the coordinator's conclusions.

## Product scope

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](../../design-preflight/references/scope-boundaries.md)

## Scenario discrimination

<!-- cpk-rule-route-only: scenario-discrimination -->
[Scenario discrimination](../../design-preflight/references/scenario-discrimination.md)

## Owner composition

<!-- cpk-rule-route-only: owner-composition -->
[Owner composition](../../design-preflight/references/owner-composition.md)

## Full-set results

<!-- cpk-rule-route-only: full-set-results -->
[Full-set results](../../design-preflight/references/full-set-results.md)

## Full correctness

Use the task base as the synthetic commit parent. The staged tree is the complete task candidate.

## Delta correctness

Use the previous reviewed candidate as the parent. The staged tree adds only the correction and its direct impact. Native review can inspect repository context, but the coordinator rejects findings that reopen unchanged behavior without a changed contract or execution path.

## Checkpoint correctness

Use the previous accepted checkpoint as the parent, or the task base for the first checkpoint. The staged tree adds one planned subtask and its interactions with completed checkpoints.

## Final correctness

Use the task base as the parent. The staged tree is the complete current candidate. This is a full correctness review, not a limited coherence review.

## Adjudication

After native discovery, the coordinator proves each finding's execution path and accepted end result. Then it applies the [Adversarial Review finding-validation procedure](../SKILL.md#validate-findings). A native severity or fix suggestion does not authorize a correction.

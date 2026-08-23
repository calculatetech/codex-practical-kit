# Reviewer lenses

## Product scope

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](../../design-preflight/references/scope-boundaries.md)

## Correctness

Always check the supported normal path:

- The requested result occurs.
- Inputs and outputs keep their documented meaning.
- Setup and cleanup agree.
- A branch does not report success before the result exists.
- Tests exercise the real owner.
- Each retained Scenario Proof row follows its production path to the required oracle in the named runnable check.
- A suite count does not substitute for a scenario result.

Apply [Scenario discrimination](../../design-preflight/references/scenario-discrimination.md) to every retained scenario. Apply [Owner composition](../../design-preflight/references/owner-composition.md) and [Full-set results](../../design-preflight/references/full-set-results.md) when they are applicable.

## Delta correctness

Inspect the candidate slice, direct-impact sources, and prior findings named in the review packet.

## Checkpoint correctness

Inspect the current subtask delta, its direct dependencies, and its interactions with completed checkpoints. Do not reopen unchanged completed work.

## Final coherence

Inspect the cross-component interactions, transition-closed scenario mappings, and unresolved findings named in the review packet.

## Optional lenses

Add one of these lenses to the same reviewer only when the active task names it:

- Security for an explicit trust boundary.
- API contract for an external interface.
- Migration for a declared data change.
- Performance for a measured resource problem.

Do not review excluded conditions. Do not attack assumptions that define the supported operating model.

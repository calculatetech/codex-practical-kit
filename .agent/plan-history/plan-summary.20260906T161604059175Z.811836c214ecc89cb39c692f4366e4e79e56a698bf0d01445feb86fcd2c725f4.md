<proposed_plan>
# CPK-056 — Ask material questions in dependency order

## Summary

Extend the existing interview rules so Codex settles prerequisite decisions before asking dependent questions. Keep interviews bounded by the requested outcome.

Checkpoint relay is deferred. No diagnosis or correction-gate changes are included.

## Implementation

Keep [decision-handoffs.md](/home/mbeutler/Projects/codex-practical-kit/assets/skills/delivery-lifecycle/references/decision-handoffs.md) as the sole rule owner.

- When product intent is unclear, identify material decisions and their prerequisites in working context.
- Resolve discoverable facts before asking the user.
- Ask the highest-impact question whose prerequisites are settled. Batch up to three independent questions when useful.
- After an answer or relevant discovery, reassess which questions remain necessary. Accept partial answers without repeating settled questions.
- Stop interviewing once material behavior, scope, and acceptance criteria are settled. Do not require exhaustive questioning or another confirmation of already approved decisions.
- Preserve the existing decision brief for each material technical choice. Adjust the single-question wording to permit bounded batches.

Add no skill, dependency, hook, persistent decision tree, or duplicate planning artifact. Record CPK-056 through the existing roadmap lifecycle.

## Validation and delivery

Extend the existing decision-handoff test to cover prerequisite ordering, independent batches, partial answers, and the stopping condition. Retain its checks for source-backed options, brief ordering, and routine-question exclusions.

Run the focused test, `./run-tests.sh`, rule-owner and link checks, manifest validation, and `git diff --check`. Finalize affected documentation before native review. After clean review, complete normal local delivery, installation, and Doctor checks. Publication remains separate.

## Prior plan reconciliation

Carry the CPK-041 Plan record forward: material-choice criteria, explanation requirements, and routine-question exclusions remain unchanged. Preserve the completed CPK-008 and CPK-041 specifications as historical records.

Existing correction-authority and preflight requirements remain in force. Investigating a specific boundary escape remains separate from this interview improvement.

<!-- cpk-plan-spec: docs/plans/cpk-008-decision-handoffs.md -->
<!-- cpk-plan-spec: docs/plans/cpk-041-implementation-aware-decisions.md -->
</proposed_plan>
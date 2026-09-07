<proposed_plan>
# CPK-057 — Separate review from testing and complete Astra guidance

## Summary

Reviewers inspect source and existing evidence without running tests. Implementation completes validation before review.

Incorporate the remaining applicable [Astra prompting advice](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices) through existing rule owners. Adopt bounded proactive delegation. Its live validation belongs to the other project.

## CP1 — Separate review from validation

- Put the reviewer execution restriction in Adversarial Review. Prohibit suites, focused tests, reproduction scripts, and delegated test execution during review.
- Permit source inspection, reading test bodies and existing results, and reporting source-backed defects. Passing tests do not suppress valid findings.
- Assign validation to the implementation owner before review. Preserve required checks and meaningful regression tests.
- Repeat or broaden completed checks only for changed code, failures, or a concrete unresolved concern. Perform this work outside review.
- Preserve native `codex review --commit`, exact candidate identity, and independent discovery. Include this task’s actual no-tests requirement in the first synthetic commit’s accepted intent.
- Carry the canonical execution restriction into both initial and repeated hosted review requests. Preserve the separate CI gates.
- Update the existing review and lifecycle instruction checks. Validate, review, and commit this checkpoint.

## CP2 — Complete the collaboration guidance

Update existing owners with these missing requirements:

| Owner | Addition |
|---|---|
| Delivery Lifecycle | Finish authorized work, preserve prior authorization, and prepare concrete results before necessary approval. Avoid speculative permission barriers. |
| Coordination | Give user instructions precedence over skill guidelines. Explain skill-caused stops with the exact file, relevant quotation, and explicit requirement versus interpretation. |
| Docs Maintainer | Lead with the outcome. Prefer concise, connected prose, appropriate technical detail, and useful formatting. Remove stock phrases and invented labels. |
| Coordination | Delegate concrete independent work when useful. Preserve existing writer, capacity, child-role, and native-review restrictions. Keep agent messages legible. |
| Toolkit Maintainer | Check applicable instructions for conflicts and duplication when changing guidance. |

Keep autonomy within the active mode, accepted scope, and existing correction authority. Preserve material-decision explanations, required structured output, and technical identifiers.

Record each guide item as added, already covered, or adapted in the ExecPlan. Reuse Simple English and preserve upstream Ponytail behavior.

## Validation and delivery

- Extend only the necessary existing instruction checks. Run normal owner, route, link, suite, syntax, checksum, and diff checks before review.
- Inspect actual native review tool activity to confirm that reviewers execute no tests. Use the required reviews themselves; add no separate review experiment.
- Do not add delegation assessments or repeat CPK-056 cases. Make no claim that delegation behavior was validated here.
- Review and commit CP2, then complete the final native review.
- Apply normal closure, install the reviewed toolkit, and require Doctor to report `ready`.

## Assumptions and prior plan reconciliation

Create `task/cpk-057-review-astra-guidance` from `a33c806`, with one ExecPlan at `docs/plans/cpk-057-review-and-astra-guidance.md`.

Carry the applicable CPK-041 through CPK-048, CPK-053, CPK-055, and final CPK-056 records, including their recorded supersessions. Preserve completed checkpoints.

No new skill, framework, runtime configuration, model setting, or external-project change is included. Version selection and publication remain separate.

<!-- cpk-plan-spec: docs/plans/cpk-057-review-and-astra-guidance.md -->
<!-- cpk-plan-spec: docs/plans/cpk-041-implementation-aware-decisions.md -->
<!-- cpk-plan-spec: docs/plans/cpk-042-large-plan-checkpoints.md -->
<!-- cpk-plan-spec: docs/plans/cpk-043-review-gated-publication.md -->
<!-- cpk-plan-spec: docs/plans/cpk-044-review-correction-authority.md -->
<!-- cpk-plan-spec: docs/plans/cpk-045-boundary-trace-closure.md -->
<!-- cpk-plan-spec: docs/plans/cpk-046-repowise-worktree-recovery.md -->
<!-- cpk-plan-spec: docs/plans/cpk-047-bounded-preflight-publication.md -->
<!-- cpk-plan-spec: docs/plans/cpk-048-shared-instruction-reconciliation.md -->
<!-- cpk-plan-spec: docs/plans/cpk-053-continuous-path-proof.md -->
<!-- cpk-plan-spec: docs/plans/cpk-055-native-ponytail.md -->
<!-- cpk-plan-spec: docs/plans/cpk-056-interviews-and-assessment.md -->
</proposed_plan>
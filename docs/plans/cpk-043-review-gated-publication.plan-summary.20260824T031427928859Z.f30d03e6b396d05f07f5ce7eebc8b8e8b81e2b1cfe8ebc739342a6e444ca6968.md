<proposed_plan>
<!-- cpk-plan-spec: CPK-043 review-gated PR publication -->
# CPK-043 — Review PRs Before Hosted CI

## Summary

Correct PR publication so Codex reviews the latest commit while the PR remains draft. Hosted CI starts only after the review has no retained findings.

OpenAI supports an explicit `@codex review` request on a PR. GitHub supports workflows that start when a PR becomes ready. Together, these remove the need for a new dispatcher or state machine. [OpenAI Codex review guidance](https://openai.com/index/introducing-upgrades-to-codex/), [GitHub workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)

Implement this bugfix as version `0.21.1`. Create `cpk-043-review-gated-publication` from the current CPK-042 branch. Do not modify either CPK-042 commit.

## Publication Changes

- Before any push, prove that task-branch pushes and draft PRs cannot start hosted CI. If `main` requires PRs but CI is not draft-safe, stop with a configuration error. Do not fall back to direct integration.
- Push the branch, open a draft PR, verify its scope, and post `@codex review`.
- Keep the PR draft while reviewing and correcting findings. Each push invalidates the earlier review.
- Define a clean review as a completed Codex review of the current head with no retained applicable findings. A raw thumbs-up is sufficient but not required when all comments are correctly excluded.
- Mark the PR ready only after the current-head review is clean. Readiness may then start hosted CI.
- If a later correction needs a push, convert the PR to draft first. Repeat the review gate before CI runs again.
- Preserve the existing latest-head CI, conversation-resolution, mergeability, squash-merge, and integration checks.

Route every PR finding through the existing Adversarial Review owner:

- Apply the scope and supported-model gates before accepting the reviewer’s severity.
- Resolve an excluded finding with boundary evidence. Do not change code, run preflight, count a defect, or stop publication.
- Send a contract gap for human scope direction without treating it as a severe defect.
- Send an applicable correction through the same Design Preflight, validation, documentation, and local review flow used for local findings.
- Stop immediately for a validated P0 or P1 in executable production code. Run the existing severe defect diagnostic and wait for human direction.
- Keep all detailed classification and severe-stop rules in `adversarial-review`. The publication owner only links to them.

## Implementation and Checks

- Update the canonical publication reference and its focused rule-owner test. Do not add a workflow, parser, publication script, or new runtime state.
- Add CPK-043 to the roadmap and create its ExecPlan. Carry CPK-042 forward unchanged. Freeze tracked task records before the task commit.
- Test these cases:
  - A draft PR receives `@codex review` before readiness or CI.
  - An irrelevant P1 is excluded before severity and does not stop.
  - An applicable production-code P1 triggers the canonical severe stop.
  - An applicable non-severe finding uses the local correction cycle.
  - A fix push resets review and CI eligibility.
  - CI that can run on a draft blocks publication before the remote branch is pushed.
  - Only a clean current head can become ready and run required CI.
- Run the focused policy test, full test suite, syntax checks, checksum validation, and one clean-context review.
- Install the reviewed candidate into the live environment and require Doctor to report ready.
- Create one CPK-043 task commit. Leave publication for explicit authorization.

## Assumptions

- The spend gate uses the current Codex review, as selected. Human reviewers can use CI evidence later.
- Repositories that use PR mode configure hosted CI for ready PRs, not draft PRs or ordinary task-branch pushes.
- An automatic Codex review after readiness is not the required review gate. The explicit draft review already covered that exact commit.
</proposed_plan>
---
name: adversarial-review
description: >
  Run clean-context, scope-bound correctness review after code or configuration
  changes. Use staged-tree checkpoints so later passes inspect only fix deltas,
  then run one final coherence pass. Stop after three counted production-code
  defect passes.
license: MIT
---

<!-- cpk-rule-owner: adversarial-review -->
<!-- cpk-rule-guard: Only defects in executable production code can increment the three-defect count or trigger a review stop. -->
<!-- cpk-rule-guard: Tests, test fixtures, documentation, static configuration, dependencies, manifests, and review housekeeping never increment or reset the count and never trigger a review stop. -->
<!-- cpk-rule-guard: After a full review finds defects, later correctness passes review only the staged-tree delta and its direct impact. -->
<!-- cpk-rule-guard: Run one cumulative coherence pass after fix deltas are clean. Do not repeat local correctness review of unchanged code. -->
<!-- cpk-rule-guard: A checkpoint review covers one planned subtask since the previous accepted checkpoint and does not trigger review closure. -->

# Adversarial review

Review the behavior that the project supports. Do not expand the product through review.

Apply [Delivery lifecycle](../delivery-lifecycle/references/delivery-lifecycle.md) before review. A review is read-only.

Apply [Review closure](references/review-closure.md) only after the checkpoint sequence has a final clean result.

## Phase mode

<!-- cpk-rule-route-only: implementation-modes -->
[Implementation modes](../delivery-lifecycle/references/implementation-modes.md)

## Scope gate

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](../design-preflight/references/scope-boundaries.md)

## Supported-model gate

<!-- cpk-rule-route-only: supported-model -->
[Supported model](../design-preflight/references/supported-model.md)

## Review pass

Use one newly spawned clean-context reviewer. The reviewer is read-only and must not delegate.

Before staging a later candidate, inspect every tracked worktree change. Each change must fix a validated finding or its direct impact. Any other tracked change invalidates the checkpoint and requires a new full review.

Stage the complete candidate. Require `git diff --quiet` to succeed so no tracked change is outside the index. Run `git write-tree` and record the returned tree hash in the ignored task result.

Use these review modes:

- `full`: Review the complete task diff from its base to the staged tree.
- `checkpoint`: Compare the current staged tree with the previous accepted checkpoint. Review the current planned subtask, its direct dependencies, and its interactions with completed checkpoints. Do not reopen unchanged completed work.
- `delta`: Compare the last reviewed tree with the current staged tree. Review the changed lines, their owners, direct callers and callees, affected tests, and prior findings.
- `coherence`: Review interactions across the complete task diff after all fix deltas are clean.

A checkpoint review covers one planned subtask since the previous accepted checkpoint and does not trigger review closure.

After a full review finds defects, later correctness passes review only the staged-tree delta and its direct impact.

A delta reviewer does not reopen unchanged code. It can inspect unchanged context only when the delta changes its contract or execution path. A requirement, scope, base, supported-model, or unrelated tracked-file change invalidates the checkpoint and requires a new full review.

If a task has one review boundary and its first full review is clean, finish without a coherence pass. A task with reviewed subtask checkpoints always ends with one coherence pass across the complete task diff.

Run one cumulative coherence pass after fix deltas are clean. Do not repeat local correctness review of unchanged code.

The coherence reviewer checks cross-component interactions and unresolved findings only. Run the coherence pass once. If it finds a defect, review that correction in delta mode and do not repeat coherence.

A clean checkpoint review is an intermediate result. A clean fix delta before coherence is an intermediate result. Neither result triggers review closure or roadmap completion.

A checkpoint has a clean result after its clean checkpoint review or the clean delta review of its correction. This result permits its planned local commit.

Final clean results are a clean first full review for a task with one review boundary, a clean coherence review, or the clean delta review of a coherence correction.

Use delta mode for corrections to the current checkpoint. Keep the consecutive production-code-defect count across every checkpoint, delta, and coherence pass in the task.

Give the reviewer:

- The accepted requirement.
- The product boundary source and owner classifications.
- The actual diff.
- Relevant source and callers.
- Applicable project rules.
- Completed checks.
- The supported model and explicit exclusions.
- The review mode, base revision, previous reviewed tree, and current staged tree.
- For checkpoint mode, the stable subtask identifier and previous accepted checkpoint.
- Prior validated findings and their current disposition.
- The accepted scenario mapping with its production paths, required oracles, runnable checks, and results.

Select only the lenses that the change needs. Always select correctness. Add another lens to the same reviewer only when the active task names that risk.

The reviewer returns the format in `references/finding-format.md`. It must cite source and give a normal-use wrong outcome.

At every review stop gate, read `references/stop-finding-format.md` completely. Render each validated stop finding as its own human decision block. Do not combine findings into one handoff.

## Validate findings

Read each cited source location. Keep only `applicable` findings. Do not spawn a refuter.

Ignore style advice, generic best practice, hypothetical environment failure, fault injection, and work outside the active task.

Only defects in executable production code can increment the three-defect count or trigger a review stop.

A confirmed P0, P1, or P2 correctness defect in executable production code makes a counted production-code-defect pass. P3 advice does not.

Executable production code is code that the product or installer runs to provide supported behavior. It includes executable migration, build, runtime, and security code.

Tests, test fixtures, documentation, static configuration, dependencies, manifests, and review housekeeping never increment or reset the count and never trigger a review stop.

These findings remain actionable. Review housekeeping includes plans, roadmap state, publication records, checksums, staging scope, and ignored test-result records.

## Three-defect breaker

Treat these results as severe stops:

- A validated P0 or P1 defect in executable production code on any pass.
- A validated architecture flaw in executable production code that makes a local patch unsafe.
- A production-code defect on the third consecutive counted pass.

For a severe stop:

1. Do not fix any finding.
2. Close the reviewer.
3. Invoke `defect-diagnostic` automatically and validate its result.
4. Compose one final response only after the diagnostic is complete.
5. In that response, render each stop finding through `references/stop-finding-format.md`.
6. Then present the complete diagnostic, including its portable summary.
7. Put the final `Review:` and `Docs:` status lines after the diagnostic.
8. Halt for human direction.

Progress commentary can state that the diagnostic is running. Do not return a finding question or final response before the diagnostic is ready.

After the halt, do not edit, test, review, spawn another subagent, commit, publish, run CI, change lifecycle state, or create follow-up work.

Otherwise, for any validated in-scope finding:

1. Reapply Delivery Lifecycle before an accepted correction.
2. Enter the selected implementation mode and fix the smallest shared cause.
3. Add or correct one focused check.
4. Run the applicable checks.
5. Finalize documentation again.
6. Record the reviewed tree and validated findings.
7. Return to the selected read-only mode and start a delta pass with a fresh reviewer.

Use one final status line:

- `Review: clean — pass N.`
- `Review: clean after fixes — pass N.`
- `Review: stopped — severe defect diagnostic complete; human direction required.`
- `Review: stopped — implementation defects found in three counted passes; human direction required.`
- `Review: stopped — architecture decision required on pass N.`

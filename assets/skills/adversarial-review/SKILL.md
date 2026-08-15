---
name: adversarial-review
description: >
  Run one clean-context, supported-model correctness review after code or
  configuration changes. Reject findings about excluded conditions. Fix
  validated normal-use defects with Ponytail. Stop after three counted
  production-code-defect passes.
license: MIT
---

<!-- cpk-rule-owner: adversarial-review -->
<!-- cpk-rule-guard: Only defects in executable production code can increment the three-defect count or trigger a review stop. -->
<!-- cpk-rule-guard: Tests, test fixtures, documentation, static configuration, dependencies, manifests, and review housekeeping never increment or reset the count and never trigger a review stop. -->

# Adversarial review

Review the behavior that the project supports. Do not expand the product through review.

Apply [Delivery lifecycle](../codex-practical-kit-rules/references/delivery-lifecycle.md) before review. A review is read-only.

Apply [Review closure](../codex-practical-kit-rules/references/review-closure.md) after a clean result.

## Scope gate

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](../codex-practical-kit-rules/references/scope-boundaries.md)

## Supported-model gate

<!-- cpk-rule-route-only: supported-model -->
[Supported model](../codex-practical-kit-rules/references/supported-model.md)

## Review pass

Use one newly spawned clean-context reviewer. The reviewer is read-only and must not delegate.

Give the reviewer:

- The accepted requirement.
- The product boundary source and owner classifications.
- The actual diff.
- Relevant source and callers.
- Applicable project rules.
- Completed checks.
- The supported model and explicit exclusions.

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

1. Fix the smallest shared cause with Ponytail.
2. Add or correct one focused check.
3. Run the applicable checks.
4. Finalize documentation again.
5. Start a new pass with a fresh reviewer.

Use one final status line:

- `Review: clean — pass N.`
- `Review: clean after fixes — pass N.`
- `Review: stopped — severe defect diagnostic complete; human direction required.`
- `Review: stopped — implementation defects found in three counted passes; human direction required.`
- `Review: stopped — architecture decision required on pass N.`

---
name: adversarial-review
description: >
  Run one clean-context, supported-model correctness review after code or
  configuration changes. Reject findings about excluded conditions. Fix a
  validated normal-use defect with Ponytail and repeat for at most three passes.
license: MIT
---

# Adversarial review

Review the behavior that the project supports. Do not expand the product through review.

Code, tests, configuration, behavior requirements, supported-model rules, and roadmap content must be final before review. A review is read-only.

Review closure does not invalidate a clean review. Review closure is limited to five updates: the task ExecPlan review result, reviewed task roadmap transition, publication status, matching checksums, and untracked test-result record.

A change to code, tests, dependencies, migrations, runtime configuration, build configuration, security configuration, behavior requirements, or the supported model invalidates review. Do not make other file changes after a clean review.

## Supported-model gate

For each finding, answer these questions with `true` or `false`:

1. Does the trigger occur during supported normal use?
2. Does the project control the trigger and result?
3. Does current code reliably produce the wrong result without fault injection?
4. Does the result violate an explicit requirement?

Keep the finding only when all answers are `true`. Otherwise, drop it. Do not report it as residual risk. Do not add it to the roadmap.

The default toolkit model has one personal user and one Codex writer. It uses normal local filesystems and Git.

Exclude these conditions unless the active task explicitly includes one:

- I/O failure.
- Permission or ownership changes.
- Link topology.
- Concurrent or outside writers.
- Interrupted or partial operations.
- Retry, restart, or recovery.
- Git submodules.
- Hostile or contradictory completion-marker text.

## Review pass

Use one newly spawned clean-context reviewer. The reviewer is read-only and must not delegate.

Give the reviewer:

- The accepted requirement.
- The actual diff.
- Relevant source and callers.
- Applicable project rules.
- Completed checks.
- The supported model and explicit exclusions.

Select only the lenses that the change needs. Always select correctness. Add another lens to the same reviewer only when the active task names that risk.

The reviewer returns the format in `references/finding-format.md`. It must cite source and give a normal-use wrong outcome.

## Validate findings

Read each cited source location. Apply the four true or false questions. Do not spawn a refuter.

Ignore style advice, generic best practice, hypothetical environment failure, fault injection, and work outside the active task.

A confirmed P0, P1, or P2 correctness defect makes the pass defectful. P3 advice does not.

## Three-pass breaker

For a defectful pass 1 or 2:

1. Fix the smallest shared cause with Ponytail.
2. Add or correct one focused check.
3. Run the applicable checks.
4. Finalize documentation again.
5. Start a new pass with a fresh reviewer.

If pass 3 finds a validated defect, stop. Do not apply another automatic fix.

Use one final status line:

- `Review: clean — pass N.`
- `Review: clean after fixes — pass N.`
- `Review: stopped — defects found in three consecutive passes; human direction required.`
- `Review: stopped — architecture decision required on pass N.`

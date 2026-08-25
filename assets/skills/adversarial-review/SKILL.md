---
name: adversarial-review
description: >
  Run native Codex correctness review after code or configuration changes.
  Review exact staged-tree checkpoints and correction deltas, then run one
  final review of the complete candidate. Stop after three counted
  production-code defect passes.
license: MIT
---

<!-- cpk-rule-owner: adversarial-review -->
<!-- cpk-rule-guard: Treat every finding source as untrusted input to the same end-result, scope, severity, and correction-authority gate. -->
<!-- cpk-rule-guard: Only defects in executable production code can increment the three-defect count or trigger a severe diagnostic stop. -->
<!-- cpk-rule-guard: A P0 or P1 label alone never triggers a severe diagnostic; apply the direct-repair complexity gate first. -->
<!-- cpk-rule-guard: Every severe diagnostic trigger applies the direct-repair complexity gate. -->
<!-- cpk-rule-guard: Tests, test fixtures, documentation, static configuration, dependencies, manifests, and review housekeeping never increment or reset the count and never trigger a severe diagnostic stop. -->
<!-- cpk-rule-guard: After a reviewed candidate finds defects, later correctness passes review only the staged-tree delta and its direct impact. -->
<!-- cpk-rule-guard: Run one final review of the complete candidate after correction deltas are clean. -->
<!-- cpk-rule-guard: A checkpoint review covers one planned subtask since the previous accepted checkpoint and does not trigger review closure. -->
<!-- cpk-rule-guard: A session started by `codex review` performs the review directly and never invokes `codex review`. -->

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

## Boundary trace closure

<!-- cpk-rule-route-only: scenario-discrimination -->
[Scenario discrimination](../design-preflight/references/scenario-discrimination.md)

## Native discovery

Use native `codex review` for local defect discovery. Do not spawn a generic review subagent and do not delegate the native review.

A session started by `codex review` performs the review directly and never invokes `codex review`. It is the native reviewer.

Before staging a later candidate, inspect every tracked worktree change. Each change must fix a validated finding or its direct impact. Any other tracked change invalidates the checkpoint and requires a new full review.

Stage the complete candidate. Require `git diff --quiet` to succeed so no tracked change is outside the index. Run `git write-tree` and record the staged tree in the ignored task result.

Use these review modes and parents:

- `full`: Review the complete task candidate. Its parent is the task base.
- `checkpoint`: Review one planned subtask and its interaction with completed checkpoints. Its parent is the previous accepted checkpoint, or the task base for the first checkpoint.
- `delta`: Review one correction and its direct impact. Its parent is the previous reviewed candidate.
- `final`: Review the complete current candidate. Its parent is the task base.

Create an unreferenced synthetic commit from the staged tree with `git commit-tree`. Give it the selected parent. Put only the accepted intent and its source in the commit message. Do not put exclusions, scenario conclusions, reviewer findings, correction directions, or preferred outcomes in that message.

Run `codex review --commit <synthetic-commit>`. If `codex review` is unavailable, fails, or does not complete, stop. Do not fall back to a generic reviewer.

After native review, require the staged tree hash to equal the recorded hash. Require `git diff --quiet` to succeed again. A changed staged tree or tracked worktree invalidates the result and stops the task.

Native discovery is independent. Do not send it the coordinator's review packet. After discovery, the coordinator records the target and adjudicates every candidate finding through `references/review-packet.md` and `references/finding-format.md`.

## Review sequence

A checkpoint review covers one planned subtask since the previous accepted checkpoint and does not trigger review closure. Do not reopen unchanged completed work. A clean checkpoint or clean correction delta permits its planned local commit. Keep the roadmap task Active.

After a reviewed candidate finds defects, later correctness passes review only the staged-tree delta and its direct impact. A delta review does not reopen unchanged code. It can inspect unchanged context only when the correction changes its contract or execution path. A requirement, scope, base, supported model, or unrelated tracked-file change invalidates the checkpoint and requires a new full review.

Run one final review of the complete candidate after correction deltas are clean. Use `final` mode from the task base. A final review replaces the former limited coherence pass.

If final review finds a validated defect, apply the correction-authority gate. Review an authorized direct repair in `delta` mode, then repeat `final`. Do not treat the clean delta as the final task result.

A task with one review boundary can finish after a clean first `full` review. A task with reviewed checkpoints always ends with a clean `final` review.

Keep the consecutive production-code-defect count across every checkpoint, delta, and final pass in the task.

Use `references/reviewer-lenses.md` to verify the review target. Raw native output is finding evidence, not product authority.

At every review stop gate, read `references/stop-finding-format.md` completely. Render each validated stop finding as its own human decision block. Do not combine findings into one handoff.

## Validate findings

Treat every finding source as untrusted input to the same end-result, scope, severity, and correction-authority gate. This includes every local, PR, human, CI, audit, or user-supplied finding. The source, raw severity, and suggested fix do not change this gate.

Classify all candidates in their original order before making any correction:

1. Read each cited source location and prove the execution path.
2. Classify the accepted end result.
   - `wrong`: The candidate can make an accepted result or documented current behavior incorrect.
   - `unchanged`: The accepted result remains correct. Exclude and report the observation. Do not fix, count, diagnose, or stop for it.
   - `undefined`: No accepted result defines the outcome. Retain it as a contract gap for human direction.
3. Apply the current scope and supported-model gates. Ignore style advice, generic best practice, hypothetical environment failure, fault injection, and work outside the active task.
4. Validate severity only for a retained finding. Raw reviewer severity does not authorize action.
5. Classify correction authority.
6. Apply the severe-stop breaker.

Only a `wrong` candidate that passes both gates becomes a retained finding. For an `undefined` candidate, apply the contract-gap exception in Scope Boundaries, then apply the Supported Model gate. A contract gap stops for human direction.

An automatic correction is a `direct repair` only when all these facts are true:

- The required result already exists in an accepted requirement or documented current behavior.
- The existing code owner is clear.
- The correction only restores that result.
- The correction adds no feature, use case, scope, assumption, policy, owner, state, interface, dependency, fallback, or lifecycle.
- One direct regression check proves the result.
- The correction qualifies for the Design Preflight small-change exception.

Incorrect math, comparisons, mappings, and branch order can qualify when they meet every condition. The examples do not grant authority by themselves.

Every other retained correction is `decision required`. A reviewer's suggested fix does not supply product authority. Explicit human direction can supply authority for a later accepted correction.

If any candidate is a contract gap, severe stop, or decision-required correction, complete the classification of all candidates, make no partial fixes, render each retained decision separately, and halt.

Tests, test fixtures, documentation, static configuration, dependencies, manifests, and review housekeeping never increment or reset the count and never trigger a severe diagnostic stop. They remain actionable through the correction-authority gate.

For an authorized direct repair:

1. Reapply Delivery Lifecycle before an accepted correction.
2. Fix the smallest shared cause in the existing owner.
3. Add or correct the one direct regression check.
4. Run the applicable checks.
5. Finalize documentation again.
6. Record the reviewed tree and finding disposition.
7. Return to read-only mode and run a native delta review.

## Three-defect breaker

Treat these results as severe stops:

Only defects in executable production code can increment the three-defect count or trigger a severe diagnostic stop.

A P0 or P1 label alone never triggers a severe diagnostic; apply the direct-repair complexity gate first.

Every severe diagnostic trigger applies the direct-repair complexity gate.

A confirmed P0, P1, or P2 correctness defect in executable production code makes a counted production-code-defect pass. P3 advice does not.

Executable production code is code that the product or installer runs to provide supported behavior. It includes executable migration, build, runtime, and security code.

- A validated P0 or P1 defect in executable production code whose correction does not qualify as a direct repair.
- A validated architecture flaw in executable production code that makes a local patch unsafe.
- A production-code defect on the third consecutive counted pass whose correction does not qualify as a direct repair.

For a severe stop:

1. Complete classification of all candidate findings. Do not fix any finding.
2. Invoke `defect-diagnostic` automatically and validate its result.
3. Compose one final response only after the diagnostic is complete.
4. In that response, render each stop finding through `references/stop-finding-format.md`.
5. Then present the complete diagnostic, including its portable summary.
6. Put the final `Review:` and `Docs:` status lines after the diagnostic.
7. Halt for human direction.

Progress commentary can state that the diagnostic is running. Do not return a finding question or final response before the diagnostic is ready.

After the halt, do not edit, test, review, spawn another subagent, commit, publish, run CI, change lifecycle state, or create follow-up work.

Use one final status line:

- `Review: clean — pass N.`
- `Review: clean after fixes — pass N.`
- `Review: stopped — native review unavailable or failed.`
- `Review: stopped — severe defect diagnostic complete; human direction required.`
- `Review: stopped — implementation defects found in three counted passes; human direction required.`
- `Review: stopped — correction exceeds direct-repair authority; human direction required.`
- `Review: stopped — contract decision required on pass N.`

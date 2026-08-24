<proposed_plan>
# CPK-044 — Separate Review Findings from Correction Authority

## Summary

Release this feature as version `0.22.0`.

Use Codex’s native review mode for local defect discovery. Then apply toolkit scope and correction gates before any edit.

This addresses two proven differences:

- The current local process uses a generic reviewer with preloaded scenarios and exclusions.
- Native Codex review independently examines the diff, repository, dependencies, and tests. This matches OpenAI’s documented PR-review approach. [OpenAI Codex review guidance](https://openai.com/index/introducing-upgrades-to-codex/)
- Recent [Tenant Keeper PR review](https://github.com/calculatetech/tenant-keeper/pull/1) and [Meridian PR review](https://github.com/calculatetech/meridian/pull/19) found defects after local review reported clean.

The cloud PR model and internal prompt remain undocumented. Do not claim exact parity.

## Review and Correction Changes

### Native defect discovery

Replace the generic review subagent with `codex review`.

- Stage the complete candidate and require no unstaged tracked changes.
- Create an unreferenced Git commit from the staged tree.
- Use the applicable review parent:
  - `full`: task base.
  - `checkpoint`: previous accepted checkpoint.
  - `delta`: previous reviewed candidate.
  - `final`: task base.
- Put only the accepted intent and its source in the synthetic commit message. Do not preload exclusions, scenario conclusions, or correction directions.
- Run `codex review --commit <synthetic-commit>`.
- If native review is unavailable or fails, stop. Do not fall back to the generic reviewer.
- After review, prove that the staged tree and tracked worktree did not change.

Replace `coherence` mode with `final` mode. After correction deltas are clean, review the complete current candidate once. If that review finds a defect, use a delta correction and repeat `final`. The existing three-pass breaker remains the limit.

### Source-independent finding gate

Treat every local, PR, human, CI, audit, or user-supplied finding as an untrusted candidate.

Apply these steps before severity or correction:

1. Read the cited source and prove the execution path.
2. Classify the accepted end result:
   - `wrong`: The finding can make an accepted result or documented current behavior incorrect.
   - `unchanged`: The accepted result remains correct. Exclude and report the finding.
   - `undefined`: No accepted result exists. Stop for human direction.
3. Apply the current scope and supported-model gates.
4. Validate severity only for a retained finding.
5. Apply the severe-stop breaker.
6. Classify correction authority.

Permit automatic correction only when all these conditions are true:

- The required result already exists.
- The existing code owner is clear.
- The correction only restores that result.
- The correction adds no feature, use case, scope, assumption, policy, owner, state, interface, dependency, fallback, or lifecycle.
- One direct regression check can prove the result.
- The correction qualifies for the Design Preflight small-change exception.

Call this a `direct repair`. Incorrect math, comparisons, mappings, and branch order are representative examples.

Classify every other correction as `decision required`. Complete the classification of all findings, make no partial fixes, render each decision separately, and halt.

A reviewer’s suggested fix does not supply product authority. Explicit human direction can supply that authority.

## Diagnostic and Records

Change severe diagnostics to present each finding in this order:

- `Problem`: Plain description of the fault.
- `End result`: `wrong`, `still correct`, or `unknown`, with one reason.
- `Prevention`: The smallest requirement, check, or review action that could have prevented the defect.
- `Required action`: The exact human decision.
- `Proof`: Compact requirement, execution path, escape reason, rule contribution, and source locations.
- `Portable summary`: A short self-contained correction record.

Keep the complete evidence, automatic diagnostic trigger, separate finding blocks, and mandatory halt from CPK-021. Do not lead with the chronological reconstruction.

Create two reviewed checkpoints:

1. Native discovery, exact review targets, final-review mode, and correction authority.
2. Diagnostic presentation, documentation, version, and manifest updates.

Create `docs/plans/cpk-044-review-correction-authority.md`. Make CPK-044 the only active roadmap item during implementation. Preserve the existing untracked environment files.

## Test Plan

Add focused contract checks for:

- Every review source uses the same finding gate.
- Raw reviewer severity cannot authorize action.
- A proven wrong calculation receives a direct repair.
- A proposed feature, fallback, new state, new interface, or assumed requirement stops before edits.
- A mixed finding set with one direct repair and one decision-required correction makes no fixes.
- A technically valid observation with an unchanged end result is excluded, reported, and does not stop.
- An undefined result becomes a contract gap.
- A relevant P0 or P1 still runs the severe diagnostic and halts.
- Native review uses the exact staged tree and the correct parent for each mode.
- Native review failure has no generic fallback.
- `final` replaces `coherence` and reviews the complete candidate.
- Diagnostic summaries precede compact proof sections and keep findings separate.

Run the complete toolkit suite, Python compilation, shell and PowerShell checks, rule-owner checks, link checks, manifest validation, and `git diff --check`.

After review, install the candidate and require Doctor to report ready. Run one opt-in native-review smoke against a temporary synthetic commit. Confirm completion and an unchanged tracked tree.

Create local checkpoint commits. Do not publish without a later request.

## Assumptions and Prior Decisions

- Carry CPK-040 and CPK-041 unchanged.
- Preserve CPK-042 checkpoint and delta reviews. Supersede only its limited coherence pass.
- Preserve CPK-043 PR sequencing. Its findings now use the new correction-authority gate.
- Preserve CPK-021’s automatic diagnostic and halt. Supersede only its chronology-first presentation.
- Preserve the existing scope and supported-model definitions.
- Add no review parser, daemon, service, dependency, telemetry, or model-evaluation harness.

<!-- cpk-plan-spec: docs/plans/cpk-044-review-correction-authority.md -->
</proposed_plan>
# Invoke planning and RepoWise throughout applicable work

This ExecPlan is a living document until review closure. Maintain it under `.agent/PLANS.md`.

## Purpose / Big Picture

Non-trivial runtime work must use Design Preflight before code even when the user does not request Plan Mode. Its fresh planning challenger uses xhigh reasoning, including for qualifying review corrections, before the main thread resumes its configured implementation effort. Each new repository discovery question must use RepoWise throughout implementation and review corrections. Initial planning and repository orientation do not satisfy later questions.

## Progress

- [x] (2026-08-17 06:32Z) Reviewed the 063F diagnostic and the current lifecycle, preflight, review, and repository-knowledge owners.
- [x] (2026-08-17 06:32Z) Created branch `cpk-032-default-mode-preflight` from `main` commit `935e592e61e1`.
- [x] (2026-08-17 07:41Z) Added focused owner-contract checks and captured the expected pre-change failure.
- [x] (2026-08-17 07:46Z) Corrected automatic preflight invocation, correction routing, reasoning phases, Scenario Proof, and continuous RepoWise routing.
- [x] (2026-08-17 07:55Z) Completed both clean-context forward tests, focused skill validation, and the 40-test suite.
- [x] (2026-08-17 08:18Z) Resolved two P2 entry-gate findings; the correction delta and final coherence review were clean.

## Surprises & Discoveries

- Observation: Design Preflight describes applicable work but does not state that implicit invocation applies outside UI Plan Mode.
  Evidence: Its current metadata describes a non-trivial change without naming Default-mode implementation or review corrections.
- Observation: Repository Knowledge requires RepoWise before broad exploration but does not bind the rule to each later discovery question.
  Evidence: Its current opening can be satisfied by one initial query.
- Observation: Owner Composition already covers retained states, reopening sources, terminal owners, and composed checks.
  Evidence: Only unordered counterexample ordering and shared-signal cause discrimination are absent from the focused owner.
- Observation: Codex applies `plan_mode_reasoning_effort` only in Plan Mode, and hooks cannot change reasoning effort.
  Evidence: The official configuration reference defines a Plan-mode-specific override and explicit subagent effort; the hook output contract contains no reasoning control.
- Observation: Review pass 1 found that the correction examples narrowed the shared entry gate and that a qualifying non-runtime correction could skip the challenger.
  Evidence: The candidate used different correction criteria in its entry and challenge sections.
- Observation: A review finding does not by itself require Design Preflight.
  Evidence: The user confirmed that a small correction with one proven owner and one direct check must keep the existing exception.

## Decision Log

- Decision: Keep automatic activation in skill metadata and lifecycle rules.
  Rationale: Hooks cannot reliably classify task semantics, and Design Preflight can run in Default mode.
  Date/Author: 2026-08-17 / Codex
- Decision: Keep query routing in Repository Knowledge.
  Rationale: It is the existing single owner for RepoWise use.
  Date/Author: 2026-08-17 / Codex
- Decision: Use an xhigh fresh planning challenger and keep implementation in the main thread's configured effort.
  Rationale: This preserves the useful Plan-mode phase split without unsupported active-thread mutation or hook machinery.
  Date/Author: 2026-08-17 / Codex
- Decision: Apply the same Design Preflight entry gate and small-change exception to accepted corrections.
  Rationale: Automatic correction planning must not force full preflight for simple review rework.
  Date/Author: 2026-08-17 / Codex
- Decision: Use version `0.17.0`.
  Rationale: Automatic reasoning-effort phase selection outside Plan Mode is a new toolkit capability after committed version `0.16.1`.
  Date/Author: 2026-08-17 / Codex

## Outcomes & Retrospective

Version `0.17.0` now applies Design Preflight outside Plan Mode when its normal entry gate matches. The same gate and small-change exception apply to accepted corrections. Qualifying corrections use a fresh xhigh planning challenger before the main thread resumes its configured implementation effort. RepoWise now owns every new repository lookup throughout a task, and Owner Composition covers outcome-changing order and shared-signal causes without exhaustive permutations.

Both clean-context forward tests selected the intended skills without explicit names. All 40 tests, skill validation, syntax checks, diff checks, and manifest checks passed. Full review found two P2 gate defects. Their correction delta and the final coherence pass were clean. Publication was not authorized.

## Context and Orientation

Design Preflight owns applicability and Scenario Proof. Delivery Lifecycle owns the transition into implementation and accepted corrections. Adversarial Review owns correction review. Repository Knowledge owns RepoWise query selection. Owner Composition owns retained-state and event-path composition. `tests/test_kit.py` protects these contracts.

The base branch is `main`. The base commit is `935e592e61e1e32caba1dc91970ef560441926d1`. The task branch is `cpk-032-default-mode-preflight`. The isolation form is one normal branch.

## Product Boundary

The authoritative sources are the accepted CPK-032 plan and `/home/mbeutler/Downloads/063F-triage.md`. The live lifecycle, preflight, owner-composition, review, and repository-knowledge owners compose. RepoWise runtime, watcher behavior, provider configuration, hooks, Ponytail, and completed records are opaque.

The supported model has one user and one Codex writer on a normal local Git filesystem. Exclude I/O faults, permissions, concurrency, interruption, retries, recovery, submodules, provider errors, new dependencies, and hook-based semantic classification.

## Scenario Proof

This task changes agent instructions, not executable product runtime. The focused owner checks and clean-context forward tests are the acceptance proof. A planning challenger is not required because ownership and scope are clear.

## Plan of Work

First add a focused test that fails unless Default-mode implementation and accepted corrections apply Design Preflight through one lifecycle owner. Extend the same test surface for unordered event counterexamples and shared-signal causes.

Then update Design Preflight metadata, Delivery Lifecycle timing, Adversarial Review correction routing, Implementation Modes reasoning phases, and Owner Composition. Update Repository Knowledge so every new discovery question uses RepoWise. Route Design Preflight and Delivery Lifecycle to that owner without copying its query rules.

Run two clean-context forward tests with raw implementation and correction prompts. Do not name Design Preflight or Repository Knowledge in those prompts. Require planning and indexed discovery before code.

Update source version `0.17.0`, focused RepoWise documentation, and the checksum manifest after content is final.

## Concrete Steps

Work in `/home/mbeutler/Projects/codex-practical-kit` on branch `cpk-032-default-mode-preflight`.

Run `./run-tests.sh`, skill validation, Python and shell syntax checks, `git diff --check`, and `sha256sum --check MANIFEST.sha256`. Store detailed results in ignored `.agent/test-results/cpk-032-default-mode-preflight.md`.

Stage the complete candidate and run Adversarial Review. Apply only Review Closure updates after the final clean result. Freeze all tracked records before the task commit.

## Validation and Acceptance

The focused contract must fail against the old rules and pass after correction. The two forward tests must select planning, xhigh challenge reasoning, the configured implementation effort, and RepoWise without explicit skill names. The full suite and manifest checks must pass. After commit, install the exact candidate and require Doctor version `0.17.0` with `Result: ready`.

## Idempotence and Recovery

The tests, skill validator, installer, and Doctor are repeatable. If a required operation fails, stop and report the exact error. Do not add retries or speculative recovery.

## Artifacts and Notes

Keep detailed test and review evidence only in the ignored task result.

The first forward test selected automatic preflight and task-long RepoWise lookup routing for a new Default-mode implementation. The second selected a fresh xhigh correction challenger, passed it the accepted finding without a preferred fix, and returned implementation to the main thread's configured effort.

## Interfaces and Dependencies

There is no new runtime interface or dependency. Design Preflight gains an implicit Default-mode trigger. Its fresh planning challenger uses xhigh before the main thread resumes its configured effort. Repository Knowledge gains task-long query routing.

Revision note (2026-08-17): Created from the accepted plan, 063F diagnostic, and inspected live owner contracts.

Revision note (2026-08-17): Added the accepted automatic xhigh planning phase for qualifying review corrections and changed the feature version to `0.17.0`.

Revision note (2026-08-17): Review pass 1 corrected the accepted-correction entry and challenge gates while preserving the small-change exception.

Revision note (2026-08-17): Closed after clean correction-delta and cumulative coherence reviews.

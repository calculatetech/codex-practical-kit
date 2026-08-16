# Scope minimalism by lifecycle phase

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must remain current. Maintain this document under `.agent/PLANS.md`.

## Purpose / Big Picture

Codex must not use implementation minimalism to shrink requirements, scenario discovery, test scope, or correctness review. After this change, lifecycle rules select normal mode for those phases and Ponytail full only while writing tests, production changes, or accepted review corrections. A scenario-to-check mapping makes every retained runtime transition auditable before implementation and review.

## Progress

- [x] (2026-08-16 16:15Z) Activated CPK-028 on branch `cpk-028-phase-scoped-minimalism` and recorded the accepted design.
- [x] (2026-08-16 16:15Z) Fixed the required checks and scenario oracles before implementation.
- [x] (2026-08-16 16:20Z) Added the canonical implementation-mode owner and routed lifecycle skills to it.
- [x] (2026-08-16 16:20Z) Added transition-closed Scenario Proof mapping to planning and review.
- [x] (2026-08-16 16:24Z) Updated focused tests, user documentation, version 0.15.0, and the manifest.
- [x] (2026-08-16 16:30Z) Passed validation, forward testing, and the first full correctness review with no findings; prepared the reviewed candidate for commit.
- [ ] Install the exact commit live and publish version 0.15.0.

## Surprises & Discoveries

- Observation: The cleaner Meridian run was not a controlled Ponytail A/B test because higher-priority rules enabled Ponytail during implementation.
  Evidence: `worktree3.md` records that the session rules forced Ponytail despite the task prompt.
- Observation: The remaining Meridian defect crossed scenarios that were checked separately.
  Evidence: The checks covered an older success after a newer assignment and retry classification, but not `A applying -> B accepted -> A retry -> B completes` as one production-path scenario.

## Decision Log

- Decision: Keep upstream Ponytail unchanged and select its documented `normal mode` at lifecycle boundaries.
  Rationale: A future third-party updater owns upstream components. Toolkit policy must compose with that interface, not fork it.
  Date/Author: 2026-08-16 / Codex and user.
- Decision: Make Delivery Lifecycle the sole owner of phase mode selection.
  Rationale: One shared phase transition rule prevents planning, implementation, and review skills from defining competing defaults.
  Date/Author: 2026-08-16 / Codex and user.
- Decision: Require transition-closed scenario mappings before implementation and concrete results before review.
  Rationale: Separate component tests and aggregate suite counts cannot prove a composed state transition.
  Date/Author: 2026-08-16 / Codex and user.
- Decision: Release this feature as version 0.15.0.
  Rationale: Phase-scoped lifecycle behavior is a new toolkit capability, so the pre-1.0 minor digit increments from committed version 0.14.0.
  Date/Author: 2026-08-16 / Codex and user.

## Outcomes & Retrospective

Version 0.15.0 passed all validation and the first full correctness review without findings. One canonical owner now selects minimalism by lifecycle phase. Transition-closed Scenario Proof mappings connect each retained path to an oracle and runnable result. Upstream Ponytail remains unchanged. No residual risk remains.

## Context and Orientation

`assets/skills/delivery-lifecycle/` owns shared task transitions. `assets/skills/design-preflight/` derives supported runtime scenarios. `assets/skills/adversarial-review/` reviews a staged candidate. `assets/AGENTS.block.md` routes agents to those owners. `tests/test_kit.py` verifies unique owners and installed content. `kit.py` contains the committed toolkit version.

Ponytail is a separately maintained implementation-minimalism skill. Normal mode means the skill is disabled for the named phase. Full mode means its shortest-correct-implementation rules apply. A transition-closed scenario follows all supported events that can affect retained state until the required terminal result is observed.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). The authoritative requirement is the accepted CPK-028 plan in this file. Delivery Lifecycle, Design Preflight, Research First, and Adversarial Review compose because this task changes their shared phase transitions. Upstream Ponytail is opaque and must not be changed. No third-party update mechanism is part of this task.

## Scenario Proof

Apply [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md). This is toolkit policy, not product runtime code, so no runtime Cartesian scenario set is required. The following policy scenarios are the acceptance proof.

| Scenario | Production path | Required oracle | Runnable test | Result |
| --- | --- | --- | --- | --- |
| Planning a non-trivial change | AGENTS -> Design Preflight -> Delivery Lifecycle mode owner | Normal mode remains active until required scenarios, oracles, and planned checks are accepted | `test_implementation_modes_are_phase_scoped` | Pass |
| Implementing an accepted plan | Delivery Lifecycle mode owner -> Ponytail | Ponytail full applies to test and production edits only after test scope is fixed | `test_implementation_modes_are_phase_scoped` | Pass |
| Correcting a review finding | Adversarial Review -> mode owner -> correction -> review | Correction uses implementation mode and the next read-only pass returns to normal mode | `test_implementation_modes_are_phase_scoped` | Pass |
| Retained state receives a later supported event | Design Preflight -> Owner Composition -> preflight card -> reviewer packet | One composed scenario follows the event sequence to a terminal oracle; component checks and suite counts cannot substitute | `test_scenario_proof_maps_transition_closed_checks` | Pass |

## Plan of Work

Create `assets/skills/delivery-lifecycle/references/implementation-modes.md` as the only detailed phase-mode owner. Route Delivery Lifecycle and the task-phase skills to it without copying its rules. Remove Research First's local instruction to apply Ponytail. Extend Owner Composition so a scenario set remains open while a supported later event can act on retained state without a terminal oracle.

Update the preflight card and independent challenge schema with production path, oracle, and planned check fields. Require the coordinator to fill the actual runnable check and result before review. Update the reviewer packet and correctness lens to inspect that mapping. Add focused ownership and behavior assertions in `tests/test_kit.py`, then update the smallest authoritative user documents, version, and manifest.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit`. Apply edits with `apply_patch`. Run `python -m unittest tests.test_kit`, the repository validation commands named in the README, and `quick_validate.py` for every changed skill. Generate `MANIFEST.sha256` only after documentation is final. Stage the complete candidate, record `git write-tree`, and run the required clean-context review workflow. Install that exact reviewed candidate with `./install.sh`, then require `./doctor.sh` to report version 0.15.0 and `Result: ready` before publication.

## Validation and Acceptance

`test_implementation_modes_are_phase_scoped` must fail if phase defaults are duplicated, planning enables Ponytail before test scope is fixed, an explicit user mode cannot override the default, or review corrections do not return to normal mode. `test_scenario_proof_maps_transition_closed_checks` must fail if the transition-closure rule, mapping columns, planned check, actual result, or reviewer verification is absent. The full test suite, skill validators, manifest check, installer, Doctor, and clean-context review must pass.

The generic A/B validation prompt asks one fresh agent to plan a stateful change, select the planning and implementation modes, and map its proof. The transition case is `A retained -> B accepted -> A retry -> B terminal`; the accepted plan must require one composed production-path check whose oracle proves A cannot reappear or become eligible.

Observed validation: one fresh agent selected normal mode for planning, mapped the complete `A applying -> B accepted -> A retry -> B completes` path to one runnable production-path check, rejected an aggregate suite pass, and selected Ponytail full for implementation.

## Idempotence and Recovery

Tests and validation commands are repeatable. The installer is designed for repeat use. If a required check, review, install, or publication gate fails, stop and report the exact result; do not invent recovery or publish an unreviewed tree.

## Artifacts and Notes

Store ignored review evidence in `.agent/test-results/cpk-028-phase-scoped-minimalism.md`. Do not stage that record. Preserve unrelated untracked workspace paths.

## Interfaces and Dependencies

Do not add dependencies or modify the upstream Ponytail skill. Use its existing exact `normal mode` interface and its default full implementation mode. Add one focused rule owner named `implementation-modes`; all other files route to it.

Revision note (2026-08-16): Created the accepted CPK-028 execution plan and fixed its implementation checks before code changes.

Revision note (2026-08-16): Recorded the implemented owners, passing checks, documentation, version, manifest, and generic forward-test result before review.

Revision note (2026-08-16): Recorded the clean full review and completed roadmap transition.

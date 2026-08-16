# Activate normal mode for Plan-mode prompts

This ExecPlan is a living document. Maintain it under `.agent/PLANS.md`.

## Purpose / Big Picture

When a user selects Codex Plan mode, the toolkit must select Ponytail normal mode before planning begins. The user does not need to type a separate mode command. Prompts in other Codex modes must not change the current Ponytail mode.

## Progress

- [x] (2026-08-16 16:41Z) Created branch `cpk-029-plan-mode-hook` from `main` commit `ab27741605695df5ef65346d83177143fb5c79d8`.
- [x] (2026-08-16 16:41Z) Completed research and an independent Design Preflight challenge.
- [x] (2026-08-16 16:41Z) Fixed the runtime scenarios, oracles, and planned checks before implementation.
- [x] (2026-08-16 16:48Z) Implemented the managed prompt hook and passed all 33 tests, Python compilation, shell syntax, and diff checks.
- [x] (2026-08-16 16:48Z) Finalized current hook and implementation-mode documentation.
- [x] (2026-08-16 16:56Z) Corrected the pass-1 duplicate-handler finding and added a focused reinstall check.
- [x] (2026-08-16 17:03Z) Passed the fix-delta review and final coherence review with no findings.
- [ ] Install the exact commit live and publish version 0.15.1.

## Surprises & Discoveries

- Observation: Codex has no event that runs when the user selects Plan mode.
  Evidence: The current hook events include `UserPromptSubmit`, and that event receives `permission_mode: "plan"` before prompt dispatch.
- Observation: A managed block and later exact unmarked handlers can coexist before reinstall.
  Evidence: Full review pass 1 found that the missing-event check left both copies active.

## Decision Log

- Decision: Use the existing hook script for `SessionStart` and `UserPromptSubmit`.
  Rationale: Event dispatch in one installed script is smaller than a second script and keeps one runtime owner.
  Date/Author: 2026-08-16 / Codex.
- Decision: Emit the exact text `normal mode` only for Plan-mode prompt events.
  Rationale: Ponytail documents this exact command. Plain hook output becomes developer context before Codex receives the prompt.
  Date/Author: 2026-08-16 / Codex.
- Decision: Release version 0.15.1.
  Rationale: This patch corrects the incomplete CPK-028 phase transition. It does not add a separate product feature.
  Date/Author: 2026-08-16 / Codex.

## Outcomes & Retrospective

Version 0.15.1 passes all 34 tests and final coherence review. Plan-mode prompts select normal mode before dispatch. Non-Plan prompts remain unchanged. Installation reconciles partial and duplicate hook configurations without changing unrelated hooks. No residual risk remains.

## Context and Orientation

`kit.py` installs one managed hook block in the user Codex `config.toml`. `assets/hooks/session_start.py` is the installed hook command. `tests/test_kit.py` checks hook installation and behavior. `assets/skills/delivery-lifecycle/references/implementation-modes.md` remains the sole policy owner.

Codex calls `UserPromptSubmit` before it sends a prompt. The input contains `permission_mode`. The value is `plan` in Plan mode. Text on standard output becomes developer context for that prompt.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). Hook configuration, hook runtime behavior, diagnostics, and the implementation-mode owner compose. Upstream Ponytail is opaque. Malformed external configuration, malformed hook input, I/O faults, concurrency, and upstream mode changes are excluded.

## Scenario Proof

| Scenario | Production path | Required oracle | Runnable test or command | Result |
| --- | --- | --- | --- | --- |
| Submit a Plan-mode prompt | `UserPromptSubmit` configuration -> installed hook -> Codex developer context | The hook exits successfully and emits exact `normal mode` context before prompt dispatch | `test_plan_mode_prompt_selects_normal_mode` | Pass |
| Submit a non-Plan prompt | `UserPromptSubmit` configuration -> installed hook -> no returned context | The hook exits successfully and emits no mode-changing output | `test_plan_mode_prompt_selects_normal_mode` | Pass |
| Start or resume a session | `SessionStart` configuration -> installed hook -> Codex developer context | The existing router announcement is unchanged | `test_session_start_still_announces_router` | Pass |
| Install, reinstall, and remove hooks | `install_core` -> managed block -> Doctor -> `uninstall_hooks` | Each required event exists once, unrelated hooks remain, and uninstall removes only the managed block | existing installer round-trip test, extended for both events | Pass |

## Plan of Work

Add `UserPromptSubmit` to the managed hook block. Make the existing script read the event input. Emit `normal mode` for Plan-mode prompt events, emit nothing for other prompt modes, and preserve the Session Start response. Make hook detection require both event handlers. Extend the focused installer and runtime checks. Update the current hook documentation, version, roadmap, and manifest.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on branch `cpk-029-plan-mode-hook`. Run `./run-tests.sh`, Python and shell syntax checks, `git diff --check`, and `sha256sum --check MANIFEST.sha256`. Stage the complete candidate and run Adversarial Review. After a clean review, commit the candidate. Install that exact commit with `./install.sh`. Require `./doctor.sh` to report version 0.15.1 and `Result: ready`. Then publish through the repository publication mode.

## Validation and Acceptance

The focused runtime check must invoke the configured command with real hook JSON. Plan mode must produce `normal mode`. A supported non-Plan mode must produce no output. Session Start must still produce the router announcement. Parsed configuration must contain one handler for each managed event after repeated installation.

## Idempotence and Recovery

Installation and validation are repeatable. If one operation fails, stop and report the error. Do not repair external configuration or publish an unreviewed candidate.

## Artifacts and Notes

Store detailed evidence in ignored file `.agent/test-results/cpk-029-plan-mode-hook.md`. Never stage it.

## Interfaces and Dependencies

Use Python standard-library JSON parsing and the current Codex hook interface. Add no dependency and no upstream Ponytail change.

Revision note (2026-08-16): Created the accepted plan with transition-closed checks before implementation.

Revision note (2026-08-16): Recorded the completed implementation, scenario results, documentation, and validation before review.

Revision note (2026-08-16): Recorded and corrected the pass-1 duplicate-handler finding.

Revision note (2026-08-16): Recorded clean delta and coherence reviews and the completed roadmap transition.

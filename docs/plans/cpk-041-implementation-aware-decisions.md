# Explain code consequences before decisions

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose

Before a material code choice, Codex must explain each option in plain language. The user must see the visible result and the implementation shape before the choice widget appears.

## Progress

- [x] (2026-08-22) Reconciled the accepted CPK-041 Plan with CPK-008 and CPK-040.
- [x] (2026-08-22) Created branch `cpk-041-implementation-aware-decisions` from reviewed commit `982321ef930b58c366c856c2504912a7bf3da7ea`.
- [x] (2026-08-22) Made CPK-041 the only Active roadmap task.
- [x] (2026-08-22) Strengthened the decision owner and routed Design Preflight choices through it.
- [x] (2026-08-22) Passed the focused checks and all 80 default Python checks.
- [x] (2026-08-22) Corrected the pass 1 scope mismatch so all material technical choices use the implementation brief.
- [x] (2026-08-22) Completed review, live installation, Doctor, and the clean-session decision smoke test.

## Prior Plan Reconciliation

Record: `.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md`

Status: carried

Reason: This record is the accepted CPK-041 implementation contract.

CPK-008 remains authoritative for the material-choice trigger, fixed labels, and routine-question exclusions. CPK-041 strengthens its incomplete option-effect rule. CPK-040 remains authoritative for Plan capture and does not conflict.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). This task composes the decision-handoff owner and the Design Preflight route. The Simple English skill is an opaque wording owner. The Codex choice widget is an opaque display owner with short question and option fields.

The supported model is a material technical choice in a normal Codex task with readable repository source. Routine preferences, discoverable facts, line-count estimates, new skills, model evaluation infrastructure, and changes to the choice widget are excluded.

## Normal-Use Behavior Floor

Codex inspects the implementation paths before it asks. Each practical option explains the visible result, code change, source anchor, new moving parts, and test or maintenance effects. Plain language comes before a source name.

The complete brief appears before `request_user_input`. The widget only collects the selected option. If source cannot prove an impact, the brief states `unknown` and names the missing evidence.

After the user selects an option, Codex records the selected behavior and implementation shape in the active ExecPlan.

## Scope Ceiling

Do not add a skill, response generator, parser, line estimator, telemetry, service, or model-evaluation harness. Do not modify the upstream Simple English skill. Do not expand the full handoff to routine questions.

## Scenario Proof

| Scenario | Discriminator | Contrast | Production path | Required oracle | Runnable check | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Material code choice | Choice changes architecture or state | routine preference | Design Preflight to decision owner | complete source-backed brief before widget | `test_material_code_decisions_explain_implementation_before_choice` | Passed |
| Option impact | existing-function extension | new state or subsystem | repository inspection to option facts | visible result and exact implementation shape differ | focused decision-owner assertions | Passed |
| Source anchor | plain role plus source name | source jargon alone | option brief | plain role appears before file or symbol | focused decision-owner assertions | Passed |
| Unknown impact | source does not prove a consequence | supported consequence is known | inspection to decision brief | `unknown` names missing evidence | focused decision-owner assertions | Passed |
| Tool boundary | complete brief before widget | widget-only explanation | handoff to `request_user_input` | widget only collects the answer | focused decision-owner assertions | Passed |
| Selected decision | user selects an option | no selection yet | choice result to active ExecPlan | behavior and implementation shape are durable | focused decision-owner assertions | Passed |

## Plan of Work

Keep `decision-handoffs.md` as the single owner. Require Simple English for the brief and widget. Define the five option facts and structural cost terms. Require repository inspection, explicit unknowns, a complete pre-widget brief, and durable selection recording.

Add a focused route from Design Preflight to the decision owner. Update the existing rule tests and version from `0.19.1` to `0.20.0`. Update only documentation that becomes wrong.

## Validation and Acceptance

Run focused rule tests, the full suite, Python compilation, shell syntax checks, link and owner checks, manifest checks, and `git diff --check`. Finalize documentation before adversarial review.

After clean review, install the candidate and run Doctor. Use one clean read-only Codex planning session to repeat the supplied paging decision. The result must explain code consequences before it asks for a choice.

## Interfaces and Dependencies

The installed decision-handoff contract gains source-backed implementation consequences. No CLI, runtime API, dependency, or persistent product state changes. The toolkit version becomes `0.20.0`.

## Outcome

Review found one wording gap: `material code decision` was narrower than the accepted technical-choice scope. The correction uses `material technical decision` in the guard, option rule, and selection rule. The delta and final coherence reviews were clean.

The reviewed candidate is installed. Doctor reports `Result: ready` for version `0.20.0`. A clean read-only planning smoke explained all three paging options before the interactive-tool marker. It named visible behavior, structural changes, new state, proof, maintenance cost, and unavailable source facts.

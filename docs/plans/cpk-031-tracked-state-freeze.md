# Freeze tracked task status before delivery

This ExecPlan is a living document. Maintain it under `.agent/PLANS.md`.

## Purpose / Big Picture

Tracked task records must stop changing before delivery starts. The roadmap must describe durable product state. The ExecPlan must describe implementation, validation, and review. Git and GitHub must own later delivery status.

## Progress

- [x] (2026-08-16 22:08Z) Inspected the roadmap, ExecPlan, review-closure, delivery, publication, and rule-owner contracts.
- [x] (2026-08-16 22:08Z) Accepted one tracked-state freeze for all tracked task records.
- [x] (2026-08-16 22:08Z) Created branch `cpk-031-tracked-state-freeze` from CPK-030 commit `81450545d9ca`.
- [x] (2026-08-16 22:12Z) Corrected the canonical owners and added one focused regression check.
- [x] (2026-08-16 22:12Z) Validated version `0.16.1`, documentation, tests, syntax, diff, and manifest integrity.
- [x] (2026-08-16 22:22Z) Completed adversarial review and recorded the final durable outcome.

## Surprises & Discoveries

- Observation: Review Closure permits a tracked `publication status` update after clean review.
  Evidence: `assets/skills/adversarial-review/references/review-closure.md` lists it as one of five closure updates.
- Observation: Roadmap Maintainer requires the transient text `validation is complete and review is pending`.
  Evidence: `assets/skills/roadmap-maintainer/SKILL.md` requires this text before review.
- Observation: Existing ExecPlans contain delivery checkboxes and publication-status prose.
  Evidence: The current `.agent/PLANS.md` does not bound `Progress` at review closure.
- Observation: `.agent/PLANS.md` is installed in two locations with different relative-path roots.
  Evidence: Review pass 1 found that its new repository-relative route breaks in `$CODEX_HOME/PLANS.md`.

## Decision Log

- Decision: Delivery Lifecycle owns the general tracked-state freeze.
  Rationale: It already owns the boundary between implementation, review, commit, and delivery.
  Date/Author: 2026-08-16 / Codex
- Decision: Keep roadmap and ExecPlan rules specific to their content.
  Rationale: This keeps one general rule owner and prevents duplicate authority.
  Date/Author: 2026-08-16 / Codex
- Decision: Use version `0.16.1`.
  Rationale: This task corrects committed workflow behavior after version `0.16.0`.
  Date/Author: 2026-08-16 / Codex
- Decision: Route Delivery Lifecycle through AGENTS instead of `.agent/PLANS.md`.
  Rationale: AGENTS already owns skill routing and uses the correct installed skill path.
  Date/Author: 2026-08-16 / Codex

## Outcomes & Retrospective

The tracked-state owners now agree on one pre-delivery freeze. All 39 tests pass. Review pass 1 found one broken installed link. Its focused correction passed delta review and final coherence review. No residual risk remains. No separate user manual change is necessary because the focused skills own this behavior.

## Context and Orientation

`assets/skills/delivery-lifecycle/references/delivery-lifecycle.md` owns the shared task sequence. Roadmap Maintainer owns durable task states. `.agent/PLANS.md` owns ExecPlan content. Review Closure owns permitted final record updates. Publication owns Git and GitHub delivery actions. `tests/test_kit.py` protects these rule contracts.

The base branch is `cpk-030-repowise-index-routing`. The base commit is `81450545d9ca335c0744f9f8bf79efc097873783`. The task branch is `cpk-031-tracked-state-freeze`. The isolation form is a normal stacked branch.

## Product Boundary

The product source is the accepted CPK-031 plan and the current managed lifecycle skills. This task composes the live delivery, roadmap, ExecPlan, review-closure, and publication owners. Completed ExecPlans and roadmap history are records. They are not live rule owners and remain unchanged.

This task changes agent instructions. It does not change executable runtime behavior. Design Preflight does not need an independent challenge because ownership and scope are clear.

## Scenario Proof

This task has no runtime Scenario Proof. The focused rule check is the required oracle.

## Plan of Work

Add one general freeze rule to Delivery Lifecycle. Remove transient review state from Roadmap Maintainer. Bound ExecPlan progress at final review closure. Remove publication status from Review Closure. Make Publication consume the frozen tracked candidate without writing delivery results to tracked files.

Add one focused test that reads these live owners. The test must reject duplicate freeze ownership, transient roadmap readiness, future delivery actions in ExecPlan progress, and tracked publication-result updates.

Update the source version to `0.16.1`. Update the manifest after all tracked files reach their final content.

## Concrete Steps

Work in `/home/mbeutler/Projects/codex-practical-kit` on branch `cpk-031-tracked-state-freeze`.

Run `./run-tests.sh`, Python syntax checks, shell syntax checks, `git diff --check`, and `sha256sum --check MANIFEST.sha256`. Record detailed results in `.agent/test-results/cpk-031-tracked-state-freeze.md`. Never stage that file.

Stage the complete candidate and run Adversarial Review. After a clean review, apply only Review Closure updates. Then freeze the tracked candidate before its task commit.

## Validation and Acceptance

The focused check must fail against the old rules and pass against the corrected owners. The full suite and manifest checks must pass. After the task commit, `./install.sh` and `./doctor.sh` must report version `0.16.1` and `Result: ready`. These results must not change a tracked file.

## Idempotence and Recovery

The tests, installer, and Doctor are repeatable. If a required command fails, stop and report the exact error. Do not write delivery progress to a tracked document.

## Artifacts and Notes

Store detailed command and review evidence only in `.agent/test-results/cpk-031-tracked-state-freeze.md`.

## Interfaces and Dependencies

There is no new runtime interface or dependency. The public agent contract gains one tracked-state freeze before delivery.

Revision note (2026-08-16): Created from the accepted CPK-031 plan and the inspected live rule conflicts. Finalized after implementation, validation, one corrected review finding, and clean coherence review.

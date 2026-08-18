# Require discriminating Scenario Proof checks

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, a Scenario Proof cannot rely on a test that exercises adjacent behavior while the named requirement remains false. Each retained scenario identifies the one meaningful distinction under test, a minimal contrast that exposes the nearby wrong meaning, and the terminal result that must differ.

## Progress

- [x] (2026-08-17 18:31Z) Accepted the CPK-034 plan and created the isolated task branch.
- [x] (2026-08-17 18:31Z) Activated CPK-034 as the sole roadmap task.
- [x] (2026-08-17 18:39Z) Added the focused rule owner and routed planning, review, and documentation surfaces to it.
- [x] (2026-08-17 18:44Z) Added the structural integration test and forward-tested the corrected raw source packet for all seven defect shapes.
- [x] (2026-08-17 18:46Z) Finalized linked documentation and passed skill validation, 41 tests, shell syntax, diff, and manifest checks.
- [x] (2026-08-17 18:50Z) Completed a clean full review of staged tree `888e94a0db41fc5feae331afb0c40980cbec8801` and closed the task.
- [x] (2026-08-18) Selected version `0.18.0` and completed a clean full review of the publication candidate.

## Surprises & Discoveries

- Observation: Current rules require a production path, terminal oracle, runnable check, and result.
  Evidence: `assets/skills/design-preflight/references/preflight-card.md` contains those columns, but it does not require a contrast that makes the wrong meaning observable.
- Observation: The seven supplied defects share one test-design failure.
  Evidence: Each cited test held the decisive values equal, omitted the decisive state, or stopped before the terminal consumer.
- Observation: The first forward-test packet misstated cross-line ownership and omitted the batch creation order.
  Evidence: Its result permitted retargeting and split ingestion from scheduling. The corrected raw packet rejected cross-line edits and retained batch disposition as a contract gap.

## Decision Log

- Decision: Add one focused `scenario-discrimination` rule instead of seven workflow-specific rules.
  Rationale: One contrast requirement covers identity, value, state, time, source, and event distinctions without a checklist.
  Date/Author: 2026-08-17 / user and Codex
- Decision: Require a named discriminator and contrast, but do not require mutation-testing software or MC/DC metrics.
  Rationale: A small proof obligation detects the observed gap without adding dependencies or exhaustive combinations.
  Date/Author: 2026-08-17 / Codex
- Decision: Publish as version `0.18.0` through direct integration.
  Rationale: CPK-034 adds a feature before 1.0.0. The repository has no CI workflows, so PR mode is off.
  Date/Author: 2026-08-18 / Codex

## Outcomes & Retrospective

Implementation, forward testing, documentation, validation, and review are complete. The clean reviewer reported no findings.

## Context and Orientation

The task branch is `cpk-034-scenario-discrimination`. Its base branch is `main`, and its base commit is `e1d8ac887267590a763e733106121f79c927d121`.

`assets/skills/design-preflight/SKILL.md` owns the preflight procedure. Its preflight card and challenger result define the Scenario Proof interface. Adversarial Review consumes the accepted mapping. `tests/test_kit.py` protects unique rule ownership and complete routing.

A discriminator is the one identity, value, state, time, source, or event whose documented meaning a scenario proves. A contrast is the smallest paired input or seeded state that makes the required and nearby wrong meanings produce different terminal results.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). The toolkit rule surfaces are `composes`. Installed copies and tenant project code are `opaque`. Actual mutation tooling, coverage metrics, exhaustive combinations, and seven workflow-specific rules are excluded.

The supported model has one coordinator planning supported repository behavior. The project controls the preflight schema, rule routes, tests, and installed skill content. The supplied first-pass diagnostic reproduces the wrong proof result without environmental faults. The accepted plan defines the required result.

## Scenario Proof

This task changes a static planning interface, not product runtime behavior. The runtime Scenario Proof entry gate does not apply to this toolkit implementation itself.

The rule-owner check must prove that one authoritative file owns scenario discrimination and every live consumer links to it. The schema check must prove that a retained scenario names its discriminator, contrast, production path, terminal oracle, runnable check, and result. The forward check must apply the same general rule to all seven supplied defect shapes without adding shape-specific live instructions.

## Plan of Work

Add `assets/skills/design-preflight/references/scenario-discrimination.md` as the single rule owner. Require one requirement-derived discriminator, a minimal contrast that exposes the nearest wrong meaning, fixed unrelated inputs when practical, and a terminal oracle. Split a Scenario Proof row when one contrast cannot prove every claimed outcome.

Link Design Preflight, its card and challenger schema, the Adversarial Review packet, and reviewer lenses to the owner. Add the new fields to the existing Scenario Proof mapping. Do not copy the rule into routers or manuals.

Add one integration test that protects unique ownership, routes, schema fields, and the rule guards. Update the README and operating manual with links only. Update the manifest after all distributed files are final.

## Concrete Steps

Work in `/home/mbeutler/Projects/codex-practical-kit`.

Run:

    python3 /home/mbeutler/.codex/skills/.system/skill-creator/scripts/quick_validate.py assets/skills/design-preflight
    python3 -m unittest tests.test_kit.IntegrationTests.test_scenario_proof_requires_a_discriminating_case
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record detailed results in `.agent/test-results/cpk-034-scenario-discrimination.md`. Never stage that file.

## Validation and Acceptance

The focused test must fail when the rule owner, a route, a discriminator field, a contrast field, or the split-row requirement is absent. The full suite must pass.

Forward evidence must show that the general rule exposes all seven supplied shapes: cross-identity authorization, equal-baseline retained state, historical versus current value, staged rollover, zero versus absent, equal value under a new identity, and prior versus same-run state.

One clean-context reviewer must inspect the staged candidate from base commit `e1d8ac887267590a763e733106121f79c927d121`.

## Idempotence and Recovery

The edits are static rules and tests. Validation commands are safe to repeat. If a command fails, stop and report the error.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, and `.vscode/`. They are untracked environment state outside this task.

## Interfaces and Dependencies

The challenger scenario object gains `discriminator` and `contrast`. The Scenario Proof table gains matching columns. No runtime dependency or external service changes.

Revision note: Created from the accepted CPK-034 plan and the supplied first-pass defect diagnostic.
Revision note: Recorded implementation and the corrected seven-shape forward test.
Revision note: Recorded final validation and documentation status before review.
Revision note: Recorded the clean staged-tree review and task closure.
Revision note: Recorded the authorized publication version and direct-integration path before delivery.
Revision note: Recorded the clean publication-candidate review before the version commit.

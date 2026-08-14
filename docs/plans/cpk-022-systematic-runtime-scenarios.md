# Derive runtime scenarios before implementation

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, Design Preflight derives normal-use runtime scenarios with a repeatable method. One fresh read-only challenger performs an independent derivation before implementation. Undefined normal-use outcomes stop planning instead of becoming accidental behavior.

## Progress

- [x] (2026-08-14 21:14Z) Compared systematic test-design methods and selected three scenario lenses.
- [x] (2026-08-14 21:18Z) Completed one clean-context planning challenge from raw workflow examples.
- [x] (2026-08-14 21:20Z) Received human decisions to require the challenge and stop on unresolved contracts.
- [x] (2026-08-14 21:48Z) Created stacked branch `cpk-022-systematic-runtime-scenarios` and activated CPK-022.
- [x] (2026-08-14 22:08Z) Implemented the scenario proof, independent challenge, durable ExecPlan rules, compact policy, documentation, and focused test.
- [x] (2026-08-14 22:21Z) Forward-tested scheduled-worker, date-input, persistent-event, and collection-decision workflows. Retested date input after correcting the result schema.
- [x] (2026-08-14 22:28Z) Passed skill validation, the focused integration test, all 31 tests, shell syntax checks, diff checks, and the 94-line profile limit. Updated the authoritative documentation.
- [x] (2026-08-14 22:39Z) Corrected two validated pass-1 findings and confirmed that a prospective path remains applicable without a current implementation.
- [x] (2026-08-14 22:48Z) Reached a clean third review pass after two pass-1 implementation corrections and one pass-2 documentation correction. Prepared the local checkpoint.

## Surprises & Discoveries

- Observation: The current preflight derives no general boundary scenarios.
  Evidence: `assets/skills/design-preflight/SKILL.md` defines ownership, scope, and one complete-set rule only.
- Observation: The optional preflight reviewer receives the coordinator's card.
  Evidence: This packet can anchor the reviewer to scenarios that the coordinator already found.
- Observation: The existing reviewer schema cannot preserve an undefined normal-use outcome.
  Evidence: It drops a result when the explicit-requirement value is false.
- Observation: Defect-style applicability fields made valid scenarios claim that they violated a requirement.
  Evidence: The first forward tests had to set `violates_explicit_requirement` to `true` for correct expected results. The schema now asks whether a result is defined instead.
- Observation: Review found that the legacy current-path reproduction gate conflicted with prospective scenario feasibility.
  Evidence: A planned normal-use path could fail the old gate before implementation even when its trigger was feasible without fault injection.
- Observation: Review found that a runtime preflight could require a Scenario Proof without independently requiring an ExecPlan.
  Evidence: The temporary card was merged only for work that already met the narrower ExecPlan triggers.

## Decision Log

- Decision: Use input-domain, path-and-transition, and collection-semantics lenses.
  Rationale: These lenses derive the supplied date, cutoff, orphan-state, filter, and cardinality cases without a universal checklist.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Require one independent challenge for every Design Preflight that covers non-trivial runtime behavior.
  Rationale: The implementer's own experience is not a reliable scenario generator.
  Date/Author: 2026-08-14 / user
- Decision: Start the challenger without inherited task conversation.
  Rationale: Raw requirements and source reduce anchoring from the coordinator's proposed checks or correction.
  Date/Author: 2026-08-14 / Codex
- Decision: Stop planning when supported normal use has no explicit result.
  Rationale: The coordinator must not invent public behavior.
  Date/Author: 2026-08-14 / user
- Decision: Keep version 0.11.0.
  Rationale: No `0.11.0` tag or GitHub release exists. This branch is stacked on unpublished work.
  Date/Author: 2026-08-14 / Codex
- Decision: Use trigger feasibility for all Design Preflight requirements and require one ExecPlan for every non-trivial runtime preflight.
  Rationale: Prospective behavior cannot reproduce a current defect, and the accepted Scenario Proof needs one durable owner.
  Date/Author: 2026-08-14 / Codex, review pass 1

## Outcomes & Retrospective

Implementation, independent forward testing, corrections, validation, documentation, and clean review are complete. The change is ready for its local checkpoint. Publication is not authorized.

The final reviewer found no defects. Pass 1 found two implementation-policy conflicts. Pass 2 found one documentation inconsistency, which did not increment or reset the defect count. Pass 3 was clean.

## Context and Orientation

The task uses branch `cpk-022-systematic-runtime-scenarios`. Its base branch is `cpk-021-severe-defect-stop-diagnostics`, and its base commit is `b36de27`.

`assets/skills/design-preflight/SKILL.md` owns the pre-implementation process. Its `references/preflight-card.md` owns the temporary card. Its `references/preflight-review.md` owns challenger output. `.agent/PLANS.md` owns the durable ExecPlan contract. The accepted scenario proof must move into the ExecPlan. It must not create a second durable plan.

## Supported Operating Model

One coordinator reads repository source and writes one preflight. One fresh read-only challenger derives scenarios independently. The coordinator compares both results once. Small changes with one proven owner and one direct check continue to skip Design Preflight.

Exclude I/O faults, permission changes, concurrency, interruption, retry, recovery, hostile input, outside writers, and external outages unless the task includes them.

## Scenario Proof

For each changed runtime outcome, trace the entry point through relevant gates to its terminal owner. Derive only feasible cases from three lenses.

The input-domain lens covers presence, syntax, semantic validity, range boundaries, and explicit relationships. The path-and-transition lens covers selectors, filters, transformations, controlled time boundaries, state transitions, and terminal obligations. The collection lens covers supported empty input, one record, duplicates, a duplicate prefix with a later counterexample, and every record that owes a terminal result.

A retained scenario has a source requirement, a concrete trigger, an expected result, and a runnable check. An inapplicable lens has one short reason. Do not combine all inputs into a Cartesian product.

If normal use, project control, and trigger feasibility without fault injection are true but no explicit result exists, record a contract gap. Stop for human direction before implementation. Do not classify the gap as a defect or invent an outcome.

The challenger receives raw requirements, the supported model, exclusions, source locations, owners, gates, and current tests. It does not receive the coordinator's card, scenarios, implementation, previous diagnostics, corrections, severity, or preferred outcome.

## Scope Ceiling

Do not add a new skill, runtime script, service, dependency, persistent scenario database, universal edge-case checklist, fuzzing mandate, exhaustive input product, multiple challenger loop, or special zero-delta rule. Do not remove the direct-fix exception.

## Plan of Work

Update Design Preflight to require the independent challenge for non-trivial runtime behavior. Replace the anchored reviewer packet with raw evidence. Apply the supported-model gate once. Merge accepted scenarios into the preflight and ExecPlan.

Expand the existing preflight card with one concise Scenario Proof section. Update the existing reviewer reference with `scenarios`, `contract_gaps`, `exclusions`, and `coverage` outputs. Do not add another reference file.

Update `.agent/PLANS.md`, the compact global policy, and Session Start guidance. Add one focused integration test. Update the README, operating manual, and design rationale. Regenerate `MANIFEST.sha256` after content is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit`.

Run:

    python3 /home/mbeutler/.codex/skills/.system/skill-creator/scripts/quick_validate.py assets/skills/design-preflight
    python3 -m unittest tests.test_kit.IntegrationTests.test_runtime_scenario_preflight_is_independent_and_durable
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record detailed results in `.agent/test-results/cpk-022-systematic-runtime-scenarios.md`. Never stage that file.

## Validation and Acceptance

Forward-test raw scheduled-worker, date-input, persistent-event, and collection-decision artifacts. The challenger must find the applicable scenario classes without receiving the expected cases. It must preserve an undefined supported result as a contract gap. It must exclude unsupported environmental failures.

The focused test must fail if the challenge is optional for non-trivial runtime behavior, inherits the coordinator's proposed scenarios, lacks contract gaps, permits implementation with an unresolved contract, omits a lens, creates a second artifact, or removes the direct-fix exception.

The managed AGENTS source must remain below 100 lines. One fresh correctness reviewer must inspect the cumulative diff from `b36de27`.

## Idempotence and Recovery

The changes are static policy and documentation. Repeating validation is safe. If a command fails, stop and report it. Do not add retry or recovery behavior.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, and `.vscode/`. They are untracked environment state outside this task.

## Interfaces and Dependencies

The challenger JSON uses `reviewer`, `scenarios`, `contract_gaps`, `exclusions`, and `coverage`. A scenario requires normal use, project control, a feasible trigger without fault injection, and a defined result. A contract gap has the first three values and no defined result.

No public command, runtime dependency, or external service changes.

Revision note: Created from the accepted conversational plan and clean-context planning challenge.
Revision note: Recorded implementation, four unrelated forward tests, and the corrected scenario applicability schema.
Revision note: Recorded the pass-1 corrections and prospective-path retest.
Revision note: Corrected one pass-2 review-housekeeping inconsistency in this ExecPlan.
Revision note: Recorded clean review closure and local checkpoint readiness. Publication remains unauthorized.

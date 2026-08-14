# Protect full-set invariants from bounded samples

This ExecPlan is a living document. Maintain it according to the repository's `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, an agent cannot use a bounded raw-input sample to approve a result that depends on every matching record. Design Preflight states the full-set invariant before implementation. Correctness review challenges limits, sampling, and early success. One focused check uses duplicate prefix values followed by a different value.

## Progress

- [x] (2026-08-14 20:01Z) Reproduced the process defect from the supplied Microsoft renewal example.
- [x] (2026-08-14 20:01Z) Identified the managed policy, Design Preflight, and correctness lens as the outcome owners.
- [x] (2026-08-14 20:01Z) Defined the behavior floor, scope ceiling, and exact checks.
- [x] (2026-08-14 20:01Z) Created branch `cpk-020-protect-full-set-invariants` and activated CPK-020.
- [x] (2026-08-14 20:04Z) Corrected the policy owners and operating manual.
- [x] (2026-08-14 20:04Z) Passed the focused check, all 29 tests, Python compilation, shell lint, diff check, and checksum check.
- [x] (2026-08-14 20:04Z) Completed clean-context review pass 1 with no findings. A local checkpoint is ready.

## Surprises & Discoveries

- Observation: Ponytail already forbids simplifying explicit validation and requires correct edge-case behavior.
  Evidence: The installed Ponytail skill says that the ladder runs after complete understanding and must not simplify explicit validation.
- Observation: A blanket ban on limits or early termination rejects correct implementations.
  Evidence: `COUNT(DISTINCT value)`, `DISTINCT value LIMIT 2`, and stopping after the first proven violation preserve the required result.

## Decision Log

- Decision: Treat this as a process defect in invariant definition and review preparation.
  Rationale: The implementation optimized before it expressed the requirement over the complete matching set.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Forbid successful full-set conclusions from bounded raw inputs.
  Rationale: Duplicate prefix rows can hide a later counterexample.
  Date/Author: 2026-08-14 / Codex
- Decision: Permit aggregates and bounded reads that preserve the full-set result.
  Rationale: The rule must reject the faulty operation order without banning correct database operations.
  Date/Author: 2026-08-14 / Codex
- Decision: Keep version 0.11.0.
  Rationale: No `0.11.0` tag or GitHub release exists. A local checkpoint does not change the version.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

The toolkit now defines one full-set rule across implementation policy, Design Preflight, correctness review, and the operating manual. The focused policy check and all 29 tests pass. Python compilation, shell lint, diff, and checksum checks pass. Clean-context review pass 1 found no findings. The local checkpoint is ready, but publication is not authorized by this request.

## Context and Orientation

The task uses branch `cpk-020-protect-full-set-invariants`. Its base branch is `main`, and its base commit is `33128b02ee2040c3dba2d527528b656fad013eb3`. The work uses one writable implementation stream in the current checkout.

The reported defect used `LIMIT 2` on raw rows before duplicate renewal dates were removed. Two duplicate rows supported a false success result while a later distinct date remained unread. The requirement covered all matching products in the latest billing month.

The toolkit-managed global policy is `assets/AGENTS.block.md`. The Session Start summary is `assets/hooks/session_start.py`. Design preparation is owned by `assets/skills/design-preflight/SKILL.md`. Correctness review prompts are owned by `assets/skills/adversarial-review/references/reviewer-lenses.md`.

## Normal-Use Behavior Floor

When an explicit requirement covers every matching record, the success path must use the complete set or a logically equivalent aggregate. It must not limit raw records before grouping, deduplication, or aggregation and then claim success.

The implementation check must include duplicate prefix values followed by a later counterexample. A correct implementation rejects that data. Correct aggregates and short-circuit failure paths remain valid.

## Scope Ceiling

Do not ban all uses of `LIMIT`, sampling, or early termination. Do not add database-specific query guidance, runtime enforcement, a new skill, a new dependency, or a general combinatorial test checklist. Do not change review-cycle accounting or supported environmental conditions.

## Plan of Work

Add one compact full-set rule to the managed policy and Session Start summary. Add the detailed design obligation to Design Preflight. Add the matching challenge to the correctness reviewer lens.

Add one integration test that requires the rule in each owner and preserves the managed-profile line limit. Update the operating manual with the durable process rule. Regenerate `MANIFEST.sha256` after all content is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-020-protect-full-set-invariants`.

Run:

    python3 -m unittest tests.test_kit.IntegrationTests.test_full_set_invariants_reject_bounded_raw_samples
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record results in `.agent/test-results/cpk-020-protect-full-set-invariants.md`. Never stage that file.

## Validation and Acceptance

The focused check must fail if the managed policy, Session Start summary, Design Preflight, or correctness lens loses its role. The complete suite must pass. The managed global profile must remain below 100 installed lines.

A reader must see that a raw sample cannot prove success for a complete-set requirement. The same reader must see that a correct aggregate or proven failure short-circuit remains allowed.

## Idempotence and Recovery

The policy edits are static text. Repeating validation is safe. Stop and report the first command failure. Do not add retry or recovery behavior.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, and `.vscode/`. They are untracked environment state outside this task.

## Interfaces and Dependencies

No runtime interface or dependency changes. The public behavior is the toolkit's implementation and review policy for requirements over complete matching sets.

Revision note: Created from a confirmed implementation shortcut that limited raw rows before deduplication and produced a false success result. Closed after clean review pass 1.

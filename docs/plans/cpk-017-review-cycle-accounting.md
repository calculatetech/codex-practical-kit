# Count only implementation defects toward the review breaker

This ExecPlan is a living document. Maintain it according to the repository's `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, documentation and review-housekeeping findings can be corrected without consuming the three-defect breaker. The breaker counts only consecutive review passes that find validated defects in executable source, tests, migrations, dependencies, or runtime, build, or security configuration.

## Progress

- [x] (2026-08-14 17:24Z) Confirmed that the current review skill counts every validated P0, P1, or P2 finding.
- [x] (2026-08-14 17:24Z) Defined the count floor, scope ceiling, and existing review skill as the behavior owner.
- [x] (2026-08-14 17:24Z) Created stacked task branch `cpk-017-review-cycle-accounting` and activated CPK-017.
- [x] (2026-08-14 17:31Z) Corrected the review skill and its installed summaries.
- [x] (2026-08-14 17:31Z) Added one consistency test and updated affected documentation.
- [x] (2026-08-14 17:31Z) Passed the focused test, 27 full-suite tests, compilation, shell syntax, and the diff check.
- [x] (2026-08-14 17:39Z) Validated checksums and completed clean-context review on pass 1.

## Surprises & Discoveries

- Observation: The installed agent rules already say to stop when pass 3 finds a code defect, but the detailed review skill counts all validated correctness defects.
  Evidence: `assets/AGENTS.block.md` names a code defect. `assets/skills/adversarial-review/SKILL.md` makes every P0, P1, or P2 finding defectful.

## Decision Log

- Decision: Documentation and review-housekeeping findings neither increment nor reset the breaker count.
  Rationale: They remain valid work, but they are not evidence of repeated implementation failure.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Keep the limit at three consecutive counted passes.
  Rationale: The user corrected what counts. The user did not change the implementation-defect limit.
  Date/Author: 2026-08-14 / Codex
- Decision: Keep version 0.11.0.
  Rationale: This policy correction is part of the unpublished 0.11.0 candidate. It does not consume another version.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

The review skill now counts only implementation defects toward the three-defect breaker. Documentation and housekeeping remain actionable without changing the count. The focused policy test and all 27 tests pass. Review pass 1 is clean.

Publication status: A local checkpoint commit is authorized. Push is not authorized for CPK-017.

## Context and Orientation

The task uses branch `cpk-017-review-cycle-accounting`. Its base branch is `cpk-016-required-repowise`, and its base commit is `ebf461f376f1ceead82f4962bf7a4c0d07bae4e7`. This normal stacked branch preserves the reviewed CPK-016 checkpoint. CPK-015 and CPK-016 are not integrated into `main`.

`assets/skills/adversarial-review/SKILL.md` owns the detailed finding and breaker procedure. `assets/AGENTS.block.md` installs the main agent rules. `README.md`, `docs/REVIEW.md`, `docs/OPERATING-MANUAL.md`, and `docs/WHY-THIS-SHAPE.md` explain the same policy. `tests/test_kit.py` checks that distributed policy owners agree.

A counted defect is a validated P0, P1, or P2 correctness defect in executable source, tests, migrations, dependencies, or runtime, build, or security configuration. A documentation finding concerns prose or static documentation. Review housekeeping includes plans, roadmap state, publication records, checksums, manifests, staging scope, and ignored test-result records.

## Normal-Use Behavior Floor

Every validated in-scope finding remains actionable. Fixing a finding requires validation and a fresh reviewer when the candidate changes. Only a pass with a counted implementation defect advances the three-defect breaker. A documentation-only or housekeeping-only pass does not increment or reset the current count.

The coordinator stops before another automatic fix when the third consecutive counted pass finds an implementation defect. The four-part supported-model gate remains unchanged.

## Scope Ceiling

Do not weaken finding validation, review coverage, clean-review requirements, or documentation maintenance. Do not change the limit from three. Do not add persistent counter state or automation. Do not change version 0.11.0.

## Plan of Work

Rewrite the validation and breaker sections in `assets/skills/adversarial-review/SKILL.md` so any validated finding can be fixed, while only implementation defects affect the breaker count. Synchronize the shorter rule in `assets/AGENTS.block.md` and the current explanatory documents.

Add one integration test in `tests/test_kit.py`. The test must read every current policy owner and require the shared rule that documentation and housekeeping findings do not increment or reset the count. Regenerate `MANIFEST.sha256` after all tracked content is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-017-review-cycle-accounting`.

Run:

    python3 -m unittest tests.test_kit.IntegrationTests.test_review_cycle_counts_only_implementation_defects
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record results in `.agent/test-results/cpk-017-review-cycle-accounting.md`. Never stage that file.

## Validation and Acceptance

The focused test must fail if a current review-policy owner says that documentation or housekeeping advances or resets the breaker. The full suite, compilation, shell syntax, diff, and manifest checks must pass.

A human reading the detailed review skill must see that any validated finding remains actionable, that documentation and housekeeping do not change the counter, and that the third consecutive counted implementation-defect pass stops automatic correction.

## Idempotence and Recovery

The edits are static policy text and tests. Repeating validation is safe. Stop and report the first command failure. Do not add retry or recovery behavior.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, and `.vscode/`. They are untracked environment state outside this task.

## Interfaces and Dependencies

No runtime interface or dependency changes. The policy term `counted implementation defect` is introduced only to distinguish breaker accounting from other actionable findings.

Revision note: Created after review housekeeping consumed two passes during CPK-016 and the user corrected the intended breaker accounting.

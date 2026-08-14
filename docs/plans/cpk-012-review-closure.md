# Prevent self-invalidating review closure

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, a clean review remains valid when the coordinator records only its result and updates matching integrity metadata. A change to code, tests, runtime configuration, requirements, or the supported model still requires a fresh review.

## Progress

- [x] (2026-08-14 01:59Z) Reproduced the circular policy and accepted CPK-012.
- [x] (2026-08-14 01:59Z) Activated CPK-012 and merged Design Preflight into this ExecPlan.
- [x] (2026-08-14 02:00Z) Reconciled the distributed review, documentation, roadmap, and ExecPlan rules.
- [x] (2026-08-14 02:00Z) Added one focused policy-consistency check.
- [x] (2026-08-14 02:00Z) Completed validation and prepared the documentation-complete review candidate.
- [x] (2026-08-14 02:02Z) Completed fresh review pass 1 and applied review closure.

## Surprises & Discoveries

- Observation: The repository excludes plans, documentation, generated files, and review artifacts from meaningful code changes.
  Evidence: The repository instructions require review only for executable source, migrations, dependencies, and runtime, build, or security configuration.
- Observation: The installed skills override that boundary with a rule that invalidates review after any candidate file changes.
  Evidence: `assets/skills/docs-maintainer/SKILL.md` says that any candidate file change invalidates a clean review.
- Observation: The roadmap rules require a terminal state both before review and only after review completes.
  Evidence: Roadmap finalization precedes review, while the publication gate defines pre-commit review as delivery work that must complete before the terminal transition.

## Decision Log

- Decision: Define a small, explicit review-closure class.
  Rationale: Status and integrity metadata do not change the behavior or requirements that the reviewer evaluated.
  Date/Author: 2026-08-14 / Codex and user
- Decision: Keep automatic classification out of the toolkit.
  Rationale: A clear policy and one consistency check solve the current defect without a new commit framework.
  Date/Author: 2026-08-14 / Codex
- Decision: Keep version 0.5.0.
  Rationale: The current feature candidate is not committed or released.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

The toolkit now has one consistent material-change boundary and one fixed review-closure list. The focused check and complete 24-test suite pass. Fresh correctness review pass 1 was clean. Review closure records that result without starting a recursive review.

## Context and Orientation

`assets/AGENTS.block.md` contains the distributed agent rules. The skills under `assets/skills/` own review, documentation, and roadmap procedures. `.agent/PLANS.md` owns ExecPlan procedure. `docs/REVIEW.md` and `docs/OPERATING-MANUAL.md` explain the workflow to users. `tests/test_kit.py` contains policy propagation checks.

A review-invalidating change can alter behavior, test expectations, requirements, or the supported operating model. A review-closure change records the result of a completed review without changing what the reviewer evaluated.

## Plan of Work

Replace the blanket post-review freeze with one shared rule. Code, tests, dependencies, migrations, runtime configuration, security configuration, behavior requirements, and supported-model rules invalidate review. The only permitted review-closure changes are the review result in the active ExecPlan, the same task's roadmap terminal transition, publication status, integrity checksums caused by those updates, and the untracked test-result record.

Before review, finish code, tests, behavior documentation, and supported-model rules. Keep the roadmap task Active and mark it ready for review. After a clean review, apply only review-closure changes and commit without another review. If review finds a defect, return the task to implementation and review the corrected candidate with fresh context.

Add one focused consistency check in `tests/test_kit.py`. It must require the closure rule in each policy owner and reject the old blanket invalidation sentence. Update the user documentation only where its current sequence becomes wrong.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit`.

Run:

    ./run-tests.sh
    python3 -m py_compile kit.py tests/test_kit.py
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Then run one fresh read-only adversarial review. After a clean result, update only the CPK-012 review status, roadmap terminal state, and checksum manifest.

## Validation and Acceptance

The focused check must prove that all distributed policy owners allow review closure without another review. It must also prove that material changes still invalidate review. The existing test suite and lint checks must pass.

Acceptance has three scenarios. First, a review-result checkbox, terminal roadmap move, and matching checksum update do not require another review. Second, a code, test, configuration, requirement, or supported-model change requires a fresh review. Third, a defect correction follows the existing fresh-pass loop.

## Idempotence and Recovery

Policy installation and checks remain repeatable. If an operation fails, stop and report the error. This task does not add retries, rollback, recovery state, or automatic diff classification.

## Artifacts and Notes

Record detailed command results in `.agent/test-results/cpk-012-review-closure.md`. This ignored file is not part of the candidate.

## Interfaces and Dependencies

No public command or runtime dependency changes. The public workflow gains one term: review closure. It means the fixed set of status and integrity updates permitted after a clean review.

Revision note: Created from the accepted failure analysis and implementation plan.

# Review only new fixes after the first pass

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, a review finding does not cause every later reviewer to inspect the full task again. Git identifies each staged candidate with a tree hash. Later reviewers inspect only the fix delta and its direct impact. One final coherence pass checks interactions across the task.

## Progress

- [x] (2026-08-16 00:53Z) Created branch `cpk-026-review-checkpoints` from `5c0d7b01fc78e86fb108f715c9b6a17399ae30ce`.
- [x] (2026-08-16 00:53Z) Activated CPK-026 and placed CPK-027 next in `docs/roadmap.md`.
- [x] (2026-08-16 00:55Z) Added the checkpoint workflow and review packet fields.
- [x] (2026-08-16 00:55Z) Updated focused tests, version `0.13.0`, and checksums.
- [x] (2026-08-16 01:18Z) Passed validation and correctness review after two reviewed corrections.
- [x] (2026-08-16 01:19Z) Prepared the reviewed CPK-026 checkpoint candidate for commit.

## Surprises & Discoveries

- Observation: `git write-tree` creates a deterministic tree from the current index.
  Evidence: The installed Git manual states that the index must be fully merged and updated first.
- Observation: The first review found that staging before checkpoint validation could absorb an unrelated tracked edit into a fix delta.
  Evidence: Review finding R1 cited the ordering in `assets/skills/adversarial-review/SKILL.md`.
- Observation: The coherence review found that generic clean-result closure could close a task after an intermediate fix delta.
  Evidence: Review finding R2 composed Adversarial Review with Roadmap Maintainer and Review Closure.

## Decision Log

- Decision: Store review checkpoint facts in the existing ignored task review record.
  Rationale: This reuses the current evidence owner and adds no runtime or tracked ledger.
  Date/Author: 2026-08-16 / Codex and user.
- Decision: Use the staged Git tree hash as the candidate identity.
  Rationale: Git already provides the deterministic content address. A custom hashing tool is unnecessary.
  Date/Author: 2026-08-16 / Codex and user.
- Decision: Use version `0.13.0`.
  Rationale: Review checkpoints add a toolkit feature before version `1.0.0`.
  Date/Author: 2026-08-16 / Codex and user.

## Outcomes & Retrospective

Version `0.13.0` now identifies staged candidates with Git tree hashes. A full pass found one pre-stage invalidation gap. The fix delta passed. The final coherence pass found one premature-closure conflict, and its correction delta passed. No residual risk remains.

## Context and Orientation

`assets/skills/adversarial-review/SKILL.md` owns the review procedure. Its `references/review-packet.md` owns reviewer inputs. Its `references/reviewer-lenses.md` defines review lenses. Detailed task results already live in ignored `.agent/test-results/` files.

The initial review uses the full staged task candidate. If it reports findings, the result record stores that tree hash and the validated findings. A later review compares the prior tree with the current staged tree. It reads direct impact around that delta but does not reopen unrelated unchanged code.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/codex-practical-kit-rules/references/scope-boundaries.md). CPK-026 composes Adversarial Review and its templates. Git installation, product code, and unrelated toolkit skills are opaque. No deferred capability is promoted.

## Scenario Proof

This task changes an agent procedure, not runtime product behavior. No runtime Scenario Proof is required. The user resolved the ownership and review boundaries before implementation.

## Plan of Work

Extend the existing review skill. Require an exact staged candidate and use `git write-tree` to identify it. Define full, delta, and coherence modes. Add the checkpoint facts to the review packet. Keep all checkpoint rules in the review skill.

Add one focused repository test for the workflow. Update `KIT_VERSION` to `0.13.0`. Regenerate `MANIFEST.sha256` after the task documentation is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on branch `cpk-026-review-checkpoints`. Run:

    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Expect every command to exit with status zero.

## Validation and Acceptance

The first review must cover the full staged task. If it has findings, the next pass must compare staged tree hashes and inspect only the fix delta and its direct impact. After a clean delta review, one coherence pass must inspect interactions across the cumulative task. If the first full review is clean, it is final.

The focused test must fail when checkpoint identity, delta review, unchanged-code protection, or final coherence is absent.

## Idempotence and Recovery

Validation commands are safe to repeat. A changed requirement, scope, base, supported model, or unrelated tracked file invalidates the checkpoint. Classify tracked worktree changes before staging a later candidate. In an invalidation case, restart with a full review.

## Artifacts and Notes

Store detailed results in `.agent/test-results/cpk-026-review-checkpoints.md`. Do not stage that record.

## Interfaces and Dependencies

Use the installed Git CLI. Add no dependency, script, service, or persistent tracked state.

Revision note: Created the plan from the accepted review-checkpoint design.

Revision note: Recorded the implemented review modes and focused test.

Revision note: Recorded successful pre-review validation.

Revision note: Required pre-stage tracked-change classification after review finding R1.

Revision note: Limited review closure to final checkpoint results after coherence finding R2.

Revision note: Recorded the final clean review and completed roadmap transition.

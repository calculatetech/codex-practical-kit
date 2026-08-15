# Bind reviews to documented product scope

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, planning and correctness review use the product's documented boundary. Reviewers can examine owners that the task composes, protect current behavior of opaque owners, and exclude deferred placeholders. This prevents review from creating future product obligations.

## Progress

- [x] (2026-08-15 20:48Z) Created branch `cpk-024-product-scope-boundaries` from `a5766bf3d8be20bc5342eeeefd8b9815ffc82dea`.
- [x] (2026-08-15 20:48Z) Activated CPK-024 in `docs/roadmap.md`.
- [x] (2026-08-15 20:51Z) Added the canonical scope-boundary owner and linked its planning and review consumers.
- [x] (2026-08-15 20:51Z) Updated tests, documentation, version `0.12.0`, and `MANIFEST.sha256`.
- [x] (2026-08-15 20:55Z) Validated, received a clean pass-1 review, and closed the roadmap. The local checkpoint commit follows this record update.

## Surprises & Discoveries

- Observation: RepoWise retrieval succeeded, but its index predates the current commit and has no prose provider.
  Evidence: It reported indexed commit `7e8190d71946` and live commit `a5766bf3d8be`.

## Decision Log

- Decision: Keep one canonical owner at `assets/skills/codex-practical-kit-rules/references/scope-boundaries.md`.
  Rationale: Rule ownership forbids summaries of a shared rule in live consumers.
  Date/Author: 2026-08-15 / Codex and user.
- Decision: Keep the main coordinator as the implementer on one task branch.
  Rationale: This policy change has one implementation stream and no independent writable components.
  Date/Author: 2026-08-15 / Codex and user.
- Decision: Use version `0.12.0`.
  Rationale: This adds a toolkit capability before `1.0.0`, so it increments the minor version.
  Date/Author: 2026-08-15 / Codex and user.

## Outcomes & Retrospective

CPK-024 added one canonical scope owner and linked its planning and review consumers. The focused tests, all 28 repository tests, skill validation, shell checks, diff check, and manifest check passed. The clean-context correctness review returned no findings on pass 1. No runtime, dependency, configuration, or project-specific special case was added.

## Context and Orientation

The managed rules package stores shared policy in focused files under `assets/skills/codex-practical-kit-rules/references/`. Design Preflight owns task analysis. Adversarial Review owns correctness review. Their templates carry task facts, while shared rules remain in one owner.

The product boundary for this task comes from the user's accepted correction plan. The task composes Design Preflight, ExecPlans, and Adversarial Review. Existing rule owners are opaque unless this task changes their links. No deferred product capability is promoted. Meridian and its set-aside implementation are validation context only; they are not toolkit-specific requirements.

## Scenario Proof

This change does not add runtime behavior. No runtime Scenario Proof is required. The user resolved the product boundary and owner classifications before implementation, so no planning challenger is required.

## Plan of Work

Add one focused scope-boundary rule. Link Design Preflight and Adversarial Review to it. Extend their factual templates with boundary sources, owner classifications, changed production entry points, and task-visible outcomes. Keep the definitions and gate behavior only in the new owner.

Update the rule lists, focused tests, source version, and manifest. Update user documentation only where the new rule must be discoverable. Do not add a runtime, dependency, configuration option, or project-specific special case.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on branch `cpk-024-product-scope-boundaries`. Edit files with exact patches. Run:

    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Expect every command to exit with status zero.

## Validation and Acceptance

The tests must prove that the new rule has one owner, every required consumer links to it, the review schema requires the scope trace, and the package has 13 focused rule files. Manual inspection must show that deferred owners cannot produce findings unless the task promotes them.

Run one clean-context adversarial review after documentation and roadmap preparation. A clean result permits review closure and a local checkpoint commit. This task does not authorize push, tag, release, integration, or branch cleanup.

## Idempotence and Recovery

Tests and validation commands are safe to repeat. If a command fails, keep CPK-024 Active and fix only the demonstrated cause. Do not publish partial work.

## Artifacts and Notes

The ignored test record will be `.agent/test-results/cpk-024-product-scope-boundaries.md`. It can mention Meridian only as an external validation scenario. Shipped rules and tests must stay product-neutral.

## Interfaces and Dependencies

The change adds Markdown policy and schema fields. It adds no library, service, command, or runtime interface.

Revision note: Created the implementation plan from the accepted CPK-024 correction plan.

Revision note: Recorded the implemented policy surface and successful pre-review validation.

Revision note: Recorded the clean pass-1 review and completed roadmap transition.

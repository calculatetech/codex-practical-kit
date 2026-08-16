# Route toolkit rules through lifecycle skills

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, the managed AGENTS block names applicable skills instead of linking to a general rule package. Each skill loads only the focused rules needed for its lifecycle task. Every live rule still has one authoritative file.

## Progress

- [x] (2026-08-16 01:21Z) Created branch `cpk-027-lifecycle-skills` from CPK-026 checkpoint `37bdba5999615930d10ed03db1ddefea00b20cd0`.
- [x] (2026-08-16 01:22Z) Activated CPK-027 and mapped all 13 shared rule owners to lifecycle skills.
- [x] (2026-08-16 01:34Z) Migrated the rule owners, installer registration, router, tests, and current documentation.
- [x] (2026-08-16 01:39Z) Passed tests, nine skill validations, shell checks, manifest verification, and a six-case clean-context trigger test.
- [x] (2026-08-16 01:45Z) Passed the first full correctness review with no findings and prepared the reviewed candidate for commit.
- [ ] Install the exact commit live and publish version `0.14.0`.

## Surprises & Discoveries

- Observation: The installed RepoWise CLI supports index refresh but not the MCP-only `get_answer` command.
  Evidence: `repowise update --no-agents` indexed checkpoint `37bdba59`; `repowise get_answer` returned `No such command`.

## Decision Log

- Decision: Create four missing lifecycle skills and extend two existing skills.
  Rationale: This removes the catch-all package without creating one skill for each small reference.
  Date/Author: 2026-08-16 / Codex and user.
- Decision: Use version `0.14.0`.
  Rationale: Moving rule activation into lifecycle skills is a new pre-1.0 toolkit feature after committed version `0.13.0`.
  Date/Author: 2026-08-16 / Codex and user.

## Outcomes & Retrospective

Version `0.14.0` passed validation, clean-context trigger testing, and full correctness review without findings. The managed AGENTS block names skills instead of detailed rule paths. Four new lifecycle skills and two existing skills own the migrated references. The installer removes the obsolete general package. Current manuals link to the new owners. No residual risk remains.

## Context and Orientation

`assets/AGENTS.block.md` is the managed router. Lifecycle skills now contain the 13 canonical shared rule owners. `kit.py` selects installed skills and removes the obsolete general package during upgrade. `tests/test_kit.py` verifies unique owners, valid links, installation, and versioning.

The migration groups owners as follows:

- `delivery-lifecycle`: coordination, delivery lifecycle, Git isolation, and decision handoffs.
- `design-preflight`: scope boundaries, supported model, owner composition, and full-set results.
- `adversarial-review`: review closure.
- `publication`: publication and versioning.
- `repository-knowledge`: repository knowledge.
- `toolkit-maintainer`: rule ownership.

## Product Boundary

CPK-027 composes the managed router, canonical rule owners, skill installation, current manuals, and ownership validation. Historical completed ExecPlans remain records. Runtime RepoWise behavior and unrelated toolkit procedures are opaque.

## Scenario Proof

This task changes instruction activation and installation, not application runtime behavior. No runtime Scenario Proof is required. Focused installer and rule-owner tests prove the supported results.

## Plan of Work

Move each canonical owner into the lifecycle skill that needs it. Keep references focused. Give each new skill a precise triggering description. Update all live links. Replace AGENTS file links with skill names and retain the ExecPlan path because it is not a skill.

Register the four new skills, retire `codex-practical-kit-rules` during upgrade, and update the installer assertions. Preserve the owner and guard tests so duplicate rule text still fails.

Update current documentation for the new skill layout. Do not rewrite historical ExecPlans solely to change old paths. Set `KIT_VERSION` to `0.14.0` and regenerate checksums.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on branch `cpk-027-lifecycle-skills`. Run:

    ./run-tests.sh
    python3 /home/mbeutler/.codex/skills/.system/skill-creator/scripts/quick_validate.py assets/skills/<changed-skill>
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Expect each command to exit with status zero.

## Validation and Acceptance

The installed managed AGENTS block must route tasks to skill names without linking to rule references. Every canonical owner must occur once under an applicable skill. Every live Markdown link must resolve. Reinstallation must install the new skills and remove the obsolete general package.

One fresh clean-context forward test must identify the applicable skill for representative repository inspection, implementation delivery, design, review, publication, and toolkit-maintenance prompts. One adversarial correctness review must pass before commit.

## Idempotence and Recovery

Skill installation and validation are safe to repeat. The installer owns only its recorded skill copies. If validation fails, correct the branch candidate and rerun the focused check.

## Artifacts and Notes

Store detailed results in `.agent/test-results/cpk-027-lifecycle-skills.md`. Do not stage that record.

## Interfaces and Dependencies

Use the existing skill loader and installer. Add no dependency, runtime service, or custom router.

Revision note: Created the plan from the accepted lifecycle-skill design.

Revision note: Recorded the completed rule and installer migration.

Revision note: Recorded successful validation and lifecycle-skill trigger testing.

Revision note: Recorded the clean full review and completed roadmap transition.

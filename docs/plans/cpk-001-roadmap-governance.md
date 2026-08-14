# Establish authoritative roadmap governance

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

Repositories can use `docs/roadmap.md` as the human source of truth for accepted work. Agents update it before implementation and at every process change.

The toolkit provides one Roadmap Maintainer skill and one reusable template. Installation never creates or replaces a repository roadmap.

## Progress

- [x] (2026-08-13) Created the toolkit roadmap and assigned permanent CPK identifiers.
- [x] (2026-08-13) Added the Roadmap Maintainer skill and template.
- [x] (2026-08-13) Added roadmap lifecycle rules to global and session guidance.
- [x] (2026-08-13) Documented Plan Mode as read-only work.
- [x] (2026-08-13) Set version `0.3.0` for the new feature.
- [x] (2026-08-13) Stopped the original review after speculative recovery work caused repeated defect cycles.
- [x] (2026-08-13) Moved that rejected design to CPK-010 and CPK-009.
- [x] (2026-08-13) Completed final validation with CPK-010 and prepared the documentation-complete review candidate.

## Surprises & Discoveries

- Observation: Exact-candidate and recovery work grew beyond the personal single-user operating model.
  Evidence: The rejected candidate reached 64 tests and repeated three-pass review stops.
- Observation: The roadmap exposed the scope change before the first commit.
  Evidence: CPK-010 records the accepted simplification and CPK-009 records declined transactional installation.

## Decision Log

- Decision: Use `docs/roadmap.md` as the only roadmap authority.
  Rationale: The user needs one readable view of active, planned, declined, and completed work.
  Date/Author: 2026-08-13 / user
- Decision: Initialize a roadmap only after an explicit user request.
  Rationale: Installation must not create a new project authority.
  Date/Author: 2026-08-13 / user
- Decision: Finalize documentation and roadmap state before review and commit.
  Rationale: Post-commit documentation changes are forbidden.
  Date/Author: 2026-08-13 / user
- Decision: Release the feature as version `0.3.0`.
  Rationale: New features increment the second version digit.
  Date/Author: 2026-08-13 / user
- Decision: Reject speculative recovery and proof-style verification.
  Rationale: These features do not serve the supported operating model.
  Date/Author: 2026-08-13 / user

## Outcomes & Retrospective

The roadmap, skill, template, Plan Mode rules, and documentation order are implemented. The roadmap now shows the final candidate before its one supported-model review and shared root commit.

## Context and Orientation

`assets/skills/roadmap-maintainer/SKILL.md` owns roadmap lifecycle changes. Its template is under the same skill. `assets/AGENTS.block.md` installs the global rules. `assets/hooks/session_start.py` provides session guidance.

## Plan of Work

Install the Roadmap Maintainer skill with the core skills. Preserve permanent task identifiers and at most one Active task. Add Planned next, Planned later, Accepted residual risk, Declined, and Completed sections.

Update documentation and the roadmap before review. Do not change documentation after the task commit.

## Concrete Steps

Run the shared CPK-010 checks from `/home/mbeutler/Projects/codex-practical-kit`.

## Validation and Acceptance

The unit suite must prove template propagation, one Active section, a Declined section, and repository roadmap preservation.

The final roadmap must show no incorrectly Active task. The commit must contain all documentation.

## Idempotence and Recovery

Roadmap updates preserve identifiers and human notes. Installation does not mutate repository roadmaps.

## Artifacts and Notes

Detailed combined results belong in `.agent/test-results/cpk-010.md` and remain untracked.

## Interfaces and Dependencies

The public skill name is `roadmap-maintainer`. Its installed template is `assets/roadmap-template.md` relative to the skill.

No dependency or service is added.

Revision note: Replaced rejected recovery history with the final roadmap-governance design selected through CPK-010.

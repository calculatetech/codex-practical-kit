# Make ExecPlan the durable task model

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

The toolkit will give each non-trivial task one durable implementation plan. Codex will use a repository `.agent/PLANS.md` when present. Otherwise, it will use the toolkit-managed `$CODEX_HOME/PLANS.md` fallback.

Plan Mode and Design Preflight remain preparation stages. They feed the ExecPlan instead of creating competing task records. Task Brief is obsolete and will no longer be installed.

## Progress

- [x] (2026-08-13) Confirmed ExecPlan as the only durable implementation model.
- [x] (2026-08-13) Selected `$CODEX_HOME/PLANS.md` as the managed fallback.
- [x] (2026-08-13) Completed the design preflight and activated CPK-002.
- [x] (2026-08-13) Updated planning policy and removed Task Brief.
- [x] (2026-08-13) Added managed plan installation, upgrade, diagnostics, and uninstall behavior.
- [x] (2026-08-13) Added focused lifecycle tests.
- [x] (2026-08-13) Finalized documentation, the roadmap, and the checksum manifest.
- [ ] Run one fresh adversarial review (completed: all required validation; remaining: review).
- [x] (2026-08-13) Updated the authorized live installation and confirmed that `doctor` reports ready.

## Surprises & Discoveries

- Observation: The live unmanaged profile already contains the ExecPlan rule.
  Evidence: `~/.codex/AGENTS.md` contains a Planning section before the kit-managed block.
- Observation: The current kit installs Task Brief as a durable handoff while `.agent/PLANS.md` defines ExecPlan as the durable execution specification.
  Evidence: `assets/skills/task-brief/SKILL.md` and `.agent/PLANS.md` both claim durable task ownership.
- Observation: Manifest schema version 1 can record the new managed plan without a schema change.
  Evidence: Existing manifests ignore unknown fields, and the focused lifecycle tests cover old manifests without `plans_file`.

## Decision Log

- Decision: ExecPlan is the only durable implementation plan.
  Rationale: The OpenAI ExecPlan model has worked well for the user and already exists in this repository.
  Date/Author: 2026-08-13 / user
- Decision: Install `$CODEX_HOME/PLANS.md` as a managed fallback.
  Rationale: Every repository gets the model without duplicate repository copies. A repository can still provide `.agent/PLANS.md` as an override.
  Date/Author: 2026-08-13 / user
- Decision: Remove Task Brief from the core kit.
  Rationale: A second durable handoff creates ambiguous ownership.
  Date/Author: 2026-08-13 / user
- Decision: Keep Plan Mode and Design Preflight as temporary preparation stages.
  Rationale: They improve the ExecPlan but do not need separate task artifacts.
  Date/Author: 2026-08-13 / Codex

## Outcomes & Retrospective

The repository and live installation now use one managed ExecPlan fallback. Repository overrides remain supported, and the obsolete Task Brief skill is absent. Fourteen tests and all required checks pass. The final review remains.

## Context and Orientation

`.agent/PLANS.md` is the canonical ExecPlan template in this repository. `assets/AGENTS.block.md` is copied into the managed section of `$CODEX_HOME/AGENTS.md`. `kit.py` owns installation, upgrade, diagnostics, and uninstall. The install manifest records which shared files and skills the toolkit owns.

`assets/skills/design-preflight/SKILL.md` defines a short, temporary design card. It must merge its accepted result into the ExecPlan. `assets/skills/task-brief/` is the obsolete competing model.

The supported operating model has one personal user and one Codex writer on a normal local filesystem with Git. The task excludes concurrent writers, interruption, retry, rollback, recovery, links, permissions, submodules, and outside influence.

## Plan of Work

Update `.agent/PLANS.md` and the managed AGENTS block so that complex features, multi-file changes, and significant refactors use one ExecPlan. Use a repository `.agent/PLANS.md` first and `$CODEX_HOME/PLANS.md` otherwise. Keep small isolated changes plan-free. Store task plans in `docs/plans/` and use a roadmap identifier in the filename when one exists.

Make Design Preflight merge its accepted card into the ExecPlan. Remove Task Brief from the skill list, source tree, documentation, examples, manifest checksum, and installed records. Keep Spec Kit as an optional behavior-input system while ExecPlan owns execution progress.

Extend `kit.py` to install the canonical `.agent/PLANS.md` content at `$CODEX_HOME/PLANS.md`. Record the path in manifest schema version 1. A fresh install creates the file. A reinstall replaces it only when the current manifest records ownership. An unrecorded destination is a conflict and stops before installation changes shared state. Upgrade removes a Task Brief skill only when the prior manifest owns it. Uninstall removes only the recorded plan and recorded skills. Doctor compares the managed plan with the canonical source.

Update the version to `0.4.0`, user documentation, installation prompt, and checksum manifest. Then run the required tests and checks. Finalize the roadmap before one fresh read-only adversarial review.

After a clean candidate exists, update the live profile. Remove only unmanaged ExecPlan text duplicated by the managed block. Run the installer to create the global plan and remove the manifest-owned Task Brief skill. Preserve all other live instructions.

## Concrete Steps

Work in `/home/mbeutler/Projects/codex-practical-kit`.

Run:

    PYTHONDONTWRITEBYTECODE=1 ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Store command results in `.agent/test-results/cpk-002.md`. Do not stage this file.

After the clean review, run:

    ./install.sh
    ./doctor.sh

## Validation and Acceptance

A fresh installation creates `$CODEX_HOME/PLANS.md` with the same content as `.agent/PLANS.md`. The manifest records the plan path. Reinstallation replaces a recorded plan. An unrecorded plan causes a conflict before other shared installation state changes.

Upgrade removes a manifest-owned Task Brief skill. The new manifest and installed skills exclude it. Uninstall removes a recorded plan and preserves an unrecorded plan.

The installed AGENTS block states one ownership chain. Plan Mode and Design Preflight feed one ExecPlan. A repository `.agent/PLANS.md` overrides the global fallback. Doctor reports a missing or changed managed plan.

The final live profile contains one ExecPlan rule, one global plan file, and no kit-owned Task Brief skill. All required checks pass.

## Idempotence and Recovery

Install and uninstall remain repeatable in the supported model. If an operation fails, stop and report the error. Do not retry, roll back, or repair partial work.

## Artifacts and Notes

OpenAI documents ExecPlans at `https://developers.openai.com/cookbook/articles/codex_exec_plans/`. OpenAI documents global and repository AGENTS discovery at `https://learn.chatgpt.com/docs/agent-configuration/agents-md`.

Existing untracked `.claude/`, `.mcp.json`, `.repowise/`, and `.vscode/` files are outside this task.

## Interfaces and Dependencies

The public skill list no longer contains `task-brief`. The install manifest keeps schema version 1 and adds `plans_file` with the absolute managed path.

No command-line flag, dependency, service, or repository plan copy is added.

Revision note: Created from the accepted CPK-002 conversational plan and design preflight.

Revision note: Recorded the completed implementation, documentation, focused tests, and live installation before final validation.

Revision note: Recorded final validation and the documentation-complete review candidate.

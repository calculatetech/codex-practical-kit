# Restore deterministic least effort

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

The toolkit must guide Codex toward the smallest useful implementation. It must not turn unsupported environmental scenarios into product requirements.

Version `0.3.0` installs skills as ordinary copies. Its Stop hook compares plain Git status and current completion markers. Review rejects a finding unless it occurs in the declared operating model.

## Progress

- [x] (2026-08-13) Accepted the deterministic least-effort direction and selected copy-only installation.
- [x] (2026-08-13) Selected a plain Git-status Stop gate and the kit policy layer for the new rule.
- [x] (2026-08-13) Completed the bounded design preflight.
- [x] (2026-08-13) Made CPK-010 the sole Active roadmap task.
- [x] (2026-08-13) Deleted speculative installer, hook, review, and test machinery.
- [x] (2026-08-13) Finalized documentation and roadmap state.
- [x] (2026-08-13) Validated the final candidate with 12 focused tests, shell syntax checks, CLI help checks, and Git diff checks.
- [x] (2026-08-13) Review pass 1 found that a changed `skills_home` could reuse ownership names from the prior directory.
- [x] (2026-08-13) Scoped ownership to the manifest's recorded `skills_home` and added the focused reinstall check.
- [x] (2026-08-13) Review pass 2 found that uninstall still used command-line destinations instead of recorded destinations.
- [x] (2026-08-13) Made uninstall use the manifest's `codex_home` and `skills_home`, and extended the lifecycle check.
- [ ] Run supported-model review pass 3 on the corrected frozen candidate.
- [ ] Create the authorized local root commit.

## Surprises & Discoveries

- Observation: The installed `0.2.1` toolkit still provides a small working hook baseline.
  Evidence: `/home/mbeutler/.local/share/codex-practical-kit/install-manifest.json` reports version `0.2.1`.
- Observation: The rejected candidate grew to 64 tests through fault injection and edge-case simulations.
  Evidence: The replacement suite has 12 focused tests after those cases were removed.
- Observation: Skill-name ownership is not sufficient when the public `--skills-home` option changes the destination.
  Evidence: Review pass 1 reproduced replacement of an unrecorded same-name directory in the new location.
- Observation: Install and uninstall must read destination ownership from the same manifest fields.
  Evidence: Review pass 2 reproduced removal from a command-line skills directory that the manifest did not own.

## Decision Log

- Decision: Support one personal user and one Codex writer on normal local filesystems and Git.
  Rationale: This is the toolkit's real operating model.
  Date/Author: 2026-08-13 / user
- Decision: Use copied skill directories and manifest names as ownership.
  Rationale: A true or false ownership claim is enough for installation and removal.
  Date/Author: 2026-08-13 / user
- Decision: Compare plain Git status at Stop.
  Rationale: The hook is a reminder, not a proof system.
  Date/Author: 2026-08-13 / user
- Decision: Keep the new rule in toolkit policy and do not fork Ponytail.
  Rationale: The external skill remains pinned and replaceable.
  Date/Author: 2026-08-13 / user
- Decision: Apply manifest ownership only in the manifest's recorded `skills_home`.
  Rationale: A copied name in another supported destination is unrecorded and must remain a conflict.
  Date/Author: 2026-08-13 / Codex
- Decision: After uninstall locates a manifest, use its recorded `codex_home` and `skills_home`.
  Rationale: Those fields identify the installed files that the manifest owns.
  Date/Author: 2026-08-13 / Codex

## Outcomes & Retrospective

Version `0.3.0` now uses copied skills, manifest-scoped install and uninstall ownership, a plain Git-status Stop reminder, and one supported-model reviewer per pass. The corrected candidate is validated and documentation-complete. Only review pass 3 and the authorized local commit remain.

## Context and Orientation

`kit.py` owns installation and removal. The install manifest records skill names owned by the toolkit. `assets/hooks/hook_common.py` stores one session baseline. `assets/hooks/stop_gate.py` checks Git status and completion markers. `assets/AGENTS.block.md`, Design Preflight, and Adversarial Review define the operating model.

The rejected candidate contained digests, backups, rollback, link inspection, permission inspection, submodule handling, and persistent review evidence. This task removes those features.

## Plan of Work

Replace skill-link installation with direct copies. A recorded destination is owned. An unrecorded destination is a conflict. Upgrade removes a recorded `0.2.1` destination and copies the new skill. Uninstall removes recorded destinations once.

Replace candidate fingerprints with `git status --porcelain=v1 --untracked-files=all`. Store that text at Session Start. At Stop, compare the current text with the baseline. Check current Review and Docs markers when the text differs. Return immediately in Plan Mode.

Add the supported-model true or false gate to global rules, Design Preflight, Task Brief, and Adversarial Review. Use one fresh reviewer per review pass. Delete automatic refuters and review fan-out.

Replace tests that preserve excluded behavior. Keep normal lifecycle, conflict, `0.2.1` upgrade, Stop truth table, roadmap propagation, and managed configuration checks.

Update user documentation. Remove recovery and exact-candidate claims. Add a Declined roadmap section. Regenerate `MANIFEST.sha256` after all documentation is final.

## Concrete Steps

Work in `/home/mbeutler/Projects/codex-practical-kit`.

Run:

    PYTHONDONTWRITEBYTECODE=1 ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Store detailed results in `.agent/test-results/cpk-010.md`. Do not stage that file.

## Validation and Acceptance

Installation copies every skill. Reinstallation replaces manifest-owned copies only in the recorded `skills_home`. An unrecorded conflict stops before installation changes a skill. An installed `0.2.1` link upgrades through the normal recorded-destination path.

Uninstall removes recorded copies and managed configuration from the manifest's recorded destinations. An absent manifest reports that the toolkit is not installed and changes nothing.

Plan Mode never starts a Stop continuation. A changed Git status requires the applicable current markers. Accepted markers advance the baseline.

The final review uses one fresh correctness reviewer. A finding counts only when all four supported-model questions are true.

## Idempotence and Recovery

Normal installation and removal are repeatable. If an operation fails, the command stops and reports the exception. The toolkit does not retry, roll back, or repair partial work.

## Artifacts and Notes

The final candidate remains version `0.3.0`. No earlier version in this repository was committed or released.

## Interfaces and Dependencies

Remove `install --replace-existing` and `uninstall --force`. Keep `uninstall --purge`.

The install manifest keeps `schema_version`, `kit_version`, paths, upstream pins, and a `skills` list. Each new skill record contains only `name`. The recorded `skills_home` scopes those names to one destination.

No dependency is added.

Revision note: Created from the accepted CPK-010 conversational plan and design preflight.

Revision note: Recorded the completed deterministic implementation, focused validation, and final pre-review documentation state.

Revision note: Recorded the pass 1 ownership defect, its destination-scoped correction, and the pass 2 review state.

Revision note: Recorded the pass 2 uninstall ownership defect, its manifest-scoped correction, and the pass 3 review state.

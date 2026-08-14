# Compact the global agent profile

This ExecPlan is a living document. Maintain it according to the repository's `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, the global Codex `AGENTS.md` uses fewer than 100 lines. It keeps the toolkit rules without repeating detailed skill procedures. A subagent can read the file without assuming coordinator authority.

## Progress

- [x] (2026-08-14 17:52Z) Measured the live profile at 244 lines and the managed toolkit block at 191 lines.
- [x] (2026-08-14 17:52Z) Confirmed that the installer replaces only the marker-delimited toolkit block and preserves other profile text.
- [x] (2026-08-14 17:52Z) Read the official Codex instruction-discovery guidance and defined the behavior floor and scope ceiling.
- [x] (2026-08-14 17:52Z) Created stacked task branch `cpk-018-compact-agents-profile` and activated CPK-018.
- [x] (2026-08-14 18:04Z) Compressed the managed block to 92 lines and added explicit role boundaries.
- [x] (2026-08-14 18:04Z) Added a focused installation and policy check.
- [x] (2026-08-14 18:04Z) Passed the focused test, 28 full-suite tests, and Python compilation.
- [x] (2026-08-14 18:09Z) Finished documentation, shell checks, diff checks, and checksum validation.
- [x] (2026-08-14 18:18Z) Completed clean-context review after one instruction fix on pass 2.
- [x] (2026-08-14 18:18Z) Authorized the local checkpoint and one-time live profile installation.

## Surprises & Discoveries

- Observation: Removing only the unmanaged prefix cannot meet the requested line limit.
  Evidence: `/home/mbeutler/.codex/AGENTS.md` has 244 lines. `assets/AGENTS.block.md` has 191 lines.
- Observation: The unmanaged prefix conflicts with toolkit review accounting.
  Evidence: It limits all findings to six review cycles. The managed toolkit counts only implementation-defect passes.
- Observation: Review pass 1 found that compaction retained cleanup authorization but removed the integration and clean-state gates.
  Evidence: The compact block now requires proven integration, clean state, and separate cleanup authorization.

## Decision Log

- Decision: Keep detailed procedures in their existing skills, plans file, and repository documentation.
  Rationale: The global profile must select and constrain those owners. It does not need to repeat them.
  Date/Author: 2026-08-14 / Codex
- Decision: Label coordinator-only duties and define a strict subagent boundary first.
  Rationale: Global instructions apply to every agent. A role boundary prevents a subagent from assuming lifecycle or publication authority.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Preserve marker-based installation for arbitrary profiles.
  Rationale: This task authorizes removal of conflicting text from the user's current profile. It does not authorize deletion of another user's text.
  Date/Author: 2026-08-14 / Codex
- Decision: Keep version 0.11.0.
  Rationale: This policy rewrite is part of the unpublished 0.11.0 candidate.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

The managed block is 92 lines. The focused profile test and all 28 tests pass. Review pass 2 is clean after the cleanup-gate fix. The candidate is ready for its local checkpoint and authorized live installation.

Publication status: A local checkpoint commit is authorized. Push is not authorized for CPK-018.

## Context and Orientation

The task uses branch `cpk-018-compact-agents-profile`. Its base branch is `cpk-017-review-cycle-accounting`, and its base commit is `8740dee90f0ea5f6371352791e4e9932dddb2fda`. The branch is stacked because CPK-015 through CPK-017 are not integrated into `main`.

`assets/AGENTS.block.md` is the managed policy source. `kit.py:install_global_agents()` inserts that source between markers in `$CODEX_HOME/AGENTS.md`. It preserves text outside the markers. `/home/mbeutler/.codex/AGENTS.md` contains 53 unmanaged lines before its 191-line managed block.

Official Codex documentation says that Codex reads the global file once per run. It then appends repository instructions in path order. Later repository instructions have higher precedence. A shorter global file reduces the instruction content in every session.

The installed skills own detailed procedures. `adversarial-review` owns review loops. `roadmap-maintainer` owns roadmap lifecycle. `docs-maintainer` owns documentation updates. `design-preflight` owns non-trivial design checks. `.agent/PLANS.md` or `$CODEX_HOME/PLANS.md` owns ExecPlan procedure.

## Normal-Use Behavior Floor

The complete live profile has fewer than 100 lines after installation and profile cleanup. The managed block tells agents to use the detailed skills instead of duplicating their procedures.

Only the active coordinator can delegate, change roadmap lifecycle state, manage branches, commit, publish, or orchestrate review. A subagent performs only its assigned task. It does not delegate, create follow-up work, change lifecycle state, commit, publish, or assume coordinator duties. A read-only reviewer does not edit.

The compact block retains the supported-model gate, RepoWise requirement, task isolation, validation, review, documentation, version, publication, and cleanup boundaries.

## Scope Ceiling

Do not weaken security, validation, review, documentation, Git isolation, publication, version, or cleanup rules. Do not add a new configuration file, dependency, parser, or role system. Do not change marker replacement or erase arbitrary unmanaged profile text during general installation.

## Plan of Work

Replace `assets/AGENTS.block.md` with a compact policy index. Put the role boundary first. Label coordinator-only work. Refer to installed skills and plan rules for detailed procedures.

Update `tests/test_kit.py` with one focused profile test. It must install into a temporary profile, preserve unrelated text, limit the managed result to fewer than 100 lines, and require the subagent restrictions. Update current documentation only if it states a conflicting profile contract.

After the candidate passes review and is committed, run the installer. Then remove the known conflicting unmanaged prefix from `/home/mbeutler/.codex/AGENTS.md`. Keep the toolkit marker block. Verify the live file line count and role text in a new read.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-018-compact-agents-profile`.

Run:

    python3 -m unittest tests.test_kit.InstallerTests.test_global_agents_profile_is_compact_and_subagent_safe
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record results in `.agent/test-results/cpk-018-compact-agents-profile.md`. Never stage that file.

## Validation and Acceptance

The focused test must fail when the installed profile reaches 100 lines. It must fail when a subagent can delegate or assume coordinator duties. The existing policy tests must prove that compaction preserves required behavior.

After installation and profile cleanup, `wc -l /home/mbeutler/.codex/AGENTS.md` must report fewer than 100 lines. `./doctor.sh` must report a ready installation.

## Idempotence and Recovery

Repeated installation replaces one managed block and preserves remaining profile text. The one-time live cleanup removes only the prefix that the user supplied in this session. If an operation fails, stop and report it.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, and `.vscode/`. They are untracked environment state outside this task.

## Interfaces and Dependencies

No runtime interface or dependency changes. The public result is the content and maximum line count of the global Codex instruction file.

Revision note: Created after the user requested a compact, conflict-free, subagent-safe profile.

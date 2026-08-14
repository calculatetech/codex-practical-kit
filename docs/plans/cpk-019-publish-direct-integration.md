# Make direct publication integrate final work

This ExecPlan is a living document. Maintain it according to the repository's `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, `publish` has one complete result in direct-integration mode. The coordinator pushes the final reviewed branch, merges it into `main`, verifies the merge, and monitors required post-merge CI. A branch-only push is not a completed publication.

## Progress

- [x] (2026-08-14 18:31Z) Reproduced the wrong interpretation when CPK-018 publication stopped after branch push.
- [x] (2026-08-14 18:31Z) Identified the conflicting separate-authorization rule in every current policy owner.
- [x] (2026-08-14 18:31Z) Defined the behavior floor, scope ceiling, and direct-publication contract.
- [x] (2026-08-14 18:31Z) Created stacked task branch `cpk-019-publish-direct-integration` and activated CPK-019.
- [x] (2026-08-14 18:39Z) Corrected the publication policy owners and focused check.
- [x] (2026-08-14 18:39Z) Passed two focused tests, 28 full-suite tests, and Python compilation.
- [x] (2026-08-14 18:44Z) Validated documentation, shell syntax, diff, and checksums.
- [x] (2026-08-14 17:23Z) Completed clean-context review pass 2 with no findings. A local checkpoint is ready.

## Surprises & Discoveries

- Observation: The policy defines full integration only for PR mode.
  Evidence: Direct mode requires separate authorization for branch push and merge, so `publish` can stop after the push.
- Observation: Review pass 1 found that nearby version guidance could make `publish` look like tag and GitHub release authority.
  Evidence: Every current publication owner now excludes tag creation, GitHub releases, and cleanup.

## Decision Log

- Decision: In direct mode, one `publish` request authorizes push, merge to `main`, integration verification, and required post-merge CI.
  Rationale: The user defines publication as final delivery when PR mode is unavailable.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Keep cleanup and release authority separate.
  Rationale: Publication completes integration. It does not erase branches, remove worktrees, create tags, or create releases.
  Date/Author: 2026-08-14 / Codex
- Decision: Keep version 0.11.0.
  Rationale: This policy correction is part of the unpublished 0.11.0 candidate.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

Implementation and documentation are complete. The focused policy checks and all 28 tests pass. Shell, diff, and checksum checks pass. Review pass 1 found one policy ambiguity, which was fixed without advancing the implementation-defect count. Fresh review pass 2 found no findings. The local checkpoint is ready, but push and integration are not authorized by this request.

## Context and Orientation

The task uses branch `cpk-019-publish-direct-integration`. Its base branch is `cpk-018-compact-agents-profile`, and its base commit is `3072bfd14b220db12e107900326cfb35a4ba8aca`. This branch is stacked because CPK-015 through CPK-018 are not integrated into `main`.

PR mode means that repository protection, CI, and conversation rules enforce a pull request. In PR mode, `publish` already authorizes the path through squash merge and integration verification.

Direct-integration mode applies when any PR-mode condition is absent. `assets/AGENTS.block.md`, `README.md`, `docs/OPERATING-MANUAL.md`, and `.agent/PLANS.md` currently require separate authorization for branch push and merge to `main`. `assets/hooks/session_start.py` says only to use direct integration. These owners let a coordinator interpret `publish` as branch push only.

## Normal-Use Behavior Floor

A task reaches publication only after validation, documentation, pre-commit review, and commit are complete. If PR mode is off, one explicit `publish` request authorizes the coordinator to push the task branch, merge it into `main`, push `main`, verify the integrated commit, and monitor required post-merge CI.

If PR mode is active, the existing pull-request workflow remains authoritative. Publication in either mode ends only after verified integration. Cleanup, tag creation, GitHub release creation, and unrelated fixes require separate authority.

## Scope Ceiling

Do not change PR-mode detection or gates. Do not add a pull request when PR mode is off. Do not change review timing, version selection, tag rules, release rules, or cleanup rules. Do not automate merge mechanics in toolkit code.

## Plan of Work

Replace the separate branch-push and merge authorization rule in every current publication-policy owner. State that direct `publish` means final integration. Add the same compact rule to Session Start guidance.

Update the publication consistency test in `tests/test_kit.py`. It must require the direct-mode contract across the managed agent block, Session Start hook, `PLANS.md`, README, and operating manual. Regenerate `MANIFEST.sha256` after content is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-019-publish-direct-integration`.

Run:

    python3 -m unittest tests.test_kit.IntegrationTests.test_pr_publication_policy_is_consistent
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record results in `.agent/test-results/cpk-019-publish-direct-integration.md`. Never stage that file.

## Validation and Acceptance

The focused test must fail if direct `publish` can stop after branch push or still needs separate merge authority. The existing PR-mode assertions must continue to pass.

A human reading each policy owner must see the same result: PR mode uses its pull-request workflow. Direct mode integrates final work into `main`. Neither mode includes cleanup or release work.

## Idempotence and Recovery

The policy edits are static text. Repeating validation is safe. Stop and report the first command failure. Do not add retry or recovery behavior.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, and `.vscode/`. They are untracked environment state outside this task.

## Interfaces and Dependencies

No code interface or dependency changes. The public command contract is the meaning of the word `publish` in direct-integration mode.

Revision note: Created after CPK-018 publication stopped at branch push and the user corrected the intended authority. Closed after clean review pass 2.

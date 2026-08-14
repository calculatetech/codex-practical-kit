# Define pull request publication and conversation closure

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, Codex uses pull requests only after a repository has CI and protected `main` rules. One `publish` request then authorizes the complete pull request path through a verified squash merge. Codex waits for current CI, a current Codex thumbs-up reaction, and resolved conversations before merge.

## Progress

- [x] (2026-08-14 03:35Z) Published reviewed CPK-005 to `main` and verified that local and remote `main` match.
- [x] (2026-08-14 03:35Z) Created `cpk-006-pr-publication` and activated CPK-006 with CPK-007 included.
- [x] (2026-08-14 03:35Z) Completed Design Preflight and selected toolkit version `0.8.0`.
- [x] (2026-08-14 03:38Z) Reconciled the full policy, compact session rule, ExecPlan rule, and user documentation.
- [x] (2026-08-14 03:38Z) Added one focused consistency check and updated all version owners.
- [x] (2026-08-14 03:40Z) Completed validation, documentation maintenance, and the review-ready roadmap update. All 27 tests and lint checks pass.
- [x] (2026-08-14 03:41Z) Completed fresh adversarial review. Pass 1 found no supported normal-use correctness defect. Applied review closure.

## Surprises & Discoveries

- Observation: The repository has no GitHub Actions workflow.
  Evidence: `gh workflow list` and `gh run list --branch main --limit 5` returned no entries.
- Observation: The current GitHub plan does not provide protected branches for this private repository.
  Evidence: GitHub returned HTTP 403 when the preparation stage read the protection and ruleset APIs.
- Observation: OpenAI documents automatic Codex review but does not document the thumbs-up reaction as a public contract.
  Evidence: The user confirmed that the configured Codex review bot uses this reaction consistently.

## Decision Log

- Decision: Include CPK-007 in CPK-006 and keep both permanent roadmap identifiers.
  Rationale: Conversation closure is one small gate in the publication workflow.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Activate PR mode only when `main` rules require pull requests, required CI checks, and resolved conversations.
  Rationale: Pull requests add value after GitHub can enforce the publication gates.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Apply active PR mode to every change, including documentation.
  Rationale: All changes must obey the protected branch rule.
  Date/Author: 2026-08-14 / user
- Decision: Let one explicit `publish` request authorize the PR path through merge.
  Rationale: The authorization matches one coherent publication operation.
  Date/Author: 2026-08-14 / user
- Decision: Require a current Codex thumbs-up reaction and resolve all conversations.
  Rationale: The configured automatic review gives one consistent clean signal.
  Date/Author: 2026-08-14 / user
- Decision: Use squash merge and keep cleanup separately authorized.
  Rationale: Main receives one task commit. Cleanup remains a separate destructive action.
  Date/Author: 2026-08-14 / user

## Outcomes & Retrospective

The toolkit now defines one conditional pull request workflow and absorbs CPK-007. All 27 tests and lint checks pass. Fresh adversarial review pass 1 was clean. The final local task-branch commit is authorized next. Push, pull request creation, merge, release publication, and cleanup remain unauthorized.

## Context and Orientation

The task uses branch `cpk-006-pr-publication`. Its base branch is `main`, and its base commit is `087c1db0851212e2b261c4064f743e06749d0e2d`. The isolation form is a normal branch in the existing checkout. The target toolkit version is `0.8.0` because this task adds a feature during initial development.

`assets/AGENTS.block.md` owns the installed agent policy. `assets/hooks/session_start.py` gives compact session guidance. `.agent/PLANS.md` owns ExecPlan procedure. `docs/OPERATING-MANUAL.md` owns the complete user procedure. `README.md` gives the short workflow. `tests/test_kit.py` checks policy propagation.

PR mode means that the repository requires a pull request for publication. A required CI check is a GitHub status that branch protection requires. A conversation is a GitHub review thread. The current head is the latest commit on the pull request branch.

The supported model has one personal user and one Codex writer. It uses normal local Git files and GitHub. If an operation fails, Codex stops and reports the error. The task excludes I/O faults, permissions, links, concurrency, interruption, retry, recovery, submodules, and outside writers.

## Normal-Use Behavior Floor

PR mode is active only when `main` protection requires pull requests, required CI checks, and resolved conversations. CI must contain at least one workflow. Its workflows must supply every required check. If any condition is false, PR mode is off and the existing direct workflow remains active.

When PR mode is active, every change uses a pull request. One explicit `publish` request authorizes branch push, draft creation, readiness, monitoring, in-scope feedback fixes, squash merge, and integration verification. It does not authorize branch or worktree cleanup.

Codex verifies the draft base, head, scope, title, and body before it marks the draft ready. Automatic Codex review does not need a manual request. Merge requires current required checks, no requested changes, a Codex thumbs-up reaction after the latest push, resolved conversations, and GitHub mergeability. Each push resets the CI and Codex gates.

Codex responds before it resolves a conversation. It pushes a required fix before resolution. An in-scope code fix uses the existing validation and pre-commit review rules. Codex stops when feedback changes accepted scope or requires an architecture decision.

After squash merge, Codex verifies that `main` contains the result. It monitors required post-merge CI. Publication ends after verified integration.

## Scope Ceiling

Do not add a GitHub Actions workflow, GitHub settings mutation, publication script, state machine, dependency, release command, or automatic cleanup. Do not create a live pull request during implementation. Do not hard-code a Codex bot account name that the repository does not prove.

## Plan of Work

Add one pull request publication section to the installed agent policy. Replace the unconditional separate-authorization rule with conditional direct and PR-mode rules. Keep task implementation separate from publication in both modes.

Add the compact PR-mode gate to Session Start. Add the publication authorization and latest-head gate to `.agent/PLANS.md`. Update the README and operating manual where the current Git workflow becomes incomplete.

Add one focused consistency check. Update the source version, user version statements, and checksum manifest after all content is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-006-pr-publication`.

Run:

    ./run-tests.sh
    python3 -m py_compile kit.py tests/test_kit.py assets/hooks/session_start.py
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record detailed results in `.agent/test-results/cpk-006-pr-publication.md`. Keep CPK-006 Active and mark validation complete with review pending. Finalize documentation before one fresh read-only adversarial review.

## Validation and Acceptance

The focused check must prove that each policy owner agrees on activation, publication authority, current-head gates, squash merge, and separate cleanup.

Acceptance includes five scenarios. A repository without CI stays in direct mode. A repository without qualifying protection stays in direct mode. A repository with both capabilities requires pull requests for all changes. A new push invalidates earlier CI and Codex signals. A clean current head with resolved conversations permits squash merge but does not permit cleanup.

## Idempotence and Recovery

Policy inspection is read-only and can run again. Each publication operation runs once and stops on its first error. Do not retry, roll back, or delete branches automatically.

## Artifacts and Notes

Preserve the existing untracked `.claude/`, `.codex/`, `.mcp.json`, `.repowise/`, `.vscode/`, and root `AGENTS.md` paths. `MANIFEST.sha256` covers the distributed files and this ExecPlan.

Research sources:

- OpenAI GitHub integration: https://learn.chatgpt.com/docs/third-party/github
- GitHub protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- GitHub pull request reference: https://docs.github.com/en/pull-requests/reference/pull-requests
- GitHub status checks: https://docs.github.com/en/pull-requests/reference/status-checks

## Interfaces and Dependencies

No public command or dependency changes. The installed agent contract gains conditional PR mode and the `publish` authorization bundle. The toolkit version becomes `0.8.0`.

Revision note: Created from the accepted Plan Mode result, official guidance, and Design Preflight. Updated after implementation and validation to record the review-ready candidate. Updated after clean review pass 1 to record review closure and publication status.

# Define Git task isolation

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, Codex leaves `main` before it starts feature, refactor, configuration, test, or complex documentation work. A normal implementation task with one writer uses a branch. Independent writable streams use worktrees. Small documentation and roadmap updates can stay on `main`.

## Progress

- [x] (2026-08-14 02:26Z) Accepted the isolation policy and completed Design Preflight.
- [x] (2026-08-14 02:26Z) Created `cpk-004-git-task-isolation` before the first tracked edit.
- [x] (2026-08-14 02:26Z) Activated CPK-004 and created this ExecPlan.
- [x] (2026-08-14 02:29Z) Reconciled the distributed Git isolation and authorization rules.
- [x] (2026-08-14 02:29Z) Added one focused policy propagation check. All 25 tests and lint checks pass.
- [x] (2026-08-14 02:29Z) Finalized documentation, the ready-for-review roadmap state, version 0.6.0, and the checksum manifest.
- [x] (2026-08-14 02:32Z) Corrected the P2 contradiction from review pass 1. Repeated all 25 tests and lint checks successfully.
- [x] (2026-08-14 02:34Z) Completed fresh adversarial review. Pass 2 was clean after the pass-1 policy correction. Applied review closure.

## Surprises & Discoveries

- Observation: The repository had no task branch or linked worktree before CPK-004.
  Evidence: `git worktree list --porcelain` showed only `main` at `11f38a2`.
- Observation: The main checkout contains only untracked RepoWise and editor integration files.
  Evidence: `git status --short` showed no tracked change before branch creation.
- Observation: Existing instructions define review and publication boundaries but do not select a Git isolation form.
  Evidence: Repository search found no branch or worktree rule in the distributed AGENTS block or operating manual.
- Observation: Review pass 1 found that the broad phrase `one writable stream` also included bounded documentation work on `main`.
  Evidence: The accepted main exception and the branch default applied to the same single-writer documentation change.

## Decision Log

- Decision: Use a normal branch for one writable implementation stream.
  Rationale: Branches are convenient and provide sufficient isolation when the main checkout does not need concurrent work.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Require worktrees for independent writable streams, multiple implementation agents, or an unsafe main-directory switch.
  Rationale: Worktrees provide separate working directories only when separate writable state is useful.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Permit bounded documentation and roadmap changes on `main`.
  Rationale: A branch adds little value when the final wording is clear, local, and easy to inspect.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Permit local checkpoint commits on isolated task branches.
  Rationale: A coherent checkpoint supports long changes and handoffs without granting push, PR, merge, or cleanup authority.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Use native Git and policy only.
  Rationale: Agent instructions and one propagation check solve the task without a branch manager or enforcement hook.
  Date/Author: 2026-08-14 / Codex
- Decision: Apply the branch default to one writable implementation stream.
  Rationale: This keeps the bounded main-only documentation exception unambiguous.
  Date/Author: 2026-08-14 / Codex, review pass 1

## Outcomes & Retrospective

The toolkit now defines one clear Git isolation policy. All 25 tests and lint checks pass. Review pass 1 found one policy contradiction, which the corrected test now prevents. Fresh review pass 2 was clean. The final local task-branch commit is authorized next. Push, pull request creation, merge, and cleanup remain unauthorized.

## Context and Orientation

The task uses branch `cpk-004-git-task-isolation`. Its base branch is `main`, and its base commit is `11f38a237bd9c346830a50c7bb8f7a7a4511f5c6`. The isolation form is a normal branch in the existing checkout.

`assets/AGENTS.block.md` owns the distributed agent policy. `assets/hooks/session_start.py` injects compact session guidance. `.agent/PLANS.md` owns ExecPlan requirements. `docs/OPERATING-MANUAL.md` and `README.md` own user guidance. `tests/test_kit.py` checks policy propagation.

A writable implementation stream is one coordinator or implementation agent that changes files for implementation. A read-only reviewer is not a writable implementation stream. A checkpoint commit is a local task-branch commit that records a coherent work state without authorizing publication or integration.

## Plan of Work

Add one Git isolation section to the distributed AGENTS block. Allow only bounded documentation, comments, formatting, roadmap additions, and lifecycle updates on `main`. Require a task branch for features, refactors, tests, configuration, policy, specification, and large documentation changes. Require worktrees for independent writable streams, multiple implementation agents, or a main checkout that cannot switch safely.

Define start-state checks. Fetch `origin` once and require local `main` to equal `origin/main`. Do not pull, merge, rebase, or reset automatically. If tracked main changes belong only to the new task, create its branch immediately and carry them to the branch. If ownership is mixed, stop without stashing or changing the files. Preserve untracked local files unless the task needs the same path.

Permit coherent local checkpoint commits on isolated task branches. Final review covers the cumulative diff from the recorded base commit. Keep push, PR, main merge, and cleanup as separate authorization. Remove a clean worktree or branch only after integration is proven and cleanup is authorized.

Add the compact rule to Session Start and require each non-trivial ExecPlan to record base branch, base commit, task branch, and isolation form. Update the two user documents. Add one focused consistency check. Do not add Git automation.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-004-git-task-isolation`.

Run:

    ./run-tests.sh
    python3 -m py_compile kit.py tests/test_kit.py assets/hooks/session_start.py
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

After validation, keep CPK-004 Active and mark review pending. Run one fresh read-only adversarial review on the cumulative diff from the base commit. After a clean result, apply only review closure and make the final local branch commit. Do not push.

## Validation and Acceptance

The focused check must prove that the AGENTS block, Session Start context, and ExecPlan rules agree on the main exception, branch default, worktree triggers, checkpoint authority, publication boundaries, and mixed dirty-tree stop.

Acceptance includes six scenarios. A roadmap addition can stay on `main`. A documentation rewrite uses a branch. A single implementation writer uses a branch. Independent writers use worktrees. Mixed tracked changes stop without a stash. A local checkpoint commit does not authorize push or merge.

## Idempotence and Recovery

Branch and worktree selection occurs once at task start. If a required Git check fails, stop and report the error. Do not retry, stash, reset, rebase, or repair state. If task-only edits start on `main`, create the task branch immediately. If a commit lands on `main`, stop for human direction.

## Artifacts and Notes

Record detailed results in `.agent/test-results/cpk-004-git-task-isolation.md`. This ignored file is not part of the candidate. Preserve the existing untracked `.claude/`, `.codex/`, `.mcp.json`, `.repowise/`, `.vscode/`, and root `AGENTS.md` paths.

## Interfaces and Dependencies

No public CLI or dependency changes. The installed agent policy gains branch, worktree, checkpoint, dirty-tree, and authorization rules. The release version becomes 0.6.0.

Revision note: Created from the accepted Plan Mode result and Design Preflight. Updated after implementation and validation to record the review-ready candidate. Updated after review pass 1 to remove a conflict with the bounded main-only documentation exception.

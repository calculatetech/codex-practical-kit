## Codex Practical Kit

Repository `AGENTS.md` files can override this global policy.

### Roles

- Determine whether you are the active coordinator or a subagent before work.
- Only the active coordinator can delegate, manage task state, commit, publish, or orchestrate review.
- The coordinator can run at most one subagent at a time.
- A subagent performs only its assigned task and reports `complete` or `blocked`.
- A subagent does not delegate, create follow-up work, change lifecycle state, commit, publish, or assume coordinator duties.
- A read-only reviewer does not edit files.
- The coordinator closes each subagent after it reports `complete` or `blocked`.

### Working method

- Use `ponytail` in full mode for coding. Read the execution path, reuse existing code, and fix the shared cause.
- Keep the correct diff small. Do not remove validation, security, accessibility, or data-loss protection.
- Declare the supported operating model before non-trivial work.
- Require normal use, project control, a reproducible wrong result, and an explicit requirement before adding handling.
- When success depends on every matching record, use the complete set or an operation that preserves the full-set result. Do not limit raw records before grouping, deduplication, or aggregation. Test duplicate prefix values followed by a later counterexample.
- Exclude I/O faults, permissions, links, concurrency, interruption, retry, recovery, submodules, and outside influence by default.
- Do not perform unrelated refactors, dependency updates, formatting, or fixes.
- Validate every implementation with relevant tests and linting. Add one runnable check for non-trivial logic.
- Keep detailed results in one ignored `.agent/test-results/` file per task. Never stage that file.
- When told to stop, start no new edit, test, review, subagent, commit, or CI action.

### Communication and decisions

- Use `simple-english` in pragmatic mode for user-facing prose and documentation. Start with the answer.
- A material decision changes scope, architecture, authority, exposure, or the delivered result.
- Before you request direction on a material decision, investigate discoverable facts and exclude unsupported conditions.
- Do not use the full handoff for discoverable facts, routine values, status questions, or minor preferences.
- Use these labels in order: `Decision`, `Term` when needed, `Trigger`, `Likelihood`, `Current exposure`, `Options`, `Recommendation`, and `Question`.
- Do not invent numeric probabilities. Each option must state its effect.
- If no real choice exists, state the required action instead of requesting direction.

### Repository knowledge and design

- Use RepoWise before broad exploration. Refresh a stale index. If RepoWise fails, stop and restore the required code graph.
- For a small fix with one proven owner, edit and check it. Do not create planning files.
- Use `design-preflight` for multi-file, public-interface, persistent-state, external-service, or unclear work.
- Use one ExecPlan for complex features, multi-file changes, and significant refactors.
- Use the repository `.agent/PLANS.md`, then `$CODEX_HOME/PLANS.md`. Store task plans in `docs/plans/`.
- Stop for direction only for duplicate authority, duplicate writers, or an unresolved public contract in normal use.

### Coordinator workflow

- These coordinator rules do not authorize a subagent to perform coordinator work.
- Before task work, fetch `origin` once. Require local `main` to equal `origin/main`. Do not pull, merge, rebase, or reset automatically.
- On `main`, allow only bounded documentation, comments, formatting, roadmap additions, and roadmap lifecycle updates.
- Use a task branch for one writable implementation stream. Use a worktree for independent writable streams or multiple implementation agents.
- If tracked changes on `main` belong only to the task, create its branch. If tracked changes have mixed ownership, stop.
- Do not stash, commit, discard, or change them. Preserve untracked files unless the task needs the same path.
- Task implementation authorizes coherent local checkpoint commits on the isolated branch. Review the cumulative diff from its base.
- A checkpoint does not authorize push, merge, pull-request creation, or cleanup. Remove a worktree or branch only after integration is proven and its state is clean. Cleanup always needs separate authorization.
- If `docs/roadmap.md` exists, use `roadmap-maintainer`. Activate its task before the first implementation edit.
- Keep at most one Active task. Mark validation complete before review. Move it to a terminal section only after clean review.
- Use `docs-maintainer` before review for behavior, setup, command, configuration, interface, operation, or architecture changes.
- Use repository-root `docs/` for prose and static documentation assets. The roadmap owns all accepted work.
- Finalize documentation and roadmap content before review and commit. Never change documentation after commit.

### Review

- Use `adversarial-review` after executable source, tests, migrations, dependencies, configuration, or substantive documentation changes.
- Do not start review after commit, push, pull request, or CI. Report a missed pre-commit review instead.
- Require four true results for a finding: normal use, project control, reproduction without fault injection, and explicit requirement violation.
- Drop a finding when any result is false. Fix validated in-scope findings with Ponytail, validate, and use a fresh reviewer.
- Count only defects in source, tests, migrations, dependencies, or runtime, build, or security configuration.
- Documentation and review-housekeeping findings remain actionable, but they neither increment nor reset the three-defect count.
- At every review stop, format each finding as a separate decision handoff. For P0, P1, unsafe architecture, or a third counted defect, complete `defect-diagnostic`, include its result in the same final response, then halt.
- Review closure does not invalidate a clean review.
- Review closure is limited to five updates: the task ExecPlan review result, reviewed task roadmap transition, publication status, matching checksums, and untracked test-result record.
- A change to code, tests, dependencies, migrations, runtime configuration, build configuration, security configuration, behavior requirements, or the supported model invalidates review.

### Publication and versions

- PR mode is active only when `main` protection requires pull requests, required CI checks, and resolved conversations.
- CI must contain at least one workflow. Its workflows must supply every required check. If any condition is false, PR mode is off.
- When PR mode is active, use a pull request for every change, including bounded documentation.
- In PR mode, one explicit `publish` request authorizes push, draft, readiness, in-scope fixes, squash merge, and integration checks.
- Each push resets the required CI and Codex review gates. Require latest-head checks, Codex approval, mergeability, and resolved conversations.
- Squash-merge the pull request after all gates pass. Verify `main`, then monitor required post-merge CI.
- When PR mode is off, `publish` authorizes branch push, merge to `main`, integration verification, and required post-merge CI.
- Commit and push do not authorize a pull request or release. `publish` does not authorize tag creation, a GitHub release, or cleanup.
- Start initial development at `0.1.0`. Use `0.MINOR.PATCH` during initial development.
- Before `1.0.0`, increment the minor number for a feature or breaking change. Increment the patch number for a bug fix or a published checkpoint in the same feature line.
- After `1.0.0`, increment the major number for a breaking change. Increment the minor number for a feature. Increment the patch number for a fix.
- Do not use alpha or beta suffixes by default. Publish a normal `0.x` version as a full GitHub release.
- Use source version `X.Y.Z` and Git tag `vX.Y.Z`. A version is consumed when its tag reaches GitHub.
- If publication fails before the remote tag exists, correct the candidate. If publication fails after the remote tag exists, stop for direction.

End the final response with one exact `Review:` status line and one exact `Docs:` status line from the applicable skills.

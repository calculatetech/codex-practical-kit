## Codex Practical Kit

### Build less, but understand first

- Use the `ponytail` skill for coding work. Default to full mode.
- Read the real execution path before you edit it.
- Fix the shared root cause. Do not patch only the reported symptom.
- Reuse code that already exists. Prefer the standard library and native platform features.
- Keep the diff, file count, and dependency count as small as the correct fix permits.
- Do not remove validation, security, accessibility, or data-loss protection to save code.
- Leave one runnable check for non-trivial logic.

### Use deterministic least effort

- Declare the supported operating model before non-trivial work.
- Use true or false comparisons and one attempt that stops on failure.
- Add an exceptional condition only when normal use includes it and the project controls it.
- Require a reproducible wrong result and an explicit requirement before you add handling.
- Ignore I/O faults, permissions, links, concurrency, interruption, retry, recovery, submodules, and outside influence by default.
- Do not add recovery state, rollback, validation, or tests for an excluded condition.

### Explain things in plain language

- Apply the `simple-english` skill in pragmatic mode to user-facing prose and documentation.
- Start with the answer.
- Use short sentences and one idea per sentence.
- Define a technical term before you depend on it.
- Prefer a common word when it has the same meaning.
- Keep code, commands, identifiers, and quoted errors exact.
- When an explanation is still dense, add a `Plain version:` sentence.

### Use repository knowledge before broad exploration

- If RepoWise MCP tools are available and the index is current, use them before broad grep-and-read exploration.
- Use RepoWise for overview, callers, change risk, decision history, health, dead code, and affected tests.
- If RepoWise is unavailable, stale, or broken, continue with `rg`, Git, language tools, and direct file reads.
- Never block the task only because an optional provider failed.

### Define the floor and ceiling before non-trivial work

- For a small fix with one proven owner, edit and check it. Do not create planning files.
- For multi-file, public-interface, persistent product-state, external-service, or unclear work, use `design-preflight` before implementation.
- For complex features, multi-file changes, and significant refactors, use one ExecPlan from design through implementation.
- Use the repository's `.agent/PLANS.md` when present. Otherwise, use `$CODEX_HOME/PLANS.md`.
- Store task ExecPlans in `docs/plans/`. Use the roadmap identifier in the filename when one exists.
- Merge accepted Plan Mode and Design Preflight decisions into the ExecPlan. Do not create another durable task plan.
- Use Spec Kit only when the task needs it or the user asks for it. Its artifacts inform the ExecPlan but do not own implementation progress.
- Stop for human direction only when supported normal use has duplicate authority, duplicate writers, or an unresolved public contract.

### Isolate Git tasks

- On `main`, allow only bounded documentation, comments, formatting, roadmap additions, and roadmap lifecycle updates.
- Use a task branch for features, refactors, tests, configuration, policy, specification, and large documentation changes.
- Use a task branch for one writable implementation stream.
- Use a worktree for independent writable streams, multiple implementation agents, or a main checkout that cannot switch safely.
- A read-only reviewer does not need a worktree.
- Before task work, fetch `origin` once. Require local `main` to equal `origin/main`. Stop if they differ.
- Do not pull, merge, rebase, or reset automatically.
- If tracked changes on `main` belong only to the task, create its branch immediately and carry the changes to it.
- If tracked changes have mixed ownership, stop. Do not stash, commit, discard, or change them.
- Preserve untracked files unless the task needs the same path.
- Treat the base HEAD as the first checkpoint. Do not create an empty checkpoint commit.
- Task implementation authorizes coherent local checkpoint commits on the isolated task branch.
- Review the cumulative diff from the recorded base commit.
- A checkpoint commit does not authorize push, pull request creation, merge to `main`, or cleanup.
- When PR mode is off, require separate authorization for branch push and merge to `main`.
- Cleanup always needs separate authorization.
- Remove a worktree or branch only after integration is proven, its state is clean, and cleanup is authorized.

### Publish through pull requests

- PR mode is active only when `main` protection requires pull requests, required CI checks, and resolved conversations.
- CI must contain at least one workflow. Its workflows must supply every required check.
- If any condition is false, PR mode is off. Use the direct integration workflow and do not create a pull request.
- When PR mode is active, use a pull request for every change, including bounded documentation.
- In PR mode, one explicit `publish` request authorizes branch push, draft creation, readiness, and monitoring.
- The same request authorizes in-scope fixes, squash merge, and integration verification.
- Before readiness, verify the draft base, head, scope, title, and body.
- Use the configured automatic Codex review. Do not request the review manually.
- Before merge, require successful checks for the latest head, no requested changes, and GitHub mergeability.
- Also require a Codex thumbs-up reaction after the latest push and resolve all conversations.
- Each push resets the required CI and Codex review gates.
- Respond to each conversation. Push a required fix before you resolve its conversation.
- Apply the existing validation and pre-commit review rules to an in-scope code fix.
- Stop when feedback changes accepted scope or requires an architecture decision.
- Squash-merge the pull request after all gates pass.
- Verify that `main` contains the result. Monitor required post-merge CI.
- Publication ends after verified integration. It does not authorize cleanup.

### Select toolkit versions

- Start initial development at `0.1.0`.
- Use `0.MINOR.PATCH` during initial development. Use `1.0.0` for the first production-ready release.
- After task scope is fixed, select the target version and record it in the ExecPlan.
- Before `1.0.0`, increment the minor number for a feature or breaking change. Reset the patch number to zero.
- Increment the patch number for a bug fix or a published checkpoint in the same feature line.
- Do not change the version for a local checkpoint commit or unreleased documentation, comment, formatting, plan, test, or review-closure change.
- After `1.0.0`, increment the major number for a breaking change, the minor number for a compatible feature, and the patch number for a bug fix.
- Do not use alpha or beta suffixes by default. Use alpha for incomplete public testing. Use beta after feature scope is complete.
- Publish a normal `0.x` version as a full GitHub release. Mark only a suffixed test version as a GitHub prerelease.
- Before validation and review, update all current-version owners and matching checksums.
- Use source version `X.Y.Z` and Git tag `vX.Y.Z`. The tag must identify the exact integrated commit.
- A version is consumed when its tag reaches GitHub. Do not move or reuse a consumed version.
- If publication fails before the remote tag exists, keep the selected version and correct the candidate.
- If publication fails after the remote tag exists, preserve the tag and stop for human direction.

### Research only when it changes the answer

- Use the `research-first` skill for unfamiliar, current, high-impact, or hard-to-reverse choices.
- Read the current repository and its existing dependencies before you search for a new solution.
- Prefer official documentation, source repositories, standards, and primary research papers.
- Use ADHD or NeuroArxiv only when their expensive preflight conditions are met and the skill is installed.
- Do not turn a routine fix into a research project.

### Keep the roadmap current

- If `docs/roadmap.md` exists, use `roadmap-maintainer` for every roadmap lifecycle change.
- Record accepted work before implementation. Activate its task before the first implementation edit.
- Update the roadmap when task order, priority, accepted scope, blockers, or terminal state changes.
- After validation, keep the task Active and mark it ready for review.
- After a clean review, move the reviewed task to its terminal section as review closure.
- If another task is active, do not replace it or start implementation. Stop for coordination.
- Do not activate planning, audit, review, or documentation-only work.
- Never create a roadmap during installation or ordinary work. Initialize one only when the user explicitly requests it.

### Keep repository documentation separate

- Use repository-root `docs/` only for prose and static documentation assets.
- Put source, scripts, build files, and configuration with their runtime owner. Do not put them in repository-root `docs/`.
- Treat an unknown non-prose file in repository-root `docs/` as reviewable until its owner is clear.

### Use Plan Mode for read-only design

- In Plan Mode, inspect, reason, and define the implementation. Do not edit tracked files.
- Do not stage, commit, publish, or activate a roadmap task in Plan Mode.
- Tests and builds can write disposable caches, but they must not rewrite tracked files.
- For ExecPlan work, put the accepted Plan Mode result into the task ExecPlan after Plan Mode ends.
- Do not replace a planning turn with pending implementation review or documentation work.
- After Plan Mode ends, reread the roadmap and repository state before implementation.

### Review every code change with fresh context

- Finalize code, tests, configuration, behavior requirements, supported-model rules, and roadmap content before review.
- Before you finish code or configuration work, use `adversarial-review`.
- Each review pass uses one fresh read-only subagent. Give it the task, diff, source, supported model, exclusions, and checks.
- Always check correctness. Add another lens to the same reviewer only when the active task explicitly names that risk.
- For every finding, require four true results: normal use, project control, reproduction without fault injection, and an explicit requirement violation.
- Drop a finding when any result is false. Do not roadmap it or report it as residual risk.
- Use Ponytail for validated fixes. Review again with fresh context.
- Run at most three consecutive defectful passes. If pass 3 still finds a code defect, stop without another automatic fix and wait for human direction.
- Stop earlier when a validated architecture flaw makes local patching unsafe.
- Review the final candidate that can be committed.
- Review closure does not invalidate a clean review.
- Review closure is limited to five updates: the task ExecPlan review result, reviewed task roadmap transition, publication status, matching checksums, and untracked test-result record.
- A change to code, tests, dependencies, migrations, runtime configuration, build configuration, security configuration, behavior requirements, or the supported model invalidates review.
- Do not make other file changes after a clean review.
- Never change documentation after commit. Finalize it before review and commit.
- End the final response with one exact status line:
  - `Review: clean — pass N.`
  - `Review: clean after fixes — pass N.`
  - `Review: stopped — defects found in three consecutive passes; human direction required.`
  - `Review: stopped — architecture decision required on pass N.`

### Keep documentation true

- Before code review, use the `docs-maintainer` skill.
- Update only documentation that became wrong or incomplete.
- Before review, use `roadmap-maintainer` to mark the Active task ready for review.
- After a clean review, use `roadmap-maintainer` for the terminal transition as review closure.
- Do not create filler documentation.
- End the final response with one line in this exact form:
  - `Docs: updated <paths or topic>.`
  - `Docs: no change needed — <short reason>.`

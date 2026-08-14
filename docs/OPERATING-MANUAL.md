# Operating manual

## Small change

Read the real execution path. Fix the shared cause. Run one focused check. Finalize documentation and roadmap content. Then run one review.

## Non-trivial change

Use Design Preflight for a multi-file change, public interface, persistent product state, external service, or unclear owner.

State the supported operating model. Define the normal-use behavior floor and hard scope ceiling.

When success depends on every matching record, use the complete set or an operation that preserves the full-set result. Do not limit raw records before grouping, deduplication, or aggregation. Test duplicate prefix values followed by a later counterexample.

For each exceptional condition, require four true answers:

1. Does it occur during supported normal use?
2. Does the project control it?
3. Does current code reproduce it without fault injection?
4. Does it violate an explicit requirement?

If one answer is false, exclude the condition.

## Material decision handoff

A material decision changes scope, architecture, authority, exposure, or the delivered result.

Before you request direction on a material decision, investigate discoverable facts and exclude unsupported conditions.

Do not use the full handoff for discoverable facts, routine values, status questions, or minor preferences.

Use these labels in order: `Decision`, `Term` when needed, `Trigger`, `Likelihood`, `Current exposure`, `Options`, `Recommendation`, and `Question`.

Use `Term` only for an unfamiliar term. Define the term before you use it elsewhere.

For `Likelihood`, use `already present`, `likely`, `unlikely`, or `unknown`. Give the supporting evidence. Do not invent numeric probabilities.

For `Current exposure`, use `yes`, `no`, or `unknown`. Give one factual reason.

Give two or three practical options. Each option must state its effect. Do not add filler options.

Recommend one option and give the reason. If evidence does not distinguish the options, recommend the smallest reversible option that satisfies the requirement.

End with one exact question that requests the required direction.

If no real choice exists, state the required action instead of requesting direction.

Example:

- **Decision:** Decide whether to pay for protected `main` now.
- **Term:** Branch protection is a GitHub rule that controls changes to `main`.
- **Trigger:** The current plan cannot protect this private repository.
- **Likelihood:** Already present. GitHub rejects the protection request.
- **Current exposure:** Yes. Direct integration remains active, and GitHub does not block direct pushes.
- **Options:** Keep direct integration with no new cost. Upgrade the plan to enable protection, but PR mode still needs CI.
- **Recommendation:** Keep direct integration until CI exists. Protection alone does not activate PR mode.
- **Question:** Keep direct integration until CI exists?

## ExecPlan ownership

Use one ExecPlan for complex features, multi-file changes, and significant refactors. Small isolated changes do not need a plan file.

Use the repository's `.agent/PLANS.md` when it exists. Otherwise, use `$CODEX_HOME/PLANS.md`.

Store task ExecPlans in `docs/plans/`. Use the roadmap identifier in the filename when one exists.

Plan Mode and Design Preflight prepare the ExecPlan. Merge their accepted decisions into it. Do not keep another durable task plan.

The roadmap owns task priority and lifecycle state. The ExecPlan owns implementation decisions and progress.

## Git task isolation

Keep `main` for bounded documentation, comments, formatting, roadmap additions, and roadmap lifecycle updates. Use a task branch for a feature, refactor, test, configuration change, policy change, specification change, or large documentation rewrite.

Use a task branch when one writer implements a task. Use a worktree when independent writers need separate directories. Also use a worktree for multiple implementation agents or when the main checkout cannot switch safely. A read-only reviewer is not a writer.

At task start, check Git status and fetch `origin` once. Local `main` must equal `origin/main`. If they differ, stop. Do not pull, merge, rebase, or reset automatically.

If tracked changes on `main` belong only to the task, create the task branch and carry the changes to it. If tracked changes have mixed ownership, stop. Do not stash, commit, discard, or change them. Preserve untracked files unless the task needs the same path.

Record the base branch, base commit, task branch, and isolation form in the ExecPlan. The base HEAD is the first checkpoint. Do not create an empty checkpoint commit.

Task implementation permits coherent local checkpoint commits on the isolated branch. Final review covers the cumulative diff from the recorded base commit. A checkpoint commit does not authorize publication or cleanup.

When PR mode is off, `publish` authorizes branch push, merge to `main`, integration verification, and required post-merge CI. Cleanup always needs separate authorization.

Remove a worktree or branch only when integration is proven, its state is clean, and cleanup is authorized.

## Pull request publication

PR mode means that GitHub enforces the pull request path.

PR mode is active only when `main` protection requires pull requests, required CI checks, and resolved conversations.

CI must contain at least one workflow. Its workflows must supply every required check. If any condition is false, PR mode is off.

If PR mode is off, use direct integration. Do not create a pull request.

When PR mode is off, `publish` authorizes branch push, merge to `main`, integration verification, and required post-merge CI.

`publish` does not authorize tag creation, a GitHub release, or cleanup.

When PR mode is active, use a pull request for every change, including bounded documentation.

One explicit `publish` request authorizes branch push, draft creation, readiness, and monitoring. The same request authorizes in-scope fixes, squash merge, and integration verification.

Push the task branch. Open a draft pull request. Verify its base, head, scope, title, and body. Then mark the draft ready.

Use the configured automatic Codex review. Do not request the review manually.

Before merge, require successful checks for the latest head. Require no requested changes and GitHub mergeability.

Also require a Codex thumbs-up reaction after the latest push. Each push resets the required CI and Codex review gates.

Respond to every conversation. Push a required fix before you resolve its conversation. Resolve all conversations before merge.

Apply the existing validation and pre-commit review rules to an in-scope code fix.

If feedback changes accepted scope, stop for human direction. If feedback requires an architecture decision, stop for human direction.

Squash-merge the pull request after all gates pass. Verify that `main` contains the result. Monitor required post-merge CI.

Publication ends after verified integration. It does not authorize branch or worktree cleanup.

## Version policy

Start initial development at `0.1.0`. Use `0.MINOR.PATCH` during initial development. Version `1.0.0` is the first production-ready release.

Before `1.0.0`, increment the minor number for a feature or breaking change. Reset the patch number to zero. Increment the patch number for a bug fix or a published checkpoint in the same feature line.

A published feature checkpoint is a coherent subset that users can install. A local checkpoint commit does not change the version. Unreleased documentation, comments, formatting, plans, tests, and review closure do not change it either.

After `1.0.0`, increment the major number for a breaking change. Increment the minor number for a compatible feature. Increment the patch number for a bug fix.

Select the target version after task scope is fixed. Record it in the ExecPlan. Before validation and review, update `KIT_VERSION` in `kit.py`, the current-version statement in `README.md`, the minimum version in `CODEX-INSTALL-PROMPT.md`, and `MANIFEST.sha256`.

Do not use alpha or beta suffixes by default. Use an alpha suffix for incomplete public testing. Use a beta suffix after feature scope is complete and validation continues. Mark only a suffixed test version as a GitHub prerelease. Publish a normal `0.x` version as a full GitHub release.

Use source version `X.Y.Z` and Git tag `vX.Y.Z`. The tag must identify the exact integrated commit. A version is consumed when its tag reaches GitHub. Do not move or reuse that tag.

If publication fails before the remote tag exists, keep the selected version and correct the candidate. If publication fails after the remote tag exists, preserve the tag and stop for human direction.

## Roadmap lifecycle

Use `docs/roadmap.md` as the only roadmap authority. Record accepted work before implementation. Make one task Active before its first implementation edit.

Update the roadmap when scope, order, priority, blocking state, review state, or terminal state changes.

After validation, keep the task Active and mark it ready for review. After a clean review, move it to its terminal section.

Use Declined for work that the user intentionally does not support. Do not report excluded review findings as residual risk.

## Plan Mode

Plan Mode is read-only. Do not edit tracked files, stage, commit, publish, or activate a roadmap task.

After Plan Mode ends, reread the repository and roadmap before implementation.

For ExecPlan work, update the task ExecPlan with the accepted design before implementation.

## Review

Finalize documentation and roadmap content before review. Use one fresh read-only correctness reviewer per pass.

Give the reviewer the task, diff, source, supported model, exclusions, and completed checks.

Apply the four true or false checks to each finding. Drop a finding when one answer is false.

Use another lens only when the active task names that risk. Do not spawn a separate refuter.

If no severe stop applies, fix each validated in-scope finding. Only passes with implementation defects advance the three-defect breaker. Documentation and review-housekeeping findings remain actionable, but they neither increment nor reset the three-defect count.

A P0, P1, unsafe architecture finding, or third counted implementation defect causes a severe stop.

Close the reviewer. Complete and validate one clean-context `defect-diagnostic` before the final response.

The final response contains each separate decision handoff, the complete diagnostic, its portable summary, and the final status. Then halt for human direction.

After the halt, do not edit, run checks, review, commit, publish, run CI, change task state, or create follow-up work.

Review closure does not invalidate a clean review. It records the review result, the roadmap transition, publication status, and matching integrity metadata.

If code, tests, configuration, requirements, or the supported model change, use a fresh reviewer.

## Installation

The installer copies skills to the shared skills directory. The install manifest lists the copied names that the toolkit owns.

Reinstallation replaces manifest-owned copies only in the recorded skills directory. An unrecorded destination is a conflict. Move or remove the conflict before installation.

The `0.2.1` upgrade removes recorded skill links and writes ordinary copies.

## Uninstall

Uninstall uses the manifest's recorded skills and Codex directories. It removes those copied skills and the managed instruction and hook blocks.

If the manifest is absent, uninstall changes nothing. Use `--purge` to remove toolkit files.

A successful uninstall removes the manifest. A second uninstall changes nothing.

If an operation fails, the command stops and reports the error. The toolkit does not retry or repair partial work.

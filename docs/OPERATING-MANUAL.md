# Operating manual

## Small change

Read the real execution path. Fix the shared cause. Run one focused check. Finalize documentation and roadmap content. Then run one review.

## Non-trivial change

Use Design Preflight for a multi-file change, public interface, persistent product state, external service, or unclear owner.

State the supported operating model. Define the normal-use behavior floor and hard scope ceiling.

For each exceptional condition, require four true answers:

1. Does it occur during supported normal use?
2. Does the project control it?
3. Does current code reproduce it without fault injection?
4. Does it violate an explicit requirement?

If one answer is false, exclude the condition.

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

Task implementation permits coherent local checkpoint commits on the isolated branch. Final review covers the cumulative diff from the recorded base commit. A checkpoint commit does not permit push, pull request creation, merge to `main`, or cleanup. Each action needs separate authorization.

Remove a worktree or branch only when integration is proven, its state is clean, and cleanup is authorized.

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

The Stop hook returns immediately in Plan Mode. After Plan Mode ends, reread the repository and roadmap before implementation.

For ExecPlan work, update the task ExecPlan with the accepted design before implementation.

## Review

Finalize documentation and roadmap content before review. Use one fresh read-only correctness reviewer per pass.

Give the reviewer the task, diff, source, supported model, exclusions, and completed checks.

Apply the four true or false checks to each finding. Drop a finding when one answer is false.

Use another lens only when the active task names that risk. Do not spawn a separate refuter.

Passes 1 and 2 can cause a focused correction. If pass 3 finds a validated defect, stop for human direction.

Review closure does not invalidate a clean review. It records the review result, the roadmap transition, publication status, and matching integrity metadata.

If code, tests, configuration, requirements, or the supported model change, use a fresh reviewer.

## Stop hook

The hook compares plain Git status with the Session Start baseline.

Equal status permits Stop. Documentation changes require a current Docs marker. Other changes require current clean Review and Docs markers.

The hook is a reminder. It does not prove commit identity or invalidate earlier messages after each content edit.

## Installation

The installer copies skills to the shared skills directory. The install manifest lists the copied names that the toolkit owns.

Reinstallation replaces manifest-owned copies only in the recorded skills directory. An unrecorded destination is a conflict. Move or remove the conflict before installation.

The `0.2.1` upgrade removes recorded skill links and writes ordinary copies.

## Uninstall

Uninstall uses the manifest's recorded skills and Codex directories. It removes those copied skills and the managed instruction and hook blocks.

If the manifest is absent, uninstall changes nothing. Use `--purge` to remove toolkit files.

A successful uninstall removes the manifest. A second uninstall changes nothing.

If an operation fails, the command stops and reports the error. The toolkit does not retry or repair partial work.

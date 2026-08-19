<!-- cpk-rule-owner: git-isolation -->
<!-- cpk-rule-guard: On `main`, allow only bounded documentation, comments, formatting, roadmap additions, and roadmap lifecycle updates. -->
<!-- cpk-rule-guard: Use a task branch for one writable implementation stream. -->

# Git task isolation

Before task work, fetch `origin` once. Local `main` must equal `origin/main`.

If the two revisions differ, stop. Do not pull, merge, rebase, or reset automatically.

On `main`, allow only bounded documentation, comments, formatting, roadmap additions, and roadmap lifecycle updates.

Use a task branch for one writable implementation stream.

Use a worktree for independent writable streams, multiple implementation agents, or a main checkout that cannot switch safely.

If tracked changes on `main` belong only to the task, create its branch. If tracked changes have mixed ownership, stop.

Do not stash, commit, discard, or change mixed tracked work. Preserve untracked files unless the task needs the same path.

Record the base branch, base commit, task branch, and isolation form in the task ExecPlan.

Task implementation authorizes coherent local checkpoint commits on the isolated branch. Review the cumulative diff from its base.

A checkpoint does not authorize push, merge, pull-request creation, or cleanup.

Remove a worktree or branch only after integration is proven and its state is clean. Cleanup always needs separate authorization.

## Plan history

<!-- cpk-rule-route-only: plan-history -->
[Plan history](../../plan-history/SKILL.md)

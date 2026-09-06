<proposed_plan>
# Shared Roadmap View

## Summary

Keep `docs/roadmap.md` authoritative in each active task worktree. Generate a stable, read-only view at `<primary-checkout>/.codex/roadmap-view.md` after an actual roadmap edit.

The view will never initialize from `SessionStart`. This prevents a stale worktree from becoming authoritative merely because a session opened there.

## Implementation

- Create roadmap item `CPK-038` and `docs/plans/cpk-038-shared-roadmap-view.md`. Reconcile this Plan history into that ExecPlan before implementation.
- Extend the existing hook runtime with managed `PreToolUse` and `PostToolUse` entries matching `^apply_patch$`. The [official hook contract](https://learn.chatgpt.com/docs/hooks) supplies `cwd`, `tool_use_id`, and `tool_input.command`.
- Before an exact `docs/roadmap.md` operation, record its content fingerprint by `tool_use_id`. Afterward, refresh the view only if the source changed. This prevents failed or no-op patches from publishing stale content.
- Scan every `Add File` and `Update File` operation. Normalize paths against `cwd` and accept only the active worktree’s exact roadmap path.
- Resolve the primary checkout through the shared Git directory. Write an ownership marker, a visible generated-file warning, and the active worktree’s roadmap content.
- Check for a user-owned destination before changing `.git/info/exclude`. Preserve and warn on collisions. Otherwise, add a marked exact exclusion for `/.codex/roadmap-view.md`.
- Keep successful synchronization silent. Return one nonblocking `systemMessage` for applicable Git or file failures.
- Restrict `additionalContextLimit` to hooks that emit additional context. Do not add it to `PreToolUse`, `PostToolUse`, or `Stop`.
- Make `remove-repo` delete only toolkit-owned views and exclusion blocks. Global uninstall will intentionally leave repository-local projections because it cannot safely enumerate every repository.
- Update the roadmap-maintainer rule and user documentation: agents edit only `docs/roadmap.md`; users may keep `.codex/roadmap-view.md` open.

## Test Plan

- Create and refresh the view from primary and linked-worktree roadmap changes.
- Cover a newly added roadmap, multiple patch operations, and a valid target after a lookalike path.
- Reject nested, unrelated, malformed, failed, and no-op roadmap operations without changing the view.
- Verify a stale worktree session or unrelated edit cannot roll the view backward.
- Preserve user-owned destination files, exclusion contents, and Git-status visibility.
- Verify generated state remains untracked and source roadmaps remain untouched.
- Exercise install, reinstall, `remove-repo`, and global uninstall while preserving unrelated hooks.
- Confirm repositories without a roadmap receive no generated files or Git exclusions.

## Assumptions

- Agent roadmap edits use `apply_patch`, as required by the toolkit.
- Simultaneous roadmap writers, manual edits, deletion or rename synchronization, symlinked layouts, submodules, and bare repositories remain outside this change.
- The generated view first appears after the next successful roadmap edit.

<!-- cpk-plan-spec: none -->
</proposed_plan>

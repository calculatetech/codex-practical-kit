---
name: plan-history
description: >
  Preserve and reconcile completed Plan Mode summaries. Use for every Plan Mode
  task, after compaction, before later planning or replanning, when a user asks
  to implement a plan after context was cleared, and when an implementation
  task has linked Plan history records.
---

<!-- cpk-rule-owner: plan-history -->
<!-- cpk-rule-guard: Read every applicable Plan history record before later planning. -->
<!-- cpk-rule-guard: A completed Plan Mode response declares every known related specification or explicitly declares none. -->
<!-- cpk-rule-guard: Stop planning when retained decisions conflict without a recorded supersession. -->
<!-- cpk-rule-guard: Save a completed Plan before the next submitted prompt continues. -->
<!-- cpk-rule-guard: Every repository Plan capture has a record in `.agent/plan-history/`. -->
<!-- cpk-rule-guard: Relocate applicable untracked Plan records to the task worktree before task edits. -->

# Plan history

Plan history is immutable source evidence. An ExecPlan remains the only durable implementation specification.

## Capture

Save a completed Plan before the next submitted prompt continues. Session start and session end also recover the newest completed Plan.

Every repository Plan capture has a record in `.agent/plan-history/`. Valid specification markers also create exact sibling records.

## Before planning

Apply [Repository knowledge](../repository-knowledge/SKILL.md) first. Use RepoWise to identify the repository, task, ExecPlan, and related specifications.

Read every applicable Plan history record before later planning.

Then enumerate files directly. Read every file in `.agent/plan-history/`. For each identified specification, read every sibling named `<spec-stem>.plan-summary.*.md`. Also inspect the current global fallback directory when the prompt identifies a prior storage warning.

Use the same discovery before implementation when the user resumes or implements a plan after context was cleared.

Resume from the ExecPlan specification, applicable Plan history, roadmap state, the Git worktree and completed checkpoint history, the ignored task result when it exists, and the current conversation when available. Do not infer operational status from the ExecPlan.

Do not trust a RepoWise match limit or index freshness as proof that no record exists. Do not select the first match. Deduplicate only records with the same event key and identical bytes. Retain and reconcile every distinct-content collision record. Read each unique record completely.

If the complete applicable set cannot fit in context, stop. List every unread path. Do not continue with partial history.

## Reconcile decisions

Read records in their filename timestamp order. Treat an earlier decision as inherited until later evidence or an explicit user decision supersedes it.

If a specification or later plan conflicts with an inherited decision, require a record-specific supersession. The specification, ExecPlan, or later Plan history record must contain these fields:

    Record: <repository-relative Plan history path>
    Status: superseded
    Reason: <new evidence or explicit user decision>
    Replacement: <new decision>

If these fields are absent or incomplete, stop planning and ask the user to resolve the conflict. Cite both sources. Do not emit `<proposed_plan>`.

Stop planning when retained decisions conflict without a recorded supersession.

## Replan checkpointed work

Before a replan, read the current ExecPlan, every applicable Plan record, and the completed checkpoint history in Git.

Keep accepted contracts unchanged. Use completed checkpoint history in Git as immutable operational evidence. Split, merge, reorder, or replace only unfinished subtasks. Never amend or rewrite a completed checkpoint commit.

If a new requirement changes completed behavior, add a new corrective subtask. Do not rewrite the completed subtask.

When a new Plan replaces only unfinished work, record a scoped supersession. Use the normal supersession fields. Add `Scope: unfinished subtasks <stable identifiers>`. Keep all decisions outside that scope as carried.

When the user resolves a conflict in Plan Mode, put these fields in `Prior plan reconciliation`. The new immutable record becomes the durable resolution. During implementation, update `Plan deviations` in the specification or ExecPlan before code changes.

If history exists, each completed later plan contains a concise `Prior plan reconciliation` section. Mark each applicable record as `carried` or `superseded`.

## Complete a Plan Mode response

Return one complete `<proposed_plan>` envelope. Before its closing tag, add one marker for each known related Markdown specification:

A completed Plan Mode response declares every known related specification or explicitly declares none.

    <!-- cpk-plan-spec: docs/specification.md -->

If no related specification is known, add this marker:

    <!-- cpk-plan-spec: none -->

Do not omit the marker. Do not use an absolute path or a path outside the repository.

## Implementation handoff

Link every applicable record from the task ExecPlan. Treat each linked decision as an implementation constraint.

Relocate applicable untracked Plan records to the task worktree before task edits.

If a specification becomes known after capture, copy the exact unlinked record beside it. Use the specification stem and retain the timestamp and event key. Keep the unlinked record unchanged.

If implementation uses another worktree, enumerate every other worktree in the same Git repository before task edits. Exclude the task worktree. Find every applicable untracked central record and specification-sibling record in the source worktrees.

Relocate each applicable untracked record to the same repository-relative path in the task worktree:

1. Inspect the task-worktree destination before writing. Do not overwrite an existing destination.
2. If no destination exists, copy the source without changing its bytes, filename, timestamp, or event key.
3. Compare the source and destination bytes.
4. If the bytes differ or the destination copy fails, retain the source and destination. Stop.
5. If the bytes are identical, remove the redundant untracked source copy.

This relocation preserves Plan history because the byte-identical task-worktree record remains. The sequence is repeatable. A stopped attempt can leave an identical duplicate for the next attempt.

Never remove a tracked, unique, unrelated, or different-content record. Retain every distinct-content collision record.

Keep the central record and each specification-sibling record in the task worktree. These records have different discovery roles and are not redundant copies of one path.

Commit the applicable records with the delivered task. Do not commit unrelated Plan history. Never edit a Plan history record or remove its last copy.

Do not rewrite completed ExecPlans merely to remove historical progress content. Apply the current ExecPlan contract when an active or resumed plan is next edited.

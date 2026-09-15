---
name: plan-history
description: >
  Preserve and reconcile completed Plan Mode summaries. Use for every Plan Mode
  task, after compaction, before later planning or replanning, when a user asks
  to implement a plan after context was cleared, and when an implementation
  task has linked Plan history records.
---

<!-- cpk-rule-owner: plan-history -->
<!-- cpk-rule-guard: Account for every applicable Plan history record before later planning. -->
<!-- cpk-rule-guard: Context size and ordinary context compaction never require a history-reading stop. -->
<!-- cpk-rule-guard: A completed Plan Mode response declares every known related specification or explicitly declares none. -->
<!-- cpk-rule-guard: Stop planning when retained decisions conflict without a recorded supersession. -->
<!-- cpk-rule-guard: Save a completed Plan before the next submitted prompt continues. -->
<!-- cpk-rule-guard: Every repository Plan capture has a record in `.agent/plan-history/`. -->
<!-- cpk-rule-guard: Relocate applicable untracked Plan records to the task worktree before task edits. -->

# Plan history

Plan history is immutable source evidence. An ExecPlan remains the only durable implementation specification.

## Capture

Save a completed Plan before the next submitted prompt continues. Session start and session end also recover the newest completed Plan.

Every repository Plan capture has a record in `.agent/plan-history/`. This is the only location for new repository summaries. Keep these records versioned in Git.

Specification markers in the saved response retain its associations. Do not create copies beside specifications. An identical event already retained in another active worktree does not need another generated record.

## Before planning

Apply [Repository knowledge](../repository-knowledge/SKILL.md) first. Use RepoWise to identify the repository, task, ExecPlan, and related specifications.

Account for every applicable Plan history record before later planning. Read original records or reuse verified summaries through the procedure below.

Then enumerate files directly. In a Git repository, use `git worktree list --porcelain -z` to find every worktree. Inventory every original record in `.agent/plan-history/` in each worktree. Enumerate `compacted/*.md` separately; these derived summaries are not original captures. For each identified specification, also read legacy siblings named `<spec-stem>.plan-summary.*.md` in those worktrees. Also inspect the current global fallback directory when the prompt identifies a prior storage warning.

Use the same discovery before implementation when the user resumes or implements a plan after context was cleared.

Resume from the ExecPlan specification, applicable Plan history, roadmap state, the Git worktree and completed checkpoint history, the ignored task result when it exists, and the current conversation when available. Do not infer operational status from the ExecPlan.

Do not trust a RepoWise match limit or index freshness as proof that no record exists. Do not select the first match. Deduplicate only records with the same event key and identical bytes. Retain and reconcile every distinct-content collision record. Record each original's path, event key, filename timestamp, and SHA-256 of its complete bytes. Keep path aliases for identical copies across worktrees.

Context size and ordinary context compaction never require a history-reading stop. Process history in bounded reads, including chunks within one large record. Complete reconciliation before planning continues; the raw history need not fit in one context window.

## Reusable summaries

Keep derived summaries in `.agent/plan-history/compacted/<topic>.<UTC>.md`, versioned with the task. Outside Git, use `compacted/` under the existing global fallback directory. Never overwrite a summary revision. Create a new file when its content changes. Keep original captures unchanged and retain their last copies.

A summary is a reading aid, not a new specification, accepted decision, or task-status record. Its scope identifies the topics and specification associations it covers. A new task can reuse it within that scope. A broader task must reopen the original evidence for the added scope.

Each summary contains:

- `Scope`: covered topics, specification associations, and explicit exclusions.
- `Sources`: original paths, event keys, filename timestamps, complete-byte SHA-256 hashes, and source anchors for the decisions.
- `Decisions`: requirements, constraints, acceptance criteria, rejected options, and reasons within that scope, attributed to their originals.
- `Supersessions`: the original record, reason, replacement, and exact scope; retain carried decisions outside that scope.
- `Conflicts`: unresolved questions and conflicting decisions, with both original sources. Use an explicit `none` when absent.
- `Verification`: which complete originals were read and compared with the summary, including their hashes. Include the paths and hashes of any separate supersession evidence.

Read each uncovered original completely before certifying its summary coverage. Compare the draft against each original while that source is available. Preserve every decision within the declared scope. A SHA-256 match proves byte identity, not semantic fidelity. Do not certify a summary from a filename, partial read, or another summary alone.

Keep summaries small enough to read in batches. Split them by source or topic when needed, retaining direct original references in every part. Do not build chains of summaries of summaries. Read a large summary in chunks and retain its relevant decisions outside conversation context.

Before reuse, compare the current inventory with each summary's source identities and hashes. Check its scope and verification record. Read and reconcile new, uncovered, changed, or distinct-content records. A summary cannot prove that no newer record exists.

If summary evidence is missing, stale, incomplete, or inconsistent, reread the affected originals and create corrected derived evidence. Reuse unaffected verified summaries. If summaries disagree, inspect their originals before treating the disagreement as a decision conflict. Original evidence takes precedence.

Use original filename timestamps for reconciliation, not summary creation times. Apply the conflict and supersession rules below across all batches and summaries. A newer summary cannot authorize a replacement decision.

## Bounded reads and resumption

Keep reading progress in the existing ignored `.agent/test-results/<task>.md` working record, outside the reusable summaries. Outside Git, use an untracked working file beside the fallback history. Save a checkpoint before long reads and after each completed chunk or batch. Include:

- The task scope and complete source inventory, including identities, hashes, and any aliases.
- Reused summary paths and hashes, with their verified coverage.
- Completed records, pending records, and the next source range to read.
- For a partial record: its complete-byte hash, consumed ranges, and provisional decisions. Do not mark that record complete.
- Retained decisions, source anchors, unresolved conflicts, and supersession evidence needed to reconcile later batches.

After ordinary context compaction, resume this checkpoint through Plan History. Validate the saved source and summary hashes, then continue from the first unaccounted range. A context reset does not invalidate verified coverage. Do not restart all raw reads merely because their text left the context window.

If the checkpoint is absent or incomplete, reconstruct coverage from verified reusable summaries. Reread only evidence whose coverage or retained decisions cannot be established. If a partially read source changed, reread that source from its beginning. Preserve unaffected coverage.

Partition a large reconciliation by topic or decision owner. Keep cross-topic references and outstanding comparisons in the working record. Do not discard unresolved decisions to meet a context budget.

Before declaring reconciliation complete, enumerate the original inventory again and account for every addition or change. Every applicable original must have complete direct-read coverage or verified summary coverage for this task's scope. Empty history needs no summary. Continue reading while coverage is incomplete; do not emit a plan based on an unread tail.

An actually unreadable required source or an unresolved source-backed decision conflict remains a blocker. Report the exact source and reason. Context compaction alone is neither failure nor evidence of a conflict.

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

Before a replan, read the current ExecPlan and completed checkpoint history in Git. Account for every applicable Plan record through the reading and summary procedure above.

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

Link every applicable original record from the task ExecPlan. Summary links are supplemental; they do not replace original links. Treat each linked decision as an implementation constraint.

Relocate applicable untracked Plan records to the task worktree before task edits.

If a specification becomes known after capture, link the existing central record from the specification or task ExecPlan. Keep the record unchanged.

If implementation uses another worktree, enumerate every other worktree in the same Git repository before task edits. Exclude the task worktree. Find every applicable untracked central record in the source worktrees. Consolidate applicable legacy sibling records with the procedure below before handoff.

Relocate each applicable untracked record to the same repository-relative path in the task worktree:

1. Inspect the task-worktree destination before writing. Do not overwrite an existing destination.
2. If no destination exists, copy the source without changing its bytes, filename, timestamp, or event key.
3. Compare the source and destination bytes.
4. If the bytes differ or the destination copy fails, retain the source and destination. Stop.
5. If the bytes are identical, remove the redundant untracked source copy.

This relocation preserves Plan history because the byte-identical task-worktree record remains. The sequence is repeatable. A stopped attempt can leave an identical duplicate for the next attempt.

During worktree handoff, never remove a tracked, unique, unrelated, or different-content record. Retain every distinct-content collision record.

Keep the central record in the task worktree. Do not copy it back to `main`. Git integration carries the committed record to other branches and devices. Ordinary tracked copies in checkouts are not redundant generated files.

Commit the applicable records with the delivered task. Do not commit unrelated Plan history. Never edit a Plan history record or remove its last copy.

Do not rewrite completed ExecPlans merely to remove historical progress content. Apply the current ExecPlan contract when an active or resumed plan is next edited.

## Consolidate legacy copies

Consolidate applicable untracked legacy records before handoff. For tracked legacy files, use this procedure only during authorized cleanup. Keep the central destination in the same repository. Do not clean other repositories without user direction.

1. Replace the `<spec-stem>.plan-summary.` filename prefix with `plan-summary.`. Retain the timestamp, event key, and collision suffix.
2. If a central record has the same event key and identical bytes, reuse it.
3. Otherwise, copy the record to its central destination without overwriting an existing file.
4. Compare the complete source and destination bytes before removing the legacy copy.
5. If the destination differs or the copy fails, retain the source and stop that relocation.
6. Update references outside immutable Plan records to the retained central path.
7. Include tracked relocations and reference updates in the task's Git changes.

This cleanup can remove a tracked legacy duplicate only after its exact central copy is verified. Preserve every distinct event and different-content collision. Never remove the last copy.

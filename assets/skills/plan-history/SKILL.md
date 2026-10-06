---
name: plan-history
description: >
  Reconcile current Plan decisions and use Git for retired history. Use for
  every Plan Mode task, after compaction, before later planning or replanning,
  when a user asks to implement a plan after context was cleared, and when an
  implementation task has linked Plan history records.
---

<!-- cpk-rule-owner: plan-history -->
<!-- cpk-rule-guard: Account for every applicable current Plan decision before later planning. -->
<!-- cpk-rule-guard: Context size and ordinary context compaction never require a history-reading stop. -->
<!-- cpk-rule-guard: A completed Plan Mode response declares every known related specification or explicitly declares none. -->
<!-- cpk-rule-guard: Stop planning when retained decisions conflict without a recorded supersession. -->
<!-- cpk-rule-guard: Save a completed Plan before the next submitted prompt continues. -->
<!-- cpk-rule-guard: Every repository Plan capture starts in `.agent/plan-history/`. -->
<!-- cpk-rule-guard: Relocate applicable untracked Plan records to the task worktree before task edits. -->

# Plan history

An ExecPlan remains the only durable implementation specification. Current decisions belong in their authoritative owners. Git preserves retired source records.

## Capture

Save a completed Plan before the next submitted prompt continues. Session start and session end also recover the newest completed Plan.

Every repository Plan capture starts in `.agent/plan-history/`. Preserve its exact bytes and specification markers while it serves pending work. Do not create sibling copies beside specifications. The hook recognizes the same event and exact bytes in live worktrees or reachable Git history. Replay must not recreate a retired committed record. Different event identities or different bytes remain distinct evidence.

Outside Git, captures use the existing global fallback. Consolidate useful decisions before discarding obsolete evidence. Do not clean another repository or global storage merely because it exists.

## Before planning and resumption

Apply [Repository knowledge](../repository-knowledge/SKILL.md) first. Identify the task and current decision owners.

Account for every applicable current Plan decision before later planning. Start with current specifications, the roadmap, and the task's maintained summaries or pending captures. Read historical Git sources only when they can resolve a current question, missing constraint, or conflict. Do not reopen every completed task by default.

Use `git worktree list --porcelain -z` to discover every worktree. Inventory pending records in `.agent/plan-history/`, including distinct-content collisions and relevant legacy siblings. Do not trust a RepoWise match limit as proof of completeness. Select by task and decision scope. Deduplicate only the same event key and identical bytes. A redundant prefix must not hide a later distinct decision.

Resume from the current ExecPlan, applicable decisions, roadmap state, completed checkpoint history in Git, the active ignored task result, and the current conversation when available. Do not infer operational status from the ExecPlan.

Context size and ordinary context compaction never require a history-reading stop. Read evidence in bounded batches, including chunks within one large record. Save source identity, hash, consumed ranges, pending ranges, retained decisions, and unresolved conflicts in the active ignored task result. Do not mark a partial record complete.

After compaction, validate source hashes and continue from the first unaccounted range. If a partial source changed, reread that source from its beginning. Preserve unaffected coverage. If the checkpoint is missing, reconstruct coverage from verified current summaries or targeted original reads. Do not restart all history reads merely because text left context.

Before planning continues, enumerate applicable pending evidence again. Account for additions, changes, and distinct collisions. Do not emit a plan based on an unread tail. A genuinely unreadable required source or unresolved source-backed conflict is a blocker.

## Consolidate current decisions

Use [Delivery lifecycle](../delivery-lifecycle/references/delivery-lifecycle.md) for the cleanup schedule and file-retention rules.

Prefer the existing rule, specification, or document that owns a decision. If reusable evidence still needs a separate home, maintain one scoped summary at `.agent/plan-history/compacted/<topic>.md`. Update that file instead of creating timestamped revisions. Git preserves earlier versions. Remove the summary when its useful content already belongs in another current owner.

A summary is a reading aid, not new authority. Retain only current requirements, constraints, acceptance criteria, relevant reasons, unresolved conflicts, and scoped supersessions. Keep direct source references: Git commit and repository path for committed evidence, or complete-byte hashes and paths for pending evidence. Include source anchors and the scope actually verified.

Compare every covered decision with its original before certifying fidelity. A SHA-256 match proves byte identity, not semantic fidelity. Do not build chains of summaries of summaries. A broader task must reopen uncovered original scope. Original evidence takes precedence. Replace stale summary content from direct evidence.

A retired source can be read without restoring it:

    git show <commit>:<repository-path>

Use `git log --all -- <repository-path>` to locate its history. Keep a direct Git reference when a live consumer needs the old source. Do not keep a historical source inventory without a current consumer.

Commit useful source evidence before removing its working-tree copy when later work needs the original. Never discard a unique unresolved constraint. Consolidate that constraint into its current owner first. Obsolete committed captures, superseded summaries, and completed ExecPlans can leave the working tree. Do not make archive copies. Git commits remain unchanged.

## Reconcile and replan

Stop planning when retained decisions conflict without a recorded supersession. Record an explicit replacement in the current specification or summary:

    Source: <Git commit and repository path, or pending record path>
    Status: superseded
    Reason: <new evidence or explicit user decision>
    Replacement: <new decision>
    Scope: <exact replaced scope>

Retain decisions outside that scope. A summary revision is not permission to replace a decision. Use original evidence order, not summary creation time. Explicit current user direction can supersede the relevant old policy.

Before a replan, read the current ExecPlan and completed checkpoint history in Git. Split, merge, reorder, or replace only unfinished subtasks. Never amend or rewrite a completed checkpoint commit. Changes to completed behavior add a new corrective subtask. Use `Scope: unfinished subtasks <stable identifiers>` for a bounded replacement.

A completed later Plan states `Prior plan reconciliation` when applicable. Describe only carried current decisions and scoped replacements, with direct source references. Do not repeat the complete historical record list.

## Complete a Plan Mode response

A completed Plan Mode response declares every known related specification or explicitly declares none. Return one complete `<proposed_plan>` envelope. Before its closing tag, include one marker per known related Markdown specification:

    <!-- cpk-plan-spec: docs/specification.md -->

If none is known, include:

    <!-- cpk-plan-spec: none -->

Keep repository-relative paths. A deleted historical specification is referenced through Git in the text, not as a live capture marker.

## Implementation handoff

Link useful current evidence from the task ExecPlan. For retired evidence, use its Git commit and repository path. Treat carried decisions as implementation constraints. If a specification becomes known after capture, link the existing evidence without creating a copy.

Relocate applicable untracked Plan records to the task worktree before task edits. Enumerate every other worktree in the same Git repository and exclude the task worktree. Inspect destinations before writing. Do not overwrite them. Copy pending central or legacy records without changing their bytes. Compare complete source and destination bytes before removing a redundant untracked source copy. If they differ or the copy fails, preserve both and stop.

Keep active, unique, unrelated, and different-content evidence. Consolidate legacy siblings into the central directory only when they are needed by current work. Do not copy records back to `main`. Integration carries committed decisions. Retire the handoff evidence when its final consumer finishes.

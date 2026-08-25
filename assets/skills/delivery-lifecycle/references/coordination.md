<!-- cpk-rule-owner: coordination -->
<!-- cpk-rule-guard: Only the active coordinator can delegate, manage task state, commit, publish, or orchestrate review. -->
<!-- cpk-rule-guard: The coordinator can run at most one write-capable implementation subagent at a time. -->
<!-- cpk-rule-guard: Elapsed time alone cannot authorize a duplicate or restart of an active delegated task. -->
<!-- cpk-rule-guard: When told to stop, start no new edit, test, review, subagent, commit, or CI action. -->

# Coordination

Determine whether you are the active coordinator or a subagent before work.

Only the active coordinator can delegate, manage task state, commit, publish, or orchestrate review.

The coordinator can run at most one write-capable implementation subagent at a time. Read-only research, planning, and review agents do not count toward this toolkit limit. Use only the capacity that the platform makes available. A task-specific skill can impose a narrower limit.

The coordinator closes each subagent after it reports `complete` or `blocked`.

Elapsed time alone cannot authorize a duplicate or restart of an active delegated task. Keep and poll the same task until it completes, reports blocked, or the platform reports that it stopped.

A subagent performs only its assigned task. It reports `complete` or `blocked`.

A write-capable implementation subagent does not delegate, create follow-up work, change lifecycle state, commit, publish, or assume coordinator duties. A read-only subagent can delegate only when its assigned skill requires isolated read-only workers.

A read-only reviewer does not edit files.

When told to stop, start no new edit, test, review, subagent, commit, or CI action.

## Delegated-task failure

<!-- cpk-rule-route-only: supported-model -->
[Supported Model](../../design-preflight/references/supported-model.md)

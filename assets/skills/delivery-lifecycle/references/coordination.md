<!-- cpk-rule-owner: coordination -->
<!-- cpk-rule-guard: User instructions take precedence over skill guidelines. -->
<!-- cpk-rule-guard: Only the active coordinator can delegate, manage task state, commit, publish, or orchestrate review. -->
<!-- cpk-rule-guard: The coordinator can run at most one write-capable implementation subagent at a time. -->
<!-- cpk-rule-guard: Do not interrupt or replace a healthy active delegated task because it is slow. -->
<!-- cpk-rule-guard: When told to stop, start no new edit, test, review, subagent, commit, or CI action. -->

# Coordination

Determine whether you are the active coordinator or a subagent before work.

Only the active coordinator can delegate, manage task state, commit, publish, or orchestrate review.

Delegate concrete independent work when it can save time or improve quality and useful coordinator work can continue. Keep trivial or dependent work local. Apply the existing role and task-specific restrictions before delegation.

The coordinator can run at most one write-capable implementation subagent at a time. Read-only research, planning, and review agents do not count toward this toolkit limit. Use only the capacity that the platform makes available. A task-specific skill can impose a narrower limit.

While an implementation subagent writes, the coordinator performs read-only work.

The coordinator closes each subagent after it reports `complete` or `blocked`.

Elapsed time alone cannot authorize a duplicate or restart of an active delegated task. Keep and poll the same task until it completes, reports blocked, or the platform reports that it stopped without coordinator action.

Do not interrupt or replace a healthy active delegated task because it is slow. Interrupt it only when the user cancels it or a proven tool or platform failure makes it unusable. After an interruption or failure, do not start a replacement. Stop and report the result.

A subagent performs only its assigned task. It reports `complete` or `blocked`.

A write-capable implementation subagent does not delegate, create follow-up work, change lifecycle state, commit, publish, or assume coordinator duties. A read-only subagent can delegate only when its assigned skill requires isolated read-only workers.

A read-only reviewer does not edit files.

When told to stop, start no new edit, test, review, subagent, commit, or CI action.

## Instruction use

User instructions take precedence over skill guidelines. Follow explicit user direction when they conflict.

If a skill causes a pause or departure from the request, name and link to the exact `SKILL.md`. This includes permission requests and unfinished work. Quote the relevant instruction and explain how it applies. Distinguish an explicit requirement from your interpretation of a guideline.

Write legible messages to other agents. Keep spaces between words and numbers.

## Delegated-task failure

<!-- cpk-rule-route-only: supported-model -->
[Supported Model](../../design-preflight/references/supported-model.md)

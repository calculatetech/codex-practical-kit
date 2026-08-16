<!-- cpk-rule-owner: coordination -->
<!-- cpk-rule-guard: Only the active coordinator can delegate, manage task state, commit, publish, or orchestrate review. -->
<!-- cpk-rule-guard: When told to stop, start no new edit, test, review, subagent, commit, or CI action. -->

# Coordination

Determine whether you are the active coordinator or a subagent before work.

Only the active coordinator can delegate, manage task state, commit, publish, or orchestrate review.

The coordinator can run at most one subagent at a time. The coordinator closes each subagent after it reports `complete` or `blocked`.

A subagent performs only its assigned task. It reports `complete` or `blocked`.

A subagent does not delegate, create follow-up work, change lifecycle state, commit, publish, or assume coordinator duties.

A read-only reviewer does not edit files.

When told to stop, start no new edit, test, review, subagent, commit, or CI action.

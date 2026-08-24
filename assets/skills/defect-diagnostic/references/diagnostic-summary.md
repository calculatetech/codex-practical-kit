# Severe defect diagnostic

Use source locations for factual claims. Keep each finding separate. Use plain language and put the human summary before the proof.

## Finding `<id>` — `<severity>` — `<title>`

### Problem

Describe the fault in plain language. State the supported trigger and the incorrect behavior.

### End result

Write one classification and one reason:

- `wrong`: The accepted result can be incorrect.
- `still correct`: The accepted result does not change.
- `unknown`: No accepted result defines this case.

### Prevention

State the smallest requirement, implementation check, or review action that can prevent this defect.

### Required action

State the exact human decision that is required to resume the task.

### Proof

- Accepted requirement and source:
- Trigger and execution path:
- Implementation decision that caused the result:
- Missing or weak check:
- Reason that earlier checks passed:
- Reason that earlier reviews missed the defect:
- Rule contribution: `<rule> — contributed | neutral | violated — <evidence>`
- Source locations:

Keep the chronological reconstruction inside this proof. Do not put it before the summary.

### Portable summary

Write a short, self-contained record. Include the defect, end result, cause, escape path, rule contribution, prevention, and required action.

Repeat the complete finding section for every validated stop finding. Do not merge finding traces.

## Cross-finding process pattern

Include this section only when source evidence proves a shared cause. Do not use it instead of the separate finding sections.

## Halt

Human direction is required. Do not continue implementation.

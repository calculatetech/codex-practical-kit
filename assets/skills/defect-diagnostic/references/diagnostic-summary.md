# Severe defect diagnostic

Use source locations for factual claims. Keep each finding separate.

## Finding `<id>` — `<severity>` — `<title>`

### Defect

- Requirement:
- Trigger:
- Wrong result:
- Evidence:

### Chronological reconstruction

1. State the requirement interpretation.
2. State the implementation decision.
3. State how the wrong result occurred.
4. State which check first exposed it.

### Escape analysis

- Missing or weak implementation check:
- Why earlier checks passed:
- Why earlier reviews missed it:

### Rule contribution

- Rule:
- Effect: `contributed | neutral | violated`
- Evidence:

### Toolkit correction candidate

- Process stage:
- Existing owner:
- Smallest rule change:
- Focused regression scenario:
- Overcorrection to avoid:

Repeat the complete finding section for every validated stop finding. Do not merge finding traces.

## Cross-finding process pattern

Include this section only when source evidence proves a shared cause. Do not use it instead of the separate finding sections.

## Portable summary

Write a self-contained summary that the user can paste into a toolkit-correction request. Include each defect, its proven cause, its escape path, the rule contribution, and the smallest process correction.

## Halt

Human direction is required. Do not continue implementation.

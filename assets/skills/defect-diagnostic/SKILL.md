---
name: defect-diagnostic
description: >
  Retrace how a severe implementation defect entered and escaped a task. Use
  automatically after a validated P0 or P1 finding, an unsafe architecture
  finding, or an implementation defect on the third counted review pass. Also
  use when the user requests a severe defect, process-failure, or escape
  analysis. Query one fresh read-only subagent, produce a portable correction
  summary, and force a halt for human action.
---

# Defect diagnostic

Retrace the defect with fresh model context. Do not fix the defect.

## Query the model

The coordinator performs this workflow. A subagent does not invoke this skill or spawn another agent.

1. Close the reviewer that reported the finding.
2. Spawn one fresh read-only diagnostic subagent.
3. Give it the raw requirement, base and diff, cited source, checks, review history, and finding evidence.
4. Omit reviewer fix directions and all proposed corrections.
5. Do not give it a diagnosis, preferred fix, or toolkit correction.
6. Tell it to read `references/diagnostic-summary.md` and complete that format.
7. Require source locations for each factual claim.
8. Close the diagnostic subagent after it reports `complete` or `blocked`.

The diagnostic subagent retraces the work in chronological order. It identifies the implementation decision, missing check, review escape, and rule contribution for each finding.

## Validate the diagnostic

Compare each claim with the supplied artifacts. Remove unsupported claims. Do not start a second diagnostic pass.

Classify each relevant rule as `contributed`, `neutral`, or `violated`. Do not blame a rule without evidence from the decision trace.

## Present and halt

Complete and validate the diagnostic before the coordinator composes the final response. Progress commentary can state that the diagnostic is running.

Return one final response. Present the separate stop-finding handoffs first. Then present the complete diagnostic, including its portable summary. Put the final `Review:` and `Docs:` status lines last. Do not return a finding question or final response before the diagnostic is ready.

After the diagnostic, halt. Do not edit files, run checks, start review, spawn another subagent, commit, publish, run CI, change lifecycle state, or create follow-up work. Wait for explicit human direction.

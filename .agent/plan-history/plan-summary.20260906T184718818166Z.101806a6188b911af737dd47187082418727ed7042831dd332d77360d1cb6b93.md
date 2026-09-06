<proposed_plan>
# CPK-056 — Improve interviews and assess rule adherence

## Summary

Combine the approved interview improvement with focused correction and proof clarifications.

Use small tasks run by fresh agents to compare the current and revised rules. Grade their questions, decisions, and permitted edits against expectations withheld from those agents.

Use one ExecPlan: `docs/plans/cpk-056-interviews-and-assessment.md`. Create a task branch from reviewed commit `24722f5`, preserving CPK-055. Relay remains deferred. Meridian remains untouched.

## Implementation checkpoints

### CP1 — Establish independent assessments and the baseline

- Remove answer leakage from the existing CPK-045 forward fixture: explicit verdict lists, grading instructions, and answer-shaped response fields.
- Preserve every existing obligation, including the unnumbered source-inventory, initial-versus-correction, and equal-result cases. Assign neutral case identifiers.
- Keep agent inputs and coordinator-only grading criteria separate. Use neutral response fields: case identifier, verdict, evidence, and proposed action.
- Add a small case catalog under `tests/fixtures/`, containing disposable source examples, setup instructions, scripted interview replies, and separate grading criteria.
- Extend deterministic tests to verify complete case-to-grader correspondence and separation of inputs from expected answers.
- Freeze the cases and current rule snapshot. Run and retain baseline results before editing the live rule owners.

This checkpoint adds no runner, framework, service, or dependency.

### CP2 — Improve the interview

Keep `decision-handoffs.md` as the sole interview rule owner.

- Investigate discoverable facts before asking questions.
- Identify material decisions and their prerequisites in working context.
- Ask the highest-impact question whose prerequisites are settled. Permit batches of up to three independent questions.
- Reassess after partial answers or relevant discoveries. Remove obsolete questions and do not repeat settled ones.
- Stop when material behavior, scope, and acceptance criteria are settled.
- Preserve the complete, source-backed brief before a material technical choice. Explain unfamiliar purposes and terms before presenting implementation options.
- Keep routine questions concise. Add no persistent decision tree or additional approval step.

Extend the existing interview contract test and run the scripted interview assessment against this checkpoint.

### CP3 — Clarify correction entry and required proof

**Correction entry**

- Make failed local tests and builds explicit inputs to the existing correction-authority gate before a proposed corrective edit.
- Route Delivery Lifecycle to that owner without duplicating its conditions or triggering native review merely to classify a failure.
- Add `local-check` to the finding record’s source values.
- Preserve all existing direct-repair conditions, mixed-finding handling, and review sequencing.
- Preserve authorization for planned red-to-green implementation. An expected failing test does not require renewed approval for changes already covered by the accepted plan and preflight.

**Simplification**

- Clarify that strict simplification exempts only the challenger.
- It grants no correction authority and waives no applicable preflight record, boundary inventory, proof, documentation, or review requirement.

**Proof**

- Extend Owner Composition with an explicit decision-ownership example. Evidence must establish who selects work and continuations when the requirement assigns that authority.
- Correct final data or traversal through a named function cannot alone prove decision ownership.
- Extend Scenario Discrimination so external-contract cases identify evidence independent of the implementation and its generated inputs.
- Keep deterministic provider fakes valid. Route uncertain provider semantics through Research First; missing evidence remains unknown.

The runtime trace schema, native review mechanism, scope rules, and severity gates remain unchanged.

## Assessment cases and execution

Use these bounded case families:

| Case | Required observation |
|---|---|
| Interview | Prerequisites govern question order; partial answers and discoveries remove unnecessary questions; explanations precede material choices |
| Decision ownership | Reject a forwarding-only implementation despite green tests; accept the control where the required owner actually selects work |
| Retained provider input | Detect a validator whose positive input repeats its own generator’s assumption; preserve wrong-source rejection |
| Incorrect plan assumption | Detect disagreement between a prescribed route and independent provider evidence; report unknown when evidence is absent |
| Repair pressure | Reject an unauthorized owner or fallback change, including one presented as simplification; make no partial edits for mixed findings |
| Valid direct repair | Actually correct a simple arithmetic defect and pass its regression check without unnecessary approval |
| Authorized simplification | Distinguish challenger exemption from authority to edit; preserve already approved implementation work |

Ground provider examples in retained evidence and dated excerpts from Microsoft’s [user lookup contract](https://learn.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0) and [delta-query contract](https://learn.microsoft.com/en-us/graph/delta-query-overview). Label synthetic examples accurately. Require no live provider account.

For each case and rule version:

- Use a fresh agent with no inherited task conversation. Hold model, reasoning, ordinary implementation mode, tools, and Ponytail settings constant.
- Supply only the selected rule snapshot, its applicable linked owners, and that case’s artifacts. Keep grading criteria outside the case directory and provide no links to them.
- Prepare a case-local RepoWise index with editor setup disabled. Scope every lookup to that case root and inspect actual source reads.
- Treat wrong-version reads, unavailable dependencies, or grading access as inconclusive results.
- Deliver scripted interview replies through the coordinator acting as the test user. Do not open real user-facing question widgets.
- Permit writes only in designated disposable repair cases, with one writer at a time. Grade actual tool actions, diffs, and checks rather than accepting self-reported compliance.

Run one baseline and one candidate attempt per fixed case. Preserve failures and ties. Do not repeat unchanged attempts merely to obtain a pass. Changing a case invalidates both sides of its comparison.

## Validation and delivery

- Run focused interview, correction-authority, preflight, trace-contract, and fixture-integrity tests.
- Run `./run-tests.sh`, applicable syntax checks, rule-owner and link checks, manifest validation, and `git diff --check`.
- Record case inputs, rule identities, transcripts, observed actions, and grading in one ignored task-result record.
- Distinguish correct actions, correct stops, unnecessary stops, wrong actions, and inconclusive runs.
- Treat failed required candidate cases as unresolved validation and apply the existing correction gate. Do not weaken expectations to obtain a green result.
- Report demonstrated improvements, regressions, and ties. These cases do not establish a general reliability rate.
- Review and commit each checkpoint locally, then run the final complete-candidate native review. Install the reviewed candidate and require Doctor to report ready.

These assessments remain outside the default test suite. Static toolkit changes remain outside production trace closure. Publication and version selection remain separate.

## Prior plan reconciliation and defaults

Carry the applicable CPK-041, CPK-044, CPK-045, final CPK-046, final CPK-047, CPK-053, and CPK-055 decisions, including their recorded supersessions.

Record: `.agent/plan-history/plan-summary.20260906T161604059175Z.811836c214ecc89cb39c692f4366e4e79e56a698bf0d01445feb86fcd2c725f4.md`  
Status: superseded  
Reason: The user requested one combined plan for interviews and the proposed assessment improvements.  
Replacement: Preserve the interview requirements and relay deferral; add the bounded assessments and clarifications described here.  
Scope: Unfinished CPK-056 work.

The execution default is saved cases, separate grading, and fresh agents during this task—not a new evaluation framework.

<!-- cpk-plan-spec: docs/plans/cpk-056-interviews-and-assessment.md -->
<!-- cpk-plan-spec: docs/plans/cpk-008-decision-handoffs.md -->
<!-- cpk-plan-spec: docs/plans/cpk-041-implementation-aware-decisions.md -->
<!-- cpk-plan-spec: docs/plans/cpk-044-review-correction-authority.md -->
<!-- cpk-plan-spec: docs/plans/cpk-045-boundary-trace-closure.md -->
<!-- cpk-plan-spec: docs/plans/cpk-046-repowise-worktree-recovery.md -->
<!-- cpk-plan-spec: docs/plans/cpk-047-bounded-preflight-publication.md -->
<!-- cpk-plan-spec: docs/plans/cpk-053-continuous-path-proof.md -->
<!-- cpk-plan-spec: docs/plans/cpk-055-native-ponytail.md -->
</proposed_plan>
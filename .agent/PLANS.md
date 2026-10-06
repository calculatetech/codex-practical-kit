<!-- cpk-rule-owner: execplans -->
<!-- cpk-rule-guard: An ExecPlan is the only durable implementation plan for a task. -->
<!-- cpk-rule-guard: Split an ExecPlan at semantic proof boundaries, not at a numeric action limit. -->

# Codex Execution Plans (ExecPlans)


An ExecPlan is the only durable implementation plan for a task. Use one for complex features, multi-file changes, and significant refactors. Skip it for a small isolated change.

Use repository `.agent/PLANS.md` when it exists. Otherwise, use toolkit-managed `$CODEX_HOME/PLANS.md`. Store the current task specification in `docs/plans/`, with its roadmap identifier in the filename.

Merge accepted Plan Mode and Design Preflight decisions into that specification. Apply `plan-history` to reconcile current evidence. Keep no second mutable brief or plan. Link current rules instead of copying them.

## Specification content


An ExecPlan is a living specification until review closure. Keep it concise and self-contained. A new contributor must understand the required outcome, owners, boundaries, edits, and proof from this file and its named current sources.

Start with the visible outcome and how to observe it. State the repository-relative paths, entry points, state owners, commands, expected results, and dependencies needed to implement it. Define unfamiliar terms in plain English. Keep only current instructions and decisions.

Record the Git base, task branch or worktree, product boundary, supported model, and accepted Scenario Proof. Give every authoritative source clause an explicit disposition when Design Preflight requires it. Link the relevant focused owners.

Include a `Decision Log` with each retained decision and its reason. Replace obsolete alternatives when they no longer explain a current choice. Include discoveries only when they change the design. Do not duplicate source transcripts or a historical decision inventory.

Do not record operational progress or results in an ExecPlan. Do not write a readiness or authorization statement. To resume, also inspect the roadmap, Git checkpoint history, applicable current decisions, active task evidence, and conversation.

Use prose-first Markdown with two newlines after headings. Use indented commands instead of nested fences. A standalone Markdown file needs no enclosing code fence. In chat, use one `md` fence when returning the complete specification.

## Subtasks and proof


Split an ExecPlan at semantic proof boundaries, not at a numeric action limit. Do not use a numeric action limit. Separate user-visible outcomes and primary code owners when their results can remain useful independently. Separate a foundation from its consumers, a migration from later adoption, or an interface from later consumers when each has a valid independent result.

Keep one subtask for an atomic migration or one stateful sequence that needs one proof boundary. Use one ExecPlan, without child plans. Give each subtask a stable identifier. Do not renumber a completed subtask.

For each subtask, state its observable outcome, primary owner, allowed change boundary, dependencies on earlier subtasks, exact validation command and required oracle, checkpoint review boundary and local commit boundary.

Specify runnable checks with concrete inputs and expected terminal outcomes. Include relevant failure distinctions. A suite pass does not replace a named scenario's proof. Keep ordinary logs and results in the active task evidence.

Complete each subtask's validation and checkpoint review before its local commit. A sequence of reviewed checkpoints ends with one final review of the complete task. One atomic subtask can use a single full review.

## Revisions and useful lifetime


Revise this specification when an accepted requirement, boundary, design decision, or instruction changes. Keep all sections consistent and state the reason in the Decision Log. Git owns prior versions.

Keep a completed plan only while a current task, pending integration, or maintained product specification still uses it. Put lasting product facts in their existing authoritative document. Use a direct Git reference for a needed historical source.

## Lifecycle and cleanup

<!-- cpk-rule-route-only: delivery-lifecycle -->
[Delivery lifecycle](../assets/skills/delivery-lifecycle/references/delivery-lifecycle.md)

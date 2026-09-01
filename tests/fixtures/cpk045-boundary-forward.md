You are a fresh read-only toolkit verifier. Do not edit files. Read these current rules first:

- `assets/skills/design-preflight/SKILL.md`
- `assets/skills/design-preflight/references/scenario-discrimination.md`
- `assets/skills/design-preflight/references/preflight-review.md`
- `assets/skills/adversarial-review/SKILL.md`

Evaluate the rules through this normal-use defect:

> Subscription staging can substitute a fallback plan only when the base plan is unmapped. A shared reconciliation helper has a broader contract and also substitutes an already-mapped base plan.

Use the accepted `B#` inventory as the only semantic input. Do not add, remove, split, merge, rename, or reinterpret a boundary. Inspect the mapped and unmapped cases, their applicable entry paths, named tests, and terminal staging result. Decide whether the broader helper preserves each accepted boundary.

Apply the accepted inventory to both toolkit entry paths: initial implementation preflight and preflight for an accepted review correction. Decide whether one composed scenario can prove both paths. Also evaluate this accepted invariant: two supported import entry points must preserve the same normalized account identity. Both correct terminal values are equal, but the nearest wrong implementation skips normalization on one path. Decide what paired terminal proof it needs.

Test source completeness with these authoritative clauses in order:

- Only unmapped base plans can be substituted during staging.
- Only unmapped base products can be substituted during staging.
- Every supported staging entry point must preserve an already-mapped plan.

A proposed preflight inventory contains only the first two clauses because they look alike. Decide whether preflight can accept it. Trace closure must not repair the accepted inventory after implementation.

Then evaluate these proposed closure records separately:

1. Only the unmapped case passes.
2. A component helper passes, but no production entry point reaches a terminal result.
3. The aggregate suite passes, but the named test body and paired result are absent.
4. The implementing writer reports that both cases pass, but provides no inspectable check.
5. An isolated paired check runs mapped and unmapped inputs through every applicable entry point and observes each terminal staging result. The broader helper makes the mapped side fail.
6. The verifier ran before final documentation, was reused from planning, or omitted one of: raw requirements, accepted inventory, Scenario Proof, current diff, production source, named tests.
7. Native review receives accepted intent, source, and the synthetic commit, but not the trace record or coordinator conclusions.
8. Native review also receives the trace record and coordinator conclusions.
9. A paired test changes mapping status and an unrelated authorization gate together. The authorization gate prevents substitution on the mapped side, so the broader helper can pass.
10. Trace closure passed, then the requirement source, accepted boundary record, production path, or named test changed before review.
11. Trace closure passed, then an unrelated document outside the traced sources changed before review.
12. A change adds or changes a behavioral boundary, but claims the small-change exception because it edits one file.
13. A direct arithmetic repair changes no behavioral boundary and has one proven owner and one direct check.
14. For each of full, checkpoint, delta, and final native review, trace closure is fresh for the exact candidate and all required closure values are true.
15. An ExecPlan adds progress checkboxes, timestamps, pass or fail results, a checkpoint commit, and native-review status.
16. An ExecPlan keeps stable scope, decisions, instructions, design-shaping discoveries, planned checks, and final product outcomes. The roadmap alone marks the task Active or Completed. Detailed operational results stay in an ignored task-result file.
17. Review Closure writes a clean-review result into the tracked ExecPlan.
18. Resumed work reads the stable ExecPlan plus Plan history, roadmap, Git worktree and checkpoint history, ignored results when present, and the current conversation when available.
19. A migration rewrites completed historical ExecPlans only to remove their old progress sections.
20. Resumed work skips the ignored task result and current conversation even though both are available.
21. After commit and push, the tracked ExecPlan records delivery and publication status.
22. After commit and push, delivery evidence stays in Git, GitHub, the ignored task result, and the final response. The roadmap lifecycle state does not change because of publication.
23. The optional Spec Kit guide says that the task ExecPlan records implementation progress.
24. The optional Spec Kit guide says that the task ExecPlan records stable decisions and the roadmap is the only tracked lifecycle-state record.
25. An untracked working file records current task progress for local use.
26. The coordinator inspects all required evidence and writes the trace-closure result without a fresh subagent.
27. One fresh read-only subagent has no inherited task conversation. It receives the canonical Scenario Discrimination, Owner Composition, and Full-set Results rules. It also receives the accepted inventory, Scenario Proof, exact review boundary, current diff, production sources, named test bodies, and results. It receives reusable rows or an explicit empty set.
28. A checkpoint traces its planned subtask and interactions with accepted earlier checkpoints. A later unimplemented subtask is outside the checkpoint boundary and is not missing evidence.
29. A checkpoint is blocked only because a later planned subtask is not implemented.
30. A final review reuses checkpoint-limited trace closure and omits another task boundary.
31. A final review traces the complete task inventory.
32. A final review has only unchanged reusable rows. A fresh clean-context subagent validates and composes them before native review.
33. A final review has only unchanged reusable rows. The coordinator composes them without a fresh subagent.
34. Separate component checks execute the production entry, selector, writer, and terminal owner. No one check follows the complete causal path.
35. One named check invokes the production entry. After that call stops, the check calls the selector, writer, and terminal owner independently.
36. One named check invokes the real production entry and follows every in-scope production hop. It uses a deterministic provider fake only after the external boundary and observes the terminal result.
37. One named check invokes the real production entry but replaces the in-scope writer with a success lambda. The terminal result passes without executing that production hop.
38. One named check invokes the real production entry and drives a deterministic callback or async continuation. The continuation follows every in-scope production hop and reaches the terminal result.

Return JSON only. Include:

- `accepted_inventory_checked` with every accepted boundary and both contrast sides.
- One verdict for each numbered record.
- `weak_evidence_rejected` for positive-only, component-only, aggregate-only, and writer-report evidence.
- `duplicate_prefix_omission_blocked`.
- `initial_and_correction_paths_proved`.
- `equal_result_invariant_preserved`.
- `unrelated_gate_fixture_rejected`.
- `traced_changes_invalidate` and `unrelated_document_preserves_closure`.
- `boundary_change_requires_preflight` and `direct_arithmetic_can_use_exception`.
- `all_native_review_modes_gated`.
- `tracked_execplan_status_rejected`.
- `roadmap_only_lifecycle_state`.
- `review_closure_execplan_update_rejected`.
- `resumption_sources_complete`.
- `completed_history_rewrite_rejected`.
- `incomplete_resumption_rejected`.
- `tracked_delivery_status_rejected`.
- `spec_kit_progress_rejected`.
- `untracked_progress_allowed`.
- `coordinator_trace_rejected`.
- `fresh_trace_executor_required`.
- `canonical_coverage_rules_received`.
- `missing_tests_reported`.
- `reuse_only_fresh_executor_required`.
- `checkpoint_future_work_excluded`.
- `final_complete_inventory_required`.
- `separate_component_coverage_rejected`.
- `bundled_component_calls_rejected`.
- `continuous_production_path_required`.
- `external_boundary_fake_allowed`.
- `in_scope_seam_rejected`.
- `deterministic_async_path_allowed`.
- `production_hops_complete`.
- `one_check_traverses_complete_path`.
- `external_boundary_seams`.
- `replaced_in_scope_hops_empty`.
- `exact_missing_path_check_reported`.
- `ordered_trace_inputs_complete`.
- `native_review_independent`.
- `overall` equal to `pass` only when all requirements below are true.

Preflight rejects the incomplete proposed inventory. Trace closure checks every accepted staging case without reinterpreting it. It preserves the equal-result invariant and covers both implementation paths. It rejects the broader helper.

Reject records 1-4, 6, 8-10, 12, 15, 17, 19-21, 23, 26, 29, 30, and 33. Accept records 5, 7, 11, 13, 14, 16, 18, 22, 24, 25, 27, 28, 31, and 32.

Reject records 34, 35, and 37. Accept records 36 and 38.

Report missing tests. Gate every native review mode. Limit checkpoints to current and earlier accepted work. Require complete final closure. Keep tracked lifecycle state only in the roadmap. Permit progress in untracked or ignored working files.

For each accepted production path, list every in-scope hop in `production_hops`. Bind those hops to one exact named check. Do not combine separate checks or disconnected component calls. Permit a seam only after an opaque external boundary. Report the exact missing production-path check when closure fails.

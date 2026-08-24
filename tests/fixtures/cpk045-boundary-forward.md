You are a fresh read-only toolkit verifier. Do not edit files. Read these current rules first:

- `assets/skills/design-preflight/SKILL.md`
- `assets/skills/design-preflight/references/scenario-discrimination.md`
- `assets/skills/design-preflight/references/preflight-review.md`
- `assets/skills/adversarial-review/SKILL.md`

Evaluate the rules through this normal-use defect:

> Subscription staging may substitute a fallback plan only when the base plan is unmapped. A shared reconciliation helper has a broader contract and also substitutes an already-mapped base plan.

Independently derive every behavioral boundary before using any existing `B#` record. Hold other inputs constant. Derive the mapped and unmapped cases, their applicable entry paths, and the terminal staging result. Decide whether the broader helper preserves the requirement.

Apply that derivation to both toolkit entry paths: initial implementation preflight and preflight for an accepted review correction. Decide whether one composed scenario can prove both paths. Also evaluate this invariant: two supported import entry points must preserve the same normalized account identity. Both correct terminal values are equal, but the nearest wrong implementation skips normalization on one path. Decide whether this remains a behavioral boundary and what paired terminal proof it needs.

Test source completeness with these authoritative clauses in order:

- Only unmapped base plans can be substituted during staging.
- Only unmapped base products can be substituted during staging.
- Every supported staging entry point must preserve an already-mapped plan.

An accepted inventory contains only the first two clauses because they look alike. Independently inventory all three clauses and decide whether work can continue.

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

Return JSON only. Include:

- `source_inventory` with every derived boundary and both contrast sides;
- one verdict for each numbered record;
- `weak_evidence_rejected` for positive-only, component-only, aggregate-only, and writer-report evidence;
- `duplicate_prefix_omission_blocked`;
- `initial_and_correction_paths_proved`;
- `equal_result_invariant_preserved`;
- `unrelated_gate_fixture_rejected`;
- `traced_changes_invalidate` and `unrelated_document_preserves_closure`;
- `boundary_change_requires_preflight` and `direct_arithmetic_can_use_exception`;
- `all_native_review_modes_gated`;
- `ordered_trace_inputs_complete`;
- `native_review_independent`;
- `overall` equal to `pass` only if the rules derive all source clauses and both staging cases; preserve the equal-result invariant; cover initial and correction paths; reject the broader helper and records 1-4, 6, 8-10, and 12; accept records 5, 7, 11, 13, and 14; and gate every native review mode.

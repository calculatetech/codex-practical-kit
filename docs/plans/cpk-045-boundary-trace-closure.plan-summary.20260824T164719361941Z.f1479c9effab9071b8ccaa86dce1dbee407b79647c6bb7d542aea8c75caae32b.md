<proposed_plan>
# CPK-045 — Close Every Behavioral Boundary

## Summary

The existing design rule is correct, but its enforcement is incomplete.

Scenario Proof has no denominator that proves every explicit boundary was considered. It also lacks a post-implementation conformance gate.

Release the correction as version `0.23.0`. Create `cpk-045-boundary-trace-closure` from commit `388b23f`.

## Research Decision

NeuroArxiv searched `cs.SE`, `cs.AI`, and `cs.PL`. It read 12 abstracts across four approaches:

- Traceability: [T-SimCSE](https://arxiv.org/abs/2603.11800) `[rel7 prac7 rig8]`, [legal traceability](https://arxiv.org/abs/2502.04916) `[rel5 prac7 rig8]`, [TraceLLM](https://arxiv.org/abs/2602.01253) `[rel8 prac6 rig8]`.
- Evidence gates: [PROBE](https://arxiv.org/abs/2605.08717) `[rel8 prac8 rig8]`, [context compression](https://arxiv.org/abs/2605.11051) `[rel7 prac5 rig6]`, [embodied agents](https://arxiv.org/abs/2510.21902) `[rel3 prac5 rig6]`.
- Executable properties: [metamorphic adequacy](https://arxiv.org/abs/2412.20692) `[rel8 prac7 rig8]`, [substructural PBT](https://arxiv.org/abs/2108.01610) `[rel6 prac3 rig6]`, [ConCert](https://arxiv.org/abs/2208.00758) `[rel7 prac3 rig7]`, [programmable PBT](https://arxiv.org/abs/2602.18545) `[rel8 prac4 rig6]`, [αCheck](https://arxiv.org/abs/1604.08345) `[rel5 prac3 rig7]`.
- Intent-driven regression: [Cleverest](https://arxiv.org/abs/2501.11086) `[rel8 prac7 rig9]`.

The selected path is an external boundary trace with an evidence gate. Planning writes it. Implementation and tests must close it.

Avoid semantic-similarity ranking, a formal property language, mutation tooling, and post-failure recovery machinery. These approaches add cost without proving source completeness.

OpenAI’s [ExecPlan guidance](https://developers.openai.com/cookbook/articles/codex_exec_plans/) requires self-contained plans and observable validation. It does not provide a boundary-trace gate. The toolkit must own this mechanism.

## Implementation Changes

### CP1 — Create the complete boundary inventory

Extend the existing Scenario Discrimination owner. Do not add a skill or another durable plan.

Before implementation:

- Enumerate every in-scope requirement that limits, selects, excludes, relates, or preserves an outcome.
- Give each boundary a stable `B#` identifier.
- Record its source, condition or invariant, both sides, required oracles, applicable entry points, and Scenario Proof rows.
- Classify every relevant source clause as mapped, non-boundary, opaque, deferred, or contract gap.
- Inspect the complete source set. Do not stop after duplicate-looking clauses.
- Require one scenario per distinct production path unless one composed scenario proves all paths.
- Permit invariant boundaries whose correct results are equal. Their contrast must expose the nearest wrong behavior.
- Make any new or changed behavioral boundary override the small-change exception. Direct bugs with no boundary change retain the exception.

Add the boundary inventory to the existing preflight card and Phase 1 result. Merge the accepted inventory into the task ExecPlan.

### CP2 — Add trace closure before native review

After implementation and final documentation, run one fresh read-only trace-closure verifier.

Give it the raw requirement sources, accepted inventory, Scenario Proof, current diff, production source, and tests. It must independently enumerate the source boundaries before it checks existing `B#` records.

Add this result shape to the existing preflight review interface:

```json
{
  "reviewer": "boundary-trace-closure",
  "source_inventory_complete": true,
  "missing_or_unsupported": [],
  "boundaries": [
    {
      "boundary_id": "B1",
      "path_id": "P1",
      "entry_point": "path:line",
      "gates": ["path:line"],
      "enforcement_point": "path:line",
      "terminal_owner": "path:line",
      "implementation_matches": true,
      "fixture_matches_discriminator": true,
      "nearest_wrong_meaning_would_fail": true,
      "both_sides_executed": true,
      "terminal_oracle_reached": true,
      "check": "exact command",
      "result": "pass"
    }
  ],
  "decision": "pass"
}
```

Any `false`, `unknown`, missing boundary, unsupported classification, or missing path blocks native review.

The verifier must inspect the test body. A positive-only check, component check, aggregate suite result, or writer report cannot close a boundary.

Run trace closure immediately before native review. Invalidate it after changes to requirements, boundary records, production paths, or named tests.

Keep native `codex review` independent. Do not send it the trace record.

## Test Plan

Add focused contract tests that prove:

- Every authoritative clause receives a disposition.
- A later distinct boundary cannot hide behind duplicate-looking clauses.
- Mapped and unmapped inputs produce the required subscription-staging outcomes.
- Equal-result invariants remain valid boundaries.
- Every applicable production entry point receives proof.
- A positive-only test blocks review.
- A fixture that changes the discriminator and an unrelated gate blocks review.
- A broader helper fails `nearest_wrong_meaning_would_fail`.
- A traced documentation or implementation change invalidates closure.
- A direct arithmetic bug with no boundary change retains the small-change exception.

Run one clean-context forward test with the supplied broader-helper defect. Phase 1 must derive both mapped and unmapped cases. Trace closure must reject the broader implementation and positive-only test.

Run all toolkit tests, skill validation, Python and shell checks, PowerShell parsing, rule-owner checks, link checks, manifest validation, and `git diff --check`.

Use reviewed checkpoints for CP1 and CP2. Then run one final complete-candidate native review. Install the reviewed candidate and require Doctor to report `Result: ready`.

## Assumptions and Defaults

- This mechanism reduces semantic omissions. It does not claim formal completeness.
- The fresh closure verifier is the semantic gate. No parser or coverage percentage is added.
- Documentation is final before trace closure.
- Review Closure updates do not invalidate trace closure unless they change a traced source.
- CPK-045 becomes the only Active roadmap task during implementation.
- Local commits do not authorize publication.

## Prior Plan Reconciliation

- CPK-040 is carried. Plan capture remains unchanged.
- CPK-041 is carried. Material decisions still require source-backed effects.
- CPK-042 is carried. CP1 and CP2 use reviewed checkpoints and one final review.
- CPK-043 is carried. Pull-request sequencing remains unchanged.
- CPK-044 is carried. Native review and correction authority remain unchanged.
- CPK-022, CPK-028, CPK-034, and CPK-035 remain authoritative. CPK-045 adds source completeness and post-implementation closure.

<!-- cpk-plan-spec: docs/plans/cpk-045-boundary-trace-closure.md -->
</proposed_plan>
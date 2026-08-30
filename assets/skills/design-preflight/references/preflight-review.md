# Preflight review result

## Product scope

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](scope-boundaries.md)

## Phase 1 result

Return JSON only.

```json
{
  "reviewer": "normal-use-scenarios",
  "source_scope": {
    "initial_sources": ["path:line-line"],
    "expansions": [
      {
        "source": "path:line-line",
        "basis": "authoritative-product-boundary | direct-composing-owner",
        "evidence": "Source-backed reason this source can change the accepted outcome"
      }
    ]
  },
  "product_boundary": {
    "sources": ["path:line-line"],
    "current_production_use_cases": ["Documented use case"],
    "owners": [
      {
        "owner": "Owner name",
        "classification": "composes | opaque | deferred",
        "source": "path:line-line"
      }
    ],
    "inherited_specification_conflicts": []
  },
  "source_clauses": [
    {
      "source": "path:line-line",
      "clause": "Authoritative clause",
      "disposition": "mapped | non-boundary | opaque | deferred | contract-gap",
      "boundary_id": "B1 | null"
    }
  ],
  "boundaries": [
    {
      "id": "B1",
      "source": ["path:line-line"],
      "condition_or_invariant": "Explicit behavioral boundary",
      "contrast_sides": ["Required side", "Nearest contrasting side"],
      "required_oracles": ["Observable terminal result"],
      "production_entry_points": ["Entry point"],
      "scenario_ids": ["S1"]
    }
  ],
  "scenarios": [
    {
      "id": "S1",
      "lens": "input-domain | path-and-transition | collection-semantics",
      "source": ["path:line-line"],
      "requirement": "Explicit required result",
      "given": "Normal starting condition",
      "when": "Project-controlled trigger",
      "then": "Required result",
      "discriminator": "Requirement-derived dimension varied independently",
      "contrast": "Minimal paired input or seeded state that exposes the nearest wrong meaning",
      "production_path": ["Entry point", "State owner", "Terminal owner"],
      "required_oracle": "Observable terminal result",
      "planned_check": "Runnable test or command that exercises the complete path",
      "supported_model": {
        "normal_use": true,
        "project_controls_it": true,
        "feasible_without_fault_injection": true,
        "explicit_result_defined": true
      }
    }
  ],
  "contract_gaps": [
    {
      "id": "C1",
      "source": ["path:line-line"],
      "trigger": "Normal project-controlled trigger",
      "current_path": "Current reproducible result",
      "missing_decision": "Undefined public result",
      "supported_model": {
        "normal_use": true,
        "project_controls_it": true,
        "feasible_without_fault_injection": true,
        "explicit_result_defined": false
      }
    }
  ],
  "exclusions": [
    {
      "case": "Excluded condition",
      "reason": "Not normal use, not project-controlled, or not feasible without fault injection"
    }
  ],
  "coverage": {
    "input_domain": ["Source predicates inspected"],
    "paths_and_transitions": ["Retained-work reopening, shared-owner event gates, and authoritative-result entry points inspected"],
    "collection_semantics": ["Applicable collection rules inspected"]
  }
}
```

Apply [Scenario discrimination](scenario-discrimination.md) to every retained scenario. Apply [Owner composition](owner-composition.md) and [Full-set results](full-set-results.md) to the independent result.

The coordinator must compare the source clauses with the complete source packet inside the accepted task boundary. It must verify every `source_scope` expansion against authoritative product-boundary evidence or a direct composing-owner relationship. It must verify each boundary, discriminator, contrast, production path, oracle, and planned runnable check. Do not create a Cartesian product.

Use the canonical classifications to fill `scenarios`, `contract_gaps`, and `exclusions`. Empty arrays are valid.

## Phase 2 result

After the coordinator supplies the complete card and its decisions, return JSON only.

```json
{
  "reviewer": "preflight-adversary",
  "findings": [
    {
      "kind": "missing-scenario | unsupported-assumption | invalid-exclusion | weak-proof | contract-gap",
      "source": ["path:line-line"],
      "coordinator_claim": "Exact card claim under challenge",
      "counterexample": "Smallest supported case that disproves or weakens the claim",
      "wrong_terminal_result": "Observable result if the card remains unchanged",
      "required_card_change": "Smallest correction to the card and runnable check",
      "supported_model": {
        "normal_use": true,
        "project_controls_it": true,
        "feasible_without_fault_injection": true,
        "explicit_result_defined": true
      }
    }
  ],
  "coverage": {
    "decisions": ["Coordinator decisions inspected"],
    "assumptions": ["Coordinator assumptions inspected"],
    "exclusions": ["Coordinator exclusions inspected"],
    "proofs": ["Scenario discriminators, contrasts, paths, oracles, and checks inspected"],
    "contracts": ["Public results inspected for undefined behavior"]
  }
}
```

Empty `findings` is valid. Every finding must cite source and name the coordinator claim that it challenges.

## Trace closure result

The coordinator gives one fresh clean-context read-only subagent the canonical Scenario Discrimination, Owner Composition, and Full-set Results rules. It gives the subagent the accepted `B#` inventory, Scenario Proof, and exact review boundary. It also gives the current diff, production sources, named test bodies, and test results. It gives reusable checkpoint closures or an explicit empty set. Do not derive requirements again. Return JSON only.

```json
{
  "reviewer": "boundary-trace-closure",
  "executor": {
    "role": "fresh-clean-context-subagent",
    "read_only": true,
    "inherited_task_conversation": false
  },
  "canonical_rules_received": ["scenario-discrimination", "owner-composition", "full-set-results"],
  "review_mode": "full | checkpoint | delta | final",
  "review_boundary": "Complete task | stable subtask and earlier-checkpoint interactions | correction and direct impact",
  "accepted_boundary_ids": ["B1"],
  "closed_boundary_ids": ["B1"],
  "unclosed_or_invalidated": [],
  "missing_tests": [],
  "reused_checkpoint_closures": [{"checkpoint": "commit-or-tree", "boundary_ids": ["B1"]}],
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

Apply [Scenario discrimination](scenario-discrimination.md). Any false, unknown, missing, unsupported, or unclosed value makes `decision` equal `fail`.

The coordinator rejects a result from any other execution source. A nonempty `missing_tests` value makes `decision` equal `fail` and blocks native review.

## Supported-model classification

<!-- cpk-rule-route-only: supported-model -->
[Supported model](supported-model.md)

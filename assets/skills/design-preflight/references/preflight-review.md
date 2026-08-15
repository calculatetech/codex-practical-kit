# Preflight review result

## Product scope

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](../../codex-practical-kit-rules/references/scope-boundaries.md)

## Result

Return JSON only.

```json
{
  "reviewer": "normal-use-scenarios",
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
  "scenarios": [
    {
      "id": "S1",
      "lens": "input-domain | path-and-transition | collection-semantics",
      "source": ["path:line-line"],
      "requirement": "Explicit required result",
      "given": "Normal starting condition",
      "when": "Project-controlled trigger",
      "then": "Required result",
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

Apply [Owner composition](../../codex-practical-kit-rules/references/owner-composition.md) and [Full-set results](../../codex-practical-kit-rules/references/full-set-results.md) to the independent result.

The coordinator must add the applicable runnable checks to the accepted Scenario Proof. Do not create a Cartesian product.

Use the canonical classifications to fill `scenarios`, `contract_gaps`, and `exclusions`. Empty arrays are valid.

## Supported-model classification

<!-- cpk-rule-route-only: supported-model -->
[Supported model](../../codex-practical-kit-rules/references/supported-model.md)

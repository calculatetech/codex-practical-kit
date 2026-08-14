# Preflight review result

Return JSON only.

```json
{
  "reviewer": "normal-use-scenarios",
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
    "paths_and_transitions": ["Owners and gates inspected"],
    "collection_semantics": ["Applicable collection rules inspected"]
  }
}
```

Keep a scenario only when all four values are `true`. Put a case in `contract_gaps` only when the first three values are `true` and `explicit_result_defined` is `false`. Otherwise, put it in `exclusions`. Empty arrays are valid.

# Finding format

Return JSON only.

```json
{
  "reviewer": "correctness",
  "findings": [
    {
      "id": "R1",
      "severity": "P0 | P1 | P2 | P3",
      "confidence": 100,
      "title": "Concrete wrong outcome",
      "location": ["path:line-line"],
      "trigger": "Supported normal-use trigger",
      "execution_path": ["Step 1", "Step 2"],
      "wrong_outcome": "Observable requirement violation",
      "supported_model": {
        "normal_use": true,
        "project_controls_it": true,
        "reproducible_without_fault_injection": true,
        "violates_explicit_requirement": true
      },
      "smallest_fix_direction": "One bounded correction",
      "verification": "One check"
    }
  ],
  "coverage": ["Source and callers read"]
}
```

Drop a finding unless all four `supported_model` values are `true`. An empty findings list is valid.

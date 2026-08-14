# Preflight review result

Return JSON only.

```json
{
  "reviewer": "scope-and-ownership",
  "findings": [
    {
      "id": "P1",
      "severity": "blocking | important | advisory",
      "confidence": 100,
      "title": "Concrete normal-use gap",
      "source": ["path:line-line"],
      "scenario": ["Normal trigger", "Current path", "Wrong result"],
      "supported_model": {
        "normal_use": true,
        "project_controls_it": true,
        "reproducible_without_fault_injection": true,
        "violates_explicit_requirement": true
      },
      "smallest_correction": "One bounded correction"
    }
  ],
  "coverage": ["Source read"]
}
```

Drop a finding unless all four values are `true`. An empty findings list is valid.

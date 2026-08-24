# Finding adjudication format

Use this record after discovery. The reviewer does not complete it.

## Product scope

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](../../design-preflight/references/scope-boundaries.md)

## Result

Record one object for every candidate finding in source order.

```json
{
  "source": "native-local | github-codex | human | ci | audit | user",
  "source_id": "Stable source label",
  "finding": {
    "title": "Concrete observation",
    "location": ["path:line-line"],
    "trigger": "Supported normal-use trigger",
    "execution_path": ["Step 1", "Step 2"],
    "claimed_outcome": "Observable result"
  },
  "end_result": {
    "classification": "wrong | unchanged | undefined",
    "accepted_result": "Existing required result, or none",
    "reason": "One source-backed reason"
  },
  "task_scope": {
    "classification": "composes | opaque | deferred",
    "boundary_source": "path:line-line",
    "changed_production_entry_point": "path:line-line, or none",
    "task_visible_wrong_result": "Observable requirement violation, or none"
  },
  "supported_model": {
    "normal_use": true,
    "project_controls_it": true,
    "reproducible_without_fault_injection": true,
    "explicit_requirement_defines_result": true
  },
  "validated_severity": "P0 | P1 | P2 | P3 | none",
  "correction_authority": {
    "classification": "direct repair | decision required | excluded | contract gap | severe stop",
    "required_result_exists": true,
    "existing_owner": "path or none",
    "only_restores_required_result": true,
    "adds": ["none"],
    "direct_regression_check": "One check, or none",
    "small_change_exception": true
  }
}
```

Do not copy raw reviewer severity or a suggested fix into correction authority. `unchanged` is `excluded`. `undefined` becomes a `contract gap` when it passes the scope and supported-model gates.

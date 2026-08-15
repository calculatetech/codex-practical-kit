<!-- cpk-rule-owner: scope-boundaries -->
<!-- cpk-rule-guard: A broader specification does not import every owner or lifecycle into a focused task. -->
<!-- cpk-rule-guard: Code reachability, shared storage, and future roadmap work do not prove task relevance. -->
<!-- cpk-rule-guard: Apply the scope gate before the supported-model gate. -->

# Scope boundaries

The authoritative product specification must identify:

- Current production use cases.
- Supporting owners whose current behavior must remain unchanged.
- Deferred placeholders for future development.
- The condition that promotes a deferred placeholder into supported behavior.

A task contract or ExecPlan links these product facts. It classifies each relevant owner without copying this rule:

- `composes`: The task implements or reviews this owner.
- `opaque`: The task preserves its documented current behavior. The task does not add lifecycle obligations to it.
- `deferred`: The owner is a placeholder for future development. Exclude it unless the task explicitly promotes it.

A broader specification does not import every owner or lifecycle into a focused task.

Code reachability, shared storage, and future roadmap work do not prove task relevance.

If a raw requirement conflicts with an inherited specification, Design Preflight records a contract gap and stops before implementation.

Apply the scope gate before the supported-model gate.

For `composes`, derive task scenarios and review the required result. For `opaque`, keep only a direct regression that the task diff causes in documented current behavior. Do not invent a new obligation. For `deferred`, omit scenarios and findings unless the task promotes the owner.

Every retained review finding must cite the boundary source and classification. It must name the changed production entry point and the task-visible wrong result.

Drop an observation that has no such trace. Do not fix it, count it, diagnose it, or add it to the roadmap.

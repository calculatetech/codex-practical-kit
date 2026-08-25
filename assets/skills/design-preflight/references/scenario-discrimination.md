<!-- cpk-rule-owner: scenario-discrimination -->
<!-- cpk-rule-guard: Each retained scenario names a requirement-derived discriminator and a minimal contrast that makes the nearest wrong meaning observable. -->
<!-- cpk-rule-guard: Hold unrelated factors constant when practical and split a row when one contrast cannot prove all claimed outcomes. -->
<!-- cpk-rule-guard: A runnable check is insufficient when the named requirement can be false while the check passes. -->
<!-- cpk-rule-guard: Give every authoritative source clause one explicit disposition before implementation. -->
<!-- cpk-rule-guard: Trace closure maps each accepted behavioral boundary to every applicable production entry point. -->
<!-- cpk-rule-guard: Treat an invariant as a boundary when its nearest wrong meaning changes the result. -->
<!-- cpk-rule-guard: Trace closure uses the accepted B# inventory and cannot reinterpret it. -->
<!-- cpk-rule-guard: Any false, unknown, missing, or unsupported trace-closure result blocks native review. -->
<!-- cpk-rule-guard: Invalidate only closure rows affected by a changed boundary, production path, or named test. -->
<!-- cpk-rule-guard: Run trace closure only for executable production-code behavior with a real runnable entry point. -->

# Scenario discrimination

Apply this rule to each retained Scenario Proof row.

## Boundary inventory

Give every authoritative source clause one explicit disposition before implementation. Use `mapped`, `non-boundary`, `opaque`, `deferred`, or `contract-gap`. Do not stop after duplicate-looking clauses.

A behavioral boundary is an explicit requirement that limits, selects, excludes, relates, or preserves an outcome. Give each mapped boundary a stable `B#` identifier. Record its source, condition or invariant, both contrast sides, and required oracles. The accepted preflight inventory also records its applicable production entry points and Scenario Proof rows.

Use one scenario for each distinct production path. One composed scenario is sufficient only when it proves all paths. Treat an invariant as a boundary when its nearest wrong meaning changes the result. The correct result can stay equal on both sides. Use the nearest wrong meaning as the contrast.

A task that adds or changes a behavioral boundary cannot use the Design Preflight small-change exception. A direct bug that changes no boundary can retain the exception.

Each retained scenario names a requirement-derived discriminator and a minimal contrast that makes the nearest wrong meaning observable.

The discriminator is one identity, value, state, time, source, or event whose documented meaning the scenario proves. Derive it from the explicit requirement and actual production path.

The contrast is the smallest paired input or seeded state that makes the required meaning and the nearest wrong meaning produce different terminal results. Do not invent speculative faults.

Hold unrelated factors constant when practical and split a row when one contrast cannot prove all claimed outcomes.

Follow the production path to the required terminal oracle. A runnable check is insufficient when the named requirement can be false while the check passes.

Before implementation, record the discriminator, contrast, production path, required oracle, and planned check. Before review, run the named check and keep its result in the ignored task-result record. An aggregate suite result is supporting evidence only.

## Trace closure

Run trace closure only for executable production-code behavior with a real runnable entry point. Do not run trace closure for skills, rules, documentation, tests, or static configuration. Use their deterministic checks and native review.

The accepted `B#` inventory is the only semantic input to trace closure. Freeze it in the ExecPlan before implementation. Trace closure uses the accepted B# inventory and cannot reinterpret it. It cannot add, remove, split, merge, rename, or reinterpret a boundary. A requirement change requires preflight and an explicit inventory revision first.

After implementation and final substantive documentation, apply this rule: Trace closure maps each accepted behavioral boundary to every applicable production entry point. Inspect the production paths and test bodies. This is an evidence check, not a second requirements review.

Match trace scope to native-review scope. `checkpoint` traces the current planned subtask and its interactions with accepted earlier checkpoints. Later unimplemented subtasks are outside that boundary. `delta` traces the correction and its direct impact. `full` traces all still-open rows. `final` composes accepted checkpoint closures and traces only rows that are new, unclosed, or invalidated. The final native review still reviews the complete candidate.

For each boundary and applicable entry point, require the gates, enforcement point, terminal owner, both contrast sides, terminal oracle, exact check, and result. The fixture must isolate the discriminator. The nearest wrong meaning must fail.

Any false, unknown, missing, or unsupported trace-closure result blocks native review. Trace closure contains only values inside the selected review boundary. A positive-only check, component check, aggregate suite result, or writer report cannot close a boundary.

For an eligible executable production-code candidate with a boundary inventory, run trace closure immediately before each native review. Bind each closure row to its reviewed checkpoint. Reuse that row while its accepted boundary, production path, and named test are unchanged. Invalidate only closure rows affected by a changed boundary, production path, or named test. An unrelated documentation change does not invalidate closure.

Do not give the trace record to native review. Native discovery remains independent.

Do not require mutation-testing software, coverage metrics, or exhaustive combinations.

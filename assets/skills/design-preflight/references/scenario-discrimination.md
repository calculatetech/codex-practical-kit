<!-- cpk-rule-owner: scenario-discrimination -->
<!-- cpk-rule-guard: Each retained scenario names a requirement-derived discriminator and a minimal contrast that makes the nearest wrong meaning observable. -->
<!-- cpk-rule-guard: Hold unrelated factors constant when practical and split a row when one contrast cannot prove all claimed outcomes. -->
<!-- cpk-rule-guard: A runnable check is insufficient when the named requirement can be false while the check passes. -->
<!-- cpk-rule-guard: Give every authoritative source clause one explicit disposition before implementation. -->
<!-- cpk-rule-guard: Trace closure maps each accepted behavioral boundary to every applicable production entry point. -->
<!-- cpk-rule-guard: Treat an invariant as a boundary when its nearest wrong meaning changes the result. -->
<!-- cpk-rule-guard: Trace closure uses the accepted B# inventory and cannot reinterpret it. -->
<!-- cpk-rule-guard: One fresh clean-context read-only subagent executes every eligible trace closure, including a reuse-only closure. -->
<!-- cpk-rule-guard: Any false, unknown, missing, or unsupported trace-closure result blocks native review. -->
<!-- cpk-rule-guard: Invalidate only closure rows affected by a changed boundary, production path, or named test. -->
<!-- cpk-rule-guard: Run trace closure only for executable production-code behavior with a real runnable entry point. -->
<!-- cpk-rule-guard: Every production-path fact in a trace row comes from that row's one exact named check. -->

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

Apply [Owner composition](owner-composition.md) to each production path. Every production-path fact in a trace row comes from that row's one exact named check.

One fresh clean-context read-only subagent executes every eligible trace closure, including a reuse-only closure.

The coordinator must spawn this subagent with no inherited task conversation. Set `fork_turns` to `none`. The coordinator cannot execute or attest trace closure. The subagent must not edit, delegate, run Design Preflight, start another trace closure, or start native review. It returns one structured result to the coordinator.

Give the subagent these canonical rules: this file, [Owner composition](owner-composition.md), and [Full-set results](full-set-results.md). Give it the accepted `B#` inventory, Scenario Proof, and exact review boundary. Give it the current diff, production sources, named test bodies, and test results. Give it every valid reusable closure row or an explicit empty set. The subagent reports every missing test obligation before native review.

Match trace scope to native-review scope. `checkpoint` traces the current planned subtask and its interactions with accepted earlier checkpoints. Later unimplemented subtasks are outside that boundary. `delta` traces the correction and its direct impact. `full` traces all still-open rows. For `final`, the fresh subagent validates and composes accepted checkpoint closures, then traces rows that are new, unclosed, or invalidated. The final native review still reviews the complete candidate.

For each boundary and applicable entry point, require the production hops, gates, enforcement point, terminal owner, both contrast sides, terminal oracle, exact check, and result. The fixture must isolate the discriminator. The nearest wrong meaning must fail.

Any false, unknown, missing, or unsupported trace-closure result blocks native review. Trace closure contains only values inside the selected review boundary. A positive-only check, component check, aggregate suite result, or writer report cannot close a boundary.

A missing production hop, unsupported external seam, or replaced in-scope hop adds an exact obligation to `missing_tests` and blocks native review.

For an eligible executable production-code candidate with a boundary inventory, run trace closure immediately before each native review. Bind each closure row to its reviewed checkpoint and fresh verifier result. Reuse that row only when a fresh verifier previously closed it and its accepted boundary, production path, and named test are unchanged. Invalidate only closure rows affected by a changed boundary, production path, or named test. An unrelated documentation change does not invalidate closure. A fresh subagent still validates a reuse-only closure invocation.

Do not give the trace record to native review. Native discovery remains independent.

Do not require mutation-testing software, coverage metrics, or exhaustive combinations.

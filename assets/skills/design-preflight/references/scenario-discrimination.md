<!-- cpk-rule-owner: scenario-discrimination -->
<!-- cpk-rule-guard: Each retained scenario names a requirement-derived discriminator and a minimal contrast that makes the nearest wrong meaning observable. -->
<!-- cpk-rule-guard: Hold unrelated factors constant when practical and split a row when one contrast cannot prove all claimed outcomes. -->
<!-- cpk-rule-guard: A runnable check is insufficient when the named requirement can be false while the check passes. -->
<!-- cpk-rule-guard: Give every authoritative source clause one explicit disposition before implementation. -->
<!-- cpk-rule-guard: Each behavioral boundary names every applicable production entry point and both sides of its contrast. -->
<!-- cpk-rule-guard: Treat an invariant as a boundary when its nearest wrong meaning changes the result. -->

# Scenario discrimination

Apply this rule to each retained Scenario Proof row.

## Boundary inventory

Give every authoritative source clause one explicit disposition before implementation. Use `mapped`, `non-boundary`, `opaque`, `deferred`, or `contract-gap`. Do not stop after duplicate-looking clauses.

A behavioral boundary is an explicit requirement that limits, selects, excludes, relates, or preserves an outcome. Give each mapped boundary a stable `B#` identifier. Record its source, condition or invariant, required oracles, and Scenario Proof rows. Each behavioral boundary names every applicable production entry point and both sides of its contrast.

Use one scenario for each distinct production path. One composed scenario is sufficient only when it proves all paths. Treat an invariant as a boundary when its nearest wrong meaning changes the result. The correct result can stay equal on both sides. Use the nearest wrong meaning as the contrast.

A task that adds or changes a behavioral boundary cannot use the Design Preflight small-change exception. A direct bug that changes no boundary can retain the exception.

Each retained scenario names a requirement-derived discriminator and a minimal contrast that makes the nearest wrong meaning observable.

The discriminator is one identity, value, state, time, source, or event whose documented meaning the scenario proves. Derive it from the explicit requirement and actual production path.

The contrast is the smallest paired input or seeded state that makes the required meaning and the nearest wrong meaning produce different terminal results. Do not invent speculative faults.

Hold unrelated factors constant when practical and split a row when one contrast cannot prove all claimed outcomes.

Follow the production path to the required terminal oracle. A runnable check is insufficient when the named requirement can be false while the check passes.

Before implementation, record the discriminator, contrast, production path, required oracle, and planned check. Before review, run the named check, record its result, and verify each retained row. An aggregate suite result is supporting evidence only.

Do not require mutation-testing software, coverage metrics, or exhaustive combinations.

<!-- cpk-rule-owner: scenario-discrimination -->
<!-- cpk-rule-guard: Each retained scenario names a requirement-derived discriminator and a minimal contrast that makes the nearest wrong meaning observable. -->
<!-- cpk-rule-guard: Hold unrelated factors constant when practical and split a row when one contrast cannot prove all claimed outcomes. -->
<!-- cpk-rule-guard: A runnable check is insufficient when the named requirement can be false while the check passes. -->

# Scenario discrimination

Apply this rule to each retained Scenario Proof row.

Each retained scenario names a requirement-derived discriminator and a minimal contrast that makes the nearest wrong meaning observable.

The discriminator is one identity, value, state, time, source, or event whose documented meaning the scenario proves. Derive it from the explicit requirement and actual production path.

The contrast is the smallest paired input or seeded state that makes the required meaning and the nearest wrong meaning produce different terminal results. Do not invent speculative faults.

Hold unrelated factors constant when practical and split a row when one contrast cannot prove all claimed outcomes.

Follow the production path to the required terminal oracle. A runnable check is insufficient when the named requirement can be false while the check passes.

Before implementation, record the discriminator, contrast, production path, required oracle, and planned check. Before review, run the named check, record its result, and verify each retained row. An aggregate suite result is supporting evidence only.

Do not require mutation-testing software, coverage metrics, or exhaustive combinations.

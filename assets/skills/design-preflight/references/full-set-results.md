<!-- cpk-rule-owner: full-set-results -->
<!-- cpk-rule-guard: Do not limit raw records before grouping, deduplication, or aggregation. -->
<!-- cpk-rule-guard: Test duplicate prefix values followed by a later counterexample. -->

# Full-set results

When success depends on every matching record, use the complete set. An operation can also preserve the full-set result without materializing all records.

Do not limit raw records before grouping, deduplication, or aggregation.

Test an empty supported set, one record, duplicates, and every record that owes a result.

Test duplicate prefix values followed by a later counterexample.

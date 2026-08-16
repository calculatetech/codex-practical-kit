<!-- cpk-rule-owner: review-closure -->
<!-- cpk-rule-guard: Review closure is limited to four updates: the task ExecPlan review result, reviewed task roadmap transition, matching checksums, and untracked test-result record. -->
<!-- cpk-rule-guard: A behavior or supported-model change invalidates review. -->

# Review closure

Review closure does not invalidate a clean review.

Review closure is limited to four updates: the task ExecPlan review result, reviewed task roadmap transition, matching checksums, and untracked test-result record.

A change to code, tests, dependencies, migrations, runtime configuration, build configuration, or security configuration invalidates review.

A behavior or supported-model change invalidates review.

After these updates, review closure is complete.

## Delivery boundary

<!-- cpk-rule-route-only: delivery-lifecycle -->
[Delivery lifecycle](../../delivery-lifecycle/references/delivery-lifecycle.md)

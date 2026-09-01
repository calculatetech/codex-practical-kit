<proposed_plan>
# CPK-053 — Require Continuous Production-Path Proof

## Summary

The trace gap is structural: current closure records entry points, gates, owners, checks, and terminal results separately. A verifier can combine component evidence even though no test traverses the complete production path.

Implement this bugfix on branch `fix/cpk-053-continuous-path-proof` from `ee3aa1464e4a`. Release version `0.23.7`.

## Key Changes

- Keep Owner Composition as the single owner of traversal rules:
  - One named runnable check must invoke the real production entry point.
  - Each proof case must causally traverse every in-scope production owner or hop and reach the terminal oracle.
  - Separate component tests fail, as do disconnected component calls bundled inside one test.
  - Deterministic callbacks and async continuations are valid when the check drives them. Concurrent ordering remains excluded unless a product requirement enables it.
  - Fakes can replace only opaque external systems. Replacing an in-scope hop leaves the path unclosed.
- Make Scenario Discrimination bind every path fact in a closure row to that row’s exact named check. Link to Owner Composition without copying its traversal rules.
- Extend the trace result interface with:
  - `production_hops`: the complete in-scope hop inventory.
  - `one_check_traverses_complete_path`: must be `true`.
  - `external_boundary_seams`: permitted external seams, or an empty list.
  - `replaced_in_scope_hops`: must be empty.
- Fail closure and add an exact `missing_tests` obligation when continuity, hop coverage, or seam placement is false, missing, unknown, or unsupported.
- Add the stable CPK-053 ExecPlan and roadmap result. Update `KIT_VERSION` and its exact assertion to `0.23.7`, then regenerate `MANIFEST.sha256`. Add no skill, parser, instrumentation, dependency, or second rule owner.

## Test Plan

Update the existing focused tests and CPK-045 forward fixture to prove:

- Separate component tests cannot collectively close a path.
- Disconnected component calls inside one test body also fail.
- One real-entry traversal through every production hop passes.
- An external-provider fake passes; an in-scope writer or loader fake fails.
- A deterministically driven callback or async continuation passes.
- Every production entry point receives proof during initial and correction preflight.
- Full, checkpoint, delta, final, and reuse-only closure enforce the same rule.
- Missing traversal proof appears in `missing_tests`.
- Static toolkit rules remain outside semantic trace closure.
- Fresh trace-executor and native-review independence remain unchanged.
- The unique-owner test rejects copied guard text.

Run the focused unit tests, the clean-context forward fixture, `./run-tests.sh`, shell and PowerShell syntax checks, `git diff --check`, and `sha256sum --check MANIFEST.sha256`.

## Delivery

Use one reviewed checkpoint because this is one coherent correction. Run deterministic checks and native review; do not run semantic trace closure on this static rule change. After a clean final review, commit the candidate, install that exact commit into the live environment, and require Doctor to report version `0.23.7` and `Result: ready`. Do not push until publication is separately requested.

## Assumptions

- “End-to-end” means the real in-repository path, not live third-party infrastructure.
- A named check may be parameterized, but every proof case must traverse the complete causal path.
- Existing gate, enforcement, and terminal fields remain; `production_hops` supplies the previously missing complete inventory.
- This is a patch-level process defect correction, not a new feature.
</proposed_plan>
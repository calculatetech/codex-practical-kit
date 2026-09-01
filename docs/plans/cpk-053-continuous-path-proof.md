# Require Continuous Production-Path Proof

This ExecPlan is the stable implementation specification for CPK-053. Maintain it according to `.agent/PLANS.md`.

## Purpose

Trace closure records entry points, gates, owners, checks, and terminal results as separate facts. A verifier can combine component evidence even when no check traverses the complete production path.

After this change, one named runnable check must prove each accepted production path. The check must invoke the real repository entry point. Each proof case must follow one causal path through every in-scope production hop to the terminal oracle.

This bugfix uses version `0.23.7`. Work occurs on branch `fix/cpk-053-continuous-path-proof` from `main` at `ee3aa1464e4adebdff43ff8bee3a01c52d6c9221`. The isolation form is one task branch.

## Applicable Plan History

- `.agent/plan-history/plan-summary.20260901T024803899174Z.f5becdd56d889aba50bf375a29ab0feb9012128e404e73e7a664e0243eb5ab8f.md`
- `docs/plans/cpk-053-continuous-path-proof.plan-summary.20260901T024803899174Z.f5becdd56d889aba50bf375a29ab0feb9012128e404e73e7a664e0243eb5ab8f.md`

The two records contain identical bytes. The central record supports repository discovery. The sibling record links this specification to the accepted Plan.

## Decision Log

- Decision: Keep Owner Composition as the only owner of causal path and seam rules.
  Rationale: One shared owner prevents rule drift and covers each trace consumer.
- Decision: Add one ordered `production_hops` list instead of required and observed lists.
  Rationale: The exact named check supplies the observation evidence. A second list would duplicate the path inventory.
- Decision: Permit deterministic callbacks and async continuations that the check drives.
  Rationale: Causal traversal does not require one synchronous call stack.
- Decision: Exclude concurrent thread ordering unless an accepted product requirement includes it.
  Rationale: The supported model does not include nondeterministic ordering by default.
- Decision: Use deterministic checks and native review for this task.
  Rationale: This task changes static toolkit rules, not executable production behavior.

## Product Boundary

[Scope Boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) limits this task to production-path proof.

[Owner Composition](../../assets/skills/design-preflight/references/owner-composition.md) owns causal production-path composition and seam placement. [Scenario Discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md) owns trace evidence and eligibility. The trace result defines the structured interface. Design Preflight uses these owners for initial work and accepted corrections.

External systems, trace-executor lifecycle, native review, Full-set Results, and publication are opaque. No deferred owner is promoted.

The scope ceiling excludes live-service requirements, broad UI automation, parsers, runtime instrumentation, coverage thresholds, mutation systems, dependencies, new skills, duplicate rule owners, and exhaustive combinations.

## Required Outcome

For each eligible boundary and production entry path, one exact named check must do these actions:

1. Invoke the real in-repository production entry point.
2. Follow one causal execution through every in-scope production hop.
3. Reach and observe the terminal oracle.

Separate component checks cannot satisfy this outcome. Disconnected component calls inside one check also cannot satisfy it.

A deterministic callback or async continuation can be part of the causal execution when the check directly drives it. Concurrent thread ordering stays outside the supported model unless a product requirement includes it.

A fake, stub, or seam can replace only an opaque external system. Examples include a network, clock, operating system, or third-party provider. A seam that replaces an in-scope production hop leaves the path unclosed. Live external infrastructure is not required.

## Boundary Inventory

| Boundary | Condition or invariant | Contrast and oracle | Entry points | Scenario rows |
| --- | --- | --- | --- | --- |
| B1 | One exact check traverses the real entry, every in-scope hop, and the terminal oracle. | A causal path passes. Separate checks, disconnected calls, a skipped hop, or an early stop fail. | Initial preflight, correction preflight, and each trace-closure mode. | S1, S2, S3, S10 |
| B2 | A seam can replace only an opaque external system. | An external-provider fake passes. An in-scope writer or loader fake fails. | Each accepted production entry path. | S4 |
| B3 | A deterministic external fake is sufficient. | The fake can pass without live infrastructure. | A production path with an external dependency. | S5 |
| B4 | Semantic trace closure applies only to executable production behavior with a real entry point. | Eligible production code receives closure. Written artifacts and no-entry units do not. | Trace eligibility and the review gate. | S6, S7 |
| B5 | Every eligible closure uses the existing fresh no-history executor. | Fresh execution passes. Coordinator or reused-context attestation fails. | Full, checkpoint, delta, final, and reuse-only closure. | S8 |
| B6 | Native review stays independent from trace conclusions. | Unprimed native input passes. Trace-primed input fails. | Native discovery. | S9 |

The user requirement, accepted Plan, and inherited CPK-022, CPK-023, CPK-034, CPK-045, CPK-046, and CPK-052 decisions supply these boundaries. CPK-052 remains authoritative where it supersedes the earlier independent boundary derivation from CPK-045.

## Scenario Proof

| Scenario | Discriminator and contrast | Production path | Required oracle | Runnable check |
| --- | --- | --- | --- | --- |
| S1 | Separate entry, intermediate, and terminal checks versus one causal check. | Initial preflight to Owner Composition to Scenario Proof. | Only the causal check is accepted. | `test_scenario_proof_maps_transition_closed_checks` and the forward fixture. |
| S2 | Initial preflight versus accepted-correction preflight. | Both preflight entry routes to Scenario Proof. | Both routes require the same proof. | `test_scenario_proof_maps_transition_closed_checks` and the forward fixture. |
| S3 | Combined component evidence versus one exact production-path check. | Each trace mode to the fresh executor to the native-review gate. | Combined evidence enters `missing_tests` and blocks review. | `test_boundary_trace_closure_blocks_native_review` and the forward fixture. |
| S4 | External-provider fake versus an in-scope owner fake. | Real entry to all in-scope hops to the external boundary and terminal owner. | Only the external fake can close the row. | `test_boundary_trace_closure_blocks_native_review` and the forward fixture. |
| S5 | Deterministic external fake versus a live-service requirement. | Real repository path to the external boundary. | The deterministic fake can pass. | `test_boundary_trace_closure_blocks_native_review`. |
| S6 | Executable production code versus a static toolkit rule. | Trace eligibility to the selected validation path. | Only eligible production code receives semantic closure. | Existing eligibility assertions. |
| S7 | Executable behavior with a real entry versus a unit without one. | Trace eligibility gate. | The no-entry unit receives no invented trace proof. | Existing eligibility assertions. |
| S8 | Fresh no-history executor versus coordinator or reused-context attestation. | Trace invocation to structured result. | Only the fresh executor result is valid. | Existing executor and reuse assertions. |
| S9 | Independent native input versus trace-primed input. | Passed closure to native discovery. | Only independent native input is valid. | `test_native_review_does_not_recurse` and existing independence assertions. |
| S10 | Disconnected component calls in one check versus one entry-triggered causal traversal. | Named check body through the production hops. | Repackaged component proof fails. | The forward fixture and focused trace test. |
| S11 | Deterministic callback or async continuation versus an invented synchronous-stack rule. | Real entry through a check-driven continuation to the terminal owner. | The causal async path can pass. | The forward fixture and focused trace test. |

One named check can be parameterized. Each proof case must traverse the complete causal path.

## Implementation

Add the causal traversal and seam-placement requirements only to Owner Composition. Add distinctive `cpk-rule-guard` text only in that owner.

Make Scenario Discrimination bind every path fact in a closure row to one exact named check. It must apply Owner Composition without copying the traversal rule.

Add these fields to the existing trace result:

- `production_hops`: every in-scope production hop in order.
- `one_check_traverses_complete_path`: `true` only when one named check proves the causal traversal.
- `external_boundary_seams`: permitted external seams, or an empty list.
- `replaced_in_scope_hops`: an empty list for a valid row.

Keep the existing entry, gate, enforcement, terminal, check, and result fields. Do not add separate required-hop and observed-hop lists.

A false, unknown, missing, or unsupported continuity value fails closure. A missing production hop also fails closure. A nonempty `replaced_in_scope_hops` value fails closure. The fresh executor must add the exact missing path check to `missing_tests`.

Extend the two existing focused tests and the CPK-045 forward fixture. Do not add a test framework or another fixture.

## Semantic Subtask

CP1 is the only subtask. Its observable outcome is a trace rule that rejects proof assembled from component execution.

Owner Composition is the primary owner. Scenario Discrimination and the trace result are direct consumers. The allowed change boundary includes these owners, the two focused tests, the forward fixture, version references, task documentation, and checksums.

CP1 depends on the accepted Plan history records and no earlier checkpoint. Its focused validation uses the transition-closure, trace-closure, recursion, and unique-owner tests. Its checkpoint review covers the complete CPK-053 candidate from the task base. The local commit contains the complete reviewed task.

## Validation

Run the focused unit tests for transition closure, trace closure, native-review recursion, and unique rule ownership. Run the clean-context forward fixture. Then run `./run-tests.sh`, shell and PowerShell syntax checks, `git diff --check`, and `sha256sum --check MANIFEST.sha256`.

This task changes static toolkit rules. Use deterministic checks and native review. Do not use semantic trace closure for this candidate.

Use one reviewed checkpoint because the task has one coherent correction. After a clean review, commit the candidate. Install that exact commit in the live environment. Require Doctor to report version `0.23.7` and `Result: ready`. Do not publish without a separate request.

## Interfaces and Dependencies

The trace-closure JSON gains four evidence fields. No executable API, dependency, service, parser, or runtime state is added.

## Prior Plan Reconciliation

The accepted Plan record is carried without supersession. CPK-052 remains authoritative for accepted-inventory-only trace semantics, fresh execution, reuse-only validation, and native-review independence.

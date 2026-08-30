# Restore Independent Trace Coverage and Severity-Based Review Stops

This ExecPlan is a living specification until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

Review repetition must not turn an ordinary defect into a severe defect. A validated P2 finding must use the correction-authority gate on every pass. Only validated severe impact plus a correction that is not a direct repair can start Defect Diagnostic.

Trace closure must also inspect test coverage independently. For each eligible native review, one fresh read-only subagent receives the accepted boundaries, the production paths, and the named tests. It reports missing tests before native review starts. The coordinator cannot attest its own trace.

Work occurs on branch `fix/cpk-052-review-trace-closure`. The base branch is `main` at `56404d5a470e2c4214b42377f2e3aa31d3fafb14`. Release this bugfix as version `0.23.6`.

## Surprises & Discoveries

- The severity rule still contained the old third-counted-pass stop after the direct-repair gate was added.
- The current trace owner requires evidence inspection but does not identify an independent executor.
- The old forward fixture still requires trace closure to derive requirements again. This conflicts with the current accepted-inventory rule.
- A reuse-only final closure can bypass a fresh verifier unless the rule covers every closure invocation.

## Decision Log

- Remove only the consecutive production-defect counter and its severe-stop status. Preserve normal review-pass numbers.
- Keep correction-authority and contract-gap stops unchanged.
- Use one fresh read-only subagent with no inherited task conversation for every eligible trace closure. This includes reuse-only closure.
- Give the subagent the canonical Scenario Discrimination, Owner Composition, and Full-set Results rules.
- Give the subagent the accepted boundary inventory and Scenario Proof, exact review boundary, current diff and production sources, named test bodies and results, and reusable rows or an explicit empty set.
- Keep trace closure limited to executable production behavior with a real runnable entry point.
- Keep native review independent. The trace subagent does not edit, delegate, start another trace, run Design Preflight, or start native review.
- Do not add a new skill, hook, parser, dependency, state machine, coverage percentage, or mutation framework.
- Increment the committed source version from `0.23.5` to `0.23.6`.

## Plan History Reconciliation

CPK-044 is superseded only where it preserves the old three-pass breaker as an opaque owner. This task makes validated severe impact and the direct-repair gate the only severe-stop selector.

CPK-045 is superseded only where its trace fixture requires independent requirement derivation before it accepts the boundary inventory. This task restores its fresh read-only verifier but gives that verifier the accepted inventory as the only semantic input.

CPK-046 remains authoritative. Semantic trace closure still applies only to executable production behavior with a real runnable entry point. Written instructions use deterministic checks and native review.

## Context and Orientation

`assets/skills/adversarial-review/SKILL.md` owns finding validation, correction authority, and severe-stop selection.

`assets/skills/design-preflight/references/scenario-discrimination.md` owns trace eligibility, evidence, execution identity, review scope, reuse, and native-review independence. `preflight-review.md` owns the structured result interface.

`tests/fixtures/cpk045-boundary-forward.md` is a direct deterministic fixture for the trace rule. `tests/test_kit.py` contains the focused rule-owner checks. `docs/roadmap.md` is the only tracked lifecycle-state record.

## Product Boundary

The normal use cases are local full, checkpoint, delta, and final native reviews. Findings can come from local review, PR review, CI, audit, or a user. Every finding source uses the same validation and correction-authority gate.

The supported model has one coordinator and one writer. A fresh trace subagent is read-only. Concurrent mutation, retry after tool failure, and hostile evidence are outside the supported model.

The change does not modify Defect Diagnostic, native discovery, review lenses, publication, runtime product code, or completed historical plans.

## Boundary Inventory

| Boundary | Condition and contrast | Entry point | Required oracle | Scenario |
| --- | --- | --- | --- | --- |
| B1 | Review-pass ordinal does not escalate P2. The old contrast escalates the third P2 pass. | Finding validation to correction authority | Repeated P2 stops for correction authority and does not start Defect Diagnostic. | S1 |
| B2 | Validated P0/P1 or equivalent severe impact and a non-direct correction selects the severe path. P2, raw severity, or a direct repair does not. | Severity validation to severe breaker | Only the validated severe, non-direct side starts Defect Diagnostic. | S2, S3 |
| B3 | A nonsevere non-direct correction and an undefined result keep separate stop owners. | Accepted-result and correction-authority gates | The status names correction authority or contract decision. | S4 |
| B4 | One fresh clean-context read-only subagent executes each eligible closure. Coordinator or reused-context attestation is invalid. | Trace eligibility to closure result | The result identifies the fresh executor. | S5 |
| B5 | The verifier receives every canonical rule and evidence input and reports missing tests. An incomplete packet or weak test evidence fails. | Trace packet to evidence inspection | `missing_tests` is explicit, and any missing obligation blocks native review. | S6, S7 |
| B6 | Closure scope matches the selected review boundary. Only unchanged rows closed by a fresh verifier can be reused. | Review-mode selection to closure composition | A fresh verifier handles new, invalidated, and reuse-only closure. | S8, S9 |
| B7 | Only executable production behavior uses semantic trace closure. Native review receives no trace result, and neither stage recurses. | Eligibility gate to native discovery | Written rules use deterministic checks. Eligible code is closure-gated. | S10, S11 |

Every authoritative source clause has a disposition in the accepted preflight result. No contract gap remains.

## Scenario Proof

| Scenario | Discriminator and contrast | Terminal oracle | Runnable check |
| --- | --- | --- | --- |
| S1 | First and repeated P2 pass with all other facts equal | Both use ordinary correction authority. | `test_review_stop_diagnostics_are_per_finding_and_mandatory` |
| S2 | Validated P1 and P2 with the same non-direct correction | Only P1 can start Defect Diagnostic. | Same focused stop check |
| S3 | Direct and non-direct repair for the same validated severe defect | Direct repair proceeds; non-direct repair stops severely. | Same focused stop check |
| S4 | Defined wrong result and undefined result | Correction-authority and contract-gap statuses remain distinct. | Same focused stop check |
| S5 | Fresh no-history verifier and coordinator self-attestation | Only the fresh verifier can close the trace. | `test_boundary_trace_closure_blocks_native_review` |
| S6 | Complete packet and each required input omitted | Only the complete packet can pass. | Same focused trace check |
| S7 | Paired terminal proof and missing or weak test evidence | Missing tests are named and block review. | Same focused trace check |
| S8 | Unchanged verified row and changed or coordinator-authored row | Only the unchanged verified row is reusable. | Same focused trace check |
| S9 | Full, checkpoint, delta, final, and reuse-only closure | Each mode closes its exact boundary through a fresh verifier. | Same focused trace check |
| S10 | Executable production behavior and written instruction behavior | Only executable behavior uses semantic trace closure. | Same focused trace check |
| S11 | Native input without and with trace conclusions | Only independent native input is valid; no stage recurses. | Same focused trace check and `test_native_review_does_not_recurse` |

The input-domain, path-transition, and collection-semantic lenses all apply.

## Plan of Work

Change the severe breaker in its existing owner. Delete the obsolete consecutive-defect count and its dedicated status. Keep validated severity, direct repair, correction authority, contract gaps, and normal pass numbers.

Change the trace owner and structured result. Require one fresh clean-context verifier for every eligible invocation. Name the canonical rules and evidence packet. Add executor identity and `missing_tests` to the result. Update the existing forward fixture so it tests accepted-inventory evidence closure instead of requirement re-derivation.

Update the two focused checks, the version, roadmap, and manifest. No other owner is needed.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit`.

1. Update the canonical severe-stop and trace-closure owners.
2. Update the direct fixture and focused tests.
3. Run the focused tests and complete repository checks.
4. Regenerate the manifest after source and documentation are final.
5. Run native adversarial review before review closure.

## Validation and Acceptance

Run:

    python3 -m unittest tests.test_kit.IntegrationTests.test_boundary_trace_closure_blocks_native_review
    python3 -m unittest tests.test_kit.IntegrationTests.test_native_review_does_not_recurse
    python3 -m unittest tests.test_kit.IntegrationTests.test_review_stop_diagnostics_are_per_finding_and_mandatory
    python3 -m unittest tests.test_kit.IntegrationTests.test_lifecycle_skills_and_version
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

The focused checks must prove the B1 through B7 contrasts. The complete checks must find no rule-owner, package, or platform regression.

## Idempotence and Recovery

The change is declarative and idempotent. If a check or review fails, stop and report it. Do not retry by replacing a healthy verifier or reviewer.

## Artifacts and Notes

Keep detailed command and review results in `.agent/test-results/cpk-052-review-trace-closure.md`. Do not stage that file.

## Interfaces and Dependencies

No executable interface or dependency changes. The existing review and Design Preflight skills remain the public instruction routes.

Final note: one independent evidence pass catches missing tests without turning trace closure into a second requirements review.

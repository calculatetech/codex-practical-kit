# Close Every Behavioral Boundary

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

Implementation can preserve the common case while it violates an explicit boundary. A positive-only test can then pass. After this change, Design Preflight must inventory each explicit behavioral boundary before implementation. A fresh verifier must inspect the implementation and paired proof before native review starts.

The release version is `0.23.0`. Work occurs on branch `cpk-045-boundary-trace-closure` from commit `388b23fc165df788848d19e6ce738a973f888d2e`.

## Progress

- [x] (2026-08-24 16:47Z) Recovered and reconciled all Plan history records.
- [x] (2026-08-24 17:05Z) Completed research and the two-phase Design Preflight challenge.
- [x] (2026-08-24 16:56Z) CP1: Added the complete boundary inventory to Design Preflight and its checks.
- [x] (2026-08-24 17:05Z) CP1: Validated and reviewed checkpoint commit `7fb115a`.
- [x] (2026-08-24 17:14Z) CP2: Added trace closure before native review and its checks.
- [x] (2026-08-24 17:14Z) CP2: Finalized documentation, version `0.23.0`, and the distribution manifest.
- [ ] CP2: Validate and review the second checkpoint.
- [ ] Run final complete-candidate review, install the toolkit, and run Doctor.
- [ ] Close review records and the roadmap.

## Surprises & Discoveries

- Observation: The accepted Plan initially used unlinked storage because this specification did not exist.
  Evidence: `.agent/plan-history/plan-summary.20260824T164719361941Z.f1479c9effab9071b8ccaa86dce1dbee407b79647c6bb7d542aea8c75caae32b.md` contains the exact Plan.
- Observation: Current Scenario Proof starts with retained scenarios. It has no independent denominator for omitted source boundaries.
  Evidence: `assets/skills/design-preflight/references/preflight-review.md` records scenarios but no disposition for each source clause.
- Observation: A fresh challenger derived both mapping states and rejected the broader helper from only the raw requirement.
  Evidence: The clean-context result classified the helper as opaque and stated that the positive-only check proves only the unmapped side.

## Decision Log

- Decision: Extend Scenario Discrimination and Design Preflight. Do not add a skill or executable framework.
  Rationale: These files already own requirement-derived contrasts and the pre-review proof mapping.
  Date/Author: 2026-08-24 / Codex and user.
- Decision: A changed behavioral boundary always requires inventory and closure.
  Rationale: The user selected complete boundary tracing. A direct bug that changes no boundary retains the small-change exception.
  Date/Author: 2026-08-24 / User.
- Decision: Use one fresh read-only verifier immediately before native review.
  Rationale: The verifier independently reconstructs the source denominator and inspects actual production and test paths.
  Date/Author: 2026-08-24 / Codex and user.
- Decision: Do not provide the trace record to native review.
  Rationale: Native review remains an independent defect-discovery lens.
  Date/Author: 2026-08-24 / Codex and user.
- Decision: Replace the preflight card's numeric line cap with a compactness rule.
  Rationale: Multiple mandatory boundary and scenario rows cannot fit under the old limit. Required proof rows take priority.
  Date/Author: 2026-08-24 / Codex.

## Outcomes & Retrospective

No implementation outcome exists yet.

## Context and Orientation

`assets/skills/design-preflight/SKILL.md` owns preflight sequencing. `assets/skills/design-preflight/references/scenario-discrimination.md` owns requirement-derived discriminators and paired contrasts. `preflight-card.md` defines the coordinator's planning record. `preflight-review.md` defines the read-only challenger interfaces. `assets/skills/adversarial-review/SKILL.md` owns native review sequencing. `tests/test_kit.py` verifies rule ownership and route contracts. `kit.py` owns the version. `MANIFEST.sha256` records distributed files.

A behavioral boundary is an explicit requirement that limits, selects, excludes, relates, or preserves an outcome. Trace closure is a fresh read-only check that compares every authoritative source boundary with the implemented paths and direct tests.

Applicable immutable Plan records:

- `.agent/plan-history/plan-summary.20260822T050100617085Z.fd7dfe4c94e461a1824112794d31e1372d316ccf79eed8a3937d2754c1157e40.md`
- `.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md`
- `.agent/plan-history/plan-summary.20260823T052048899607Z.c539b46a7e5fa56092a382fef046fd00d4271c42c4fda8e0f0e2216ce94df122.md`
- `.agent/plan-history/plan-summary.20260824T031427928859Z.f30d03e6b396d05f07f5ce7eebc8b8e8b81e2b1cfe8ebc739342a6e444ca6968.md`
- `.agent/plan-history/plan-summary.20260824T135017227348Z.7cfbec79d5ce39f1a1d436a31dccfe0669c616f252b6793d4b90dc2b34ad13d6.md`
- `.agent/plan-history/plan-summary.20260824T164719361941Z.f1479c9effab9071b8ccaa86dce1dbee407b79647c6bb7d542aea8c75caae32b.md`

## Product Boundary

[Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) limits this task to accepted implementation and test proof. The authoritative source is the accepted CPK-045 Plan and the user's requirement that every explicit behavioral boundary receives trace proof.

Design Preflight, Scenario Discrimination, and the pre-review gate are `composes` owners. Native review, review correction authority, Plan capture, publication, and the supported operating model are `opaque`. No deferred owner is promoted.

The scope ceiling excludes a parser, coverage percentage, mutation system, formal property language, daemon, dependency, semantic-ranking service, post-failure recovery system, or duplicate rule owner.

## Design Preflight

Required outcome: Every in-scope behavioral boundary receives a source disposition before implementation. A fresh verifier must prove each applicable path and paired test before native review.

Existing owner: Scenario Discrimination owns the boundary trace. Design Preflight invokes it. The preflight card and review result store task-specific records. Adversarial Review invokes the completed closure gate before native discovery.

Normal-use behavior floor: Source clauses cannot disappear because they resemble earlier clauses. Equal-result invariants remain boundaries. Every applicable entry point receives proof. Positive-only tests, component tests, unrelated fixture changes, and broader helpers cannot close the trace.

Preflight: ready — extend the existing Scenario Proof record and add one fresh trace-closure phase.

## Boundary Inventory

| Boundary | Source | Condition or invariant | Required sides and oracle | Entry points | Scenario Proof |
| --- | --- | --- | --- | --- | --- |
| B1 | Accepted CPK-045 Plan, CP1 | Every authoritative clause that defines a behavioral boundary receives a disposition. | Mapped clauses enter the trace. Non-boundary, opaque, deferred, and contract-gap clauses retain an explicit disposition. An omitted later clause blocks work. | Design Preflight before implementation and accepted boundary corrections. | S1 source list with duplicate-looking prefix and later distinct clause. |
| B2 | Accepted CPK-045 Plan, CP1 | Each boundary covers every applicable production path. | One scenario per path, or one composed scenario that proves all paths. Equal-result invariants use the nearest wrong meaning as the contrast. | Design Preflight before initial implementation and before accepted boundary corrections. | S2 mapped and unmapped staging paths. S3 equal-result invariant. |
| B3 | Accepted CPK-045 Plan, CP2 | After implementation and final substantive documentation, one fresh read-only verifier receives every named input and independently enumerates source boundaries before it compares `B#` records. | Raw requirements, accepted inventory, Scenario Proof, diff, production source, and named tests are present. Reordered work, a reused verifier, or a missing input blocks review. | Full, checkpoint, delta, and final review candidates with a boundary inventory. | S4 positive-only failure. S5 unrelated fixture failure. S6 broader-helper failure. S10 verifier order and inputs. |
| B4 | Accepted CPK-045 Plan, CP2 | Closure evidence remains valid only for the exact traced candidate. | A change to requirement sources, boundary records, production paths, or named tests invalidates closure. An unrelated document change does not. | Candidate preparation immediately before native review. | S7 traced change invalidates. S8 unrelated document keeps closure. |
| B5 | User decision in the accepted Plan | A new or changed behavioral boundary cannot use the small-change exception. | Boundary change requires inventory and closure. A direct arithmetic bug with no boundary change retains the exception. | Initial work and accepted review corrections. | S9 boundary change and direct arithmetic contrast. |
| B6 | Accepted CPK-045 Plan, CP2 | Native review remains independent from trace closure. | Native review receives the accepted intent, source, and synthetic commit. Giving it the trace record or coordinator conclusions violates the boundary. | Every native checkpoint, delta, and final review after trace closure. | S11 independent native-review input. |

The immutable Plan record and its byte-identical sibling copy contain one semantic clause set. Each clause has this disposition:

| Source clause | Disposition | Boundary or reason |
| --- | --- | --- |
| Summary: the existing design is correct | non-boundary | Accepted premise. |
| Summary: existing enforcement is incomplete | non-boundary | Problem context. |
| Summary: Scenario Proof has no denominator | mapped | B1. |
| Summary: no post-implementation conformance gate | mapped | B3 and B4. |
| Version and branch | non-boundary | Delivery metadata. |
| Research: use an external boundary trace with an evidence gate | mapped | B1 and B3. |
| Research: surveyed traceability, evidence gates, executable properties, and intent-driven regression | non-boundary | Source evidence for the selected mechanism. |
| Research: exclude semantic ranking, formal properties, mutation tooling, and recovery machinery | opaque | Scope ceiling; no product behavior. |
| Research: ExecPlans do not supply a boundary-trace gate | non-boundary | Ownership context. |
| Research: the toolkit owns the missing gate | mapped | B3. |
| CP1: extend Scenario Discrimination; add no skill or durable plan | opaque | Ownership and implementation ceiling. |
| CP1: enumerate every limiting, selecting, excluding, relating, or preserving requirement | mapped | B1. |
| CP1: stable `B#` identifiers | mapped | B1. |
| CP1: record source, condition, sides, oracles, entry points, and scenarios | mapped | B1 and B2. |
| CP1: classify every relevant source clause | mapped | B1. |
| CP1: inspect the complete set despite duplicate-looking clauses | mapped | B1. |
| CP1: prove every distinct production path | mapped | B2. |
| CP1: preserve equal-result invariants with the nearest wrong contrast | mapped | B2. |
| CP1: boundary changes override the small-change exception | mapped | B5. |
| CP1: store the inventory in the card, Phase 1 result, and ExecPlan | mapped | B1. |
| CP2: run one fresh read-only verifier after implementation and final documentation | mapped | B3. |
| CP2: give all named inputs and enumerate independently before `B#` comparison | mapped | B3. |
| CP2: return the specified result shape | mapped | B3 and B4. |
| CP2: false, unknown, missing, or unsupported evidence blocks review | mapped | B3. |
| CP2: inspect test bodies and reject positive, component, aggregate, and writer evidence | mapped | B3. |
| CP2: run immediately before review and invalidate traced changes | mapped | B4. |
| CP2: do not send the trace record to native review | mapped | B6. |
| Test Plan: every authoritative clause receives a disposition | mapped | B1 and S1. |
| Test Plan: later distinct clauses survive duplicate-looking clauses | mapped | B1 and S1. |
| Test Plan: mapped and unmapped staging outcomes | mapped | B2 and S2. |
| Test Plan: equal-result invariants remain boundaries | mapped | B2 and S3. |
| Test Plan: every applicable entry point receives proof | mapped | B2 and S2. |
| Test Plan: positive-only evidence blocks review | mapped | B3 and S4. |
| Test Plan: fixtures isolate the discriminator from unrelated gates | mapped | B3 and S5. |
| Test Plan: broader helpers fail sensitivity | mapped | B3 and S6. |
| Test Plan: traced documentation or implementation changes invalidate closure | mapped | B4 and S7. |
| Test Plan: arithmetic repair without a boundary change retains the exception | mapped | B5 and S9. |
| Test Plan: clean-context proof derives both staging cases and rejects weak evidence | mapped | B2 and B3; S2, S4, S6, and S11. |
| Test Plan: complete toolkit validation | non-boundary | Delivery validation. |
| Test Plan: use reviewed CP1 and CP2 checkpoints and one final review | non-boundary | Delivery sequencing. |
| Test Plan: install the reviewed candidate and require Doctor ready | non-boundary | Delivery validation. |
| Assumptions: no formal completeness, parser, or coverage percentage | opaque | Explicit mechanism ceiling. |
| Assumptions: the fresh verifier is the semantic gate | mapped | B3. |
| Assumptions: documentation is final first | mapped | B3. |
| Assumptions: Review Closure changes invalidate only traced sources | mapped | B4. |
| Assumptions: roadmap state and no publication | non-boundary | Coordination and delivery state. |
| Prior Plan Reconciliation | non-boundary | Preserves earlier owners without changing them. |

No clause is deferred or a contract gap.

## Scenario Proof

[Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md), [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md), and [Full-set results](../../assets/skills/design-preflight/references/full-set-results.md) control this proof.

| Scenario | Discriminator | Contrast | Production path | Required oracle | Runnable test or command | Result |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | Source-clause identity | Two similar clauses followed by one distinct boundary | Raw sources to inventory to disposition | Every clause has one disposition and omission blocks work | Clean-context command from S2 and `test_preflight_inventories_every_behavioral_boundary` | Pass |
| S2 | Mapped-plan status | Same staging input with mapped and unmapped base plans | Requirement to both production entry paths | Only the required path substitutes the plan | `codex exec --ephemeral --sandbox read-only -C . -o .agent/test-results/cpk045-forward-output.json - < tests/fixtures/cpk045-boundary-forward.md` | Pass |
| S3 | Preserved invariant | Both correct sides have the same terminal result but the nearest wrong meaning differs | Requirement to implementation and terminal owner | The invariant holds on both sides | Clean-context command from S2 and `test_preflight_inventories_every_behavioral_boundary` | Pass |
| S4 | Executed boundary side | Positive-only check versus paired check | Test body to terminal oracle | Positive-only evidence blocks review | `test_boundary_trace_closure_blocks_native_review` | Pass |
| S5 | Fixture isolation | Discriminator-only fixture versus discriminator plus unrelated gate | Test body to production predicates | Unrelated variation blocks review | Clean-context command from S2 and `test_boundary_trace_closure_blocks_native_review` | Pass |
| S6 | Enforcement meaning | Exact boundary owner versus broader helper | Entry point through gates to terminal owner | Broader meaning fails sensitivity | Clean-context command from S2 and `test_boundary_trace_closure_blocks_native_review` | Pass |
| S7 | Traced-source identity | Same candidate versus changed requirement, path, record, or named test | Final docs and source to closure evidence | A traced change invalidates closure | Clean-context command from S2 and `test_boundary_trace_closure_blocks_native_review` | Pass |
| S8 | Change relevance | Traced change versus unrelated documentation change | Candidate diff to closure evidence | Unrelated documentation does not invalidate closure | Clean-context command from S2 and `test_boundary_trace_closure_blocks_native_review` | Pass |
| S9 | Change type | Boundary change versus arithmetic repair with no boundary change | Design Preflight entry gate | Only the boundary change overrides the exception | Clean-context command from S2 and `test_preflight_inventories_every_behavioral_boundary` | Pass |
| S10 | Trace preparation | Fresh verifier after final docs with every input versus reused, early, or incomplete verification | Final candidate to independent source enumeration and trace result | Only the complete ordered trace can pass | Clean-context command from S2 | Pass |
| S11 | Evidence and review independence | Paired terminal proof and source-only native input versus component, aggregate, writer, or trace-primed evidence | Trace gate to native-review input | Weak evidence blocks closure; the trace record stays out of native review | Clean-context command from S2 and `test_boundary_trace_closure_blocks_native_review` | Pass |

## Plan of Work

CP1 extends the Scenario Discrimination owner, the Design Preflight entry gate, the preflight card, and Phase 1 result. It adds the source disposition and boundary inventory without a second artifact. Focused tests verify clause completeness, duplicate-looking prefixes, equal-result invariants, all entry points, and the small-change rule. Review this checkpoint and create its local commit.

CP2 adds the fresh trace-closure result to `preflight-review.md` and makes Design Preflight run it after final documentation and before Adversarial Review. Adversarial Review links to this gate before native discovery. Focused tests verify evidence quality, invalidation, and review independence. Update `kit.py` to `0.23.0`, update product documentation only when the diff makes it inaccurate, and regenerate `MANIFEST.sha256`. Review this checkpoint, then run final review from the task base.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit`. Run focused tests with `python3 -m unittest tests.test_kit.IntegrationTests.<test-name>`. Run the complete suite with `./run-tests.sh`. Compile Python with the existing test launcher. Parse shell and PowerShell scripts with the existing checks. Run `git diff --check`. Record detailed output in `.agent/test-results/cpk-045-boundary-trace-closure.md`.

Before each review, stage the complete checkpoint and require no unstaged tracked changes. Run the trace-closure verifier for the exact candidate. Then run native `codex review` with the mode and parent required by Adversarial Review. Keep its input independent from the trace record.

## Validation and Acceptance

Focused checks must prove B1 through B6 and S1 through S11. The clean-context forward check must derive both mapped and unmapped cases from the supplied broader-helper defect. It must reject the broader implementation, positive-only proof, component proof, aggregate result, and writer report. It must also prove trace ordering, named inputs, and native-review independence.

The full toolkit suite, Python compilation, shell checks, PowerShell parsing, rule-owner checks, link checks, manifest validation, and `git diff --check` must pass. After final review, install the candidate with `python3 kit.py install --repo .`. Then run `python3 kit.py doctor --repo .` and require `Result: ready`.

## Idempotence and Recovery

Read-only checks can be repeated. Synthetic review commits do not change the branch. If a required command fails, stop and report the error. Do not add recovery behavior.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, `.vscode/`, and ignored test results. Do not stage them. Local checkpoint commits do not authorize publication.

## Interfaces and Dependencies

The existing preflight card gains a boundary inventory. The existing Phase 1 JSON gains source dispositions and boundary records. `preflight-review.md` gains the `boundary-trace-closure` result. No executable API or dependency is added.

## Prior Plan Reconciliation

CPK-040 through CPK-044 are carried. CPK-022, CPK-028, CPK-034, and CPK-035 remain authoritative. CPK-045 adds source completeness and post-implementation closure without changing their accepted behavior.

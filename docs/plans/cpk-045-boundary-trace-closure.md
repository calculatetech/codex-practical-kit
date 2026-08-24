# Close Every Behavioral Boundary

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

Implementation can preserve the common case while it violates an explicit boundary. A positive-only test can then pass. After this change, Design Preflight must inventory each explicit behavioral boundary before implementation. A fresh verifier must inspect the implementation and paired proof before native review starts.

The release version is `0.23.0`. Work occurs on branch `cpk-045-boundary-trace-closure` from commit `388b23fc165df788848d19e6ce738a973f888d2e`.

## Progress

- [x] (2026-08-24 16:47Z) Recovered and reconciled all Plan history records.
- [x] (2026-08-24 17:05Z) Completed research and the two-phase Design Preflight challenge.
- [x] (2026-08-24 16:56Z) CP1: Added the complete boundary inventory to Design Preflight and its checks.
- [ ] CP1: Validate and review the first checkpoint.
- [ ] CP2: Add trace closure before native review and its checks.
- [ ] CP2: Finalize documentation, version, and distribution manifest.
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
| B2 | Accepted CPK-045 Plan, CP1 | Each boundary covers every applicable production path. | One scenario per path, or one composed scenario that proves all paths. Equal-result invariants use the nearest wrong meaning as the contrast. | Each production entry point named by B1. | S2 mapped and unmapped staging paths. S3 equal-result invariant. |
| B3 | Accepted CPK-045 Plan, CP2 | Trace closure proves actual implementation and tests before native review. | Every boolean is true. Every path runs both boundary sides to its terminal oracle. Any missing, false, unknown, or unsupported item blocks native review. | Full, checkpoint, delta, and final review candidates when traced sources changed. | S4 positive-only failure. S5 unrelated fixture failure. S6 broader-helper failure. |
| B4 | Accepted CPK-045 Plan, CP2 | Closure evidence remains valid only for the exact traced candidate. | A change to requirement sources, boundary records, production paths, or named tests invalidates closure. An unrelated document change does not. | Candidate preparation immediately before native review. | S7 traced change invalidates. S8 unrelated document keeps closure. |
| B5 | User decision in the accepted Plan | A new or changed behavioral boundary cannot use the small-change exception. | Boundary change requires inventory and closure. A direct arithmetic bug with no boundary change retains the exception. | Initial work and accepted review corrections. | S9 boundary change and direct arithmetic contrast. |

Source dispositions: The accepted Plan's summary and research decision are non-boundary context. CP1 maps to B1, B2, and B5. CP2 maps to B3 and B4. The Test Plan maps each B record to its direct checks. Assumptions are opaque constraints. No clause is deferred or a contract gap.

## Scenario Proof

[Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md), [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md), and [Full-set results](../../assets/skills/design-preflight/references/full-set-results.md) control this proof.

| Scenario | Discriminator | Contrast | Production path | Required oracle | Runnable test or command | Result |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | Source-clause identity | Two similar clauses followed by one distinct boundary | Raw sources to inventory to disposition | Every clause has one disposition | `test_preflight_inventories_every_behavioral_boundary` | Pass |
| S2 | Mapped-plan status | Same staging input with mapped and unmapped base plans | Requirement to both production entry paths | Only the required path substitutes the plan | Fresh read-only Phase 1 forward check | Pass |
| S3 | Preserved invariant | Both correct sides have the same terminal result but the nearest wrong meaning differs | Requirement to implementation and terminal owner | The invariant holds on both sides | `test_preflight_inventories_every_behavioral_boundary` | Pass |
| S4 | Executed boundary side | Positive-only check versus paired check | Test body to terminal oracle | Positive-only evidence blocks review | Focused CPK-045 contract test | Planned |
| S5 | Fixture isolation | Discriminator-only fixture versus discriminator plus unrelated gate | Test body to production predicates | Unrelated variation blocks review | Focused CPK-045 contract test | Planned |
| S6 | Enforcement meaning | Exact boundary owner versus broader helper | Entry point through gates to terminal owner | Broader meaning fails sensitivity | Clean-context forward check | Planned |
| S7 | Traced-source identity | Same candidate versus changed requirement, path, record, or named test | Final docs and source to closure evidence | A traced change invalidates closure | Focused CPK-045 contract test | Planned |
| S8 | Change relevance | Traced change versus unrelated documentation change | Candidate diff to closure evidence | Unrelated documentation does not invalidate closure | Focused CPK-045 contract test | Planned |
| S9 | Change type | Boundary change versus arithmetic repair with no boundary change | Design Preflight entry gate | Only the boundary change overrides the exception | `test_preflight_inventories_every_behavioral_boundary` | Pass |

## Plan of Work

CP1 extends the Scenario Discrimination owner, the Design Preflight entry gate, the preflight card, and Phase 1 result. It adds the source disposition and boundary inventory without a second artifact. Focused tests verify clause completeness, duplicate-looking prefixes, equal-result invariants, all entry points, and the small-change rule. Review this checkpoint and create its local commit.

CP2 adds the fresh trace-closure result to `preflight-review.md` and makes Design Preflight run it after final documentation and before Adversarial Review. Adversarial Review links to this gate before native discovery. Focused tests verify evidence quality, invalidation, and review independence. Update `kit.py` to `0.23.0`, update product documentation only when the diff makes it inaccurate, and regenerate `MANIFEST.sha256`. Review this checkpoint, then run final review from the task base.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit`. Run focused tests with `python3 -m unittest tests.test_kit.IntegrationTests.<test-name>`. Run the complete suite with `./run-tests.sh`. Compile Python with the existing test launcher. Parse shell and PowerShell scripts with the existing checks. Run `git diff --check`. Record detailed output in `.agent/test-results/cpk-045-boundary-trace-closure.md`.

Before each review, stage the complete checkpoint and require no unstaged tracked changes. Run the trace-closure verifier for the exact candidate. Then run native `codex review` with the mode and parent required by Adversarial Review. Keep its input independent from the trace record.

## Validation and Acceptance

Focused checks must prove B1 through B5 and S1 through S9. The clean-context forward check must derive both mapped and unmapped cases from the supplied broader-helper defect. It must reject the broader implementation and a positive-only test.

The full toolkit suite, Python compilation, shell checks, PowerShell parsing, rule-owner checks, link checks, manifest validation, and `git diff --check` must pass. After final review, install the candidate with `python3 kit.py install --repo .`. Then run `python3 kit.py doctor --repo .` and require `Result: ready`.

## Idempotence and Recovery

Read-only checks can be repeated. Synthetic review commits do not change the branch. If a required command fails, stop and report the error. Do not add recovery behavior.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, `.vscode/`, and ignored test results. Do not stage them. Local checkpoint commits do not authorize publication.

## Interfaces and Dependencies

The existing preflight card gains a boundary inventory. The existing Phase 1 JSON gains source dispositions and boundary records. `preflight-review.md` gains the `boundary-trace-closure` result. No executable API or dependency is added.

## Prior Plan Reconciliation

CPK-040 through CPK-044 are carried. CPK-022, CPK-028, CPK-034, and CPK-035 remain authoritative. CPK-045 adds source completeness and post-implementation closure without changing their accepted behavior.

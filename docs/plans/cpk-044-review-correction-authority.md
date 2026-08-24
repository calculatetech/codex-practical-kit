# Separate review findings from correction authority

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

Local review must discover defects without receiving the main thread's conclusions. After discovery, the toolkit must decide whether each finding changes an accepted end result and whether Codex has authority to correct it. A valid observation that does not change the end result is reported and excluded. Any correction that would add product behavior stops for human direction. Severe diagnostics must explain the problem, relevance, prevention, and required action before the detailed proof.

## Progress

- [x] (2026-08-24) Reconciled the accepted CPK-044 Plan with CPK-040 through CPK-043.
- [x] (2026-08-24) Created branch `cpk-044-review-correction-authority` from `28734b2623555b8a539ca0157f510111b1eeacb1`.
- [x] (2026-08-24) Made CPK-044 the only Active roadmap task.
- [x] (2026-08-24) Completed Design Preflight for the review and diagnostic instruction owners.
- [x] (2026-08-24) CP1 completed: native review discovery and correction authority passed a checkpoint review and a clean correction-delta review.
- [x] (2026-08-24) CP2 implementation completed: severe diagnostics now lead with the problem, end-result relevance, prevention, and required action.
- [x] (2026-08-24) Updated documentation, version `0.22.0`, focused tests, and the distribution manifest.
- [x] (2026-08-24) Completed the full test, compile, shell, PowerShell, manifest, Plan-history, and diff checks.
- [x] (2026-08-24) CP2 passed its native checkpoint review.
- [x] (2026-08-24) Completed the final complete-candidate review, installation, Doctor check, native-review smoke, and review closure.

## Surprises & Discoveries

- Observation: `codex review --commit` accepts a commit target but cannot also accept a free-form prompt.
  Evidence: The planning feasibility probe rejected the combined form. A synthetic commit message is therefore the only task-intent input.
- Observation: The first native checkpoint review found two contract omissions in the new review instructions.
  Evidence: Review of synthetic commit `d57f668b266a968ab408e0793f71097a5ff5d1e0` found that an undefined result could be dropped by the wrong-result scope predicate and that the P0-P2 counted-pass threshold was missing.
- Observation: The complete suite found that the native-review rewrite had dropped existing lifecycle and Scenario Proof routes.
  Evidence: Four static contract tests failed. Restoring the prior route links and lifecycle phrase made all 83 tests pass, with one platform-specific skip.
- Observation: The final native review challenged broad publication authority and found a real rule-owner conflict for contract gaps.
  Evidence: Broad `publish` authority does not override CPK-044's required finding decision, so that observation was excluded. The contract-gap exception moved to the canonical scope owner.

## Decision Log

- Decision: Use an unreferenced synthetic commit for each local review target.
  Rationale: Native Codex review can inspect an exact staged tree without creating a branch reference or changing tracked files.
  Date/Author: 2026-08-24, user and Codex.
- Decision: Treat every finding source as untrusted input to one correction-authority gate.
  Rationale: Reviewer severity and fix suggestions do not define product scope or grant implementation authority.
  Date/Author: 2026-08-24, user and Codex.
- Decision: Replace the limited coherence pass with a complete final review.
  Rationale: One final native review checks the full current candidate after checkpoint and delta reviews.
  Date/Author: 2026-08-24, user and Codex.

## Outcomes & Retrospective

Version `0.22.0` now uses native review for exact staged candidates. One source-independent gate excludes findings that do not change the accepted result and permits only direct repairs without human direction. Severe diagnostics now lead with the problem, end-result relevance, prevention, and required action. All 83 tests passed, with one Windows-only skip. The installed candidate passed Doctor, the native-review smoke, correction-delta review, and final complete-candidate review.

## Prior Plan Reconciliation

Record: `.agent/plan-history/plan-summary.20260822T050100617085Z.fd7dfe4c94e461a1824112794d31e1372d316ccf79eed8a3937d2754c1157e40.md`

Status: carried

Reason: CPK-040 remains authoritative for Plan capture and implementation handoff.

Record: `.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md`

Status: carried

Reason: CPK-041 remains authoritative for source-backed material decisions.

Record: `.agent/plan-history/plan-summary.20260823T052048899607Z.c539b46a7e5fa56092a382fef046fd00d4271c42c4fda8e0f0e2216ce94df122.md`

Status: carried

Reason: CPK-042 checkpoint and delta review remain authoritative. CPK-044 supersedes only its limited coherence pass with final review.

Record: `.agent/plan-history/plan-summary.20260824T031427928859Z.f30d03e6b396d05f07f5ce7eebc8b8e8b81e2b1cfe8ebc739342a6e444ca6968.md`

Status: carried

Reason: CPK-043 PR sequencing remains authoritative. Its findings now use the source-independent gate.

Record: `.agent/plan-history/plan-summary.20260824T135017227348Z.7cfbec79d5ce39f1a1d436a31dccfe0669c616f252b6793d4b90dc2b34ad13d6.md`

Status: carried

Reason: This record is the accepted CPK-044 implementation contract.

## Plan Deviations

Plan History first used unlinked storage because this ExecPlan did not exist when the Plan was captured. The exact record is copied beside this file. The central record remains unchanged.

## Context and Orientation

`assets/skills/adversarial-review/SKILL.md` owns local review, finding validation, correction, and stop behavior. Its references define the native review target, adjudication record, and review lenses. `assets/skills/defect-diagnostic/SKILL.md` owns severe defect reconstruction. Its diagnostic template owns the human-facing order. `tests/test_kit.py` enforces these instruction contracts. `kit.py` owns the toolkit version. `MANIFEST.sha256` records distributed file checksums.

## Product Boundary

[Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) limits review to accepted product behavior. CPK-044 composes Adversarial Review and Defect Diagnostic. Delivery Lifecycle, Design Preflight, Publication, and the existing three-pass breaker are opaque and must retain their documented behavior. No owner is promoted from deferred work.

The authoritative product source is the accepted CPK-044 Plan and the user's instruction that review corrections must not add features, scope, assumptions, policy, state, interfaces, dependencies, fallbacks, or lifecycle behavior.

## Design Preflight

Required outcome: Native Codex review discovers candidate defects independently. The coordinator then excludes observations that leave the accepted result correct, stops on undefined results, and automatically applies only a direct repair that restores an existing result in its clear owner.

Existing owners: `assets/skills/adversarial-review/SKILL.md` owns the review gate. `assets/skills/defect-diagnostic/references/diagnostic-summary.md` owns diagnostic presentation.

Normal-use behavior floor: Every source uses the same gate. Severity is considered only after relevance, scope, and supported use are proven. A mixed set that contains one decision-required correction produces no partial edits. Native review targets the exact staged tree and its mode-specific parent. Native failure stops without a generic fallback. Severe diagnostics keep full proof but show the plain summary first.

Scope ceiling: Add no parser, daemon, service, dependency, telemetry, model evaluation, recovery behavior, or duplicate rule owner. Do not preload exclusions, scenario conclusions, or correction directions into native discovery. Do not claim that local and hosted Codex review use the same model or internal prompt.

Preflight: ready — revise the two existing instruction owners and add focused static contract checks.

## Plan of Work

CP1 changes `assets/skills/adversarial-review/SKILL.md` and its focused references. Stage the complete checkpoint. Create an unreferenced commit from that staged tree with only accepted intent and source in its message. Run `codex review --commit` against that commit. After a clean checkpoint review, create the planned local checkpoint commit.

CP2 changes the severe diagnostic owner and template. It also finalizes this ExecPlan, the roadmap, tests, version `0.22.0`, and the manifest. Run focused and complete validation. Review the complete candidate from the task base in `final` mode. Install that reviewed candidate, require Doctor to report ready, and run one opt-in native-review smoke before review closure and the second checkpoint commit.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit`. Use `python3 -m unittest tests.test_kit` for the complete suite, `python3 -m py_compile` for Python sources, `bash -n` for shell scripts, and PowerShell parser checks when `pwsh` is available. Use `git diff --check` and the repository manifest check. Keep detailed output in `.agent/test-results/cpk-044-review-correction-authority.md`.

For each native review, record the staged tree before and after the command. Require no unstaged tracked changes. Stop if `codex review` fails. Do not use a generic reviewer as fallback.

## Validation and Acceptance

Focused tests must prove the source-independent gate, direct-repair limit, atomic mixed-finding stop, irrelevant-finding exclusion, contract-gap stop, severe diagnostic trigger, exact native targets and parents, native failure stop, final full review, and diagnostic summary order. The complete suite must pass. Python, shell, PowerShell, rule-owner, link, manifest, and diff checks must pass.

Acceptance also requires one native-review smoke against a temporary synthetic commit. The staged tree and tracked worktree must be unchanged after that command. The installed reviewed candidate must make Doctor report `Result: ready`.

## Idempotence and Recovery

Read-only checks can be repeated. Synthetic commits are unreferenced and do not change a branch. If any required command fails, stop and report the error. Do not add fallback or recovery behavior.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, `.vscode/`, and ignored test results. Do not stage them. Local checkpoint commits do not authorize publication.

## Interfaces and Dependencies

The installed Adversarial Review contract now invokes the existing `codex review --commit` command. No new command, script, parser, service, dependency, or runtime API is added. The toolkit version becomes `0.22.0`.

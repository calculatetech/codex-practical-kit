# Review PRs before hosted CI

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose

PR publication must review the current head before hosted CI starts. Codex keeps the pull request draft, requests `@codex review`, and applies the normal review gates to each finding. A clean current-head review permits readiness and hosted CI.

## Progress

- [x] (2026-08-23) Reconciled CPK-043 with the completed CPK-040 through CPK-042 records.
- [x] (2026-08-23) Created branch `cpk-043-review-gated-publication` from `da3bb3361da35353a740d904b10a69c75e31779d`.
- [x] (2026-08-23) Made CPK-043 the only Active roadmap task.
- [x] (2026-08-23) Completed Design Preflight for the publication owner and its focused contract check.
- [x] (2026-08-23) Corrected the publication owner, focused checks, and version.
- [x] (2026-08-23) Passed the focused checks, all 82 default tests with one native Windows skip, compilation, shell syntax, and diff checks.
- [x] (2026-08-23) Completed documentation maintenance. The publication owner and this ExecPlan are the only substantive documentation changes.
- [x] (2026-08-23) Completed clean full review at staged tree `83974756aeebd1bcec086d33bd0fb1a5366b34c1`.
- [x] (2026-08-23) Completed review closure. Live installation remains untracked delivery evidence.

## Prior Plan Reconciliation

Record: `.agent/plan-history/plan-summary.20260822T050100617085Z.fd7dfe4c94e461a1824112794d31e1372d316ccf79eed8a3937d2754c1157e40.md`

Status: carried

Reason: CPK-040 remains authoritative for Plan capture and implementation handoff.

Record: `.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md`

Status: carried

Reason: CPK-041 remains authoritative for source-backed material decisions.

Record: `.agent/plan-history/plan-summary.20260823T052048899607Z.c539b46a7e5fa56092a382fef046fd00d4271c42c4fda8e0f0e2216ce94df122.md`

Status: carried

Reason: CPK-042 remains complete. CPK-043 adds a new corrective task after its checkpoint commits.

Record: `.agent/plan-history/plan-summary.20260824T031427928859Z.f30d03e6b396d05f07f5ce7eebc8b8e8b81e2b1cfe8ebc739342a6e444ca6968.md`

Status: carried

Reason: This record is the accepted CPK-043 implementation contract.

## Plan Deviations

The accepted CPK-043 marker named the task instead of a repository Markdown path. Plan History saved the record in central unlinked storage. This task copies the exact record beside this ExecPlan and keeps the central record unchanged.

## Product Boundary

[Publication](../../assets/skills/publication/references/publication.md) owns PR sequencing and publication gates. [Adversarial Review](../../assets/skills/adversarial-review/SKILL.md) owns finding scope, applicability, severity, and stop behavior. [Delivery Lifecycle](../../assets/skills/delivery-lifecycle/references/delivery-lifecycle.md) owns accepted corrections.

CPK-043 composes the PR publication procedure. The completed CPK-042 checkpoint process and direct integration remain opaque.

## Design Preflight

Required outcome: Codex reviews the latest PR head while the PR remains draft. Hosted CI starts only after no applicable finding remains.

Existing owner: `assets/skills/publication/references/publication.md`.

Normal-use behavior floor: Before remote publication, Codex proves that draft work does not start hosted CI. It opens a draft, requests `@codex review`, classifies each response through Adversarial Review, and marks the PR ready only after the current head is clean.

Scope ceiling: Do not add a workflow, parser, publication script, dispatcher, state machine, dependency, or runtime state. Do not copy the review rules into Publication.

Applicable failures and checks:

- The procedure marks a PR ready before a current-head draft review. A focused contract check must reject this sequence.
- A PR finding uses its raw severity before the scope gate. A focused route check must require Adversarial Review before any action.
- Protected `main` has draft-unsafe CI and the procedure falls back to direct integration. A focused contract check must require a configuration stop.
- A correction push preserves an earlier clean signal. A focused contract check must require a new draft review for the new head.

Preflight: ready — correct the single publication owner and add one focused contract check.

## Implementation

Replace automatic ready-state review with an explicit draft review. Define readiness from a completed current-head review with no retained applicable findings. Treat a thumbs-up as sufficient evidence, not the only clean result.

Route every PR finding to Adversarial Review before Publication considers severity, correction, or stop behavior. Route accepted corrections through Delivery Lifecycle. Keep detailed review rules in their current owners.

Require a draft-safe CI configuration before publication starts. If protected `main` requires a PR but the repository cannot prove this configuration, stop before the branch push. Keep the existing latest-head CI, conversation, mergeability, squash-merge, and integration gates.

Update the committed version from `0.21.0` to `0.21.1`. Update the focused tests and checksum manifest after content is final.

## Validation and Acceptance

The focused check must prove the draft review sequence, current-head reset, draft-safe CI gate, review-owner route, excluded-finding behavior, and severe-stop route. It must reject the obsolete automatic-review instruction.

Run the focused check, full Python suite, compilation, shell syntax, `git diff --check`, and manifest validation. Keep detailed output in `.agent/test-results/cpk-043-review-gated-publication.md`.

Finalize documentation before one fresh full review. After a final clean result, close the roadmap, update checksums, install the reviewed candidate, and require Doctor to report `Result: ready`.

## Interfaces and Dependencies

The installed `publish` contract gains a draft-review gate and a shared finding route. The toolkit version becomes `0.21.1`. No command, dependency, or runtime API changes.

## Outcome

Version `0.21.1` reviews the current PR head while the pull request remains draft. Publication scope-gates each finding before action. A clean current-head review permits readiness and hosted CI.

Full correctness review passed with no findings at staged tree `83974756aeebd1bcec086d33bd0fb1a5366b34c1`.

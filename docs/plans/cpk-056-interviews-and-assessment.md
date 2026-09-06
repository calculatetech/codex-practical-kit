# Improve interviews and assess rule adherence

This ExecPlan is the stable implementation specification for CPK-056. Maintain it according to [PLANS](../../.agent/PLANS.md).

## Purpose

Codex must ask material questions in prerequisite order and preserve accepted boundaries when a check fails. The toolkit must distinguish its written instruction checks from observed agent behavior. This task adds independent assessment cases and clarifies the existing rule owners.

## Context and orientation

The task branch is `task/cpk-056-interviews-assessment`. Its base is reviewed commit `24722f52ed1ab6e23689fb5095d6359d1848bc3b` on `task/cpk-055-native-ponytail`. The isolation form is one task branch. Preserve completed CPK-055 work and unrelated environment files.

`assets/skills/delivery-lifecycle/references/decision-handoffs.md` owns interviews. `assets/skills/adversarial-review/SKILL.md` owns correction authority. Design Preflight owns its challenger exemption. Owner Composition and Scenario Discrimination own causal proof and scenario evidence. `tests/test_kit.py` verifies their written contracts. The CPK-045 forward fixture contains assessment inputs and expected answers together.

## Applicable Plan history

The accepted implementation record is [.agent/plan-history/plan-summary.20260906T184718818166Z.101806a6188b911af737dd47187082418727ed7042831dd332d77360d1cb6b93.md](../../.agent/plan-history/plan-summary.20260906T184718818166Z.101806a6188b911af737dd47187082418727ed7042831dd332d77360d1cb6b93.md).

The prior interview record is [.agent/plan-history/plan-summary.20260906T161604059175Z.811836c214ecc89cb39c692f4366e4e79e56a698bf0d01445feb86fcd2c725f4.md](../../.agent/plan-history/plan-summary.20260906T161604059175Z.811836c214ecc89cb39c692f4366e4e79e56a698bf0d01445feb86fcd2c725f4.md).

Carry these inherited records and their existing recorded supersessions:

- [CPK-041](../../.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md): material-choice explanations and routine exclusions.
- [CPK-044](../../.agent/plan-history/plan-summary.20260824T135017227348Z.7cfbec79d5ce39f1a1d436a31dccfe0669c616f252b6793d4b90dc2b34ad13d6.md): correction authority and native review.
- [CPK-045](../../.agent/plan-history/plan-summary.20260824T164719361941Z.f1479c9effab9071b8ccaa86dce1dbee407b79647c6bb7d542aea8c75caae32b.md): behavioral boundaries, as subsequently reconciled.
- [Final CPK-046](../../.agent/plan-history/plan-summary.20260825T002911279202Z.940432714b78524077326cf1dea7571142fa6038e878a2fb7e884024bc8775a8.md): strict simplification and final native review.
- [Final CPK-047](../../.agent/plan-history/plan-summary.20260825T173129857080Z.a3ee26a1802fb85c5a0a100ccb3c33c1a6fff358bd20b65636adc61f8d0de377.md): bounded source packets and stable challenger identity.
- [CPK-053](../../.agent/plan-history/plan-summary.20260901T024803899174Z.f5becdd56d889aba50bf375a29ab0feb9012128e404e73e7a664e0243eb5ab8f.md): continuous proof and static-artifact trace eligibility.
- [CPK-055](../../.agent/plan-history/plan-summary.20260906T145108959420Z.4ca59f1efb35d2fec6091bc88b5848bb2e50226576f0a493f9ec85ed1838c57b.md): plugin-controlled Ponytail settings.

## Prior plan reconciliation

Record: `.agent/plan-history/plan-summary.20260906T161604059175Z.811836c214ecc89cb39c692f4366e4e79e56a698bf0d01445feb86fcd2c725f4.md`

Status: superseded

Reason: The user requested a combined interview and assessment implementation.

Replacement: Preserve all interview requirements and relay deferral. Add independent assessments and the correction and proof clarifications in this specification.

Scope: Unfinished CPK-056 work.

The accepted combined record is carried. Completed specifications and checkpoint commits remain historical evidence.

## Decision log

- Decision: Use saved cases, a separate grader, and fresh agents during this task.
  Rationale: A new runner or evaluation framework is unnecessary for the bounded comparison.
- Decision: Compare actual interview turns and disposable repair actions separately from instruction assertions.
  Rationale: Correct wording and self-reported compliance do not establish operational adherence.
- Decision: Keep correction authority and all proof rules in their existing owners.
  Rationale: Failure routing must not create a second policy or broaden automatic repair.
- Decision: Retain all numbered and unnumbered CPK-045 obligations under neutral identifiers.
  Rationale: The preflight challenger identified source-inventory and equal-result obligations outside the numbered list.
- Decision: Identify the selected rule snapshot and use each disposable case's own RepoWise graph.
  Rationale: A fresh conversation can otherwise read installed rules or the wrong repository graph.
- Decision: Permit expected red-to-green work already covered by an accepted plan and preflight.
  Rationale: A planned failing test does not revoke existing implementation authority.

## Product boundary and supported model

Apply [Scope Boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) and [Supported Model](../../assets/skills/design-preflight/references/supported-model.md).

The accepted combined Plan supplies the product boundary. Composing owners are Decision Handoffs, correction-entry wording and its finding format, the Design Preflight exemption, Owner Composition, Scenario Discrimination, and their test artifacts. Delivery Lifecycle composes only the route to correction authority. Research First remains the opaque research owner. Native review, severity, runtime trace JSON, install behavior, hooks, and platform internals remain opaque.

Use normal local files and one writer. Model assessments use disposable local repositories and deterministic provider examples. No real provider accounts are used. Meridian is outside the write boundary. Relay remains deferred.

The scope ceiling excludes a framework, runner, service, dependency, persistent interview tree, production instrumentation, new automatic approval, and publication. It also excludes hostile grading-file access as a security model. Such access invalidates an assessment; this task does not build a sandbox.

## Boundary inventory and checks

These boundaries describe instructions and assessments. They do not create fictional executable production paths. Static artifacts remain outside production trace closure.

| ID | Required result | Distinguishing check |
| --- | --- | --- |
| B1 | Questions follow investigated facts and settled prerequisites; batches contain at most three independent material questions. | Interview episode A and the existing decision-handoff contract test. |
| B2 | Partial answers and discoveries remove settled or obsolete questions; interviewing ends when the material contract is settled. | Staged replies in A contrast an unresolved prerequisite with a complete contract. |
| B3 | Material choices receive the existing source-backed brief before collection; routine inputs stay concise. | Episode A and `test_material_code_decisions_explain_implementation_before_choice`. |
| B4 | Agent inputs exclude grading answers and comparisons use the intended source snapshot. | Fixture correspondence checks; case-root source/read evidence and before/after transcripts. |
| B5 | Failed-check corrections use the unchanged authority gate; planned implementation retains its existing authority. | Episodes E/F/G and `test_review_findings_need_source_independent_correction_authority`. |
| B6 | Strict simplification exempts only the challenger and only when its existing conditions hold. | Episode G and `test_default_mode_preflight_and_repowise_continue_through_corrections`. |
| B7 | Decision ownership requires source and causal evidence; names and final data alone do not prove it. | Episode B and retained CPK-045 causal-path cases. |
| B8 | External-contract cases have independent evidence or remain unknown; deterministic external seams remain valid. | Episodes C/D and scenario contract assertions. |
| B9 | The assessment retains every existing numbered and unnumbered obligation and isolates its contrasts. | CPK-045 neutral case IDs, separate grader, and complete correspondence checks. |
| B10 | Rules stay single-owned and static artifacts remain ineligible for production trace closure. | Existing owner, route, link, and trace-eligibility tests. |

The accepted two-phase preflight supplied B1-B10. Both supported Phase 2 findings are incorporated in the decision log. No unresolved contract gap remains. Runtime input-domain and collection-path Scenario Proof are inapplicable to these static toolkit artifacts; the assessment catalog defines its concrete test inputs.

## Implementation and checkpoints

CP1 prepares the independent assessment artifacts and captures the baseline. Rewrite `tests/fixtures/cpk045-boundary-forward.md` as neutral inputs. Keep its grading in a separate JSON artifact. Add a CPK-056 case catalog and grading artifact under `tests/fixtures/`. Keep setup and execution instructions with that catalog. Extend `tests/test_kit.py` for complete correspondence and input separation. Freeze cases and the base rule snapshot before running fresh baseline agents. This checkpoint changes no live rule owner. Its local commit follows focused checks and native checkpoint review from the task base.

CP2 changes only the interview owner and its direct tests. Preserve the required brief while adding prerequisite ordering, independent batches, reassessment, partial-answer handling, and the stopping condition. Run its deterministic checks and the candidate interview episode. Review from CP1 and commit that checkpoint.

CP3 routes failed checks through the existing correction owner, adds `local-check` to the finding source values, and clarifies expected red tests and strict simplification. Add the decision-ownership example in Owner Composition and independent external evidence in Scenario Discrimination. Link Research First rather than copying its procedure. Extend affected contract tests. Run the remaining candidate assessments and retain their comparison. Review from CP2, commit the checkpoint, and run final native review from the task base.

## Assessment procedure

Each case has neutral facts, a task, source artifacts, and separate expected outcomes. The families are A (scripted interview), B (ownership), C (retained provider input), D (provider assumption), E (repair pressure), F (direct arithmetic repair), and G (authorized simplification). The coordinator gives scripted user replies only when the interview reaches the corresponding choice. Never open real user-facing widgets for an assessment.

Materialize each episode in a distinct temporary Git repository. Copy the selected live-rule tree and applicable relative-link targets into it. Include unchanged external skills named by applicable rules, such as `simple-english` for decision briefs. Keep grading, other cases, other rule versions, prior diagnostics, and preferred fixes outside that directory and outside the prompt. Retain source hashes in the ignored task record. Supply the selected local rule paths as the exercise's toolkit sources; do not use installed copies in their place.

Prepare only a local RepoWise index with:

    repowise init <case-root> --yes --no-prose --embedder mock --no-editor-setup --no-save-key --no-workspace

Scope lookups with the existing CLI's `--path <case-root> --no-workspace` options. Do not use the parent repository's MCP graph. Inspect actual reads and graph identity when grading. Wrong-version reads, grading access, and unavailable dependencies make the episode inconclusive.

Use a fresh agent with `fork_turns="none"` for each case and rule version. Hold the configured model, reasoning, ordinary implementation mode, tools, and Ponytail state constant. The coordinator grades source-backed answers and actual actions, not just verdict fields. Only E and F permit repository edits, and only inside their disposable roots. There is at most one write-capable assessment agent at a time. G is a classification check, not evidence that a complete operational workflow ran.

Run one baseline and one candidate attempt for each fixed case. Preserve failures, ties, and inconclusive outcomes. Do not repeat unchanged attempts to obtain a pass. A changed case invalidates both sides of its comparison. An interview result can be reused only if its selected source packet and case are unchanged.

Use short, dated authoritative references for external examples: [Microsoft Graph user lookup](https://learn.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0) and [delta query](https://learn.microsoft.com/en-us/graph/delta-query-overview). Label synthetic identities and retained examples. Offline cases do not prove live Graph compatibility.

## Validation and acceptance

Run focused tests from the repository root with:

    python3 -m unittest discover -s tests -p test_kit.py -k material_code_decisions
    python3 -m unittest discover -s tests -p test_kit.py -k assessment
    python3 -m unittest discover -s tests -p test_kit.py -k boundary_trace_closure
    python3 -m unittest discover -s tests -p test_kit.py -k correction_authority
    python3 -m unittest discover -s tests -p test_kit.py -k default_mode_preflight

Run `./run-tests.sh`, applicable shell and PowerShell syntax checks, rule-owner and link checks, `sha256sum --check MANIFEST.sha256`, and `git diff --check`. Regenerate checksums after substantive tracked changes. Static tests must preserve the old obligations and verify the new contract and fixture wiring.

Candidate assessment cases must satisfy their retained expectations. Classify each outcome as a correct action, correct stop, unnecessary stop, wrong action, or inconclusive. Failed required candidate cases remain unresolved validation and use the existing correction gate. Never relax the rubric to obtain a pass. Report ties honestly and claim no statistical reliability rate.

Finalize documentation before review. Use the existing [Adversarial Review](../../assets/skills/adversarial-review/SKILL.md) checkpoint and final sequence. Install the reviewed candidate and run Doctor. The default suite, installer, and Doctor gain no model calls. Keep version selection and publication separate.

## Artifacts and interfaces

Keep detailed evidence in `.agent/test-results/cpk-056-interviews-and-assessment.md`. It includes snapshot identities, input hashes, actual transcripts, disposable diffs, checks, grading, and native review evidence. Do not stage this record.

The finding source vocabulary gains `local-check`. Assessment responses use neutral case identifiers, verdicts, evidence, and proposed actions. No runtime API, CLI, trace schema, dependency, or persistent product state changes.

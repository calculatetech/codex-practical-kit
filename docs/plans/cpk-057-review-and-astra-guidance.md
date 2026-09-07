# Separate review from testing and complete Astra guidance

This ExecPlan is the implementation specification for CPK-057. Maintain it according to [PLANS](../../.agent/PLANS.md).

## Purpose

Reviewers inspect source and existing evidence without executing tests. Implementation completes validation before review. The toolkit also adds missing Astra guidance for authorized work, instruction precedence, communication, and useful delegation.

## Context and orientation

The task branch is `task/cpk-057-review-astra-guidance`. Its base is `a33c806c4187f89a2fefa73c913146f3f07858b8` on `task/cpk-056-interviews-assessment`. Use one branch and one implementation writer. Preserve completed checkpoints and unrelated environment files.

Adversarial Review owns reviewer behavior. Delivery Lifecycle owns implementation validation and authorized task completion. Coordination owns agent roles and instruction use. Docs Maintainer owns the additional prose guidance. Toolkit Maintainer owns the instruction conflict audit. Publication transports the canonical reviewer instructions into hosted requests.

The direct instruction checks are in `tests/test_kit.py`. The native review command remains `codex review --commit <synthetic-commit>`. The installed skills and existing AGENTS routing supply normal local instructions. Hosted reviewers cannot rely on the local installed skills.

## Applicable Plan history

The accepted record is [CPK-057](../../.agent/plan-history/plan-summary.20260907T162300226611Z.ddc507f2e3b9b24182cb6abc4eb4782feae98a0c25f8cdc174a2bf8c2c9932a1.md).

Carry these records and their recorded supersessions:

- [CPK-041](../../.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md): material decisions and explanations.
- [CPK-042](../../.agent/plan-history/plan-summary.20260823T052048899607Z.c539b46a7e5fa56092a382fef046fd00d4271c42c4fda8e0f0e2216ce94df122.md): semantic checkpoints.
- [CPK-043](../../.agent/plan-history/plan-summary.20260824T031427928859Z.f30d03e6b396d05f07f5ce7eebc8b8e8b81e2b1cfe8ebc739342a6e444ca6968.md): hosted review before CI.
- [CPK-044](../../.agent/plan-history/plan-summary.20260824T135017227348Z.7cfbec79d5ce39f1a1d436a31dccfe0669c616f252b6793d4b90dc2b34ad13d6.md): native discovery and correction authority.
- [CPK-045](../../.agent/plan-history/plan-summary.20260824T164719361941Z.f1479c9effab9071b8ccaa86dce1dbee407b79647c6bb7d542aea8c75caae32b.md): boundary inventory, as subsequently reconciled.
- [Final CPK-046](../../.agent/plan-history/plan-summary.20260825T002911279202Z.940432714b78524077326cf1dea7571142fa6038e878a2fb7e884024bc8775a8.md): final native review and bounded scope.
- [Final CPK-047](../../.agent/plan-history/plan-summary.20260825T173129857080Z.a3ee26a1802fb85c5a0a100ccb3c33c1a6fff358bd20b65636adc61f8d0de377.md): bounded preflight and publication.
- [CPK-048](../../.agent/plan-history/plan-summary.20260825T183857932150Z.47ec1ac118b8c6c23f961b4099708aacc7031581a744bc389e6795e1c2007796.md): focused repository overrides.
- [CPK-053](../../.agent/plan-history/plan-summary.20260901T024803899174Z.f5becdd56d889aba50bf375a29ab0feb9012128e404e73e7a664e0243eb5ab8f.md): continuous proof and static-artifact eligibility.
- [CPK-055](../../.agent/plan-history/plan-summary.20260906T145108959420Z.4ca59f1efb35d2fec6091bc88b5848bb2e50226576f0a493f9ec85ed1838c57b.md): upstream Ponytail ownership.
- [Final CPK-056](../../.agent/plan-history/plan-summary.20260906T184718818166Z.101806a6188b911af737dd47187082418727ed7042831dd332d77360d1cb6b93.md): interviews and correction entry.

This is new corrective work. Do not rewrite completed specifications or their checkpoint commits.

## Decision log

- Decision: Keep the existing native review command and AGENTS route.
  Rationale: The [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli) makes custom prompts incompatible with `--commit`. A configuration override can replace user instructions.
- Decision: Carry the user's actual no-tests requirement in this task's synthetic commit intent.
  Rationale: The first review precedes installation of the changed skill. The intent remains a requirement, not a coordinator verdict.
- Decision: Include the canonical execution restriction in each hosted review request.
  Rationale: [Hosted review supports additional request instructions](https://learn.chatgpt.com/docs/third-party/github). Local installed skills are not a demonstrated hosted instruction source.
- Decision: Use bounded proactive delegation with the existing role limits.
  Rationale: The user selected this adaptation of the guide's broader delegation example.
- Decision: Leave delegation behavior proof to another project.
  Rationale: The user's later instruction explicitly removes local delegation assessments from this task. Normal repository checks remain applicable.

## Product boundary and preflight

Apply [Scope Boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) and [Supported Model](../../assets/skills/design-preflight/references/supported-model.md).

The composing owners are the reviewer execution boundary, lifecycle validation and autonomy, coordination, prose guidance, instruction maintenance, hosted request wording, and their direct checks. Review modes, correction authority, severity, material-decision contracts, runtime trace rules, installation, hooks, and external skills remain opaque.

Use normal local files and Git. The scope excludes new skills, frameworks, wrappers, runtime configuration, model settings, dependencies, external-project work, and publication. Do not add delegation assessments or repeat CPK-056 cases.

These are static instruction boundaries. Production entry points and runtime Scenario Proof are inapplicable. Use deterministic instruction checks and the required native reviews.

| Boundary | Required result | Contrast and check |
| --- | --- | --- |
| B1 | Reviewers inspect source without executing or delegating tests. | Read test bodies versus execute them; direct review contract checks and actual native tool activity. |
| B2 | Implementers validate before review and repeat checks only for a concrete reason. | Unchanged validated candidate versus an authorized correction; lifecycle and correction contract checks. |
| B3 | Authorized work continues within the active mode and accepted scope. | Routine judgment versus an unresolved material choice; lifecycle and existing handoff checks. |
| B4 | User instructions outrank skill guidelines; skill-caused stops identify their exact source. | Explicit applicable requirement versus inferred approval; instruction-use checks. |
| B5 | Ordinary prose is clear while required formats and technical literals remain intact. | An explanation versus required JSON or a decision brief; prose and existing handoff checks. |
| B6 | Delegation targets useful independent work. | Useful parallel assignment versus trivial or dependent work; normal instruction consistency checks only. |
| B7 | Delegation preserves existing role, writer, capacity, and native-review restrictions. | Coordinator authority versus restricted child roles; existing coordination checks. |
| B8 | Each live rule stays in its owner with valid routes. | A canonical rule versus a copied or broken route; owner and link checks. |
| B9 | The task makes no claim of validated delegation behavior. | Instruction consistency versus observed behavior; task scope and final report. |

The latest user scope excludes local delegation observations. Keep detailed preflight evidence in the ignored task record.

## Guide coverage

The source is the Astra [Prompting best practices](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices) section, read on 2026-09-07. Its API features and model settings are outside this task.

| Advice | Disposition and owner |
| --- | --- |
| Infer action intent and finish authorized work | Add to Delivery Lifecycle, bounded by active mode and scope. |
| Prepare before approval and avoid speculative barriers | Add to Delivery Lifecycle; preserve material choices and correction authority. |
| Audit instruction conflicts | Add the scoped audit to Toolkit Maintainer. |
| User priority and visible skill-caused stops | Add to Coordination. |
| Plain words, active voice, and exact technical content | Already covered by Simple English and Docs Maintainer. |
| Connected prose, useful formatting, and appropriate detail | Add only the missing preferences to Docs Maintainer. |
| Avoid stock phrases and invented labels | Extend Docs Maintainer without copying the external vocabulary guide. |
| Useful delegation | Adapt in Coordination to the user's existing role limits. |
| Legible agent messages | Add to Coordination. |
| Proportionate tests and justified repeats | Add to Delivery Lifecycle; reviewer execution remains prohibited. |
| Focused material questions | Already covered by Decision Handoffs and completed CPK-056. |

## Implementation checkpoints

CP1 changes Adversarial Review and the implementation validation paragraph in Delivery Lifecycle. Add a named reviewer execution section. Publication reads that canonical section when it prepares both initial and repeated review requests. Extend the existing review and publication checks. Keep native targets, independent discovery, correction authority, and CI ordering unchanged. Validate the checkpoint, run native checkpoint review from the task base, and create its local commit.

CP2 adds the remaining collaboration guidance to Delivery Lifecycle, Coordination, Docs Maintainer, and Toolkit Maintainer. Preserve the existing routers and external skill contents. Add only the necessary contract assertions to the existing tests. Review this checkpoint from CP1 and commit it locally. Then run final native review from the task base.

## Validation and delivery

Publication version: `0.23.9`. This patch includes the CPK-055 installation fix and the CPK-056 and CPK-057 guidance changes.

From the repository root, run focused checks before each checkpoint review:

    python3 -m unittest discover -s tests -p test_kit.py -k review
    python3 -m unittest discover -s tests -p test_kit.py -k coordination
    python3 -m unittest discover -s tests -p test_kit.py -k material_code_decisions
    python3 -m unittest discover -s tests -p test_kit.py -k rule_

Run the repository-required suite with `./run-tests.sh`. Run applicable shell and PowerShell syntax checks, checksum validation, and `git diff --check`. Update `MANIFEST.sha256` after substantive files are final. Preserve old assertions rather than weakening them for the new guidance.

Inspect actual native review tool activity after each required review. Require zero executed or delegated tests, source-backed discovery, and unchanged reviewed tree identity. A narrated claim alone does not establish adherence. Use the existing correction gate for an unmet required check. Add no separate review experiment.

After final clean review, apply normal roadmap and checksum closure. Install the reviewed candidate with `python3 kit.py install --repo .`. Run `python3 kit.py doctor --repo .` and require `Result: ready`. Version selection, push, merge, tags, and releases remain separate.

## Records and interfaces

Keep commands, outputs, preflight evidence, reviewer tool activity, and delivery results in `.agent/test-results/cpk-057-review-and-astra-guidance.md`. Do not stage this record. The instruction interfaces change; runtime APIs, CLI options, trace schemas, and installation behavior do not.

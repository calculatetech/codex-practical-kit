# Publish Plan History through protected pull requests


This ExecPlan follows [PLANS.md](../../.agent/PLANS.md) and defines CPK-059.

## Purpose


Release reusable Plan History as version `0.24.0` from a public repository. Changes enter `main` through reviewed pull requests and required CI. A pull request remains draft during Codex review, then readiness starts the required checks.

## Context and boundary


Use `task/cpk-059-public-pr-release` from `3ced26461e9de5e97082d0b7c9e0ce1c0f4fd453`. The repository is `calculatetech/codex-practical-kit`. Its initial main commit is `6cc881661646e2bb0c96e07fcf56897e7f7cbf5f`.

The user requested public visibility, branch protection, publication, and release. The user selected Codex review plus required CI without an additional human approval.

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) and [Supported model](../../assets/skills/design-preflight/references/supported-model.md). Workflow configuration, native GitHub settings, version identity, and release delivery are composed here. The existing test launcher, installer, and [CPK-058 implementation](cpk-058-plan-history-compaction.md) remain unchanged owners.

Normal use is a single writer with GitHub administrator access and a configured Codex GitHub review connection. Preserve unrelated untracked files. No new review service, credentials, platform matrix, cleanup, or production runtime is needed.

## Decision Log


- Decision: Release `0.24.0` under the [version policy](../../assets/skills/publication/references/versioning.md).
  Rationale: CPK-058 adds reusable summaries and resumable reads, a new capability beyond `0.23.9`.
- Decision: Use one native GitHub Actions job, `toolkit-tests`.
  Rationale: The existing standard-library suite and checksum command provide the needed checks without a new dependency.
- Decision: Trigger only on PR `ready_for_review` targeting `main`, and pushes to `main`.
  Rationale: Task pushes and draft creation must not spend hosted CI. Explicit event types exclude the default PR events.
- Decision: Require zero formal approving reviews while retaining a clean Codex review as a publication gate.
  Rationale: The repository has one owner. A Codex thumbs-up is evidence for the publication procedure, not a formal GitHub approval.
- Decision: Use native branch protection and squash merges.
  Rationale: GitHub already provides required checks, conversations, administrator enforcement, and linear history.

## Implementation


Use one atomic subtask, CP1, with one full native-review and local-commit boundary. Its primary owner is `.github/workflows/ci.yml`; settings and release consume that workflow.

Create the workflow named `CI`. Its only events are `pull_request` with `branches: [main]` and `types: [ready_for_review]`, plus `push` with `branches: [main]`. Grant only `contents: read`.

Define `toolkit-tests` on `ubuntu-latest`. Use `actions/checkout@11d5960a326750d5838078e36cf38b85af677262` with `persist-credentials: false`. Use `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065` with Python `3.11`. Run `./run-tests.sh`, then `sha256sum --check MANIFEST.sha256`. Do not skip steps or tolerate failures.

Set `kit.py`'s `KIT_VERSION` and its existing test assertion to `0.24.0`. Add one static workflow test in `tests/test_kit.py`. It enumerates all workflow files and rejects extra triggers or conditional check suppression. Update README contribution instructions and distribution checksums.

After local review, set repository visibility to public and allow only squash merging. Configure main protection with strict required status context `toolkit-tests`, administrator enforcement, resolved conversations, and linear history. Disable force pushes and deletion. Set required approving count to zero, dismiss stale reviews, and require neither code-owner nor last-push human approval. Keep push restrictions null. Read back the actual settings.

Use the [publication procedure](../../assets/skills/publication/references/publication.md) for local closure, installation, draft review, readiness, squash merge, and integration. The first PR supplies the missing workflow through its merge ref. Prove the complete workflow inventory before the task push. Verify the actual hosted Codex response before readiness.

After integration and passing main CI, create the unused tag and full GitHub release `v0.24.0` at the exact integrated main commit. Release notes describe reusable summaries, resumable reading, and the PR workflow. Link the versioned README and the full changelog since the previous release, `v0.23.2`.

## Validation and acceptance


Run from the repository root:

    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Require the suite to pass and every checksum to match. Validate workflow structure with an available YAML parser without adding a package dependency. After review, install with `./install.sh` and require `./doctor.sh` to report `Result: ready` for `0.24.0`.

| Boundary | Observable evidence |
| --- | --- |
| B1: protection | API readback shows public visibility, PRs, strict required CI, conversations, administrator enforcement, and zero extra approvals |
| B2: CI timing | Complete workflow inventory excludes task pushes and draft events; actual readiness starts `toolkit-tests` |
| B3: review identity | Frozen local commit equals remote branch and PR head; clean hosted review applies to that head |
| B4: merge gates | All paginated checks and conversations are accounted for; checks pass, no changes are requested, and GitHub reports mergeability |
| B5: integration | Clean local main fast-forwards to origin/main, contains the squash result, and passes main CI |
| B6: release identity | Source version and checksums agree; unused `v0.24.0` resolves to integrated main; release is neither draft nor prerelease |
| B7: consumption | Reviewed-candidate installation and Doctor succeed |

If a correction occurs, repeat the current-head gates through the canonical procedure. Do not manufacture a correction to test this path. Static configuration invokes the unchanged launcher; it adds no production path requiring semantic trace closure.

## Plan history and recovery


Carry the original records and scoped supersessions reconciled in CPK-058. The reading checkpoint can be reused after complete source identity and hash verification. Publication and native-review contracts remain in force. The current request adds public repository setup and a release; it does not reopen the CPK-058 implementation.

- [Original 1](../../.agent/plan-history/plan-summary.20260819T195712262086Z.manual-recovery.md)
- [Original 2](../../.agent/plan-history/plan-summary.20260819T211423672232Z.manual-recovery.md)
- [Original 3](../../.agent/plan-history/plan-summary.20260822T050100617085Z.fd7dfe4c94e461a1824112794d31e1372d316ccf79eed8a3937d2754c1157e40.md)
- [Original 4](../../.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md)
- [Original 5](../../.agent/plan-history/plan-summary.20260823T052048899607Z.c539b46a7e5fa56092a382fef046fd00d4271c42c4fda8e0f0e2216ce94df122.md)
- [Original 6](../../.agent/plan-history/plan-summary.20260824T031427928859Z.f30d03e6b396d05f07f5ce7eebc8b8e8b81e2b1cfe8ebc739342a6e444ca6968.md)
- [Original 7](../../.agent/plan-history/plan-summary.20260824T135017227348Z.7cfbec79d5ce39f1a1d436a31dccfe0669c616f252b6793d4b90dc2b34ad13d6.md)
- [Original 8](../../.agent/plan-history/plan-summary.20260824T164719361941Z.f1479c9effab9071b8ccaa86dce1dbee407b79647c6bb7d542aea8c75caae32b.md)
- [Original 9](../../.agent/plan-history/plan-summary.20260825T002758364682Z.4eba52594f2ef5bdbe93f4f0ead7b61802e894668d23c749b5af459f65a19437.md)
- [Original 10](../../.agent/plan-history/plan-summary.20260825T002911279202Z.940432714b78524077326cf1dea7571142fa6038e878a2fb7e884024bc8775a8.md)
- [Original 11](../../.agent/plan-history/plan-summary.20260825T172626414955Z.9eaf7888a286b18f69d5a94869ee99522214d23dd715a553664a2041108fced3.md)
- [Original 12](../../.agent/plan-history/plan-summary.20260825T173129857080Z.a3ee26a1802fb85c5a0a100ccb3c33c1a6fff358bd20b65636adc61f8d0de377.md)
- [Original 13](../../.agent/plan-history/plan-summary.20260825T183857932150Z.47ec1ac118b8c6c23f961b4099708aacc7031581a744bc389e6795e1c2007796.md)
- [Original 14](../../.agent/plan-history/plan-summary.20260901T024803899174Z.f5becdd56d889aba50bf375a29ab0feb9012128e404e73e7a664e0243eb5ab8f.md)
- [Original 15](../../.agent/plan-history/plan-summary.20260906T145108959420Z.4ca59f1efb35d2fec6091bc88b5848bb2e50226576f0a493f9ec85ed1838c57b.md)
- [Original 16](../../.agent/plan-history/plan-summary.20260906T161604059175Z.811836c214ecc89cb39c692f4366e4e79e56a698bf0d01445feb86fcd2c725f4.md)
- [Original 17](../../.agent/plan-history/plan-summary.20260906T184718818166Z.101806a6188b911af737dd47187082418727ed7042831dd332d77360d1cb6b93.md)
- [Original 18](../../.agent/plan-history/plan-summary.20260907T162300226611Z.ddc507f2e3b9b24182cb6abc4eb4782feae98a0c25f8cdc174a2bf8c2c9932a1.md)


Record operational evidence in `.agent/test-results/cpk-059-public-pr-release.md`. Preserve existing remote state after an actual failure. Never move or recreate a published tag. A missing hosted review connection requires configuration before readiness. Do not bypass protected main or discard local changes.

Revision: define native CI, protection, and versioned release in response to the user's publication request and selected solo review gate.

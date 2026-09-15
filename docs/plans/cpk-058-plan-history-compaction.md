# Compact Plan History without losing source evidence


This ExecPlan follows [PLANS.md](../../.agent/PLANS.md). It defines the CPK-058 reading-method change.

## Purpose


Large Plan histories must remain usable across context windows and future tasks. An agent reads bounded batches, retains decisions outside conversation context, and reuses verified summaries. It never deletes original Plan captures to reduce context use.

The user requested this method on 2026-09-15 and selected reusable summaries with links to unchanged originals. Normal context compaction during a read must resume the work instead of triggering the old size-only stop.

## Context and isolation


Use branch `task/cpk-058-plan-history-compaction` from synchronized `main` at `6cc881661646e2bb0c96e07fcf56897e7f7cbf5f`. There is one writable stream.

`assets/skills/plan-history/SKILL.md` owns history discovery, reading, and reconciliation. Its old instruction stops when the complete applicable history cannot fit in context. `assets/hooks/session_start.py` routes compact-session starts back to this skill. That hook has no context-capacity detector or reading checkpoint.

`tests/test_kit.py` checks the installed instructions and executes the real hook for startup and compact events. `README.md` describes the user-visible storage behavior. Original captures remain in `.agent/plan-history/` and travel through Git.

A derived summary is a scoped reading aid. Its source inventory identifies the complete original bytes that it summarizes. It neither replaces those originals nor becomes another implementation plan.

## Decision Log


- Decision: Extend the existing instruction owner with reusable Markdown summaries and bounded reading checkpoints.
  Rationale: The failure is an instruction-level stop. A new summarization service, parser, database, or token-limit setting is unnecessary.
- Decision: Store derived evidence in `.agent/plan-history/compacted/`, separately from original captures. Keep mutable reading progress in the ignored task result.
  Rationale: Future tasks can reuse evidence through Git without confusing it with captured Plan responses or tracked lifecycle status.
- Decision: Require original source hashes, scope, decision anchors, and explicit fidelity verification before reuse.
  Rationale: A hash detects changed bytes but cannot prove that a summary preserved their meaning. A broader task must reopen uncovered scope.
- Decision: Preserve original timestamps, conflict evidence, scoped supersession, and decisions outside a replacement's scope.
  Rationale: A newer summary must not silently override an older accepted decision.
- Decision: Split large sources and summaries into bounded reads and save progress after chunks.
  Rationale: The method must work when even one original exceeds the comfortable reading budget. Missing checkpoints require evidence reconstruction, not a context-size stop.
- Decision: Use direct original references instead of recursive summary chains.
  Rationale: Each summary can be checked and replaced independently when its evidence changes.
- Decision: Validate the procedure as instructions and validate routing through the existing hook subprocess test.
  Rationale: No executable semantic compressor is added. These checks cannot establish a general model-fidelity rate or reproduce the user's suspected app interruption.

## Product boundary and reconciliation


Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) and [Supported model](../../assets/skills/design-preflight/references/supported-model.md). Normal use includes one writer, local files, Git worktrees, new history records, future tasks, and ordinary context compaction during reads.

The Plan History reading procedure, derived-summary format, compact routing text, and related checks are `composes`. Original capture timing, marker parsing, event identity, byte-preserving storage, repository setup, publication, and original-record relocation remain `opaque`. No filesystem-fault recovery, concurrent writer coordination, automatic compaction API, model selection, or external-project change is included.

The user's current request replaces the literal all-originals-in-context requirement and size-only stop. Preserve complete evidence coverage and genuine source-backed conflict stops. This supersedes only those reading restrictions in the current Plan History owner and the unchanged-reconciliation boundary of [CPK-054](cpk-054-internal-plan-history.md). The exact-capture and source-authority contract of [CPK-036](cpk-036-plan-history.md) remains.

Carry the prior records and their recorded scoped supersessions. CPK-054 remains authoritative for central-only capture and one-way byte-verified handoff. CPK-044 and final CPK-046 remain authoritative for native review. CPK-053 excludes static instruction changes from production trace closure. CPK-055 preserves upstream Ponytail ownership. CPK-056 and CPK-057 retain bounded correction, validation, and communication rules. Their prior assessment work is not repeated here.

Applicable original records (retain their recorded supersessions):

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

## Boundary inventory and checks


| Boundary | Required distinction | Check |
| --- | --- | --- |
| B1 | Small versus oversized history, including a decisive clause beyond the first chunk of one original | Existing history contract test requires intra-record chunks, complete coverage, and no unread-tail planning |
| B2 | Uninterrupted versus compacted reading, including a partial record and a missing checkpoint | Existing hook subprocess test checks compact routing; history contract checks saved ranges, hash validation, and reconstruction |
| B3 | Valid future-task summary versus new, changed, incomplete, or out-of-scope evidence | History contract checks direct originals, scope, verification, stale-evidence rereading, and supplemental original links |
| B4 | Empty or singleton inventory versus duplicate prefix followed by a distinct record or collision | Preserve full discovery and event-plus-byte identity; check separate derived-summary discovery and final inventory enumeration |
| B5 | Explicit supersession versus unresolved cross-batch conflict; scoped replacement versus unaffected decisions | Preserve canonical supersession fields, original order, both conflict sources, and carried decisions outside scope |

The fresh preflight challenger independently derives the source clauses and these distinctions, then checks the concrete procedure. These are instruction boundaries, not a new executable history subsystem.

## Implementation


Use one atomic subtask, CP1, with one full native-review and local-commit boundary. Replace the size-only stop and raw-reread wording in the existing Plan History owner. Define the summary fields, reuse validation, bounded reads, resumable working checkpoint, final inventory check, and actual blocking conditions there.

Change only the compact-session reminder in `assets/hooks/session_start.py` to route to saved reconciliation. Preserve the event dispatch, capture behavior, and output format. Extend the existing history contract and startup/compact tests in `tests/test_kit.py`. Add a short user-facing description beside the current Plan History paragraph in `README.md`.

Do not add a compression helper or create speculative summaries for unrelated topics. Agents create scoped derived summaries when history size or subsequent reuse needs them. Summary revisions are immutable; verification errors produce new derived evidence while preserving originals.

## Validation and acceptance


From the repository root, run:

    python3 -m unittest discover -s tests -p test_kit.py -k plan_history_is_immutable
    python3 -m unittest discover -s tests -p test_kit.py -k session_start_still
    ./run-tests.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Regenerate affected manifest hashes before the checksum check. Run applicable shell and PowerShell syntax checks. Keep full commands, results, source-read inventory, and native review output in `.agent/test-results/cpk-058-plan-history-compaction.md`.

Walk through five concrete examples against the procedure: a large record with a trailing constraint; compaction after a partial read; a valid reused summary followed by a new record; a duplicate prefix followed by a different-content collision; and a cross-summary conflict with and without a scoped supersession. In each case identify the retained evidence, next read, and whether planning can continue. These examples assess the procedure's completeness, not observed model reliability.

After clean native review, close the roadmap entry and create the local commit. Install the candidate with `./install.sh`; require `./doctor.sh` to report `Result: ready`. Publication and version selection remain separate.

## Recovery and dependencies


Use existing Git and ordinary Markdown files. Use SHA-256 tools to identify complete source bytes. A missing or stale derived summary permits rereading its original evidence. A changed partial source restarts that source, preserving unaffected coverage. A genuinely unreadable required original or unresolved original-source conflict remains a specific blocker.

No automatic context reset is required. A completed checkpoint remains usable after one occurs. The agent can partition large reconciliation by topic while retaining cross-topic references in its working record.

Revision: add reusable derived evidence and resumable reads in response to the user's history-capacity and compaction report.

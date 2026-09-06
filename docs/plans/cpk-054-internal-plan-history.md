# Keep one versioned Plan history

This ExecPlan follows [PLANS.md](../../.agent/PLANS.md). It records the CPK-054 storage correction.

## Purpose

Completed Plan summaries must stay versioned in `.agent/plan-history/` so another device receives them through Git. Stop creating additional files beside specifications. After an untracked summary moves into a task worktree, a later primary-checkout hook must not recreate the same event and content.

The user requested this change on 2026-09-05. The user excluded cleanup of other repositories and retained the generated roadmap view as an exception. A later request authorized publication and updating the host installation.

## Context and isolation

`save_plan` in `assets/hooks/session_start.py` owns storage. Direct `Stop` events supply a completed message. `UserPromptSubmit`, `SessionStart`, and `SessionEnd` supply it through the transcript reader. The exact message contains specification markers, so associations survive without sibling files. `write_record` already compares event identity and bytes before writing, but only in the current worktree.

`assets/skills/plan-history/SKILL.md` owns discovery and worktree handoff. `tests/test_kit.py` contains real hook subprocess checks. The README describes the storage behavior.

Use branch `fix/plan-history-storage`, based on `main` at `2115b270a50ead31f7071f5d95b5210ba7c6b290`. The earlier, reviewed roadmap instruction change remains in the same working tree and complete review candidate. There is one writable stream and no worktree transfer for this task.

## Product boundary and Decision Log

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) and [Supported model](../../assets/skills/design-preflight/references/supported-model.md). Normal use has one Codex writer, primary and linked Git worktrees, and ordinary files. Normal tracked copies in different checkouts and devices remain necessary; redundant generated records are the defect.

The storage destination, duplicate suppression, discovery instructions, affected checks, and this repository's legacy cleanup are `composes`. Transcript parsing, marker validation, capture timing, roadmap generation, and hook output formats remain `opaque`. Other repositories, scans of inactive branches, automatic migration, and new storage formats are outside this task. Publication and host installation use the existing delivery commands.

Decision: publish version `0.23.8`, a patch increment from committed version `0.23.7` for the storage correction. Run `./install.sh` and require `./doctor.sh` to report `Result: ready` before publication.

Decision: retain the existing versioned directory and remove the sibling writer. Do not use local-only Git metadata storage.

Decision: extend the existing immutable writer's search across active worktrees reported by `git worktree list --porcelain -z`. An identical event already retained in another worktree requires no new file. A new event or different response bytes still requires preservation. Do not add a shared index, database, dependency, or new command.

Decision: keep one-way handoff into the task worktree, then let Git carry the committed record to main. Do not manually copy history back to main. Do not remove ordinary tracked records from other checkouts.

Decision: during this repository's cleanup, reuse a central record only when its event identity and bytes match. Otherwise copy the legacy record centrally and verify its bytes before removing the old path. Retain timestamps, event keys, and collision suffixes. Remove only the specification-stem prefix from a migrated filename. Update references outside immutable summaries.

## Prior plan reconciliation

Record: `.agent/plan-history/plan-summary.20260822T050100617085Z.fd7dfe4c94e461a1824112794d31e1372d316ccf79eed8a3937d2754c1157e40.md`
Status: superseded
Reason: The user requested one internal, versioned summary location.
Replacement: Save repository summaries only centrally and retain associations in their unchanged markers.
Scope: specification-sibling creation only. Capture timing, exact bytes, identity, and global fallback remain carried.

Record: `.agent/plan-history/plan-summary.20260825T173129857080Z.a3ee26a1802fb85c5a0a100ccb3c33c1a6fff358bd20b65636adc61f8d0de377.md`
Status: superseded
Reason: The user reported duplicate summaries in main and requested a single versioned location.
Replacement: Hand off applicable untracked central records into the task worktree, suppress exact replay across active worktrees, and commit them there. Git integration replaces manual copying to main.
Scope: required sibling copies and duplicate replay. The byte-verified handoff and protection of unrelated records remain carried.

These decisions supersede the storage-location clauses in completed CPK-036 and CPK-040 specifications. Their historical descriptions remain evidence. Other completed task records do not add scope to this correction.

## Boundary inventory and Scenario Proof

Apply [Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md), [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md), and [Full-set results](../../assets/skills/design-preflight/references/full-set-results.md).

| Source clause | Disposition |
| --- | --- |
| User: internal organization and versioned cross-device history; old sibling creation in `save_plan` and Plan History capture/association instructions | B1 |
| User: avoid redundant main/worktree copies; existing event-key and exact-byte equality in `write_record`; handoff directions | B2 |
| Existing immutable writer: preserve distinct identities and different-content collisions; preserve non-Git capture using the same writer | B3 |
| User: one place for summaries; Plan History complete discovery, immutable evidence, and commit instructions | B4, non-runtime |
| Existing marker validation: missing markers, sole or mixed none, all valid/invalid specification targets | Opaque; keep validation and warning regressions |
| Existing envelope, newest-turn selection, transcript completion, capture timing, and hook output formats | Opaque; keep existing regressions |
| Reconciliation order, explicit supersession, immutable completed checkpoints, and partial-history stop | Opaque; unchanged |
| Roadmap generation and publication implementation | Opaque; unchanged |
| Other repositories, concurrent writers, hostile markers, bare repositories, and inactive-branch scanning | Outside task scope |
| Later user request: publish and update the host environment | Existing publication and installation workflow; no new runtime boundary |
| Readme and exact tests describing the storage facts | Supporting documentation/checks, not additional boundaries |

| Boundary | Discriminator and contrast | Production path and terminal oracle | Exact named check |
| --- | --- | --- | --- |
| B1 | One or multiple valid specification markers versus none | Each supported hook reaches `save_plan` and `write_record`: exact central record, no specification sibling, idempotent replay. Commit and clone retain that same captured record. | `test_plan_history_stays_internal_for_every_event` |
| B2 | Primary capture before handoff versus replay after the same event/bytes exists only in a linked task worktree | Each hook captures in primary; byte-verified handoff and task commit precede a primary replay. Worktree enumeration and the shared writer suppress regeneration. Git merge retains the single tracked record and clean status. | `test_plan_history_handoff_then_primary_replay` |
| B3 | Exact repeated identity/content versus changed bytes or new identity, including duplicate prefixes followed by different content | Each hook reaches the same writer across active worktrees. Exact repeats add nothing; different content and identities survive. A replay of a collision also adds nothing. Outside Git, only the existing cwd-specific fallback participates. | `test_plan_history_cross_worktree_identity` and `test_plan_history_uses_global_storage_outside_git` |
| B4 | Legacy sibling plus identical central record versus a unique legacy record | Non-runtime cleanup retains one central copy of each event/content and all distinct-content evidence. Direct discovery still includes unmigrated legacy records. | Exact Git-source/destination byte comparison and `test_plan_history_is_immutable_and_complete` |

Every hook case means direct Plan-mode Stop, UserPromptSubmit, SessionStart for resume/compact/clear, and SessionEnd. Named tests invoke the real hook subprocess; they do not replace an in-scope runtime hop. Repository-scope checks include nested cwd and a linked worktree path containing spaces. The supported handoff acts on retained state before the later replay.

## Implementation and validation

Use one atomic subtask, CP1. Remove the sibling write loop in `save_plan`. Obtain active worktree history directories with native Git and pass them to the existing writer for equality and collision searches. Keep new writes in the current repository's central directory and retain the current global fallback outside Git. Validate markers before deciding whether an event is already retained, so warnings remain observable.

Change the skill to create central records only, link later specifications to those records, and hand off only toward the task worktree. Preserve legacy discovery and document safe, explicit cleanup. Move this repository's unique legacy summaries centrally and remove verified duplicates. Correct references and the README.

Run the new central-storage check before the runtime edit. Then run all named Scenario Proof methods with `PYTHONPATH=tests python3 -m unittest test_kit.PlanHistoryHookTests.<method> -v`. Run `./run-tests.sh`, compare migrated record bytes against the task-base Git blobs, run `git diff --check`, and update and verify `MANIFEST.sha256`. Keep exact commands and results in `.agent/test-results/cpk-054-internal-plan-history.md`. On this host, use `TMPDIR=/var/tmp` because a pre-existing invalid `/tmp/.git` marker prevents a valid outside-Git fixture.

Finalize documentation, run the required fresh trace verifier for B1-B3, then run native review of the complete candidate. B4 receives deterministic validation and native review. CP1 has one full-review boundary with no intermediate commit. Close CPK-054 after a clean result. Install the reviewed candidate, verify Doctor readiness, and publish through the existing publication workflow.

## Idempotence and dependencies

Reuse the immutable writer's event key and collision suffix. Search every active worktree without copying its records. Cleanup must not overwrite a different destination or remove the last verified copy. A failed operation stops and reports its result. No new dependency, index, service, migration command, or mutable task record is needed.

Revision: user clarification retained versioned history; the source-confirmed handoff/replay path adds cross-worktree duplicate suppression to central-only capture.

# Preserve Plan Mode decisions

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, a completed Plan Mode response remains available after context compaction, later planning, or task subdivision. The toolkit saves the exact response in an immutable Markdown record. Later planning agents must read and reconcile applicable records before they produce a new plan.

## Progress

- [x] (2026-08-19) Accepted the CPK-036 plan and completed the two-phase Design Preflight challenge.
- [x] (2026-08-19) Created the stacked `cpk-036-plan-history` task branch from reviewed CPK-035.
- [x] (2026-08-19) Activated CPK-036 as the sole roadmap task.
- [x] (2026-08-19) Implemented Plan history capture, retrieval rules, installation, and focused tests.
- [x] (2026-08-19) Updated user documentation and passed the clean-context forward test.
- [x] (2026-08-19) Passed the complete test suite, all skill validators, shell syntax checks, diff checks, and checksum validation.
- [x] (2026-08-19) Corrected two P2 findings, passed delta review, and passed final coherence review.

## Surprises & Discoveries

- Observation: Codex supplies `last_assistant_message` to normal Stop hooks, but the field is optional in the documented contract.
  Evidence: The user accepted the native hook boundary. A missing value must produce a passive warning instead of unstable transcript parsing.
- Observation: RepoWise is a derived index and can omit a newly created record before its watcher updates.
  Evidence: Direct file enumeration must remain the authority after RepoWise identifies the repository and related specifications.
- Observation: A successful Stop hook must return JSON, including a no-op result.
  Evidence: The current OpenAI hook reference says that plain text is invalid. The hook now returns `{}` without continuation fields.
- Observation: A fresh planner recovered an ignored record that RepoWise did not index.
  Evidence: The forward test cited the record and conflicting specification, emitted no plan, and requested the required supersession fields.
- Observation: Review found that a valid specification stem can contain glob syntax.
  Evidence: Escaping the stem before discovery keeps identical retries idempotent for names such as `feature[1].md`.
- Observation: Same-event collision files can have different bytes.
  Evidence: Deduplication must compare both the event key and content. Distinct collision evidence remains part of reconciliation.

## Decision Log

- Decision: Extend the existing managed hook script with passive Stop handling.
  Rationale: The script already dispatches multiple hook events. This path needs no service, dependency, or second hook asset.
  Date/Author: 2026-08-19 / user and Codex
- Decision: Store the complete final assistant message without byte normalization.
  Rationale: The record must preserve the Plan Mode summary verbatim.
  Date/Author: 2026-08-19 / user and Codex
- Decision: Use project files as authoritative storage and RepoWise only for discovery.
  Rationale: File records survive index refreshes and can travel with the task.
  Date/Author: 2026-08-19 / user and Codex
- Decision: Use the native Stop-hook contract and warn when the final message is absent.
  Rationale: This matches observed Codex behavior without an App Server service or unstable transcript parser.
  Date/Author: 2026-08-19 / user and Codex
- Decision: Return `{}` for every non-warning Stop result.
  Rationale: Codex requires JSON from successful Stop hooks. An empty object does not continue or block the turn.
  Date/Author: 2026-08-19 / Codex

## Outcomes & Retrospective

The toolkit now preserves exact completed Plan Mode responses and requires full-set reconciliation before later planning or resumed implementation. The first review found two idempotence and collision-evidence defects. Both corrections passed the complete test suite, a focused delta review, and final coherence review.

## Context and Orientation

The task branch is `cpk-036-plan-history`. Its direct base is reviewed CPK-035 commit `13a23b24cc7313c5fd652a1465a742287fb83c2a`. The isolation form is one local task branch.

`assets/hooks/session_start.py` is the installed hook entry point. It handles Session Start and User Prompt Submit events. `kit.py` writes the managed hook entries in `config.toml`, installs custom skills, and checks installation state. `.agent/PLANS.md` owns ExecPlan behavior. `assets/AGENTS.block.md` routes tasks to installed skills. `tests/test_kit.py` owns installer and policy integration checks.

A Plan history record is an immutable copy of one completed Plan Mode final response. It is evidence for later planning. It is not a second mutable implementation plan.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). The hook, installer, Plan history skill, ExecPlan rules, routing, tests, and user documentation are `composes`. RepoWise indexes, user-owned hooks, project specifications, and installed records are `opaque`. An App Server client, transcript parser, database, daemon, mutable history index, review gate, and recovery of earlier lost plans are `deferred`.

Normal use includes completed Plan Mode turns, zero or more related specification files, later Plan Mode turns, compaction, and normal hook retries. The supported model has one user, one Codex writer, a normal local filesystem, and Git. I/O faults, hostile markers, concurrent writers, symlinks, and interruption remain excluded under [Supported model](../../assets/skills/design-preflight/references/supported-model.md).

## Scenario Proof

Apply [Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md), [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md), and [Full-set results](../../assets/skills/design-preflight/references/full-set-results.md).

The input-domain checks must distinguish Plan Mode from other modes and one complete `<proposed_plan>` envelope from an incomplete response. The exact-byte case must contain Unicode and must contrast trailing-newline states. The terminal oracle is one record whose bytes equal `last_assistant_message`.

The association checks must cover an explicit `none` marker, one valid specification, multiple valid specifications, invalid paths, missing files, path traversal, and a mixed valid-and-invalid set. Valid targets receive exact sibling copies. Any failed target also produces one unlinked copy and one passive warning. A missing marker is an association error, not an implicit no-spec declaration.

The retained-state checks must cover an identical retry and a repeated event identity with different content. An identical retry creates no duplicate. Different content creates a collision record and preserves the first record.

The collection checks must cover no history, one record, identical records from different turns, and duplicate-prefix records followed by a conflicting record. RepoWise can omit the final record in the check. Direct enumeration must still read every applicable record exactly once.

The composed planning checks must cover a later Plan prompt, a compacted session, an unresolved specification conflict, and a recorded user supersession. An unresolved conflict produces no completed plan. A valid supersession cites the old record, gives the reason, and states the replacement decision.

The installation checks must cover install, reinstall, doctor, uninstall, an obsolete managed Stop hook, and an unrelated user Stop hook. Installation leaves one current managed Stop entry. Uninstall preserves user hooks and all history records.

## Plan of Work

Add Plan history behavior to `assets/hooks/session_start.py`. Use only the Python standard library. Accept a completed plan only when the event is Plan Mode and the message contains one complete plan envelope. Parse exact `cpk-plan-spec` comments. Write valid associations beside each specification and write unlinked records under `.agent/plan-history/`. Use UTC capture time and a SHA-256 event key in each filename.

Add one focused `plan-history` skill. It owns marker emission, complete file discovery, chronology, reconciliation, conflicts, and supersession records. Update `.agent/PLANS.md` with the narrow immutable-evidence exception and the implementation handoff rule. Route Plan Mode work to the skill from `assets/AGENTS.block.md` and the existing hook context.

Add `Stop` to the managed hook events in `kit.py`. Keep the existing script command. Update exact ownership checks so upgrades remove obsolete toolkit Stop commands without removing unrelated hooks. Add `plan-history` to custom skill installation.

Update current user documentation with the storage contract, warning boundary, and later-planning behavior. Update the checksum manifest after all distributed files are final.

## Concrete Steps

Work in `/home/mbeutler/Projects/codex-practical-kit`.

Use focused unit and integration tests during implementation. Then run `./run-tests.sh`, skill validators, Python compilation, shell syntax checks, `git diff --check`, and `sha256sum --check MANIFEST.sha256`. Store detailed evidence in `.agent/test-results/cpk-036-plan-history.md`. Do not stage that file.

Stage the complete candidate and make sure that no tracked change remains outside the index. Record the staged tree in the ignored result. Give one fresh read-only reviewer the accepted requirements, this Scenario Proof, the diff, the checks, and the supported-model boundary.

## Validation and Acceptance

An exact-byte hook test must fail before the implementation and pass afterward. It must compare the input and record as bytes.

A clean-context forward test must start with an original plan and an intentionally stale RepoWise result. A later planner must find the omitted record through direct enumeration and reject an inverted subtask decision.

Policy checks must reject an omitted Plan history route, missing marker contract, silent truncation, unrecorded supersession, or a second mutable plan owner. Installer checks must prove the current Stop entry and preserve unrelated hooks and records.

## Idempotence and Recovery

The implementation and validation commands are safe to repeat. Exact event retries are idempotent. A conflicting event never overwrites an earlier record. If a normal operation fails, stop and report the error.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, and `.vscode/`. They are untracked environment state outside this task.

The first Design Preflight pass independently selected passive file capture, full-set restoration, and immutable conflict evidence. The informed challenge added the missing-message contract gate, required association declarations, direct enumeration after RepoWise, mixed-target behavior, safe event keys, durable conflict resolution, visible warnings, and obsolete-hook upgrade coverage.

## Interfaces and Dependencies

A completed Plan Mode response contains one or more comments in this form:

    <!-- cpk-plan-spec: docs/specification.md -->

If no specification is known, the response contains this comment:

    <!-- cpk-plan-spec: none -->

For `docs/specification.md`, the hook writes `docs/specification.plan-summary.<UTC>.<event-key>.md`. Unlinked records use `.agent/plan-history/plan-summary.<UTC>.<event-key>.md`. The event key is the SHA-256 digest of `session_id`, a NUL byte, and `turn_id`.

No new dependency or external service is permitted.

Revision note: Created from the accepted Plan Mode design and both Design Preflight challenge phases.
Revision note: Recorded implementation, the current Stop output contract, and the clean-context forward test.

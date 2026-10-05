# Report managed component updates and clean finished agent threads

This ExecPlan is a living specification until review closure. Maintain it in accordance with [`.agent/PLANS.md`](../../.agent/PLANS.md).

## Purpose / Big Picture

Users can run `python3 kit.py check-updates` to compare each managed component with its authoritative upstream source. The command reports availability and does not update files, installations, plugins, or configuration.

Codex coordinators also receive precise cleanup instructions. They preserve required follow-ups, capture each terminal delegated result, close that exact agent thread, and archive only finished history subtrees.

## Decision Log

- Decision: Add an explicit `check-updates` command instead of a startup, install, or Doctor check.
  Rationale: Network availability must not change deterministic setup and health operations.
- Decision: Treat `upstream.lock.json` sections `runtime_tools` and `skills` as the complete managed inventory.
  Rationale: The same lock owns toolkit pins and bundled skill revisions. Its `optional_tools` section is explicitly outside the installed kit.
- Decision: Compare authoritative identities without version ordering.
  Rationale: Equality can show that upstream differs. It cannot prove compatibility, safety, or that a release is chronologically newer.
- Decision: Use PyPI project JSON for RepoWise, GitHub latest full releases for uv and Ponytail, and GitHub default-branch heads for bundled skills.
  Rationale: These endpoints match each component's pinned identity type.
- Decision: Buffer every result before output and stop after the first request error.
  Rationale: A failed scan must not print a partial report that looks complete. The command does not retry.
- Decision: Native agent closure releases an open-thread slot. Native archival is a separate history operation.
  Rationale: Archival is not proof that Codex released agent capacity.
- Decision: No Plan History record applies to CPK-061.
  Rationale: Existing records describe earlier tasks. No prior Plan Mode specification defines this outcome.
- Decision: Use branch `cpk-061-component-updates-agent-cleanup` from `main` commit `00f3af7e9e91fdb7ddd31c529863c616522cdd82` in the primary checkout.
  Rationale: This task has one writable implementation stream.

## Context and Orientation

`kit.py` is the Python command-line entry point. `build_parser` defines commands, `main` dispatches them, and `load_lock` reads `upstream.lock.json`.

`upstream.lock.json` contains three managed runtime tools. RepoWise and uv have version pins. Ponytail is a Codex-owned plugin without a toolkit pin. The lock also contains two bundled skills with exact commit pins.

`assets/skills/delivery-lifecycle/references/coordination.md` is the only live owner of coordinator and subagent lifecycle rules. Do not copy these rules into another live instruction file.

`tests/test_kit.py` contains CLI and rule-owner integration tests. `README.md` owns the public command and component lifecycle documentation. `MANIFEST.sha256` records tracked package content.

## Product Boundary

The accepted user request, `upstream.lock.json`, and the canonical coordination reference define this task. Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md).

The managed lock inventory, the `kit.py` CLI, canonical coordination instructions, Design Preflight follow-up rules, and README compose the result. Existing install, Doctor, plugin lifecycle, native thread lifecycle, and Codex thread-limit behavior remain opaque. Optional tools, automatic updates, persistence, retries, and thread-limit changes remain deferred.

No inherited specification conflict exists. Do not alter component pins or installation behavior. Do not add background work, caches, schedules, dependencies, provider abstractions, version-order logic, or direct Codex state-file operations.

## Supported Operating Model

The supported path is an explicit online query against the five current managed components. A complete query returns status 0. The first network or response-shape error uses the existing `ERROR: ...` path and returns status 2.

The command reports toolkit pins and upstream identities. It does not inspect installed versions. For Ponytail, it reports the latest upstream release and Codex ownership without a current or update-needed claim.

A delegated assignment is terminal only when no required follow-up remains. After the coordinator captures that result, it closes the exact agent through the exposed native close operation before it spends another slot. If native archival is exposed, the coordinator explicitly targets a finished subtree with no active or required descendant.

## Boundary Inventory

| Boundary | Condition and contrast | Required oracle | Entry point | Scenarios |
| --- | --- | --- | --- | --- |
| B1 | Process all managed runtime tools and skills. Do not stop early, merge equal values, or include optional tools. | Five named results appear exactly once. No optional request or output occurs. | `kit.main(["check-updates"])` | S1 |
| B2 | The command performs reads and GET requests only. It does not mutate toolkit or Codex state. | Source, installation, plugin, and configuration state remain unchanged. | `kit.main(["check-updates"])` | S1, S5 |
| B3 | Compare version pins with releases and commit pins with repository heads. Do not fabricate a Ponytail baseline. | Each line uses the correct identity and same/different wording. Ponytail has Codex-owned wording only. | `kit.main(["check-updates"])` | S2, S3, S4 |
| B4 | A complete report returns 0. The first failed request returns 2 without retry, later requests, or partial success output. | Status, output, error count, and request sequence match the selected path. | `build_parser`, `main` | S1, S5, S6 |
| B5 | Capture a terminal assignment result, then close its exact agent. Archival is separate from capacity release. | The canonical rule states the actor, order, exact target, capacity purpose, and archive distinction. | Canonical coordination rule | S7 |
| B6 | Cleanup targets only finished work and preserves active or required descendants. | The rule requires an explicit archive target and forbids coordinator defaults and direct session deletion. | Canonical coordination rule | S8 |
| B7 | A finished turn is not a finished assignment when a required follow-up remains. | The same Design Preflight challenger survives both phases and becomes eligible only after Phase 2. | Coordination and Design Preflight rules | S9 |

## Scenario Proof

Apply [Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md), [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md), and [Full-set results](../../assets/skills/design-preflight/references/full-set-results.md).

| Scenario | Discriminator and contrast | Production path | Required oracle | Runnable check |
| --- | --- | --- | --- | --- |
| S1 | Use equal early identities and a different final skill revision. This exposes early stop and value deduplication. | `main` to parser, lock selection, provider parsing, comparison, and output | Exactly five managed results, no optional request, status 0, unchanged files | `python3 -m unittest discover -s tests -p test_kit.py -k test_check_updates_reports_complete_managed_inventory` |
| S2 | Vary RepoWise and uv between equal and different versions. Prefix uv tags with `v`. | `main` through real version comparison | Correct toolkit-pin and upstream-release labels, with no installed-version claim | `python3 -m unittest discover -s tests -p test_kit.py -k test_check_updates_compares_version_pins` |
| S3 | Vary each skill head between its exact pin and a different full SHA. | `main` through default-branch head requests and SHA comparison | Correct full revisions and same/different identity | `python3 -m unittest discover -s tests -p test_kit.py -k test_check_updates_compares_skill_revisions` |
| S4 | Give unpinned Ponytail the same release shape used by uv. | `main` through unpinned rendering | Upstream release and Codex-owned wording, with no installed/current/update-needed claim | `python3 -m unittest discover -s tests -p test_kit.py -k test_check_updates_reports_codex_owned_ponytail` |
| S5 | Change one later request from success to error after earlier requests complete. | `main` through the external seam and existing error owner | One error, status 2, no retry or later request, no stdout report, unchanged files | `python3 -m unittest discover -s tests -p test_kit.py -k test_check_updates_stops_once_on_request_error` |
| S6 | Select top-level help or subcommand help instead of command execution. | Parser help path | The read-only command is discoverable and makes no provider request | `python3 -m unittest discover -s tests -p test_kit.py -k test_update_check_is_explicit` |
| S7 | Compare final assignment cleanup with an idle but still-open thread or archive-only cleanup. | Canonical coordination instructions | Capture occurs before exact native closure and before another spawn. Archival is separate. | `python3 -m unittest discover -s tests -p test_kit.py -k test_coordination_cleans_terminal_agent_threads` |
| S8 | Keep a finished parent fixed and vary its descendant between active and terminal. | Canonical coordination instructions | Explicit archive targeting waits for active or required descendants and never targets the coordinator by default | `python3 -m unittest discover -s tests -p test_kit.py -k test_coordination_archive_targets_preserve_active_work` |
| S9 | Compare a Phase 1 return with completion of the full two-phase assignment. | Design Preflight through canonical cleanup gate | The same challenger remains available for Phase 2 and is cleaned only after the final result | `python3 -m unittest discover -s tests -p test_kit.py -k test_coordination_cleanup_preserves_required_followups` |

## Plan of Work

### CPK-061-A: Report managed component updates

Add the minimum standard-library implementation to `kit.py`. Reuse `load_lock`. Add one JSON GET helper, fixed provider URL selection for the current inventory, buffered result formatting, parser registration, and main dispatch.

Add the S1 through S6 tests to `tests/test_kit.py`. Replace only `urllib.request.urlopen` at the external boundary. Keep lock selection, comparison, formatting, parser dispatch, and error handling real.

Document the command in `README.md`. This subtask changes `kit.py`, `tests/test_kit.py`, `README.md`, the ExecPlan, roadmap, and manifest. Its checkpoint review boundary is the complete update-reporting path. No separate checkpoint commit is required before the cumulative task review.

### CPK-061-B: Clean finished delegated threads

Edit only the canonical coordination owner for live instructions. Define assignment completion, result capture, exact native closure, optional explicit archival, descendant protection, and the ban on direct session-file deletion.

Add the S7 through S9 deterministic owner tests to `tests/test_kit.py`. Keep the Design Preflight same-challenger text unchanged. This subtask changes the canonical coordination reference, tests, the ExecPlan, roadmap, and manifest. Its checkpoint review boundary is the instruction contract and its rule-owner checks. No separate checkpoint commit is required before the cumulative task review.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on branch `cpk-061-component-updates-agent-cleanup`.

Use `apply_patch` for tracked edits. After implementation, run each Scenario Proof command. Then run:

    python3 -m unittest discover -s tests -p 'test_*.py'
    python3 kit.py check-updates --help
    python3 kit.py --help

Regenerate `MANIFEST.sha256` with the repository's existing manifest procedure. Record command results in ignored `.agent/test-results/CPK-061.md`.

## Validation and Acceptance

The focused tests must prove both sides of each listed contrast. The complete suite must pass. Help output must describe `check-updates` as read-only and must not access the network.

A live `python3 kit.py check-updates` run can use the current network. Its output must contain RepoWise, uv, Ponytail, NeuroArxiv, and Simple English. The command can report differing identities without failing.

Before native correctness review, a fresh read-only trace reviewer must close executable boundaries B1 through B4. Deterministic source checks and native review cover instruction boundaries B5 through B7. After a clean final review, move CPK-061 from Active to Completed and apply review closure.

## Idempotence and Recovery

The update command is repeatable because it writes no state. A failed request stops the command. Run it again only after the external problem is corrected.

All source edits are ordinary Git changes. Preserve unrelated untracked `.mcp.json`, `.repowise/`, and `.vscode/` content.

## Artifacts and Notes

The preflight found no contract gap. RepoWise indexed base commit `00f3af7e9e91` with `index_behind: false` before implementation.

## Interfaces and Dependencies

Use Python's existing `urllib.request` and `json` modules. Add no dependency.

`check_updates() -> None` owns the full scan and successful report. A small JSON GET helper returns a decoded JSON value and raises `KitError` for transport, HTTP, JSON, or required-field errors. `main` returns 0 after `check_updates` completes and keeps the existing status-2 exception path.

The public interface is:

    python3 kit.py check-updates

The output uses one concise line per managed component. Each line names the toolkit baseline or Codex-owned state, the upstream identity, and whether comparable identities are the same or different.

## Outcomes & Retrospective

Users can compare all managed component pins with upstream identities through one read-only command. Coordinators now preserve required follow-ups and separate capacity-releasing closure from targeted history archival.

The fixed provider paths kept the update report small and explicit. Native Codex lifecycle operations remained in the coordination owner instead of toolkit runtime code.

Plan note: CPK-061 combines two user-requested outcomes under their existing owners. The runtime path remains read-only, and native Codex lifecycle behavior remains outside toolkit code.

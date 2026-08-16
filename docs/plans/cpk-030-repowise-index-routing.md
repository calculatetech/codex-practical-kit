# Make RepoWise index-first and self-refreshing

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

Codex must use RepoWise as a code index, not only as a weak natural-language search service. Exact identifiers must resolve to verified source without broad filesystem exploration. RepoWise must also catch up committed work before MCP serves queries and index active working-tree saves through its native watcher. No LLM provider is required. A provider configured by the user remains useful for conceptual questions.

## Progress

- [x] (2026-08-16 18:01Z) Created branch `cpk-030-repowise-index-routing` from `main` at `840a97a5586e6c03f9501e3280f5973075177e60`.
- [x] (2026-08-16 18:01Z) Completed Design Preflight and current RepoWise 0.41.0 research.
- [x] (2026-08-16 19:18Z) Implemented index-first routing, startup catch-up, active-session working-tree updates, and watcher cleanup.
- [x] (2026-08-16 19:42Z) Validated all retained scenarios, completed 37 tests, finalized user documentation, and regenerated the manifest.
- [x] (2026-08-16 20:07Z) Completed adversarial review and live installation. Prepared the local checkpoint commit.

## Surprises & Discoveries

- Observation: `get_answer` without a provider returned `degraded: no-llm-provider`, low confidence, and generic fallback targets. An exact `search_codebase(mode="symbol")` lookup returned `kit.py::install_hooks`, and `get_symbol` returned its verified live body without a filesystem read.
- Observation: The post-commit hook fired for two commits, but its background child disappeared under Codex process supervision before RepoWise advanced. A detached update advanced the index from `0045b6f` to `840a97a` in 2.3 seconds.
- Observation: RepoWise 0.41.0 provides `watch --index-only`. It batches eligible working-tree changes after a two-second debounce and avoids model calls.
- Observation: The unmodified RepoWise 0.41.0 watcher treats file-open and file-close notifications as changes. Its update reads source files, so one edit starts an endless update loop. RepoWise 0.43.0 has the same behavior.
- Observation: Ignoring only `opened`, `closed`, and `closed_no_write` notifications keeps RepoWise's native watcher stable. One edit produced one update and no later update during an eight-second observation.
- Observation: RepoWise `update` exits with status 1 before the first commit, even after a successful empty-repository `init`. Startup now skips catch-up when `HEAD` does not exist.

## Decision Log

- Decision: Keep all query-routing rules in `assets/skills/repository-knowledge/SKILL.md`.
  Rationale: It is the existing unique `repository-knowledge` owner. AGENTS remains a router.
  Date/Author: 2026-08-16 / Codex and user.
- Decision: Use model synthesis only for conceptual how/why questions.
  Rationale: Exact symbols and paths are cheaper and more reliable through deterministic selectors.
  Date/Author: 2026-08-16 / user.
- Decision: Compose synchronous startup catch-up, native active-session watch, and the existing post-commit hook.
  Rationale: RepoWise already supplies each primitive. The launcher applies one pinned compatibility filter before it invokes the native watcher.
  Date/Author: 2026-08-16 / Codex and user.
- Decision: Suppress watcher read notifications through RepoWise's Python launcher.
  Rationale: RepoWise's update reads trigger its own watcher. The filter removes the false wake and preserves native debounce and working-tree indexing.
  Date/Author: 2026-08-16 / Codex.
- Decision: Target version `0.16.0`.
  Rationale: Query corrections are fixes, but automatic uncommitted working-tree monitoring is a new supported capability before 1.0.0.
  Date/Author: 2026-08-16 / Codex.

## Outcomes & Retrospective

Version 0.16.0 routes exact lookups through RepoWise's symbol index and keeps working-tree edits indexed without model calls. The pinned watcher needs one compatibility filter for read-only filesystem events. Runtime smoke checks proved that initial and later edits each caused one update and then settled. Review pass 1 exposed a no-`HEAD` startup defect. The fix delta and final coherence review were clean. The full 38-test suite passes. Live installation and both Doctor checks reported `Result: ready`.

## Context and Orientation

`kit.py:repowise_bootstrap()` renders the required user-level MCP command. It initializes an absent index, installs RepoWise's Git hook, and starts MCP. `assets/skills/repository-knowledge/SKILL.md` is the sole owner of agent lookup behavior. `tests/test_kit.py` covers bootstrap behavior and unique rule ownership. `docs/REPOWISE.md` owns user-visible RepoWise behavior.

The task uses one normal branch because it has one writable implementation stream. Preserve the existing untracked `.claude/`, `.codex/`, `.mcp.json`, `.repowise/`, and `.vscode/` paths.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). The authoritative product sources are `docs/REPOWISE.md` and `docs/WHY-THIS-SHAPE.md`.

Repository lookup instructions and the managed MCP bootstrap are `composes`. RepoWise's watcher entry point is also `composes` because the launcher filters its event input. The AGENTS router, remaining RepoWise 0.41.0 behavior, provider configuration, and repository opt-out behavior are `opaque`. No deferred owner is promoted.

The supported model has one personal user and one Codex writer on a normal local Git filesystem. Exclude I/O faults, permissions, links, retries, recovery, arbitrary concurrency, submodules, new dependencies, provider credentials, custom watchers, and RepoWise database changes.

## Scenario Proof

Apply [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md) and [Full-set results](../../assets/skills/design-preflight/references/full-set-results.md).

| Scenario | Production path | Required oracle | Runnable test or command | Result |
| --- | --- | --- | --- | --- |
| Exact identifier without provider | repository skill → symbol search → `get_symbol` | Exact verified body; no preceding broad native search | `repowise search repowise_watch_command --mode symbol --format json`, then `repowise symbol kit.py::repowise_watch_command --format json` | Exact index match and verified source body |
| Known path or relationship | repository skill → `get_context` → needed indexed block | Requested target and relationship resolve before source confirmation | `repowise context kit.py --format json` | Indexed file card returned without broad search |
| Concept question without provider | `get_answer` → degraded session state → indexed candidates | At most one degraded answer call in the session | `test_repowise_routes_indexed_queries` | Owner contract passed |
| Concept question with provider | `get_answer` → confidence/citations/symbol bodies | Provider result remains usable without becoming required | `test_repowise_routes_indexed_queries` | Owner contract passed; no provider was installed |
| Committed index behind at startup | bootstrap → index-only update → MCP | Update completes before MCP starts | `test_bootstrap_initializes_once_and_always_installs_hook` | Passed |
| Rapid eligible saves | watcher filter → native debounce → working-tree update | Every final changed path reaches the index with no model call | Temporary-repository watcher smoke test | One update completed and the watcher settled |
| Later save after first update | watcher releases update gate → later update | Later symbol state reaches the index | Live repository watcher smoke test | A later test edit caused one update; the watcher settled again |
| MCP exit | MCP terminal event → watcher cleanup | No managed watcher remains | `test_bootstrap_initializes_once_and_always_installs_hook` | Passed; both watcher PIDs were gone |
| Empty or non-Git workspace | existing bootstrap selector | Empty folder initializes; non-empty non-Git folder stays unchanged | Real empty-folder bootstrap plus `test_bootstrap_initializes_only_empty_non_git_directory` | Real bootstrap exited 0 with Git, index, watcher, and MCP startup; test passed |

## Plan of Work

First expand the repository-knowledge owner with deterministic query-shape routing, session-scoped no-provider handling, bounded fallback, ambiguity handling, and verified-source behavior.

Then extend `repowise_bootstrap()` to run an index-only update before MCP. Start RepoWise's watcher through its pinned Python interpreter and ignore read-only filesystem notifications. Redirect non-protocol output, run MCP in the foreground, and clean up the watcher when MCP exits. Keep RepoWise's hook installation. Make eager repository setup catch an existing index up once.

Add focused bootstrap and rule-owner tests. Update the RepoWise documentation, version owners, roadmap, and checksum manifest after behavior is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on branch `cpk-030-repowise-index-routing`.

Run focused tests while editing, then run:

    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Store detailed results in `.agent/test-results/cpk-030-repowise-index-routing.md`. Do not stage that file.

## Validation and Acceptance

The new bootstrap test must fail if update does not precede MCP, automatic paths omit `--index-only`, watcher output reaches MCP stdout, or the watcher remains after MCP exits. The routing test must fail if exact symbol lookup, session-scoped degraded handling, optional conceptual synthesis, bounded native fallback, or verified-source behavior disappears.

A real temporary repository must prove that rapid eligible saves and a later separate save become queryable through RepoWise. The watcher must settle after each update. A fresh no-provider Codex trace must resolve one named function through the index without broad native exploration.

After clean review, run `./install.sh`, `./doctor.sh`, and `./doctor.sh --repo .` from the reviewed candidate. Require `Result: ready`.

## Idempotence and Recovery

Installation, setup, startup catch-up, hook installation, and watcher startup are repeatable. RepoWise owns update serialization. The compatibility filter is pinned to RepoWise 0.41.0 internals. Attempt each operation once. On failure, stop and report it. Do not add retries or recovery.

## Artifacts and Notes

RepoWise's default watcher debounce is the accepted change threshold. Automatic watch updates remain index-only even when a user later configures an LLM provider.

## Interfaces and Dependencies

No new public command or dependency is added. The generated MCP command gains startup update, a watcher event filter, and watcher lifecycle behavior. RepoWise remains pinned at 0.41.0. Source version becomes 0.16.0.

Revision note (2026-08-16): The plan now records the watcher read-event loop found by the runtime smoke test and the minimal compatibility filter that removes it.

Revision note (2026-08-16): Review pass 1 found that RepoWise cannot update a repository before its first commit. The fix skips startup catch-up until `HEAD` exists and adds real and automated checks.

Revision note (2026-08-16): Fix-delta and final coherence reviews were clean. The reviewed candidate passed live installation and both Doctor checks.

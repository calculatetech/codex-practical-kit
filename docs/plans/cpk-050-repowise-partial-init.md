# Recover Incomplete RepoWise Initialization

This ExecPlan is a living specification until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

Codex must start with the required RepoWise graph after a normal RepoWise upgrade. An older RepoWise version can leave a populated index without a completed sync commit. The current bootstrap mistakes this state for a complete index. Its update fails, and required MCP startup terminates Codex.

After this change, the bootstrap rebuilds that incomplete index once. It then runs the normal catch-up update and starts RepoWise MCP.

Work occurs on branch `fix/cpk-050-repowise-partial-init`. The base branch is `main` at `b4c592c92e15a42c0a82b8dfd4a793ac0f81f2da`. One task branch isolates the writable implementation stream.

Release this bugfix as version `0.23.4`.

## Surprises & Discoveries

- RepoWise 0.41.0 wrote the reported index. The database contains 126 pages, but `last_sync_commit` is null.
- RepoWise 0.45.0 reports that database as healthy. Its incremental update still stops with `No previous sync found`.
- RepoWise 0.45.0 ordinary no-prose initialization repaired a disposable copy in 48.4 seconds.
- The repaired copy required one normal update to refresh the stored indexed revision.
- A null sync commit is valid before the first Git commit. Recovery must also require an existing `HEAD`.

## Decision Log

- Read the RepoWise sync marker from `state.json`. Do not inspect or change `wiki.db`.
- Treat an existing index as incomplete only when `HEAD` exists and `last_sync_commit` is not a nonempty string.
- Reuse the existing noninteractive `INIT_ARGS`. Do not add `--force` or a second recovery command.
- If an index directory existed before recovery, run the normal catch-up update after initialization.
- Keep RepoWise 0.45.0. RepoWise 0.46.0 has no release note for this startup state.
- Keep RepoWise required. Do not let Codex continue without the code graph.
- Increment the committed source version from `0.23.3` to `0.23.4` for this bugfix.

## Outcomes & Retrospective

The bootstrap now repairs an incomplete index from an older RepoWise version. It preserves normal startup before the first Git commit.

Directory presence was not a sufficient readiness signal. The completed sync commit identifies the state that RepoWise can update.

## Context and Orientation

`assets/runtime/repowise_bootstrap.py` owns automatic RepoWise startup. Its `bootstrap()` function selects the Git root and prepares the index. It then installs the Git hook, starts the watcher, and starts RepoWise MCP.

`tests/test_kit.py` contains the direct bootstrap checks. `docs/REPOWISE.md` defines the user-visible runtime behavior. `docs/roadmap.md` is the only lifecycle-state record.

The existing code uses the `.repowise` directory as its only initialization signal. The RepoWise CLI uses `.repowise/state.json` and requires `last_sync_commit` for normal incremental updates.

## Product Boundary

[Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) limit this task to automatic bootstrap behavior.

The installed Python bootstrap is `composes`. RepoWise CLI behavior, Git, the Codex required-MCP setting, and the installer are `opaque`. Repository commands, agent routing, removal, and the RepoWise database format are also `opaque`.

The current production use cases include normal checkouts, linked worktrees, and empty project folders. This task preserves these use cases. It adds the reported normal upgrade state to bootstrap preparation.

The supported model has one user, one Codex writer, a normal local filesystem, and normal Git. The observed trigger needs no fault injection. The toolkit controls its RepoWise version and bootstrap gate.

This task adds no database inspection, direct state change, index removal, backup, retry loop, dependency, optional MCP path, or generic fallback. It does not add recovery for malformed JSON, I/O errors, permission errors, interruption, or outside changes.

## Boundary Inventory

[Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md) owns this inventory. [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md) owns the startup sequence.

| Boundary | Condition and contrast | Entry point | Required oracle | Scenario |
| --- | --- | --- | --- | --- |
| B1 | A rooted bootstrap reaches usable RepoWise MCP. Startup termination or an unavailable graph is the contrast. | `main()` to `bootstrap()` | MCP receives the Git root and returns its status. | S1 |
| B2 | Only an empty non-Git directory receives `git init`. One ordinary file is the contrast. | `bootstrap()` non-Git gate | Only the empty directory enters rooted setup. | Existing checks |
| B3 | With `HEAD`, an absent index or an index without a nonempty sync commit needs initialization. A nonempty commit string is complete. | `bootstrap()` index gate | The incomplete side initializes. The complete side does not. | S1 |
| B4 | An index directory that existed before startup receives catch-up when `HEAD` exists. No `HEAD` is the contrast. | `bootstrap()` catch-up gate | Recovery and normal existing indexes update. A new first index does not. | S1, S2 |
| B5 | A linked worktree keeps its root and index. Redirection to the primary checkout is the contrast. | `git_root()` and `bootstrap()` | All rooted commands use the linked path. | Existing check |
| B6 | A ready watcher permits MCP. An exited watcher prevents MCP. | `bootstrap()` readiness gate | MCP starts only after readiness, and cleanup stops the watcher. | Existing checks |
| B7 | POSIX stops one watcher. Windows stops the watcher process tree. | `stop_watcher()` | The applicable process owner stops and waits. | Existing checks |
| B8 | Setup diagnostics use stderr. MCP keeps stdout for the protocol. | `run_setup()` and MCP call | Setup output cannot enter the protocol stream. | Existing check |

Every source clause in the accepted task boundary has a disposition. B3 changes because directory presence cannot prove a completed RepoWise initialization. No accepted clause remains a contract gap.

## Scenario Proof

| Scenario | Discriminator | Minimal contrast | Production path and terminal oracle | Runnable check |
| --- | --- | --- | --- | --- |
| S1 | `last_sync_commit` with an existing `HEAD` | Null and nonempty string in otherwise equal state files | Bootstrap readiness gate to init or no init, hook, catch-up, ready watcher, rooted MCP, and cleanup | `test_bootstrap_recovers_index_without_sync_commit` and `test_bootstrap_initializes_once_and_always_installs_hook` |
| S2 | `HEAD` with an existing index and null sync commit | No commit and one commit | Bootstrap readiness gate to no recovery or recovery, then hook, watcher, MCP, and cleanup | `test_bootstrap_does_not_reinitialize_before_first_commit` |

For S1, the incomplete side must run the exact `INIT_ARGS` once. It must then run one catch-up update because the index directory existed before startup. The complete side must skip initialization and run one update.

For S2, the no-commit side must skip initialization and update. It must still install the hook and reach watcher, rooted MCP, and cleanup.

The input-domain and path-transition lenses apply. Collection semantics do not apply because the bootstrap selects one repository state.

## Plan of Work

Add one small JSON reader to `assets/runtime/repowise_bootstrap.py`. The reader returns true only for a nonempty string in `last_sync_commit`.

In `bootstrap()`, retain the original index-directory state and resolve `HEAD` once. Initialize when the directory is absent. Also initialize when the directory exists, `HEAD` exists, and the sync marker is incomplete.

After setup, install the hook as before. If the index directory existed and `HEAD` exists, run the existing update command. Keep the watcher and MCP lifecycle unchanged.

Update the focused tests in `tests/test_kit.py`. Update `docs/REPOWISE.md` with the completed-index rule.

## Concrete Steps

Work from `C:\Users\mikeb\Projects\codex-practical-kit`.

1. Change the bootstrap readiness gate and its focused checks.
2. Run the named Scenario Proof checks.
3. Run the complete Python suite and repository checks.
4. Update only documentation that became incorrect.
5. Run trace closure and native adversarial review before review closure.

## Validation and Acceptance

The S1 checks must prove both marker values and the complete production sequence. The null side must initialize and update. The nonempty side must update without initialization.

The S2 check must prove that a null marker does not cause repeated initialization before the first commit.

Run `python -m unittest tests.test_kit.RepoWiseRuntimeTests`. Then run `python -m unittest` for the complete suite. Record baseline errors separately if they remain outside this task.

Run the repository checksum, compilation, shell, PowerShell, and rule-owner checks through the existing repository test commands.

## Idempotence and Recovery

Normal startup is idempotent after RepoWise writes a completed sync commit. The bootstrap makes one initialization attempt. If that command fails, startup stops with the command status.

The implementation does not change the reported repository. A disposable copy proves the external RepoWise behavior.

## Artifacts and Notes

Keep detailed command results in `.agent/test-results/cpk-050-repowise-partial-init.md`. Do not stage that file.

The disposable proof repository is outside this repository. It contains a copied RepoWise index and no authoritative user data.

## Interfaces and Dependencies

Use only Python `json`, `subprocess`, and `pathlib`. Do not add a package.

Keep `bootstrap(repowise: str, cwd: Path) -> int` and `main(argv: list[str] | None = None) -> int` unchanged. Add one private readiness predicate with a `Path` input and a Boolean result.

Final note: this plan replaces directory-only initialization detection because that test cannot identify the reported incomplete index.

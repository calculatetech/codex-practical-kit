# Add native Windows compatibility

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose

Windows users must be able to operate every root toolkit entry point with PowerShell 7. The required RepoWise MCP server must start without a POSIX shell. Existing macOS and Linux commands must continue to work.

## Progress

- [x] (2026-08-19) Recovered the accepted Plan Mode response and stored it beside this ExecPlan.
- [x] (2026-08-19) Completed official platform research and two-phase adversarial design preflight.
- [x] (2026-08-19) Created `cpk-039-native-windows` from CPK-038 commit `66a8db7fb4627a4a281d21a0a7965a40f85f5ca3` in a linked worktree.
- [x] (2026-08-19) Implemented PowerShell entry points and platform-aware tool installation.
- [x] (2026-08-19) Replaced the shell-only RepoWise bootstrap with one cross-platform Python runtime.
- [x] (2026-08-19) Updated user instructions, the release manifest, the lock, and version surfaces.
- [x] (2026-08-21) Recorded the failed native Windows test checkpoint and completed a two-phase correction preflight.
- [x] (2026-08-21) Reproduced the uv installer failure and isolated PowerShell statement-at-a-time parsing as its cause.
- [x] (2026-08-21) Passed 67 tests through both local launchers after the uv invocation correction.
- [x] (2026-08-21) Removed ambient Windows `python` resolution from the PowerShell launcher tests and bounded their subprocess runtime.
- [x] (2026-08-21) Defined an ownership-safe Windows recovery path for a RepoWise launcher broken by Python replacement.
- [x] (2026-08-21) Completed clean correctness review of the RepoWise recovery candidate.
- [x] (2026-08-21) Validated two Windows review findings and completed a two-phase correction preflight.
- [x] (2026-08-21) Stopped the complete Windows watcher tree and passed 73 tests through `run-tests.ps1` with ambient RepoWise on `PATH`.
- [x] (2026-08-21) Corrected the Windows repository-cleanup command found by the final coherence review.
- [ ] Pass local validation and the native Windows checkpoint (completed: corrected local validation; remaining: exact-commit Windows VM validation).
- [x] (2026-08-21) Completed adversarial review and review closure after five passes.

## Prior Plan Reconciliation

- `docs/plans/cpk-039-native-windows.plan-summary.20260819T211423672232Z.manual-recovery.md`: carried. The Plan history hook could not link the completed response before this ExecPlan existed. This immutable copy preserves the exact response from the thread.

No earlier Plan history record applies to CPK-039.

## Plan Deviations

- Native checkpoint `a80ca4f446e9c1d73e20b1b18d33d716072ddd4c` is superseded only as validation evidence.
- The accepted scope is unchanged. The correction changes the Windows test environment, host-specific test contracts, and checkout bytes.
- The first correction did not rewrite `kit.py` or the RepoWise bootstrap. The uv correction changes one `ensure_uv` command argument.
- Native installation at `9850d63` proved that `pwsh -Command -` did not execute the verified multi-line uv installer as one script. The next correction changes only the `ensure_uv` PowerShell invocation and its direct test.
- The reported Python replacement adds one Windows-only recovery case. A failed RepoWise launcher is repairable only when the previous manifest records the selected fixed user-bin path.
- The correction stops the complete Windows watcher process tree and isolates the recovery fixture from ambient executable discovery. It does not change POSIX shutdown.
- The coherence correction splits the repository-cleanup command by platform. Windows uses `python`; macOS and Linux retain `python3`.

## Surprises and Discoveries

- Observation: The Plan history hook requires the marked specification file to exist before it can store a linked record.
  Evidence: No CPK-039 record existed in `.agent/plan-history/` or beside the future specification after Plan Mode ended.
- Observation: PowerShell can leave `$LASTEXITCODE` unset after command resolution fails.
  Evidence: The first local `doctor.ps1` check reported a missing `python` command but returned status 0. Each launcher now catches this error and returns status 1.
- Observation: Native Windows validation found 11 errors and 9 failures in the test checkpoint.
  Evidence: Python used cp1252 for repository text. Some tests selected the wrong host command or platform branch.
  Evidence: One excluded migration fixture required link privilege. Windows paths and Git checkout conversion changed test results.
- Observation: PowerShell returned zero after it skipped the body of a multi-line installer received through `-Command -`.
  Evidence: A local executable check reproduced a missing marker with status zero. Evaluating the complete input as one script block created the marker.
- Observation: The launcher-forwarding test could wait indefinitely on the host's ambient Windows `python` command.
  Evidence: The test did not bind the temporary launcher to the interpreter that started the suite and had no subprocess timeout.
- Observation: A retained `repowise.exe` can become non-executable after its Python installation is replaced.
  Evidence: Native reinstall reported the removed Python 3.14 path, but classified the manifest-recorded launcher as a different RepoWise version.
- Observation: `Popen.terminate()` stops only the uv console launcher on Windows.
  Evidence: A native smoke check left the Python watcher alive and immediate repository cleanup failed with `WinError 32`.
- Observation: The Windows recovery fixture selected the user's installed RepoWise before its temporary launcher.
  Evidence: `run-tests.ps1` failed with the ambient `C:\Users\mikeb\.local\bin\repowise.exe` and passed when that path was absent.
- Observation: The shared uninstall text used the POSIX-only `python3` command for Windows users.
  Evidence: The supported native Windows installation exposes `python.exe` and does not require a `python3` alias.

## Decision Log

- Decision: Support PowerShell 7 with `.ps1` entry points only.
  Rationale: The user does not require Windows PowerShell 5.1 or batch launchers.
  Date/Author: 2026-08-19 / User and Codex
- Decision: Install one Python RepoWise bootstrap instead of a second PowerShell implementation.
  Rationale: One standard-library runtime keeps lifecycle behavior identical across platforms.
  Date/Author: 2026-08-19 / Codex
- Decision: Require native VM evidence for the exact pushed checkpoint before correctness review.
  Rationale: Local PowerShell on Linux cannot prove Windows process and path behavior.
  Date/Author: 2026-08-19 / User and Codex
- Decision: Stop a live Windows watcher with one `taskkill /T /F` operation, discard its output, and then wait for the launcher.
  Rationale: Windows `taskkill /T` ends the selected process and its children. Job Objects require custom Win32 lifecycle code, and console signals require console attachment.
  Sources: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/taskkill and https://docs.python.org/3/library/subprocess.html#subprocess.Popen.terminate
  Date/Author: 2026-08-21 / Codex

## Outcomes and Retrospective

The five PowerShell entry points and the cross-platform RepoWise bootstrap are implemented. Local native Windows validation now passes, including watcher-tree cleanup and installed-runtime test isolation. Adversarial review is clean after the watcher, fixture-isolation, and cleanup-command corrections. Exact-commit VM validation remains.

## Context and Orientation

The task worktree is `/home/mbeutler/Projects/codex-practical-kit-cpk-039`. The branch is `cpk-039-native-windows`, based on completed CPK-038 commit `66a8db7fb4627a4a281d21a0a7965a40f85f5ca3`.

The root launchers are thin entry points for `kit.py`. This module owns installation, configuration, RepoWise setup, Doctor, and uninstall behavior.

The installed Python bootstrap prepares RepoWise before it starts the MCP server. Its source is `assets/runtime/repowise_bootstrap.py`.

`tests/test_kit.py` owns the executable contract checks. `README.md`, `CODEX-INSTALL-PROMPT.md`, and `docs/REPOWISE.md` own user instructions.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). The current production use cases are installation, testing, eager repository setup, Doctor, uninstall, and automatic RepoWise MCP startup.

The task composes the five Windows entry points, platform tool selection, bootstrap installation, MCP configuration, user instructions, manifest, lock, version, and tests. Existing POSIX outcomes and managed hook `commandWindows` behavior are opaque and must remain unchanged. There is no deferred owner.

The supported model is one user on native Windows 10 or 11 with PowerShell 7, Python 3.11 or later, Git, and Codex. macOS and Linux remain supported. A Windows reinstall repairs a failed RepoWise launcher only when the previous manifest records the selected fixed user-bin path. The task excludes PowerShell 5.1, batch files, Windows CI, WSL-only support, dependency installation for Python or Git, other recovery, retries, concurrency, and changes to managed install locations.

## Scenario Proof

Apply [Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md) and [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md).

| Scenario | Discriminator and contrast | Production path | Required oracle | Runnable check | Result |
| --- | --- | --- | --- | --- | --- |
| Distributed artifact set | Each current `.sh` entry point versus its peer; LF versus converted checkout bytes | Git attributes and source inventory to manifest | Exactly five `.ps1` peers and one bootstrap source occur once with valid hashes after a checkout with `core.autocrlf=true` | `test_windows_launchers_and_runtime_are_complete_distribution_artifacts`; fresh clone with `core.autocrlf=true` | Passed local checkout; forced clone pending |
| Action launcher | Simple argument versus path with spaces; success versus error | `.ps1` to Python subcommand | Arguments and exit status remain unchanged | `test_action_launchers_forward_arguments_and_exit_status`; `test_action_launcher_reports_missing_python` | Passed locally |
| Test launcher | Passing unit phase versus failing unit phase; cp1252 default versus inherited UTF-8 mode | unit discovery and child hooks to Python compilation | Success reads UTF-8 and compiles every source; failure does not compile | `test_test_launcher_compiles_kit_and_every_hook`; `test_test_launcher_stops_after_failed_unit_phase`; native `run-tests.ps1` | Passed locally; native rerun pending |
| Hook command syntax | POSIX `command` versus `commandWindows` | generated TOML to hook subprocess | The host-specific command starts the hook and preserves exact output | `test_plan_mode_prompt_selects_normal_mode` | Passed locally; native rerun pending |
| Hook interpreter | `python3` alias versus the current interpreter | test subprocess to Session Start JSON | The router test uses the interpreter running the suite | `test_session_start_still_announces_router` | Passed locally; native rerun pending |
| Platform-specific unit contracts | Unmocked host versus explicit POSIX and Windows predicates | test fixture to uv and RepoWise selectors | Each test proves its named platform branch on either host | missing-uv and missing-RepoWise POSIX and Windows tests | Passed locally; native rerun pending |
| Existing Windows executables | Present `uv.exe` and `repowise.exe` versus absent names | platform discovery to runtime result | Existing commands are reused without installation | `test_windows_runtime_discovery_uses_executable_suffix` | Passed locally |
| Missing Windows uv | Missing `uv.exe` versus the POSIX missing path; statement stream versus one script block | download, hash, and `pwsh` stdin | The exact verified installer executes as one script and creates `uv.exe` in `UV_INSTALL_DIR` | `test_missing_windows_uv_runs_verified_powershell_installer_once`; executable multi-line installer check | Passed locally; native install rerun pending |
| Missing Windows RepoWise | Missing `repowise.exe` after uv is ready | uv tool installation to discovery | One pinned persistent tool install returns `repowise.exe` | `test_missing_windows_repowise_uses_executable_result` | Passed locally |
| Broken recorded Windows RepoWise | Nonzero version result with both manifest and fixed-target ownership versus either predicate absent; ambient RepoWise present versus absent | fixture-scoped discovery, reinstall through runtime selection, forced uv replacement, and manifest writer | The temporary launcher is probed, one forced pinned install replaces its stale bytes, and the completed manifest records `repowise.exe` | `test_install_repairs_manifest_owned_broken_windows_repowise`; full `run-tests.ps1` with ambient RepoWise | Passed native Windows |
| Unowned, wrong-version, and POSIX commands | Broken unowned path versus broken owned Windows path; successful 0.40.0 versus failed process; Windows versus POSIX | selection and validation gate | Unowned, successful wrong-version, and POSIX commands stop without mutation | ownership, version, reuse, and POSIX runtime tests | Passed locally |
| Watcher platform | Valid POSIX shebang versus Windows executable | bootstrap watcher selector | POSIX uses patched Python; Windows uses `repowise.exe watch` | `test_watch_command_is_platform_specific` | Passed locally; native rerun pending |
| Watcher cleanup | Windows launcher plus child versus launcher-only termination; cleanup output versus MCP stdout | bootstrap cleanup after normal MCP completion | Both watcher processes exit before return, the repository is immediately removable, and cleanup emits no MCP stdout | `test_windows_bootstrap_stops_complete_watcher_tree`; `test_stop_watcher_is_platform_specific`; stream-ownership test | Passed native Windows |
| Watcher readiness | Watcher stays alive versus exits during the gate | watcher to MCP terminal owner | Early exit returns nonzero and MCP never starts | `test_bootstrap_stops_when_watcher_fails_to_start` | Passed locally |
| Existing Git lifecycle | Missing index versus existing index; no `HEAD` versus `HEAD` | bootstrap through watcher, MCP, and cleanup | Init occurs once, hook occurs always, update needs `HEAD`, and cleanup occurs | `test_bootstrap_initializes_once_and_always_installs_hook` | Passed locally |
| Empty and non-empty non-Git folders | Empty directory versus one existing file | bootstrap through terminal owner | Empty path gets the full no-update lifecycle; non-empty path remains unchanged and starts only MCP | `test_bootstrap_initializes_only_empty_non_git_directory` | Passed locally |
| MCP stream ownership | Bootstrap diagnostics versus MCP bytes | subprocess streams | Diagnostics use stderr; stdout contains only foreground MCP bytes | `test_bootstrap_keeps_setup_diagnostics_off_mcp_stdout` | Passed locally |
| Install and Doctor | Managed block versus unrelated TOML | install to Doctor | Python bootstrap command is valid; hooks and unrelated TOML remain | installer tests and isolated `kit.py doctor` | Passed locally |
| Eager setup | Repository without `HEAD` versus with `HEAD` | setup entry point to RepoWise | Both initialize and install the hook; only the latter updates | `test_setup_skips_catch_up_before_first_commit`; `test_setup_preserves_roadmap_and_unrelated_blocks` | Passed locally |
| Uninstall ownership | Normal uninstall versus `--purge` | ownership manifest to filesystem | Normal mode retains the runtime root; purge removes it | `test_install_preserves_global_config_and_uninstall_removes_owned_block` | Passed locally |
| Repository cleanup command | Windows `python` versus POSIX `python3` | README uninstall instructions to `kit.py remove-repo` | Each supported platform receives a command that resolves its required interpreter | `test_windows_launchers_and_runtime_are_complete_distribution_artifacts` | Passed locally |
| Native release gate | Local proof versus exact pushed Windows commit | checkpoint to Codex MCP use | Windows tests pass and a fresh Codex session can use RepoWise | user VM record bound to commit | Failed at `a80ca4f`; next checkpoint pending |

## Plan of Work

First add the five thin PowerShell files and tests for argument, exit, and test-phase behavior. Use `python`, `$PSScriptRoot`, `@args`, and `$LASTEXITCODE`. Do not add a shared PowerShell helper.

Then add small platform helpers in `kit.py`. Select executable suffixes and the pinned uv installer by the running platform. Keep the current POSIX path unchanged. Add the Windows installer URL and SHA-256 to `upstream.lock.json`.

For retained runtime recovery, keep `ensure_repowise` as the only owner. Probe process status and output. Force the existing pinned uv install only after a nonzero Windows result when the manifest path, selected path, and fixed user-bin path are equal after platform normalization. Do not delete a launcher. Keep command-start errors, POSIX failures, unowned failures, and successful wrong versions as hard stops.

Move bootstrap behavior into `assets/runtime/repowise_bootstrap.py`. Use only Python standard-library process and path functions. Copy this file into the managed runtime during installation. Generate the RepoWise MCP table with `sys.executable` and an argument array that names the installed bootstrap and RepoWise executable.

Update Doctor and eager setup to use the same selected executables. Preserve normal uninstall ownership and remove the runtime root only during purge.

Update the authoritative user instructions and the publication procedure. Set the feature version to `0.19.0`. Regenerate `MANIFEST.sha256` after all tracked content is final.

## Concrete Steps

Work in `/home/mbeutler/Projects/codex-practical-kit-cpk-039`.

Run local validation with:

    ./run-tests.sh
    pwsh -File ./run-tests.ps1
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

After local validation, make and push one checkpoint. Force the reported normal Windows conversion setting during a fresh clone:

    git -c core.autocrlf=true clone --branch cpk-039-native-windows --single-branch https://github.com/calculatetech/codex-practical-kit.git codex-practical-kit-cpk-039

In the VM, run `run-tests.ps1`, install, `setup-repo.ps1 .`, and Doctor. Start a fresh Codex session in the clone. Make sure that RepoWise initializes and answers one codebase query. Save `.repowise/.update.log` evidence. Test normal uninstall, reinstall, and purge.

Record the exact commit and results in `.agent/test-results/cpk-039-native-windows.md`. If later work changes a Windows command, installed artifact, checksum, configuration, or validation step, push a new checkpoint and repeat the affected native checks.

## Validation and Acceptance

All existing POSIX tests must pass. Every Scenario Proof row must name its actual test and result before review. Native acceptance requires a successful RepoWise MCP start and tool call from the exact pushed commit.

Finalize substantive documentation before the checkpoint. Start adversarial review only after the native result passes.

## Idempotence and Recovery

Installation and repository setup are repeatable. Each external operation gets one attempt. If an operation fails, stop and report the error. Do not add retry or recovery behavior.

## Artifacts and Notes

The Windows uv installer is `https://astral.sh/uv/0.12.4/install.ps1`. Its accepted SHA-256 is `76a0c027f3d47a7ced56f9e63e67a21cb1bcbf525c8ba9ef7ec0d633cc8f89e4`.

The preflight adversary required independent proof for executable discovery, uv installation, RepoWise installation, watcher selection, watcher failure, stream ownership, artifact completeness, uninstall ownership, and exact-commit VM validation. These cases are present in the Scenario Proof.

## Interfaces and Dependencies

The public interface adds five PowerShell 7 commands beside the existing shell commands. The managed RepoWise MCP command changes from `/bin/sh -c <embedded program>` to `<python executable> <installed bootstrap> <repowise executable>`. No new dependency or public configuration key is added.

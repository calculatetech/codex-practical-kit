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
- [ ] Pass local validation and the native Windows checkpoint (completed: local validation; remaining: exact-commit Windows VM validation).
- [ ] Complete adversarial review and review closure.

## Prior Plan Reconciliation

- `docs/plans/cpk-039-native-windows.plan-summary.20260819T211423672232Z.manual-recovery.md`: carried. The Plan history hook could not link the completed response before this ExecPlan existed. This immutable copy preserves the exact response from the thread.

No earlier Plan history record applies to CPK-039.

## Plan Deviations

No accepted decision has changed.

## Surprises and Discoveries

- Observation: The Plan history hook requires the marked specification file to exist before it can store a linked record.
  Evidence: No CPK-039 record existed in `.agent/plan-history/` or beside the future specification after Plan Mode ended.
- Observation: PowerShell can leave `$LASTEXITCODE` unset after command resolution fails.
  Evidence: The first local `doctor.ps1` check reported a missing `python` command but returned status 0. Each launcher now catches this error and returns status 1.

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

## Outcomes and Retrospective

The five PowerShell entry points and the cross-platform RepoWise bootstrap are implemented. Local validation passes. Native Windows validation and adversarial review remain.

## Context and Orientation

The task worktree is `/home/mbeutler/Projects/codex-practical-kit-cpk-039`. The branch is `cpk-039-native-windows`, based on completed CPK-038 commit `66a8db7fb4627a4a281d21a0a7965a40f85f5ca3`.

The root `.sh` files are thin entry points for `kit.py`. `kit.py` owns installation, configuration, RepoWise setup, Doctor, and uninstall behavior. It currently embeds a POSIX shell program as the RepoWise MCP command. `tests/test_kit.py` owns the executable contract checks. `README.md`, `CODEX-INSTALL-PROMPT.md`, and `docs/REPOWISE.md` own user instructions.

A bootstrap is the installed command that prepares RepoWise before it starts the MCP server. The new bootstrap is `assets/runtime/repowise_bootstrap.py`. Installation copies it into the managed runtime directory.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). The current production use cases are installation, testing, eager repository setup, Doctor, uninstall, and automatic RepoWise MCP startup.

The task composes the five Windows entry points, platform tool selection, bootstrap installation, MCP configuration, user instructions, manifest, lock, version, and tests. Existing POSIX outcomes and managed hook `commandWindows` behavior are opaque and must remain unchanged. There is no deferred owner.

The supported model is one user on native Windows 10 or 11 with PowerShell 7, Python 3.11 or later, Git, and Codex. macOS and Linux remain supported. The task excludes PowerShell 5.1, batch files, Windows CI, WSL-only support, dependency installation for Python or Git, retries, recovery, concurrency, and changes to managed install locations.

## Scenario Proof

Apply [Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md) and [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md).

| Scenario | Discriminator and contrast | Production path | Required oracle | Runnable check | Result |
| --- | --- | --- | --- | --- | --- |
| Distributed artifact set | Each current `.sh` entry point versus its peer | Source inventory to manifest | Exactly five `.ps1` peers and one bootstrap source occur once with valid hashes | `test_windows_launchers_and_runtime_are_complete_distribution_artifacts` | Passed locally |
| Action launcher | Simple argument versus path with spaces; success versus error | `.ps1` to Python subcommand | Arguments and exit status remain unchanged | `test_action_launchers_forward_arguments_and_exit_status`; `test_action_launcher_reports_missing_python` | Passed locally |
| Test launcher | Passing unit phase versus failing unit phase | unit discovery to Python compilation | Success compiles every hook; failure does not compile | `test_test_launcher_compiles_kit_and_every_hook`; `test_test_launcher_stops_after_failed_unit_phase` | Passed locally |
| Existing Windows executables | Present `uv.exe` and `repowise.exe` versus absent names | platform discovery to runtime result | Existing commands are reused without installation | `test_windows_runtime_discovery_uses_executable_suffix` | Passed locally |
| Missing Windows uv | Missing `uv.exe` versus the POSIX missing path | download, hash, and `pwsh` stdin | Exact URL and hash are used once; result is `uv.exe` | `test_missing_windows_uv_runs_verified_powershell_installer_once` | Passed locally |
| Missing Windows RepoWise | Missing `repowise.exe` after uv is ready | uv tool installation to discovery | One pinned persistent tool install returns `repowise.exe` | `test_missing_windows_repowise_uses_executable_result` | Passed locally |
| Watcher platform | Same RepoWise tool on POSIX versus Windows | bootstrap watcher selector | POSIX uses patched Python; Windows uses `repowise.exe watch` | `test_watch_command_is_platform_specific` | Passed locally |
| Watcher readiness | Watcher stays alive versus exits during the gate | watcher to MCP terminal owner | Early exit returns nonzero and MCP never starts | `test_bootstrap_stops_when_watcher_fails_to_start` | Passed locally |
| Existing Git lifecycle | Missing index versus existing index; no `HEAD` versus `HEAD` | bootstrap through watcher, MCP, and cleanup | Init occurs once, hook occurs always, update needs `HEAD`, and cleanup occurs | `test_bootstrap_initializes_once_and_always_installs_hook` | Passed locally |
| Empty and non-empty non-Git folders | Empty directory versus one existing file | bootstrap through terminal owner | Empty path gets the full no-update lifecycle; non-empty path remains unchanged and starts only MCP | `test_bootstrap_initializes_only_empty_non_git_directory` | Passed locally |
| MCP stream ownership | Bootstrap diagnostics versus MCP bytes | subprocess streams | Diagnostics use stderr; stdout contains only foreground MCP bytes | `test_bootstrap_keeps_setup_diagnostics_off_mcp_stdout` | Passed locally |
| Install and Doctor | Managed block versus unrelated TOML | install to Doctor | Python bootstrap command is valid; hooks and unrelated TOML remain | installer tests and isolated `kit.py doctor` | Passed locally |
| Eager setup | Repository without `HEAD` versus with `HEAD` | setup entry point to RepoWise | Both initialize and install the hook; only the latter updates | `test_setup_skips_catch_up_before_first_commit`; `test_setup_preserves_roadmap_and_unrelated_blocks` | Passed locally |
| Uninstall ownership | Normal uninstall versus `--purge` | ownership manifest to filesystem | Normal mode retains the runtime root; purge removes it | `test_install_preserves_global_config_and_uninstall_removes_owned_block` | Passed locally |
| Native release gate | Local proof versus exact pushed Windows commit | checkpoint to Codex MCP use | Windows tests pass and a fresh Codex session can use RepoWise | user VM record bound to commit | Pending |

## Plan of Work

First add the five thin PowerShell files and tests for argument, exit, and test-phase behavior. Use `python`, `$PSScriptRoot`, `@args`, and `$LASTEXITCODE`. Do not add a shared PowerShell helper.

Then add small platform helpers in `kit.py`. Select executable suffixes and the pinned uv installer by the running platform. Keep the current POSIX path unchanged. Add the Windows installer URL and SHA-256 to `upstream.lock.json`.

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

After local validation, make and push one checkpoint. The VM checkout command is:

    gh repo clone calculatetech/codex-practical-kit codex-practical-kit-cpk-039 -- --branch cpk-039-native-windows --single-branch

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

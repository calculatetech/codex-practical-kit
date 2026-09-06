<proposed_plan>
# CPK-039 — Native Windows Compatibility

## Summary

Add native Windows 10/11 support through PowerShell 7 while preserving existing macOS/Linux behavior. Use five thin `.ps1` launchers and one cross-platform Python RepoWise bootstrap. Do not add batch files, PowerShell 5.1 support, Windows CI, or duplicate runtime implementations.

Base `cpk-039-native-windows` on completed CPK-038 commit `66a8db7`. Create the CPK-039 ExecPlan, preserve this Plan Mode summary beside it, and make CPK-039 the sole active roadmap task.

## Implementation

- Add `install.ps1`, `uninstall.ps1`, `setup-repo.ps1`, `doctor.ps1`, and `run-tests.ps1`.
  - Require PowerShell 7.
  - Resolve `kit.py` through `$PSScriptRoot`.
  - Forward arguments without string reparsing.
  - Propagate Python exit codes.
  - Make `run-tests.ps1` stop after failed tests; otherwise compile `kit.py` and every hook Python file.
- Add minimal platform selection to `kit.py`.
  - Discover `uv.exe` and `repowise.exe` on Windows.
  - Keep existing POSIX discovery and installation behavior.
  - Install missing Windows uv through the pinned official `install.ps1`, verify its SHA-256, and execute it once through `pwsh` stdin with process-scoped execution-policy bypass.
  - Install missing RepoWise through the resolved uv executable.
- Replace the embedded shell MCP bootstrap with one installed standard-library Python script.
  - Configure MCP with `sys.executable` and argument-array paths; preserve unrelated TOML and existing hook `commandWindows` entries.
  - In Git repositories: initialize RepoWise when absent, install its hook every start, update only when `HEAD` exists, start and check the watcher, then start MCP.
  - Initialize Git only when the current non-Git directory is completely empty. Do not mutate non-empty non-Git directories.
  - Send setup diagnostics to stderr. Reserve stdout for RepoWise MCP.
  - On POSIX, retain the shebang-derived Python watcher and read-event filter.
  - On Windows, invoke `repowise.exe watch` directly.
  - If the watcher exits during readiness, return failure without starting MCP. Always terminate and wait for a live watcher after MCP exits.
- Preserve existing uninstall ownership.
  - Normal uninstall removes active integrations, copied skills, global Plans, owned configuration blocks, and the manifest.
  - It retains the source checkout, managed install root, bootstrap, uv, RepoWise, and Plan history.
  - `--purge` additionally removes the managed install root.
- Update README, install prompt, RepoWise documentation, publication instructions, manifest, upstream lock, and version surfaces to `0.19.0`. Publication must select `.ps1` on Windows and `.sh` on POSIX.

## Verification

- Add focused tests for:
  - The complete five-launcher inventory and manifest coverage of every new launcher and bootstrap asset.
  - Argument and exit-code propagation, including paths containing spaces.
  - `run-tests.ps1` success and short-circuit behavior.
  - Independent Windows cases for existing executables, missing uv, and missing RepoWise.
  - Exact Windows and POSIX watcher command arrays.
  - Ordered first-start, repeat-start, no-`HEAD`, empty-directory, and non-empty non-Git lifecycles.
  - Watcher readiness failure, prevention of MCP startup, cleanup, and stdout/stderr ownership.
  - TOML preservation, Doctor readiness, normal uninstall, purge, version, checksums, and lock contents.
  - Full POSIX regression coverage.
- PowerShell tests may skip locally when `pwsh` is unavailable. Native Windows validation remains mandatory.
- Freeze implementation, documentation, manifest, lock, and validation instructions; then commit and push the checkpoint.
- Give the user this VM checkout command:

  ```powershell
  gh repo clone calculatetech/codex-practical-kit codex-practical-kit-cpk-039 -- --branch cpk-039-native-windows --single-branch
  ```

- In the native VM, run `run-tests.ps1`, install, repository setup, Doctor, and both uninstall modes. Start a fresh Codex session in the prepared repository, confirm RepoWise initializes, successfully execute a RepoWise lookup, and retain watcher/MCP evidence.
- Record the exact tested commit and VM result in `.agent/test-results/cpk-039-native-windows.md`.
- Any later change affecting Windows commands, installed artifacts, checksums, configuration generation, or the validation procedure requires a new pushed checkpoint and repeated affected VM checks.
- Run documentation maintenance and adversarial review only after native validation passes. Leave merge and publication for a later `publish` request.

## Assumptions

- Python 3.11+, Git, PowerShell 7, and Codex are already installed.
- Existing managed installation locations remain valid on Windows.
- The user’s native VM supplies Windows proof; no Windows CI is added.
- No applicable earlier Plan history record exists for CPK-039.

<!-- cpk-plan-spec: docs/plans/cpk-039-native-windows.md -->
</proposed_plan>

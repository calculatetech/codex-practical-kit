# Repair Windows installation safely


Windows installation must avoid replacing RepoWise files while its processes hold them open. The installer must identify those processes before it calls uv. After those processes stop, installation must repair the owned runtime and succeed. A healthy runtime must remain reusable. Reinstallation must preserve native plugin configuration, including tables that Codex inserts before a toolkit closing marker.

## Context and isolation


The task branch is `fix/windows-install-repowise`. It branches from `main` at `af509d29c353ed143fbd297e481e4bec1b61891e`. This task uses the existing checkout as one writable stream. Existing untracked `.mcp.json`, `.repowise/`, and `.vscode/` belong to the user.

The user reported a Node error during Ponytail installation, followed by a failed RepoWise repair. The second attempt failed when uv removed the Windows `Scripts` directory. Initial diagnosis found active RepoWise watcher and MCP processes in that environment, and RepoWise failed with `ModuleNotFoundError`. Node worked. A later installation exposed native Ponytail tables lost during marker replacement. The system Python also reports a library-prefix warning. Its configuration is outside this repository change.

The user authorized direct source access after RepoWise lookup failed. No Plan history or earlier task specification exists in this checkout.

Publish this bug fix as source version `0.26.1`. Keep the managed component versions unchanged.

## Product boundary and owners


The accepted source is the user's Windows installation report and instruction to continue. Existing product behavior is documented in `README.md` (Install and Ponytail) and `docs/REPOWISE.md` (Runtime ownership). Roadmap CPK-009 declines complete transactional recovery.

`install.ps1` dispatches to `kit.py`. The shared runtime owner is `ensure_repowise`, reached through `ensure_repowise_runtime` by installation, setup, and managed updates. It reads the kit manifest, checks the command version, and installs through uv with explicit tool and executable directories. These owners compose the change. The lock file, plugin installation, MCP bootstrap, and skill copying are opaque: preserve their current behavior. System Python installation is outside the change.

The existing marker writers also compose this task. Native Codex 0.163.0 inserts marketplace and plugin tables before the final comment in `config.toml`. That comment can be the RepoWise or hooks closing marker. Native plugin state remains opaque, but toolkit replacement and removal must preserve those unrelated tables. This direct reproduction expands the initial configuration boundary; it does not add a new plugin lifecycle.

Use [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) and [Supported model](../../assets/skills/design-preflight/references/supported-model.md). Active RepoWise processes and a second Windows installation attempt are explicitly included by this incident. Do not add automatic process termination, rollback, retries, component version changes, external packages, or a replacement runtime layout.

## Implementation and proof boundary


One atomic subtask, S1, belongs to `kit.py::ensure_repowise`. Before a Windows uv tool installation, use PowerShell 7 and `Get-CimInstance Win32_Process` to identify executable paths inside the selected RepoWise environment or at its exact user-bin launcher. Pass paths through the existing installation environment, not shell interpolation. Use a directory separator when matching the environment prefix. Compare paths without case sensitivity.

If any matching processes exist, raise `KitError` with their process IDs and instructions to close Codex sessions and stop RepoWise before retrying. Do not call uv or terminate processes. Without matches, preserve the existing install and shell-update sequence. A healthy matching version returns before the scan. The POSIX path remains unchanged. A failed process query must stop through the existing `run` error behavior.

Add direct regression checks in `tests/test_kit.py`. Execute the actual PowerShell script with a process-query fixture to prove path selection. Set `$ErrorActionPreference = 'Stop'` in that script. Update the Runtime ownership section of `docs/REPOWISE.md` and matching entries in `MANIFEST.sha256`. Complete validation and one full native review before any local task commit.

Extend that atomic subtask to the shared marker helpers, `marker_block` and `remove_marker_block`. For the two known TOML marker types, remove only the toolkit-owned table sections: `hooks` or `mcp_servers.repowise`. Preserve other table sections, even when Codex places them inside the textual markers. Append the replacement managed block after that preserved configuration. Generic Markdown marker behavior remains unchanged. Avoid a general TOML writer or new dependency; the section syntax comes from the toolkit and native Codex serializers.

Extend the native-command fixture in `tests/test_ponytail.py` to reproduce Codex's insertion location. Prove install, reinstall, and uninstall preserve marketplace/plugin tables and enabled state. Exercise the same owner through `apply-updates` in `tests/test_updates.py`. Add direct marker checks for unrelated tables interleaved with owned tables, including similarly named tables. Preserve native settings across repository setup and removal by using their shared marker owner.

## Boundary inventory and Scenario Proof


Apply [Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md). Sources have these dispositions: the Windows failure and safe repair requirement map to B1 and B2; existing healthy reuse and ownership map to B3; existing POSIX behavior maps to B4. Existing plugin and lock behavior are opaque. The prefix warning is diagnostic context, not a new installer boundary. Complete transaction recovery is deferred by CPK-009.

| Boundary | Discriminator and contrast | Production path and required oracle | Runnable check |
| --- | --- | --- | --- |
| B1: Detect active Windows RepoWise before mutation | Selected environment or exact launcher versus unrelated and sibling-prefix executable paths; zero, one, and multiple matches; equivalent paths with different case | `ensure_repowise` -> actual PowerShell script -> `KitError`; report all matching IDs, preserve runtime bytes, make no uv calls, and do not terminate processes | New `RepoWiseRuntimeTests.test_windows_repowise_repair_checks_process_paths` |
| B2: Repair after blockers stop | Same owned broken runtime with active records, then no matching records; query error versus successful empty query | `ensure_repowise` -> process query -> uv install -> shell update -> returned launcher; no install while blocked or when the query fails | New process-path check and `test_windows_repowise_process_query_errors_stop_install`, plus existing `test_install_repairs_manifest_owned_broken_windows_repowise` |
| B3: Preserve reuse and ownership | Healthy matching version versus broken owned and unowned commands | Existing version/manifest gates return healthy command or reject an unowned replacement before mutation | Existing matching-version and ownership tests in `RepoWiseRuntimeTests` |
| B4: Preserve POSIX behavior | POSIX selection versus Windows selection with the same broken owned runtime | Existing POSIX force install and shell update; no Windows process query | Existing `test_manifest_owned_broken_posix_repowise_is_repaired` |
| B5: Preserve native configuration while replacing toolkit TOML | Unrelated native tables inside versus outside the two managed spans; similar-prefix table versus owned table; repeated replacement and removal | Install/reinstall/update/uninstall/setup/remove-repo -> shared marker owner -> parsed configuration; retain every unrelated table and exact native settings. Core uninstall removes owned integration. Repository removal retains its required disabled RepoWise override | New marker preservation check, native fixture install/reinstall/uninstall tests, composed update check, and `IntegrationTests.test_setup_preserves_roadmap_and_unrelated_blocks` with native tables reseeded inside the marker before each entry point |

The Windows process query also retains the existing one-attempt error contract: a query error prevents uv execution. No retained state, background worker, or additional collection result exists. The process collection must include every matching ID; an unrelated prefix must not hide a later matching process.

Run the focused checks from the repository root:

    python -B -m unittest discover -s tests -p test_kit.py -k RepoWiseRuntimeTests -v
    python -B -m unittest discover -s tests -p test_ponytail.py -v

Run `pwsh -File .\run-tests.ps1` for the complete suite and syntax checks. Every applicable test must pass. Verify every listed `MANIFEST.sha256` digest. Store actual results in `.agent/test-results/CPK-068-windows-install.md`.

For local recovery, inspect the exact active RepoWise paths again, stop only the diagnosed broken RepoWise processes, and run the installer once. Verify RepoWise's version, ordinary reinstall, and Doctor. Use the already installed healthy uv-managed Python for diagnosis if the system Python warning interferes. Do not alter the system Python installation.

## Decision Log


Use a read-only process guard instead of automatic termination or a new versioned environment layout. Windows can hold executable files open; uv tool installation recreates environments. The existing uv owner remains responsible for installation. See [uv tool management](https://docs.astral.sh/uv/concepts/tools/).

Keep the native Ponytail lifecycle unchanged. Preserve its configuration through toolkit updates because a live reinstall exposed the marker-span deletion. Keep the system Python warning separate because the RepoWise environment already selects a uv-managed interpreter. OpenAI's [plugin documentation](https://developers.openai.com/plugins/build/plugins) identifies native marketplace commands and user-level plugin settings as their owners.

The independent preflight requires explicit case variation and terminating CIM errors. Accept both. Use a fixture at the native process-query seam to exercise the actual PowerShell selector without copying Python executables and DLLs. A separate local run against the diagnosed live processes proves native discovery, followed by one repair after those processes stop.

The configuration preflight requires explicit repository setup and removal proof because these paths share the changed marker owner. Reseed the native table inside the marker before each command. Preserve the repository removal disable override. This adds proof of existing behavior, not a new lifecycle.

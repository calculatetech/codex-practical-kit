# Apply managed updates and add website-only 12UI

This ExecPlan is a living specification until review closure. Maintain it in accordance with `.agent/PLANS.md`.

## Purpose / Big Picture

The toolkit can report upstream releases, but it cannot act on that report. After this change, a user can run a small Bash or PowerShell command to check updates or explicitly apply every managed update. Application updates the source lock and the selected installed toolkit, so the next check, install, and Doctor result agree.

The toolkit also installs the official 12UI Codex plugin. The global toolkit router permits that skill only for website projects. The toolkit does not copy or modify the upstream 12UI skill.

## Surprises & Discoveries

- Observation: Codex CLI 0.160.0 has no general `plugin update` command. A named Git marketplace is refreshed with `codex plugin marketplace upgrade NAME`, which refreshes installed plugin caches and preserves enabled state.
  Evidence: the CLI help and the native plugin implementation expose the named marketplace upgrade operation.
- Observation: a current source pin does not prove that the selected installation is current.
  Evidence: an updated checkout can coexist with skills installed from an older checkout.
- Observation: the documented 12UI install route is an official Git marketplace, not a copied skill directory.
  Evidence: `just-every/12ui-plugin` documents `marketplace add just-every/12ui-plugin` and `plugin add 12ui-design@12ui-plugin`.
- Observation: Codex lists the 12UI package as local because the marketplace repository is also the package root.
  Evidence: the installed record keeps the official Git marketplace identity and reports a local package source.

## Decision Log

- Decision: preserve `check-updates` as a read-only operation and add a separate `apply-updates` operation.
  Rationale: checking must remain safe and explicit, while applying is an intentional mutation.
- Decision: add `check-updates.sh`, `check-updates.ps1`, `apply-updates.sh`, and `apply-updates.ps1` as thin sibling-script launchers.
  Rationale: the shell files only locate `kit.py`, select one fixed command, forward arguments, and return its status.
- Decision: use `upstream.lock.json` as the single source of runtime versions, installer identities, skill revisions, native plugin sources, and package files.
  Rationale: duplicated editable constants can make checking, installation, and Doctor disagree.
- Decision: resolve each selected skill commit through its complete, non-truncated Git tree and install every blob under its declared package root plus its declared repository license.
  Rationale: a short static file list can silently omit added, changed, or removed package files.
- Decision: apply an exact RepoWise version through the existing managed `uv tool install` owner. Download and verify both official uv installer bodies, then execute only the current platform body.
  Rationale: each installed runtime must match the selected lock identity and the platform paths remain distinct.
- Decision: manage Ponytail and 12UI through exact native Git marketplace selectors. Install an absent managed plugin and refresh an installed plugin with `marketplace upgrade`.
  Rationale: this is the upstream-native lifecycle and preserves user enablement and plugin data.
- Decision: validate the 12UI local package through its official Git marketplace record.
  Rationale: Codex resolves that local package from the verified marketplace snapshot.
- Decision: put the website-only 12UI restriction in the global routing owner, `assets/AGENTS.block.md`.
  Rationale: the router owns activation scope. The upstream plugin continues to own its workflow.
- Decision: validate all candidates before the first mutation. Stop on the first operation failure without retry or a false completion message.
  Rationale: this minimizes partial work while preserving the repository's accepted non-transactional model.
- Decision: evaluate checkout identity and tracked target modifications relative to `kit.py`'s `ROOT`, not the caller's current directory.
  Rationale: an absolute launcher path must work from another directory.
- Decision: write the source lock only after the selected installation succeeds.
  Rationale: a failed installation remains retryable, and the installed lock identifies a prior successful source write.
- Decision: no Plan History record applies to this task. The branch `cpk-062-managed-update-application-12ui` is based on reviewed CPK-061 commit `37a3bc69fc1ff09e6fc372320bafd29d4d867e2f`.
  Rationale: the user continued from that local reviewed result and did not request publication.

## Outcomes & Retrospective

Users can now check or apply all managed updates through short Bash or PowerShell commands. Apply validates complete candidates, updates the source lock, and reconciles the selected installation even when the source identities already match.

The toolkit installs or refreshes official Ponytail and 12UI plugins through their exact native marketplaces. The installed router limits 12UI to website projects. The update model remains explicit and non-transactional: it stops after the first error and can be run again after the user corrects the cause.

The main design lesson is that source identity and installed state are separate facts. End-to-end checks must prove both through the real command and launcher paths.

## Context and Orientation

`kit.py` is the Python command owner. `check_updates` reads `upstream.lock.json`, queries official provider endpoints, and reports comparable identities. `install_core` stages locked skills, installs owned files, configures native plugins, writes the installed manifest, and installs global instructions. `doctor` checks the selected installation.

`upstream.lock.json` is the authoritative managed inventory. `runtime_tools` contains RepoWise, uv, and native plugins. `skills` contains copied third-party skill packages. `optional_tools` is informative and is outside this task.

`assets/AGENTS.block.md` is the live global router installed into the user's selected Codex home. `MANIFEST.sha256` lists distribution files. `tests/test_kit.py`, `tests/test_ponytail.py`, and the new focused update tests exercise installation and update behavior.

## Product Boundary

Follow [Scope boundaries](</home/mbeutler/.agents/skills/design-preflight/references/scope-boundaries.md>). The authoritative request is to apply reported managed updates, provide simpler Bash and PowerShell actions, add 12UI, and use 12UI only for website projects.

The toolkit owns managed inventory selection, candidate validation, source-lock writes, installed toolkit files and records, exact native marketplace selection, global router text, launchers, Doctor checks, and terminal status. Official HTTP providers, installer internals, Codex plugin storage, and the internal Ponytail and 12UI workflows are opaque external owners.

Normal use is one personal user and one writer, online official provider reads, a normal Git checkout, clean tracked update targets, and a selected installation whose manifest owns its targets. A managed plugin can be absent or installed from its official source.

The hard ceiling excludes optional tools, background or scheduled updates, version-order policy, general package management, new dependencies, retry, rollback, recovery, permission or interruption models, arbitrary repository instruction overrides, plugin storage parsing, modified upstream skills, and claims about future model behavior.

## Scenario Proof

The accepted behavioral boundaries are:

- B1: Check and apply cover each managed component exactly once, including 12UI. They exclude optional tools and unrelated plugins.
- B2: Check remains explicit and read-only. It reports comparable identities honestly and does not invent a baseline for native plugins.
- B3: Apply changes the selected managed installation. Runtime versions, complete skill files, verification identities, records, and affected Doctor results must agree.
- B4: Plugin refresh targets only the exact managed marketplaces in the selected Codex home. It preserves enablement, settings, unrelated marketplaces, and the default home.
- B5: Toolkit instructions permit 12UI only for website design. Installation and refresh must not add a contradictory broader toolkit instruction.
- B6: Ordinary installation adds an absent official 12UI plugin. It reuses an existing official disabled plugin without re-enabling it.
- B7: Each launcher resolves its sibling `kit.py`, preserves arguments and destinations, and returns the Python command status from another working directory.
- B8: The first operation error stops the action after one attempt. The command returns a failure status and prints no partial check report or false apply success.

Follow [Scenario discrimination](</home/mbeutler/.agents/skills/design-preflight/references/scenario-discrimination.md>), [Owner composition](</home/mbeutler/.agents/skills/design-preflight/references/owner-composition.md), and [Full-set results](</home/mbeutler/.agents/skills/design-preflight/references/full-set-results.md).

S1 proves the complete read-only check. Equal early identities and a differing final skill, plus both managed plugins, must produce exact complete output with no writes. Run `python3 -m unittest tests.test_kit.ComponentUpdateTests.test_check_updates_reports_complete_managed_inventory`.

S2 proves runtime application through the real command path. `test_apply_main_reconciles_complete_installation_and_plugins` covers RepoWise and POSIX uv. `test_apply_main_windows_runtime_branch` covers Windows uv. Each check enters through `main`, validates candidates, writes the source lock, invokes the runtime owners, updates records, and reaches the selected-version oracle.

S3 proves complete skill replacement. `test_apply_main_reconciles_complete_installation_and_plugins` uses the real tree selector, blob verifier, staging, `install_skills`, manifest writer, and Doctor path. It also adds an obsolete installed file before an equal-source apply. The terminal file set must match the selected revision exactly.

S4 proves native plugin refresh. `test_apply_main_reconciles_complete_installation_and_plugins` uses real status selection and `codex_plugin` calls against a deterministic external Codex fixture. It uses a nondefault selected home, disabled plugins, user data, an unrelated marketplace, and a default-home sentinel. Exact named upgrades must refresh managed caches without re-enablement or unrelated changes.

S5 proves the 12UI installation and policy transition. `test_install_main_fresh_and_preserves_disabled_12ui` contrasts absent and disabled official 12UI states through real install dispatch. `test_apply_main_reconciles_complete_installation_and_plugins` checks the installed router and Doctor after application and refresh. `test_update_launchers_run_complete_actions_and_propagate_failures` repeats the transition through the Bash and PowerShell install launchers.

S6 proves full-set application and failure. `test_apply_main_reconciles_complete_installation_and_plugins` checks the complete selected inventory and excludes optional tools. `test_apply_main_stops_after_first_operation_error` pairs successful application with a later plugin failure, then checks one attempt, no later runtime operation, status 2, and no false completion.

S7 proves the actual Bash launchers from another working directory and a source path that contain spaces. `test_update_launchers_run_complete_actions_and_propagate_failures` runs complete check, apply, install, and failure paths through the real Python command.

S8 proves the equivalent PowerShell 7 paths in `test_update_launchers_run_complete_actions_and_propagate_failures`. A platform skip is not closure evidence.

S9 proves installed reconciliation when the source pin is already current. The second apply in `test_apply_main_reconciles_complete_installation_and_plugins` begins with stale owned files and equal source and upstream identities. It must restore exact installed bytes and records.

## Plan of Work

### CPK-062-A: Unify candidate preparation and source identities

Refactor `kit.py` so checking and applying share one complete managed candidate collector. Read runtime values from `upstream.lock.json`. Add complete Git-tree skill discovery, package-root and license metadata, verified blob collection, and both verified uv installer bodies. Reject incomplete provider data and truncated trees before mutation. Keep `check-updates` read-only and preserve exact reporting.

The allowed boundary is `kit.py`, `upstream.lock.json`, focused tests, and directly affected documentation. The exact focused validation is the S1 inventory test plus the candidate-selection tests in `tests/test_updates.py`. The checkpoint boundary is source candidate preparation without installed mutation.

### CPK-062-B: Apply candidates to source and selected installation

Add `apply-updates` dispatch. Check the checkout and managed tracked targets relative to `ROOT`. After complete preparation, update the lock and reconcile the selected installation even when source identities already match. Route RepoWise and uv through their existing platform owners. Replace each owned installed skill with the complete staged package and update installed records. Stop after the first operation error.

The allowed boundary is the update and existing installation owners in `kit.py`, the lock, and focused tests. Run the exact S2, S3, S6, and S9 tests. The checkpoint boundary is coherent source and installed state with a ready Doctor result.

### CPK-062-C: Add native 12UI and website-only routing

Generalize native plugin source validation only enough for Ponytail and 12UI. Install an absent official plugin. Refresh an installed plugin by its exact managed marketplace and preserve enablement and data. Add the unique website-only 12UI routing guard and router entry to `assets/AGENTS.block.md`. Add both plugins to Doctor.

The allowed boundary is native plugin helpers, install/apply/Doctor composition, the global router, the lock, and direct tests. Run the exact S4 and S5 tests and existing Ponytail tests. The checkpoint boundary is official plugin availability plus the installed website-only policy.

### CPK-062-D: Add thin launchers and finish distribution documentation

Add the four fixed launchers. Update `README.md` and third-party notices for the action commands, 12UI source and license, native lifecycle, and website-only scope. Update `MANIFEST.sha256` after all tracked files are final.

Run S7 and S8, shell syntax checks, Python compilation, checksum verification, the full unit suite, and the distribution diff check. Finalize documentation before trace closure and correctness review.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-062-managed-update-application-12ui`.

Use focused tests while editing:

    python3 -m unittest tests.test_kit.ComponentUpdateTests.test_check_updates_reports_complete_managed_inventory
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_apply_repowise_selected_version
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_apply_uv_posix
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_apply_uv_windows
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_apply_complete_skill_revision
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_apply_native_plugins_preserves_user_state
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_install_12ui_absent_or_existing
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_12ui_policy_is_website_only
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_update_set_cardinality_and_late_record
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_update_actions_stop_once_on_error
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_bash_update_launchers_complete_path
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_powershell_update_launchers_complete_path
    python3 -m unittest tests.test_updates.ApplyUpdateTests.test_apply_reconciles_stale_installed_skill
    python3 -m unittest tests.test_updates.ComposedUpdateTests

Then run:

    python3 -m py_compile kit.py tests/test_kit.py tests/test_updates.py tests/test_ponytail.py
    sh -n check-updates.sh apply-updates.sh
    pwsh -NoProfile -Command '$ErrorActionPreference="Stop"; [void][scriptblock]::Create((Get-Content -Raw ./check-updates.ps1)); [void][scriptblock]::Create((Get-Content -Raw ./apply-updates.ps1))'
    python3 -m unittest discover -s tests -p 'test_*.py'
    sha256sum --check MANIFEST.sha256
    git diff --check

Each command must exit 0. The PowerShell launch check must run, not skip, on this supported host.

## Validation and Acceptance

`check-updates` and both check launchers must report every managed runtime tool and skill, including 12UI, without persistent mutation. `apply-updates` and both apply launchers must make the source lock and selected owned installation match the validated candidates. A second equal-source application must still repair a stale owned installation.

An absent 12UI plugin must be installed from `just-every/12ui-plugin`. An existing official disabled 12UI plugin must remain disabled after refresh. Exact named marketplace upgrades must leave unrelated marketplaces, plugin data, and the default Codex home unchanged.

Doctor must report both native plugins and the selected runtime identities. The installed global instructions must state that `12ui-design` is used only for website projects. No toolkit-owned live instruction may broaden that activation scope.

Any provider, validation, installer, plugin, or write failure must stop after one attempt, return status 2, omit later actions, and omit the complete-success message.

## Idempotence and Recovery

Checking is repeatable and read-only. Applying an already selected identity is repeatable, but it must reconcile stale owned installed content. The command validates all candidate metadata and bytes before mutation and refuses tracked modifications to managed source targets. It preserves unrelated untracked files.

The operation is not transactional. If an operation fails after mutation begins, it stops and reports the error. The user can correct the reported cause and run the same explicit apply command again. There is no automatic retry, rollback, or recovery.

## Artifacts and Notes

The ignored working record is `.agent/test-results/CPK-062.md`. Keep operational test and review results there, not in this specification.

Applicable Plan History records: none.

## Interfaces and Dependencies

Use only the Python standard library and existing repository helpers. Keep `kit.py check-updates` stable. Add `kit.py apply-updates` with the same selected-home arguments as installation where applicable.

The native plugin records in `upstream.lock.json` must identify the Git marketplace source, marketplace name, and plugin identifier. Ponytail uses `DietrichGebert/ponytail`, marketplace `ponytail`, and plugin `ponytail@ponytail`. 12UI uses `just-every/12ui-plugin`, marketplace `12ui-plugin`, and plugin `12ui-design@12ui-plugin`.

The skill records must declare a package root and repository license path. The applied `files` list is a sorted complete list of destination paths and Git blob SHA-1 identities for every package blob plus the license.

Do not add a dependency, daemon, cache, plugin-state parser, general package manager, or modified upstream 12UI asset.

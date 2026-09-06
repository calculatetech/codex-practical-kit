# CPK-055 — Install the official Ponytail plugin

This specification follows `.agent/PLANS.md`. It defines two independent checkpoint boundaries.

## Purpose


Install all official Ponytail features through Codex. Users control modes and persistent defaults through the upstream plugin. The toolkit no longer changes modes at phase boundaries. Codex exposes the six skills through its skill interface, including `@ponytail-review`; a slash-menu entry is not promised.

## Context and orientation


`kit.py` currently downloads only Ponytail's main skill and license through `UPSTREAM_SKILLS` and `upstream.lock.json`. `assets/AGENTS.block.md`, the lifecycle implementation-mode reference, and `assets/hooks/session_start.py` impose toolkit mode choices. The native plugin includes six skills and SessionStart, UserPromptSubmit, and SubagentStart hooks. Codex owns its installation, version, enabled state, and cache. Node.js runs its hooks.

The task uses branch `task/cpk-055-native-ponytail` from `main` at `c5fe5779d6b5f40a8338b213283b20b2017d3733`, in the existing checkout. Publication is separate from local implementation. Host installation and Doctor follow the complete reviewed candidate.

## Decision Log


- Replace the copied skill with the official native plugin to retain all documented upstream features.
- Preserve existing official plugin versions, settings, and disabled state. Codex owns updates and removal, including installations first created by this toolkit.
- Reject foreign marketplace sources and unowned standalone skills before native writes. Remove a legacy skill only after successful native installation or reuse and proof of prior manifest ownership.
- Require Node.js and native plugin-command support before changing an existing installation. Do not install Node.js, implement aliases, modify upstream bytes, or grant hook trust.
- Keep the existing shared subprocess helper and explicit selected `CODEX_HOME`. Do not add a plugin ownership ledger or mode state.
- Document complete removal on POSIX and Windows, including retained plugin data, shared settings, RepoWise, uv, repository indexes, and Plan history.

## Plan deviations and reconciliation


The accepted source is [.agent/plan-history/plan-summary.20260906T145108959420Z.4ca59f1efb35d2fec6091bc88b5848bb2e50226576f0a493f9ec85ed1838c57b.md](../../.agent/plan-history/plan-summary.20260906T145108959420Z.4ca59f1efb35d2fec6091bc88b5848bb2e50226576f0a493f9ec85ed1838c57b.md). Its decisions are carried. The user's explicit plugin-only mode choice supersedes phase-based mode selection in [CPK-028](cpk-028-phase-scoped-minimalism.md) and [CPK-029](cpk-029-plan-mode-hook.md). Their other requirements remain carried; their historical contents remain unchanged. Earlier Plan records retain their unrelated decisions, including installation ownership and central Plan capture.

Record: [.agent/plan-history/plan-summary.20260824T164719361941Z.f1479c9effab9071b8ccaa86dce1dbee407b79647c6bb7d542aea8c75caae32b.md](../../.agent/plan-history/plan-summary.20260824T164719361941Z.f1479c9effab9071b8ccaa86dce1dbee407b79647c6bb7d542aea8c75caae32b.md)

Status: superseded

Scope: its retained CPK-028 authority for automatic Ponytail mode selection only.

Reason: the user explicitly selected plugin-only mode ownership in the accepted CPK-055 Plan.

Replacement: the upstream plugin and user selections control modes. All unrelated retained decisions remain carried.

## Surprises & Discoveries


Native Codex refuses plugin inspection when the selected `CODEX_HOME` directory does not exist. Fresh installation creates that directory before inspection. Existing installation files remain unchanged during prerequisite checks.

## Product boundary


Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) and [Supported model](../../assets/skills/design-preflight/references/supported-model.md). The accepted Plan and explicit user decisions define the product result. Toolkit installation, migration, Doctor, and managed hook output are in-scope owners. Native Codex commands and the unmodified Ponytail package are external owners. Tests may substitute only those opaque commands and network providers. User hook trust remains manual. Toolkit uninstall and purge retain native plugin resources for fresh and pre-existing installations alike.

## Scenario Proof


Apply [Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md) and [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md). The following accepted inventory maps every behavior clause. CP1 covers B2 and B9; CP2 covers the remaining runtime rows and B10 documentation. Upstream model quality is opaque. Publication is outside this task.

| Boundary | Discriminator and minimal contrast | Production path and required oracle | Named check |
| --- | --- | --- | --- |
| B1 | Complete native plugin versus copied main skill | Install through native commands; six skills and all three hook declarations exist | `test_fresh_install_registers_complete_plugin`, isolated native smoke |
| B2 | Plugin active versus off, with toolkit phase changes | Managed hook and static routes never select a mode | `test_plan_prompt_preserves_plugin_mode_and_history`, `test_ponytail_modes_have_only_upstream_owner` |
| B3 | Manifest-owned legacy skill versus unowned same path | Actual install removes only recorded legacy skill after native success; conflict preserves user data | `test_legacy_skill_migration_requires_recorded_ownership` |
| B4 | Absent versus existing official plugin; foreign versus official marketplace | Actual install creates absent plugin, preserves existing version/settings/enabled state, rejects foreign source before writes | `test_existing_official_plugin_is_reused`, `test_foreign_marketplace_is_preserved` |
| B5 | Fresh versus pre-existing native installation | Install, reinstall, uninstall and purge retain native resources and settings | `test_native_plugin_survives_reinstall_and_uninstall` |
| B6 | Selected Codex home versus process-default home | Install and Doctor use selected home; uninstall follows recorded toolkit destinations without native removal | `test_plugin_commands_use_selected_codex_home` |
| B7 | Native plugin and Node.js versus legacy-only or missing prerequisites | Doctor rejects missing requirements; install independently rejects missing Node.js and unsupported native commands before old skill/hooks/config/manifest changes | `test_doctor_requires_native_plugin_and_node`, `test_missing_prerequisites_preserve_existing_installation` |
| B8 | Plugin installation versus user hook approval | Actual install configuration and output preserve manual trust | `test_fresh_install_registers_complete_plugin` |
| B9 | Plan versus ordinary prompt, and session lifecycle | Configured installed hook preserves history and reminder without a mode directive; session announcement remains | `test_plan_prompt_preserves_plugin_mode_and_history`, existing Plan and SessionStart checks |
| B10 | Toolkit removal versus full optional component cleanup | README documents ordered POSIX and Windows cleanup and retained state | Documentation inspection and native review |

The preflight challenger identified two additional test obligations within B4 and B7: foreign marketplace rejection and independent prerequisite failures through actual installation. Both are included above. All accepted clauses are mapped or explicitly opaque or outside scope. No unresolved contract gap remains.

## Plan of work


CP1 removes the managed Ponytail route, automatic mode instructions, and prompt-hook `normal mode` output. Retain test-scope requirements, challenger reasoning, Plan capture, planning reminders, and other hooks. Update the installed-hook and rule-owner tests in `tests/test_kit.py`. Correct the README's prompt-hook statement. This checkpoint's owner is the managed hook and lifecycle reference. Its review and local commit cover only this boundary and its specification.

CP2 changes `kit.py` to inspect `codex plugin marketplace list --json` and `codex plugin list --marketplace ponytail --json`. Pass the selected Codex home to every native command. Add the official `DietrichGebert/ponytail` marketplace and `ponytail@ponytail` plugin only when absent. Validate prerequisites and ownership before mutation. Remove Ponytail from copied upstream skills and add its legacy name to obsolete skills. Put the native integration checks in `tests/test_ponytail.py`. Update Doctor, the lock descriptor, README, CODEX-INSTALL-PROMPT.md, THIRD_PARTY.md, and checksums. This checkpoint depends on CP1 and covers native lifecycle, migration, and cleanup documentation.

## Concrete steps and acceptance


From the repository root, run focused checks with `TMPDIR=/var/tmp python3 -m unittest discover -s tests -p 'test_*.py' -k <test-name>`. CP1 must preserve the Plan reminder and emit no mode choice. CP2 must meet each row's terminal oracle through the actual toolkit path. Run `TMPDIR=/var/tmp ./run-tests.sh` for the complete suite. `/var/tmp` avoids an unrelated invalid `/tmp/.git` marker on this host.

Use an isolated Codex home for a real native installation smoke check. Confirm all six skill files and three hook events from its native catalog and package. Exercise full, lite, ultra, off, status, persistent defaults, and lifecycle hooks with isolated upstream state. Preserve upstream package bytes. Complete checkpoint trace verification and native reviews, followed by the final complete native review. Then run `./install.sh` and `./doctor.sh` on the host; Doctor must report `Result: ready`.

## Idempotence and removal


Repeated installation reuses official native resources without upgrades or forced enablement. Native command errors stop the operation. Complete installation transactionality remains outside the supported model. Prerequisite and ownership conflicts must occur before changes to existing installation data.

README cleanup instructions first remove repository integrations, then purge toolkit files. Optional upstream state cleanup precedes native plugin removal because removal deletes its cache. The upstream uninstall script does not remove Codex's `plugins/data/ponytail-ponytail` state. Document that state separately, plus shared Ponytail configuration and its effect on other clients. Then describe native plugin and marketplace removal, optional RepoWise and uv removal, and retained Plan history and indexes. Do not perform cleanup in other repositories.

## Artifacts


Keep detailed command, trace, and review results in `.agent/test-results/cpk-055-native-ponytail.md`. This ignored record is not part of the product specification. Regenerate `MANIFEST.sha256` for each review candidate. No new dependency, wrapper, or custom state format is needed.

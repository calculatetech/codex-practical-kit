# Install Codex hooks in config.toml

This ExecPlan is a living document. Maintain it according to the repository's `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, the installer records the toolkit Session Start hook in `$CODEX_HOME/config.toml`, which is the documented Codex configuration file. Repeated installation preserves unrelated TOML configuration and does not create the legacy `$CODEX_HOME/hooks.json` file.

## Progress

- [x] (2026-08-14 15:39Z) Inspected the installer path, the current converted configuration, and the official Codex configuration reference.
- [x] (2026-08-14 15:39Z) Defined the normal-use behavior floor and scope ceiling.
- [x] (2026-08-14 15:39Z) Activated CPK-015 on an isolated task branch.
- [x] (2026-08-14 15:48Z) Replaced legacy JSON hook management with a marker-delimited TOML block.
- [x] (2026-08-14 15:48Z) Updated the focused installer test and affected install documentation.
- [x] (2026-08-14 15:48Z) Passed all 25 initial tests, Python compilation, shell syntax, diff, and manifest checks.
- [x] (2026-08-14 16:01Z) Corrected the sibling-handler preservation defect from review pass 1 and passed all 26 tests.
- [x] (2026-08-14 16:10Z) Corrected the inline-comment boundary defect from review pass 2 and passed all 26 tests.
- [x] (2026-08-14 16:31Z) Applied the user direction to delete text-boundary adoption and use parsed hook-entry existence only.
- [x] (2026-08-14 16:31Z) Passed the focused existing-hook checks and all 25 tests after simplification.
- [x] (2026-08-14 16:42Z) Corrected the pre-existing-file rewrite found in fresh review pass 1 and passed all 25 tests.
- [x] (2026-08-14 16:50Z) Completed fresh review pass 2. The candidate is clean after the pass-1 correction. Applied review closure.

## Surprises & Discoveries

- Observation: The installer calls the legacy file `hooks.json`, although the report called it `config.json`.
  Evidence: `load_hooks_config()`, `install_hooks()`, `uninstall_hooks()`, and `doctor()` in `kit.py` read `$CODEX_HOME/hooks.json`.
- Observation: The current converted environment already contains the accepted Session Start TOML shape.
  Evidence: `$CODEX_HOME/config.toml` uses `[[hooks.SessionStart]]` and `[[hooks.SessionStart.hooks]]` with the current command fields.
- Observation: An exact handler can be the first handler in a Session Start group that also contains an unrelated handler.
  Evidence: Review pass 1 showed that a marker around only the matching prefix makes uninstall change the remaining handler's parent table.
- Observation: A valid TOML array-table header can have an inline comment.
  Evidence: Review pass 2 showed that a bare-string comparison missed `[[hooks.SessionStart.hooks]] # user hook`.
- Observation: TOML quoted keys and whitespace around dots can name the same array table.
  Evidence: Review pass 3 showed that `[[hooks."SessionStart".hooks]]` bypasses the canonical-header expression and can orphan an unrelated handler during uninstall.
- Observation: `remove_marker_block()` normalizes whitespace even when its marker is absent.
  Evidence: Fresh review pass 1 showed that hook uninstall could rewrite a pre-existing file without owning a hook block.

## Decision Log

- Decision: Manage one marker-delimited Session Start block in `$CODEX_HOME/config.toml`.
  Rationale: `kit.py` already uses marker blocks to preserve unrelated TOML when it installs RepoWise configuration.
  Date/Author: 2026-08-14 / Codex
- Decision: Adopt an exact unmarked copy of the current Session Start block on first installation.
  Rationale: Superseded. Textual adoption created false ownership of neighboring TOML content.
  Date/Author: 2026-08-14 / Codex
- Decision: Do not migrate arbitrary legacy JSON hook entries.
  Rationale: The task only changes the install procedure, and the current environment needs no migration. Unrelated user configuration remains outside toolkit ownership.
  Date/Author: 2026-08-14 / Codex
- Decision: Keep version `0.10.0`.
  Rationale: Version `0.10.0` is an untagged release candidate. This correction fixes its Session Start installation procedure before release.
  Date/Author: 2026-08-14 / Codex
- Decision: Stop automatic correction and publication after review pass 3.
  Rationale: The repository breaker forbids another automatic fix after three consecutive defectful passes.
  Date/Author: 2026-08-14 / Codex
- Decision: Parse `config.toml` and check only for the expected nested Session Start handler values.
  Rationale: The user rejected textual table-boundary logic. Existing matching entries remain unchanged. Absent entries get one managed block.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Drop the fresh review pass 2 whitespace-only finding.
  Rationale: Blank-line normalization does not change a TOML entry or behavior. It does not violate the user's explicit entry-based requirement.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

CPK-015 is complete. The installer parses `config.toml` with the Python standard library. If the expected nested Session Start handler exists, installation leaves it unchanged. If it is absent, installation appends one managed block. Uninstall returns without writing when that marker is absent. Quoting, comments, table order, whitespace, and unrelated configuration do not affect the existence check. All 25 tests pass. Fresh review pass 2 was clean after the pass-1 correction. Direct branch publication is authorized because PR mode is off.

## Context and Orientation

The task uses branch `cpk-015-config-toml-hooks`. Its base branch is `cpk-014-stop-doc-commit`, and its base commit is `7be10c6de3b47b88c6bae6d57942d859ac8aa61a`. This stacked branch is necessary because CPK-014 is pushed but is not yet integrated into `main`. The isolation form is a normal branch in the existing checkout. The target toolkit version remains `0.10.0`.

`kit.py` owns installation, removal, and diagnosis. Its hook functions read `$CODEX_HOME/config.toml` with the standard library `tomllib` parser. The file also has `marker_block()` and `remove_marker_block()` helpers for blocks that the installer creates.

`tests/test_kit.py` has a focused reinstall test. It proves that an existing matching handler remains unchanged, including when TOML uses quoted keys. It also proves idempotence and the absence of a new JSON file.

`README.md` and `CODEX-INSTALL-PROMPT.md` name the legacy hook file. These statements must name `config.toml` after the behavior changes.

The supported operating model has one personal user and one Codex writer on a normal local filesystem. The installer owns only its marker-delimited TOML block and its installed hook script. On failure, it stops and reports the error.

## Normal-Use Behavior Floor

A fresh install adds one Session Start hook block to `$CODEX_HOME/config.toml`. A repeated install produces the same managed block. If the expected nested handler already exists, installation leaves it unchanged. Unrelated TOML content remains unchanged. Installation does not create `$CODEX_HOME/hooks.json`.

Uninstall removes only a toolkit marker block that installation created. It does not remove a matching pre-existing handler. Doctor passes when the expected handler values and installed script are present.

## Scope Ceiling

Do not edit the live `$CODEX_HOME/config.toml`. Do not migrate arbitrary JSON handlers. Do not manage unrelated Codex hooks or the RepoWise Git `post-commit` hook. Do not add a TOML writing dependency, a general parser, recovery behavior, or compatibility configuration.

## Plan of Work

In `kit.py`, parse `config.toml` with `tomllib`. Check the nested Session Start handler values without inspecting text boundaries. If the handler is absent, append the managed block. On uninstall, remove only that marker block. Update doctor and command output to inspect `config.toml`.

In `tests/test_kit.py`, use a TOML file with unrelated configuration and an existing matching handler under quoted keys. Install twice and prove that no duplicate or marker appears. Uninstall and prove that the pre-existing handler remains. For a fresh configuration, prove that install and uninstall add and remove only the managed block.

Update only the affected install instructions. Regenerate `MANIFEST.sha256` after all tracked content is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-015-config-toml-hooks`.

Run:

    python3 -m unittest tests.test_kit.InstallerTests.test_reinstall_accepts_existing_config_toml_hook
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record current commands, exit status, and concise evidence in the untracked `.agent/test-results/cpk-015-config-toml-hooks.md` file. Before review, mark validation complete and review pending.

## Validation and Acceptance

The focused test must fail if installation creates `hooks.json`, duplicates the existing Session Start hook, or removes pre-existing TOML. The fresh-install test must fail if uninstall leaves its managed block. The full test suite, Python compilation, shell syntax, diff, and manifest checks must pass.

## Idempotence and Recovery

Installation is repeatable when the handler is pre-existing or managed. Uninstall removes only the managed marker block. If an operation fails, stop and report it. Do not retry, roll back, or repair unrelated configuration.

## Artifacts and Notes

Preserve the existing untracked `.mcp.json`, `.repowise/`, and `.vscode/` paths. Never stage `.agent/test-results/`.

## Interfaces and Dependencies

No new dependency or public command is required. `kit.py` continues to use Python's standard library. The installed TOML interface is one `[[hooks.SessionStart]]` table with one nested `[[hooks.SessionStart.hooks]]` command table.

Revision note: Created after repository inspection and Design Preflight to record the accepted CPK-015 implementation.

Revision note: Updated after implementation, documentation maintenance, validation, and the ready-for-review roadmap transition.

Revision note: Updated after review pass 1 to record the sibling-handler correction and fresh validation.

Revision note: Updated after review pass 2 to record the inline-comment correction and fresh validation.

Revision note: Updated after review pass 3 to record the validated blocker and stop publication.

Revision note: Replaced textual adoption with the user-directed parsed existence check. The resumed task now awaits fresh review.

Revision note: Updated after fresh review pass 1 to record the no-marker uninstall guard and byte-preservation check.

Revision note: Updated after fresh review pass 2 to record the rejected whitespace-only finding, clean review closure, and authorized publication.

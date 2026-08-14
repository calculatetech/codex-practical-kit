# Remove the Stop hook

This ExecPlan is a living document. Maintain it according to the toolkit-managed `$CODEX_HOME/PLANS.md`.

## Purpose / Big Picture

After this change, Codex can stop without a toolkit command that checks review and documentation markers. The installed agent instructions remain the review authority. A fresh install adds only the Session Start hook. A reinstall removes old toolkit-owned Stop and Session End hooks.

## Progress

- [x] (2026-08-14 12:58Z) Reproduced the original documentation-commit problem and started CPK-014.
- [x] (2026-08-14 13:03Z) Stopped the commit-classification approach after three defectful review passes.
- [x] (2026-08-14 13:03Z) Accepted the user decision to remove Stop gating and completed a new Design Preflight.
- [x] (2026-08-14 15:11Z) Removed Stop-hook installation, state management, scripts, and tests.
- [x] (2026-08-14 15:11Z) Added one focused reinstall check that preserves unrelated hooks.
- [x] (2026-08-14 15:11Z) Updated version owners and user documentation.
- [x] (2026-08-14 15:11Z) Corrected the compiled-hook cleanup defect from removal review pass 1.
- [x] (2026-08-14 15:11Z) Completed fresh removal review pass 2. The review was clean after the pass-1 correction. Applied review closure.

## Surprises & Discoveries

- Observation: Commit classification expanded from one reported documentation case into Git-history policy.
  Evidence: Three review passes found distinct defects in baseline status, merge diffs, and divergent branches.
- Observation: Session End exists only to erase state that the Stop hook uses.
  Evidence: `assets/hooks/session_end.py` calls only `remove_baseline()`.
- Observation: The documented test command can create compiled hook files before installation.
  Evidence: Removal review pass 1 found that recursive copy preserved obsolete files under `assets/hooks/__pycache__`.

## Decision Log

- Decision: Remove the toolkit-owned Stop and Session End hooks.
  Rationale: The installed agent instructions already require review. The user monitors missed reviews and rejected more Stop-hook complexity.
  Date/Author: 2026-08-14 / user
- Decision: Preserve old hook names as uninstall identifiers.
  Rationale: Reinstallation must remove toolkit-owned entries from earlier versions without changing unrelated hooks.
  Date/Author: 2026-08-14 / Codex
- Decision: Use version `0.10.0`.
  Rationale: Removing an installed hook is a breaking change before version 1.0.0.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

CPK-014 is complete. The toolkit installs only Session Start. Reinstallation replaces the hook directory and preserves unrelated configured handlers. Removal review pass 1 found one compiled-file cleanup defect. The correction is complete. All 25 tests pass. Python compilation, Session Start JSON, shell syntax, diff, and manifest checks pass. Fresh removal review pass 2 was clean after fixes. Publication is authorized. PR mode is off, so the reviewed branch will be pushed without a pull request or merge.

## Context and Orientation

The task uses branch `cpk-014-stop-doc-commit`. Its base branch is `main`, and its base commit is `3546f98923dd9784b5a512456a17088c9867d0e2`. The isolation form is a normal branch in the existing checkout. The target toolkit version is `0.10.0`.

`kit.py` copies hook scripts into the toolkit install directory and manages entries in `$CODEX_HOME/hooks.json`. `HOOK_HANDLER_BASENAMES` identifies toolkit-owned handlers from current and old versions. `install_hooks()` removes those entries before it adds current handlers.

`assets/hooks/session_start.py` injects the compact working agreement. It also saves Git state for `assets/hooks/stop_gate.py`. `assets/hooks/session_end.py` removes that state. If Stop gating is removed, the saved state and Session End cleanup have no remaining reader.

`tests/test_kit.py` contains direct Stop-hook behavior tests. It also contains installer tests that can prove upgrade cleanup and preservation of unrelated configuration.

The supported model has one personal user and one Codex writer on a normal local filesystem. Agent instructions require review for code and configuration changes. The user observes the agent workflow.

## Normal-Use Behavior Floor

A fresh install adds the toolkit-owned Session Start hook. It does not add a Stop or Session End hook.

A reinstall removes old toolkit handler entries and obsolete hook files. It preserves unrelated handlers in the same hook events.

Session Start continues to inject the compact working agreement. It does not create per-session Git state.

The doctor command passes only when Session Start is installed and obsolete toolkit hooks are absent.

## Scope Ceiling

Do not weaken or remove review rules from agent instructions, skills, ExecPlan rules, or documentation. Do not add a replacement reminder, a configuration switch, telemetry, or persistent state. Do not change RepoWise or its separate Git `post-commit` hook. Do not change unrelated user hook entries.

## Plan of Work

In `kit.py`, keep all old toolkit hook names for ownership detection. Install only `session_start.py`. Remove obsolete scripts from an existing install directory. Make the doctor reject obsolete toolkit handlers.

Make `assets/hooks/session_start.py` emit its fixed context without shared state helpers. Delete `assets/hooks/hook_common.py`, `assets/hooks/stop_gate.py`, and `assets/hooks/session_end.py`.

Delete direct Stop behavior tests from `tests/test_kit.py`. Add one installer test that begins with toolkit-owned old hooks and an unrelated Stop handler. Reinstall the toolkit. Prove that only the unrelated Stop handler and the current Session Start handler remain. Prove that obsolete script files are absent.

Remove current Stop-hook behavior from `README.md` and `docs/OPERATING-MANUAL.md`. Keep historical version documents unchanged. Update the installation prompt and version owners to `0.10.0`. Regenerate `MANIFEST.sha256` after all tracked content is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-014-stop-doc-commit`.

Run:

    python3 -m unittest tests.test_kit.InstallerTests.test_reinstall_removes_stop_hooks
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record current results in `.agent/test-results/cpk-014-stop-doc-commit.md`. Keep CPK-014 Active and mark validation complete with review pending. Finalize documentation before one fresh read-only adversarial review.

## Validation and Acceptance

The focused check must fail if installation adds a Stop or Session End hook. It must fail if reinstallation keeps an obsolete toolkit handler or removes an unrelated handler.

The full suite must pass. Python compilation, shell syntax, diff, and manifest checks must pass.

## Idempotence and Recovery

Installation removes owned hook entries before it adds Session Start. Repeated installation gives the same managed hook configuration. If an operation fails, stop and report it. Do not retry or repair state.

## Artifacts and Notes

Preserve the existing untracked `.mcp.json`, `.repowise/`, and `.vscode/` paths. Do not stage `.agent/test-results/`.

## Interfaces and Dependencies

No new dependency or public command is required. `$CODEX_HOME/hooks.json` keeps the current Codex hook format. The toolkit installs only `assets/hooks/session_start.py`.

Revision note: Replaced the stopped commit-classification design after the user chose to remove Stop gating.

Revision note: Updated after implementation, validation, documentation maintenance, and the ready-for-review roadmap transition.

Revision note: Updated after removal review pass 1 to replace the installed hook directory with one Session Start file.

Revision note: Updated after clean removal review pass 2 to record review closure and publication status.

Revision note: Updated before commit to record authorized direct branch publication with PR mode off.

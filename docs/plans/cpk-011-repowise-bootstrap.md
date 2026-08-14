# Make RepoWise self-starting and self-updating

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must stay current while work proceeds. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, installing Codex Practical Kit makes RepoWise available in every Git repository opened by Codex. The first MCP start creates a deterministic local wiki when necessary, installs RepoWise's post-commit hook, and then serves the query tools. A commit starts a background update so the wiki follows the repository without a manual command.

## Progress

- [x] (2026-08-14 01:31Z) Reproduced MCP cancellation and proved that `default_tools_approval_mode = "approve"` permits a RepoWise tool call.
- [x] (2026-08-14 01:31Z) Confirmed RepoWise 0.41.0 has no MCP auto-initialization option and that `--yes` skips its Git hook prompt.
- [x] (2026-08-14 01:31Z) Activated CPK-011 and created this ExecPlan.
- [x] (2026-08-14 01:43Z) Implemented dependency bootstrap and global MCP ownership.
- [x] (2026-08-14 01:43Z) Implemented automatic initialization, Git hook installation, project opt-out, and diagnostics.
- [x] (2026-08-14 01:43Z) Added focused tests and completed required validation with 23 passing tests.
- [x] (2026-08-14 01:43Z) Completed local installation, a fresh Codex tool call, automatic initialization, and post-commit trigger checks.
- [x] (2026-08-14 01:43Z) Updated durable documentation, version metadata, the manifest source list, and roadmap state for the final review candidate.
- [x] (2026-08-14 01:46Z) Completed the required fresh adversarial review. Pass 1 was clean.

## Surprises & Discoveries

- Observation: RepoWise starts and completes the MCP handshake, but Codex cancels its first unannotated tool before dispatch.
  Evidence: A fresh `codex exec` failed until the server received `default_tools_approval_mode = "approve"`; the same call then completed.
- Observation: Non-interactive `repowise init --yes` intentionally skips the post-commit hook.
  Evidence: RepoWise 0.41.0 returns early from `offer_hook_install` when `yes` is true, so the kit must call `repowise hook install` explicitly.
- Observation: RepoWise's generated hook needs a persistent `repowise` command on `PATH`; `uvx` alone is insufficient.
  Evidence: With `repowise` removed from `PATH`, `uv run repowise --version` fails with `No such file or directory`.
- Observation: Regular-expression replacement interpreted the generated TOML string's escaped newlines as real line breaks.
  Evidence: The first live reinstall made Codex reject `.codex/config.toml`; a callable replacement preserved the escapes, and both configuration files now parse as TOML.

## Decision Log

- Decision: Configure one user-level RepoWise MCP server and keep project configuration only for explicit setup and opt-out.
  Rationale: A project-local server cannot initialize a repository before that repository has configuration, while user-level configuration is present on the first Codex start.
  Date/Author: 2026-08-14 / Codex and user
- Decision: Use RepoWise's own marker-delimited post-commit hook and background update path.
  Rationale: It preserves unrelated hooks and already provides queue markers, logging, and single-flight updates.
  Date/Author: 2026-08-14 / Codex and user
- Decision: Install pinned RepoWise as a persistent uv tool when no matching command exists.
  Rationale: The generated Git hook resolves `repowise` from `PATH`; an ephemeral `uvx` invocation cannot satisfy that runtime contract.
  Date/Author: 2026-08-14 / Codex
- Decision: Set RepoWise's Codex default tool approval mode to `approve`.
  Rationale: Codex canceled the first unannotated RepoWise call before dispatch. The setting makes the pinned server usable without an approval interruption.
  Date/Author: 2026-08-14 / Codex and user

## Outcomes & Retrospective

The final candidate installs missing runtime tools, configures RepoWise globally, initializes repositories on first use, and maintains the wiki after commits. Twenty-three tests, syntax checks, live installation, a fresh Codex tool call, and a temporary-repository hook check pass. A shared marker replacement defect found during live installation was fixed before the final candidate. Fresh adversarial review pass 1 found no supported normal-use correctness defect.

## Context and Orientation

`kit.py` owns core installation, project setup, removal, diagnostics, and the generated Codex MCP configuration. `tests/test_kit.py` exercises those paths with temporary Git repositories. Repository documentation under `docs/` and the root README describe installation and removal. RepoWise is pinned to 0.41.0. Its `hook install` command adds only a marker-delimited block to `.git/hooks/post-commit` and preserves other content.

## Plan of Work

Extend the existing installer helpers instead of adding a second installer. Resolve a matching `repowise` command first. If necessary, resolve or install pinned uv 0.12.4, use `uv tool install repowise==0.41.0`, and update the user's shell path. Record the exact runtime paths in the install manifest.

Add one managed RepoWise table to the user Codex configuration. Its command starts a small POSIX bootstrap generated by the kit. The bootstrap resolves the Git root, creates a no-prose index if `.repowise` is absent, calls `repowise hook install`, and finally replaces itself with `repowise mcp`. It sends setup output to stderr so MCP stdout contains only protocol messages. It skips initialization outside Git.

Keep `setup-repo` as the eager and migration path. Make it install the Git hook even when the index already exists. Make `remove-repo` uninstall RepoWise's hook, preserve unrelated hook content, and write a project `enabled = false` override so the global server does not recreate the index. Update `doctor` for the global configuration and hook state.

Update the authoritative installation and RepoWise documentation, third-party records, version metadata, and checksum manifest. Preserve the unrelated CPK-002 changes already in the working tree.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit`.

Run the focused suite and syntax checks:

    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh

Install the final candidate and check this repository:

    ./install.sh --repo .
    ./doctor.sh --repo .

Start a fresh non-interactive Codex process and require one RepoWise `list_repos` call to complete. Exercise automatic initialization and post-commit maintenance in a temporary Git repository, then remove that temporary data.

## Validation and Acceptance

The existing test suite and Python compilation must pass. New tests must prove existing dependency reuse, missing dependency installation, checksum rejection, managed global configuration, initialization before MCP startup, hook installation for new and existing indexes, project opt-out, and marker-preserving hook removal.

Acceptance requires a fresh Codex process to complete a RepoWise tool call without cancellation. A temporary repository must gain `.repowise` and the RepoWise post-commit marker automatically. After a later commit, RepoWise state or its update log must show that the hook targeted the new commit. Unrelated post-commit content must remain before and after removal.

## Idempotence and Recovery

Installation, setup, hook installation, and removal are repeatable. Each operation makes one attempt and stops on failure. The task does not add retries, rollback, corrupt-index repair, submodule handling, or custom concurrency control. RepoWise owns concurrency inside its background updater.

## Artifacts and Notes

Detailed command results belong in `.agent/test-results/cpk-011-repowise-bootstrap.md`, which is ignored by Git. Do not stage it.

## Interfaces and Dependencies

The public commands remain `install`, `setup-repo`, `remove-repo`, `repowise-update`, and `doctor`. Core installation now enables RepoWise globally. `remove-repo` becomes the per-repository opt-out. The implementation uses only Python's standard library, Git, POSIX `sh`, pinned uv 0.12.4, and pinned RepoWise 0.41.0.

Revision note: Created from the accepted Plan Mode result and revised to require RepoWise's post-commit wiki updater.

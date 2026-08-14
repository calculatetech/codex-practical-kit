# Codex Practical Kit

Codex Practical Kit installs a small working agreement for personal repositories. It favors direct code, clear documentation, and bounded review.

Version `0.11.0` makes the RepoWise code graph a required part of Codex startup.

## Operating model

The default model has one user and one Codex writer. It uses normal local filesystems and Git.

The toolkit uses these rules:

- Use true or false comparisons.
- Attempt an operation once.
- If the operation fails, stop and report the error.
- Add exceptional behavior only when the active task requires it.
- Do not design for I/O faults, permissions, links, concurrency, interruption, retry, recovery, submodules, or outside influence by default.

## Included skills

- `ponytail` keeps code small.
- `simple-english` keeps prose clear.
- `design-preflight` defines the normal-use floor and scope ceiling.
- `research-first` checks current evidence for costly choices.
- `docs-maintainer` keeps existing documentation true.
- `roadmap-maintainer` owns `docs/roadmap.md` lifecycle changes.
- `adversarial-review` runs one supported-model correctness review per pass.

The kit also installs a Session Start hook.

## Install

Run:

```bash
./run-tests.sh
./install.sh
./doctor.sh
```

The installer copies each skill to `~/.agents/skills/`. These copies belong to the toolkit. Do not edit them directly.

The installer also adds managed blocks to `~/.codex/AGENTS.md` and `$CODEX_HOME/config.toml`. The compact agent block puts role boundaries first and stays below 100 lines. The installer preserves profile text outside its markers. The `config.toml` block contains the Session Start hook.

The installer uses an existing `uv` command. If `uv` is absent, it installs pinned uv 0.12.4 from a verified upstream script. It then installs pinned RepoWise 0.41.0 as a persistent uv tool when necessary.

An existing unrecorded skill directory is a conflict. Ownership applies only in the skill directory recorded by the install manifest. The installer stops before it changes a conflicting skill. Move or remove the conflict, then run the installer again.

Version `0.4.0` removes the obsolete Task Brief skill when the prior toolkit manifest owns it.

The installer also writes `$CODEX_HOME/PLANS.md`. This file is the default ExecPlan model for repositories that do not contain `.agent/PLANS.md`.

Open a new Codex session after installation. Use `/hooks` to review and trust the Session Start command.

## Normal workflow

For a small change:

```text
read the real path
  -> fix the shared cause
  -> run a focused check
  -> finalize documentation and mark the roadmap ready for review
  -> run one fresh supported-model review
  -> record review closure
  -> commit
```

Use Design Preflight for multi-file changes, public interfaces, persistent product state, external services, or unclear ownership.

Use one ExecPlan for complex features, multi-file changes, and significant refactors. Store it in `docs/plans/`.

Use the repository's `.agent/PLANS.md` when present. Otherwise, use `$CODEX_HOME/PLANS.md`. Merge accepted Plan Mode and Design Preflight decisions into the ExecPlan.

Keep `main` for bounded documentation, comments, formatting, and roadmap updates. Use a task branch for one writable implementation stream. Use a worktree for independent writable streams, multiple implementation agents, or a main checkout that cannot switch safely.

Task implementation permits coherent local checkpoint commits on the isolated branch. It does not authorize publication or cleanup.

## Material decisions

A material decision changes scope, architecture, authority, exposure, or the delivered result.

Before Codex requests direction, it states the trigger, likelihood, current exposure, practical options, effects, and one recommendation. It defines unfamiliar terms before use.

Routine facts, values, status questions, and minor preferences stay concise. Codex investigates discoverable facts instead of asking the user for them.

## Pull request publication

PR mode is active only when `main` protection requires pull requests, required CI checks, and resolved conversations. CI workflows must supply every required check.

If PR mode is off, use direct integration. Branch push and merge to `main` need separate authorization.

If PR mode is active, use a pull request for every change. One `publish` request authorizes the path through squash merge and integration verification.

Required CI and the Codex thumbs-up reaction must apply to the latest head. Requested changes or unresolved conversations block merge. Cleanup always needs separate authorization.

## Version policy

Start initial development at `0.1.0`. Use `0.MINOR.PATCH` during initial development. Version `1.0.0` is the first production-ready release.

Features and pre-1.0 breaking changes increment the minor number. Bug fixes and published same-feature checkpoints increment the patch number. Local checkpoint commits do not change the version.

Do not add alpha or beta suffixes by default. Use them only for public testing of a specific target version. Publish normal `0.x` versions as full GitHub releases so GitHub can identify the latest release.

The source uses version `X.Y.Z`. Its Git tag uses `vX.Y.Z` and identifies the exact integrated commit. A version is consumed when its tag reaches GitHub.

## Supported-model review

Every finding must pass four checks:

1. The trigger occurs during supported normal use.
2. The project controls the trigger and result.
3. Current code reproduces the wrong result without fault injection.
4. The result violates an explicit requirement.

Drop the finding when any answer is false. Do not record it as residual risk.

Each pass uses one fresh read-only reviewer. Fix every validated in-scope finding. Only implementation defects advance the three-defect breaker. Documentation and review-housekeeping findings remain actionable, but they neither increment nor reset the three-defect count. The third consecutive counted implementation-defect pass stops for human direction.

## Documentation order

Finalize documentation before review and commit. Never make a documentation change after the task commit.

If `docs/roadmap.md` exists, it is the human source of truth. Record accepted work before implementation. Make the task Active before the first implementation edit. Update it at every scope or state change.

After validation, keep the task Active and mark it ready for review. After a clean review, record review closure and move the task to its terminal section. Review closure does not require another review.

Repository-root `docs/` contains prose and static documentation assets. Put source, scripts, build files, and configuration with their runtime owner.

## Plan Mode

Plan Mode is read-only. Inspect the repository and define the implementation. Do not edit tracked files, stage, commit, publish, or activate roadmap work.

After Plan Mode ends, reread the repository and roadmap. Activate the accepted task before implementation.

For ExecPlan work, put the accepted Plan Mode result into the task ExecPlan after Plan Mode ends.

## RepoWise

The core install requires RepoWise for Git repositories. If Codex starts in a completely empty folder, the MCP command initializes Git first. It does not initialize Git in a non-empty folder.

On the first start, the managed MCP command creates a no-prose `.repowise` index when necessary. Codex waits up to 1,800 seconds for RepoWise. It does not start or resume the session without the graph.

The bootstrap installs RepoWise's `post-commit` hook. Later commits start a background wiki update.

Use eager setup when you want the index before the next Codex session:

```bash
./setup-repo.sh /path/to/repository
./doctor.sh --repo /path/to/repository
```

The setup command initializes the index, installs or refreshes the Git hook, and adds managed RepoWise blocks to repository configuration. It does not create or replace `docs/roadmap.md`.

If the index is stale, run `repowise update --no-agents` before broad exploration. If RepoWise is unavailable, stop and restore it.

Opt out one repository with:

```bash
python3 kit.py remove-repo /path/to/repository
```

This command disables the global RepoWise server in that repository and removes RepoWise's part of `post-commit`. It preserves unrelated hook content. Add `--delete-index` to remove the local `.repowise` directory too.

## Uninstall

Remove managed integrations and copied skills from the destinations recorded by the install manifest:

```bash
./uninstall.sh
```

Also remove toolkit files:

```bash
./uninstall.sh --purge
```

If the install manifest is absent, uninstall reports that the toolkit is not installed and changes nothing.

A successful uninstall removes the manifest. Running uninstall again reports that the toolkit is not installed.

If an operation fails, uninstall stops and reports the error. It does not retry, restore, or repair partial work.

Core uninstall removes the managed MCP configuration. It leaves `uv` and RepoWise installed because other tools or repositories can use them.

## Verification

Run:

```bash
./run-tests.sh
sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
git diff --check
sha256sum --check MANIFEST.sha256
```

`MANIFEST.sha256` covers the distributed files. Regenerate it only after documentation and code are final.

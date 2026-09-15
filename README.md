# Codex Practical Kit

Codex Practical Kit installs a small working agreement for personal repositories. It favors direct code, clear documentation, and bounded review.

The managed `AGENTS.md` is a small skill router. Skill descriptions keep unrelated rules out of task context.

## Included components

The kit installs the official Ponytail plugin and these task skills:

- `simple-english`
- `neuroarxiv`
- `design-preflight`
- `delivery-lifecycle`
- `repository-knowledge`
- `research-first`
- `docs-maintainer`
- `roadmap-maintainer`
- `adversarial-review`
- `defect-diagnostic`
- `publication`
- `toolkit-maintainer`
- `plan-history`

Each lifecycle skill contains its focused rule owners or links to the one skill that owns a shared rule.

## Install

Install Node.js and a Codex CLI that supports `codex plugin` before running the installer.

On macOS or Linux, run:

```bash
./run-tests.sh
./install.sh
./doctor.sh
```

On Windows, install PowerShell 7 and Python 3.11 or later. Then run:

```powershell
pwsh -File .\run-tests.ps1
pwsh -File .\install.ps1
pwsh -File .\doctor.ps1
```

The installer copies managed skills to `~/.agents/skills/`. Do not edit installed copies. Codex manages Ponytail separately as a native plugin.

The installer writes a managed block in `~/.codex/AGENTS.md`. It renders the absolute PLANS path and names installed skills.

The installer also writes `$CODEX_HOME/PLANS.md` and managed Codex hooks. Session Start announces the AGENTS router.

## Global and repository instructions

The installer manages `~/.codex/AGENTS.md` and `$CODEX_HOME/PLANS.md`. These files apply to every repository unless a nearer repository file overrides them.

A repository `AGENTS.md` can add or replace instructions for its directory tree. A repository `.agent/PLANS.md` replaces the global ExecPlan contract for that repository.

The installer does not update repository-owned instruction files. `setup-repo` only removes its obsolete managed RepoWise block from `AGENTS.md`.

Do not copy the global files into a repository.

A copied file stops receiving toolkit updates. It can conflict with newer rules.

If a repository needs an override, keep only the project-specific rule in the nearest `AGENTS.md`. Remove a generic `.agent/PLANS.md` copy to use the current global contract.

Keep a repository `.agent/PLANS.md` only when the project needs a different ExecPlan contract. You must maintain that file manually.

Prompt submission adds a Plan history reminder to Plan-mode prompts. Managed hooks save a completed Plan before the next prompt continues and at session lifecycle boundaries.

The edit hooks update `<primary-checkout>/.codex/roadmap-view.md` after an agent changes `docs/roadmap.md`. Keep this generated file open to follow worktree progress. Edit only `docs/roadmap.md`.

The [Plan history skill](assets/skills/plan-history/SKILL.md) keeps repository summaries versioned in `.agent/plan-history/`. Specification associations stay in each record. Later planning sessions find these records across worktrees and reconcile their decisions.

For large histories, agents create reusable reading summaries under `.agent/plan-history/compacted/`. Original records remain unchanged. The skill also preserves reading progress across normal context compaction.

An unrecorded destination skill is a conflict. The installer stops before it changes that directory.

Open a new Codex session after installation. Use `/hooks` to review and trust the toolkit and Ponytail commands.

## Ponytail

The installer uses the official `DietrichGebert/ponytail` marketplace and installs `ponytail@ponytail` when absent. It preserves an existing official plugin's version, settings, and enabled or disabled state.

The complete plugin provides `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, and `ponytail-help`. Its lifecycle hooks control mode activation and persistence.

In Codex, use the skill picker or `@` commands:

```text
@ponytail full
@ponytail lite
@ponytail ultra
@ponytail off
@ponytail
@ponytail default off
@ponytail-review
@ponytail-help
```

Bare `@ponytail` reports the mode. `@ponytail default off` changes the default for later sessions. The upstream plugin controls lifecycle behavior. The toolkit does not select modes.

The upstream Codex instructions use `@` commands; they do not promise a `/ponytail` slash-menu entry. See the [official Ponytail commands](https://github.com/DietrichGebert/ponytail#commands).

Use Codex's plugin manager for updates, enablement, and removal. Toolkit reinstall does not update or re-enable Ponytail.

Migration removes an old standalone Ponytail skill only when the toolkit manifest owns its destination and native installation succeeds. An unowned skill or conflicting marketplace source stops installation. Resolve that ownership conflict before retrying.

`--codex-home` selects the Codex home for installation and Doctor. Otherwise, the toolkit uses `CODEX_HOME` or `~/.codex`. Use the same home for native plugin commands.

## Rule owners

An applicable skill selects only the rules needed for its task:

- [Rule ownership](assets/skills/toolkit-maintainer/SKILL.md)
- [Coordination](assets/skills/delivery-lifecycle/references/coordination.md)
- [Supported model](assets/skills/design-preflight/references/supported-model.md)
- [Scope boundaries](assets/skills/design-preflight/references/scope-boundaries.md)
- [Decision handoffs](assets/skills/delivery-lifecycle/references/decision-handoffs.md)
- [Repository knowledge](assets/skills/repository-knowledge/SKILL.md)
- [Research First](assets/skills/research-first/SKILL.md)
- [Delivery lifecycle](assets/skills/delivery-lifecycle/references/delivery-lifecycle.md)
- [Implementation modes](assets/skills/delivery-lifecycle/references/implementation-modes.md)
- [Git isolation](assets/skills/delivery-lifecycle/references/git-isolation.md)
- [Plan history](assets/skills/plan-history/SKILL.md)
- [Full-set results](assets/skills/design-preflight/references/full-set-results.md)
- [Owner composition](assets/skills/design-preflight/references/owner-composition.md)
- [Scenario discrimination](assets/skills/design-preflight/references/scenario-discrimination.md)
- [Review closure](assets/skills/adversarial-review/references/review-closure.md)
- [Publication](assets/skills/publication/references/publication.md)
- [Versioning](assets/skills/publication/references/versioning.md)

Skill-specific procedures remain in each skill. [ExecPlan rules](.agent/PLANS.md) remain focused on executable plans.

## RepoWise

The core install provides pinned `uv` and RepoWise when they are absent. It configures one required user-level RepoWise MCP server.

In a Git repository, the first MCP start creates the index and installs RepoWise's `post-commit` hook. Each MCP session catches up the index and watches working-tree edits without model calls. A completely empty folder becomes a Git repository. A non-empty, non-Git folder remains unchanged.

In a linked worktree, RepoWise keeps a separate index and uses Git's shared hook path. No extra setup is necessary.

On macOS or Linux, run eager setup when you need the index before the next Codex session:

```bash
./setup-repo.sh /path/to/repository
./doctor.sh --repo /path/to/repository
```

On Windows, run:

```powershell
pwsh -File .\setup-repo.ps1 C:\path\to\repository
pwsh -File .\doctor.ps1 --repo C:\path\to\repository
```

See [RepoWise notes](docs/REPOWISE.md) for setup, refresh, opt-out, and trust-boundary details.

## Uninstall

Uninstall removes toolkit-managed global integrations and copied skills. `--purge` also removes the toolkit data directory. Both retain native Ponytail resources, settings, uv, RepoWise, and Plan history.

For complete removal, follow the ordered steps below. Keep the source checkout until the removal commands finish.

### 1. Remove repository integrations

Run `remove-repo` for each repository before core uninstall. Use a normal checkout; removal stops in linked worktrees because the Git hook is shared.

On macOS or Linux:

```bash
python3 kit.py remove-repo /path/to/repository --delete-index
```

On Windows:

```powershell
python kit.py remove-repo C:\path\to\repository --delete-index
```

Omit `--delete-index` to keep that repository's `.repowise` index. Removal also clears the owned roadmap view and its Git exclusion. See [RepoWise removal](docs/REPOWISE.md#day-to-day-commands).

### 2. Remove toolkit files

On macOS or Linux:

```bash
./uninstall.sh --purge
```

On Windows:

```powershell
pwsh -File .\uninstall.ps1 --purge
```

Omit `--purge` to keep the toolkit data directory. Use the installation's `--install-root` when it differs from the default.

### 3. Optionally remove Ponytail state

Close sessions that use Ponytail. Run any upstream cleanup script before native plugin removal, because removal deletes the plugin cache.

The upstream cleanup script removes shared Ponytail configuration and Claude state, including its status-line entry. Skip it if another client needs that state.

Use `codex plugin list --marketplace ponytail --json` to find the installed version. Replace `VERSION` below with that value.

On macOS or Linux:

```bash
cpk_codex_home="${CODEX_HOME:-$HOME/.codex}"
node "$cpk_codex_home/plugins/cache/ponytail/ponytail/VERSION/scripts/uninstall.js"
rm -rf -- "$cpk_codex_home/plugins/data/ponytail-ponytail"
```

On Windows:

```powershell
$cpkCodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
node "$cpkCodexHome/plugins/cache/ponytail/ponytail/VERSION/scripts/uninstall.js"
Remove-Item -LiteralPath "$cpkCodexHome/plugins/data/ponytail-ponytail" -Recurse -Force -ErrorAction SilentlyContinue
```

If installation used `--codex-home`, set the variable to that directory instead. The upstream script does not remove Codex's plugin data; the second command removes it explicitly.

Shared configuration is `$XDG_CONFIG_HOME/ponytail/config.json` when `XDG_CONFIG_HOME` is set. Otherwise, it is `~/.config/ponytail/config.json` on POSIX or `%APPDATA%\ponytail\config.json` on Windows. Remove any `PONYTAIL_*` environment settings from your shell profile if no client needs them.

### 4. Remove the native plugin and marketplace

Set `CODEX_HOME` to the selected directory with `export CODEX_HOME="$cpk_codex_home"` on POSIX or `$env:CODEX_HOME = $cpkCodexHome` on Windows. Then run:

```text
codex plugin remove ponytail@ponytail
codex plugin marketplace remove ponytail
```

Keep the marketplace if you still use another plugin from it. Normal toolkit uninstall never runs these commands.

### 5. Optionally remove RepoWise and uv

If no repository or other tool needs RepoWise, run this command in either shell:

```text
uv tool uninstall repowise
```

If no other tool needs uv, follow [uv's uninstall procedure](https://docs.astral.sh/uv/getting-started/installation/#uninstallation). Use `uv cache dir`, `uv python dir`, and `uv tool dir` to locate shared data before removing uv. `uv cache clean` clears its cache. Remove managed Python and tool directories only if you intend to remove those other installations too.

For uv installed in the default user bin directory, remove its executables on POSIX:

```bash
rm -f -- "$HOME/.local/bin/uv" "$HOME/.local/bin/uvx"
```

On Windows:

```powershell
Remove-Item "$HOME/.local/bin/uv.exe", "$HOME/.local/bin/uvx.exe", "$HOME/.local/bin/uvw.exe" -Force -ErrorAction SilentlyContinue
```

For a custom or package-managed uv installation, use its actual location or package manager. The toolkit does not install Node.js or Codex.

### 6. Review retained files

Plan history remains in repository `.agent/plan-history/` directories and the `$CODEX_HOME/plan-history/` fallback. Keep versioned records for future work, or remove them deliberately in each repository and commit that deletion.

Repository-owned `AGENTS.md`, `.agent/PLANS.md`, roadmaps, and other project documentation remain. So do indexes and views in repositories that you did not remove in step 1. Core uninstall does not keep a repository list.

Remove the toolkit source checkout or downloaded archive only when you no longer need it. Leave unrelated Codex configuration and other plugins intact.

## Verification

On macOS or Linux, run:

```bash
./run-tests.sh
sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
git diff --check
sha256sum --check MANIFEST.sha256
```

On Windows, run:

```powershell
pwsh -File .\run-tests.ps1
git diff --check
```

`MANIFEST.sha256` covers distributed files. Regenerate it after code and documentation are final.

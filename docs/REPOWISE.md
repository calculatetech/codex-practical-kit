# RepoWise notes

RepoWise is the repository knowledge provider installed by the kit.

## What it provides

Its keyless index combines:

- A code and symbol graph.
- Git history and ownership.
- Change risk and bug history.
- Dead-code and code-health checks.
- Test-impact information.
- Generated wiki pages.
- Architectural decision evidence.
- MCP tools for Codex.

The first no-prose index does not need an API key. Higher-level prose can run through the authenticated Codex CLI subscription.

The repository skill uses exact symbols and paths before natural-language synthesis. A user-configured model provider remains available for conceptual questions.

If no model provider is configured, RepoWise still returns indexed candidates. Later questions continue through indexed search, context, and symbol tools.

## How the kit uses it

### Throughout implementation

Use RepoWise for each new repository discovery question. Design Preflight and implementation can ask for:

- The current execution path.
- Callers and dependencies.
- Ownership and decision history.
- Hidden coupling and recent bug fixes.
- Existing tests and documentation clues.

Reuse verified results that remain current. Read focused source when an edit needs wider context or the index reports approximate bounds.

### During review

Adversarial Review can use RepoWise for:

- Blast-radius leads.
- Callers outside the diff.
- Change risk.
- Co-change history.
- Impacted tests.
- Architectural decisions.

Agent evidence and review-packet rules are in [Repository knowledge](../assets/skills/repository-knowledge/SKILL.md).

## Runtime ownership

RepoWise is a large external tool and uses AGPL-3.0. The kit does not copy it, modify it, or depend on its database format.

Core installation reuses `uv` when present. If it is absent, the kit installs pinned uv 0.12.4 from a checksum-verified upstream script. Windows uses the official PowerShell installer. macOS and Linux use the official shell installer. The kit installs RepoWise 0.41.0 as a persistent uv tool when no matching command exists.

The installer adds a user-level RepoWise MCP server. If Codex starts in a completely empty folder, the server command initializes Git first. It does not initialize Git in a non-empty folder.

The first start in a Git repository initializes a no-prose index when `.repowise` is absent. Each start then installs RepoWise's marker-delimited `post-commit` hook and catches up the index.

While MCP runs, an index-only watcher collects working-tree edits and uses the RepoWise debounce period. It does not make model calls. The POSIX launcher ignores file-open and file-close events because these events are not edits. The Windows event source reports change events and does not need this filter.

The MCP configuration starts one installed Python bootstrap on all platforms. This bootstrap starts the watcher before RepoWise MCP. It stops MCP startup if the watcher stops during its readiness check.

The managed Codex configuration makes RepoWise required and approves its MCP calls. Codex waits up to 1,800 seconds for initialization.

After you install or upgrade the kit, start a new Codex session. A running session does not reload changed skills or configuration.

The hook starts a background update after each commit. RepoWise owns its queue marker, log, and single-flight update behavior. The active watcher stops when MCP stops.

Agent behavior is defined by [Repository knowledge](../assets/skills/repository-knowledge/SKILL.md).

## Day-to-day commands

On macOS or Linux, set up before the first MCP call:

```bash
python3 kit.py setup-repo .
```

Refresh:

```bash
python3 kit.py repowise-update .
```

Check:

```bash
python3 kit.py doctor --repo .
```

Opt out this repository and keep the index. This command also removes the owned roadmap view and its exclusion:

```bash
python3 kit.py remove-repo .
```

Opt out and remove the index:

```bash
python3 kit.py remove-repo . --delete-index
```

On Windows, use the same `kit.py` commands with `python`. The root launchers provide the common commands:

```powershell
pwsh -File .\setup-repo.ps1 .
pwsh -File .\doctor.ps1 --repo .
```

Core uninstall removes the global MCP block. It leaves `uv` and RepoWise installed.

## Trust boundary

Treat graph edges, health scores, generated pages, and mined decisions as evidence. Read the source for a change that can affect correctness, data, security, or public behavior.

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

## How the kit uses it

### Before implementation

Design Preflight can ask RepoWise for:

- The current execution path.
- Callers and dependencies.
- Ownership and decision history.
- Hidden coupling and recent bug fixes.
- Existing tests and documentation clues.

### During review

Adversarial Review can use RepoWise for:

- Blast-radius leads.
- Callers outside the diff.
- Change risk.
- Co-change history.
- Impacted tests.
- Architectural decisions.

Agent evidence and review-packet rules are in [Repository knowledge](../assets/skills/codex-practical-kit-rules/references/repository-knowledge.md).

## Runtime ownership

RepoWise is a large external tool and uses AGPL-3.0. The kit does not copy it, modify it, or depend on its database format.

Core installation reuses `uv` when present. If it is absent, the kit installs pinned uv 0.12.4 from a checksum-verified upstream script. The kit installs RepoWise 0.41.0 as a persistent uv tool when no matching command exists.

The installer adds a user-level RepoWise MCP server. If Codex starts in a completely empty folder, the server command initializes Git first. It does not initialize Git in a non-empty folder.

The first start in a Git repository initializes a no-prose index when `.repowise` is absent. It installs RepoWise's marker-delimited `post-commit` hook before it starts the MCP server.

The managed Codex configuration makes RepoWise required and approves its MCP calls. Codex waits up to 1,800 seconds for initialization.

The hook starts a background update after each commit. RepoWise owns its queue marker, log, and single-flight update behavior.

Agent behavior is defined by [Repository knowledge](../assets/skills/codex-practical-kit-rules/references/repository-knowledge.md).

## Day-to-day commands

Set up before the first MCP call:

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

Opt out this repository, remove RepoWise's hook block, and keep the index:

```bash
python3 kit.py remove-repo .
```

Opt out and remove the index:

```bash
python3 kit.py remove-repo . --delete-index
```

Core uninstall removes the global MCP block. It leaves `uv` and RepoWise installed.

## Trust boundary

Treat graph edges, health scores, generated pages, and mined decisions as evidence. Read the source for a change that can affect correctness, data, security, or public behavior.

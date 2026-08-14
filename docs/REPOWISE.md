# RepoWise notes

RepoWise is the recommended replacement trial for the broken CBM installation.

## Why it is worth trying

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

Every RepoWise result is an observation until source confirms it.

The review packet must record the indexed revision. A stale index cannot prove absence.

## Why it stays optional

RepoWise is a large external tool and uses AGPL-3.0. The kit does not copy it, modify it, or depend on its database format.

The Codex integration invokes the exact pinned package through `uvx`. Removal only deletes the project config block. It does not need the RepoWise executable to start.

When RepoWise fails, use Git, `rg`, language tools, tests, and direct source reads. Continue the task.

## Day-to-day commands

Set up:

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

Remove the integration, but keep the index:

```bash
python3 kit.py remove-repo .
```

Remove both:

```bash
python3 kit.py remove-repo . --delete-index
```

## Trust boundary

Treat graph edges, health scores, generated pages, and mined decisions as evidence. Read the source for a change that can affect correctness, data, security, or public behavior.

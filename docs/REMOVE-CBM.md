# Remove a broken CBM installation

Do not run the broken CBM uninstall routine first.

## Procedure

1. Close Codex sessions.
2. Search global and repository Codex files for `codebase-memory`, `codebase-memory-mcp`, and `cbm`.
3. Remove only matching MCP tables, hook handlers, plugin entries, and managed instruction blocks.
4. Run `codex mcp list`. Make sure that CBM is absent.
5. Stop a remaining CBM process.
6. Identify its package manager or plugin owner.
7. Remove the package through that owner.
8. Remove a CBM data directory only after its name and owner are clear.
9. Start a new Codex session. Run `codex mcp list` again.

## Operation handling

<!-- cpk-rule-route-only: supported-model -->
[Supported model](../assets/skills/codex-practical-kit-rules/references/supported-model.md)

## Codex prompt

```text
Remove the broken CBM integration without running its uninstall routine first.

First read assets/skills/codex-practical-kit-rules/references/supported-model.md. Inspect global and project Codex configuration, hooks, plugins, skills, AGENTS files, running processes, package records, and CBM data directories. Remove only CBM-owned entries. Preserve unrelated entries. Apply the supported-model rules. Verify with `codex mcp list` and a new Codex session. Do not install a replacement during this task.
```

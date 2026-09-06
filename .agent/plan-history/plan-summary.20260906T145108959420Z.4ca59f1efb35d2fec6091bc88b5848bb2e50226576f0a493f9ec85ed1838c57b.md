<proposed_plan>
# CPK-055 — Install and preserve the official Ponytail plugin

## Summary

Replace the toolkit’s partial Ponytail installation with the official Codex plugin. Preserve all six skills, lifecycle hooks, mode controls, and persistent defaults.

Codex invokes these capabilities through its skill interface, including `@ponytail-review`. The upstream documentation does not promise a `/ponytail` slash-menu entry. [Ponytail documentation](https://github.com/DietrichGebert/ponytail#commands)

The plugin and user selections will control Ponytail modes. The toolkit will stop changing them during planning, implementation, or review.

## Implementation

**CP1 — Remove toolkit mode overrides**

- Remove the Ponytail implementation route from the managed AGENTS block.
- Remove automatic normal/full selections from the lifecycle instructions. Retain the existing test-scope and challenger-reasoning requirements.
- Remove the `normal mode` output from the managed prompt hook. Preserve Plan capture, its planning reminder, and other hook behavior.
- Update the corresponding instruction and installed-hook tests, then review and commit this checkpoint.

**CP2 — Use native plugin installation**

- Extend `kit.py` to inspect and install Ponytail through native Codex plugin commands:
  - `codex plugin marketplace add DietrichGebert/ponytail`
  - `codex plugin add ponytail@ponytail`
- Install only when absent. Preserve an existing official plugin’s version, settings, and enabled or disabled state.
- Honor the selected Codex home for inspection, installation, and diagnostics.
- Check Node.js and native plugin-command support before changing an existing installation. Report missing prerequisites directly.
- Treat a conflicting marketplace source or unowned standalone Ponytail skill as an installation conflict.
- Retire the old copied skill only when the previous toolkit manifest owns it and native installation succeeds.
- Update Doctor to check the native plugin and Node.js. Report a user-disabled plugin without re-enabling it.
- Remove Ponytail from the copied-skill dependency list. Keep plugin updates and removal under Codex’s plugin manager.
- Update installation documentation, third-party declarations, and checksums. Review and commit this checkpoint.

## Full-removal documentation

Document what normal uninstall and `--purge` remove, plus the additional steps for complete removal:

1. Remove repository integrations and generated views before removing the toolkit.
2. Purge toolkit-owned files.
3. Perform optional Ponytail state cleanup before deleting its plugin cache.
4. Remove the plugin with `codex plugin remove ponytail@ponytail`, then remove its marketplace.
5. Remove RepoWise with `uv tool uninstall repowise`. Document optional `uv` cleanup when other tools no longer need it.
6. Identify retained Plan history, project indexes, and shared settings, with explicit cleanup choices.

Include POSIX and Windows instructions. Account for Codex’s Ponytail data directory: the upstream cleanup script does not remove that state.

## Validation

- Prove fresh installation exposes all six skills and the declared hooks through a real isolated Codex installation.
- Exercise install → reinstall → uninstall and purge. Native plugin resources and user settings must remain intact.
- Contrast owned and unowned legacy skills, official and conflicting marketplaces, and selected versus default Codex homes.
- Test missing Node.js and missing plugin-command support separately. Both must preserve the previous installation before reporting failure.
- Exercise installed hooks with Plan and ordinary prompts. Confirm preserved history behavior and no toolkit mode directives.
- Check documented mode switching, off, status, persistent defaults, and lifecycle behavior using isolated plugin state.
- Run the full toolkit suite, required trace verification, checkpoint reviews, and final native review. Then update the host and run Doctor.

## Decisions and reconciliation

Use one CPK-055 ExecPlan and two reviewed checkpoints. No custom command aliases, Ponytail fork, mode storage, or automatic hook trust will be added.

The user’s plugin-only mode choice supersedes the mode-selection requirements in CPK-028 and CPK-029. Preserve their historical records and unrelated requirements.

Native Ponytail installations remain after toolkit uninstall, as selected. Publication remains a separate step.

<!-- cpk-plan-spec: docs/plans/cpk-028-phase-scoped-minimalism.md -->
<!-- cpk-plan-spec: docs/plans/cpk-029-plan-mode-hook.md -->
</proposed_plan>
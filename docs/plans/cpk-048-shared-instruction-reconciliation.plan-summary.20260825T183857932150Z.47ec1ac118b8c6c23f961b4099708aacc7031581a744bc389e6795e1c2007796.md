<proposed_plan>
# CPK-048 — Reconcile Shared Agent and Plan Instructions

## Summary

The toolkit correctly updates global `AGENTS.md` and `PLANS.md`, but it never updates repository-owned copies. Twenty-five older project copies therefore override the current checkpoint rules.

Keep one canonical Plan contract. Do not add a migrator, Doctor warning, new skill, or duplicate checkpoint rule. Document the precedence, remove obsolete copies from eligible projects, and preserve deliberate project-specific rules.

Keep version `0.23.2` because it has not been published.

## CP1 — Document the Shared Contract

- Add CPK-048 to the current unpublished branch and roadmap.
- Update the README in Simple English:
  - The installer-managed `AGENTS.md` and `PLANS.md` apply across repositories.
  - Repository `AGENTS.md` and `.agent/PLANS.md` files take priority.
  - The installer and `setup-repo` never update repository-owned instruction files.
  - Do not copy the global Plan contract into projects.
  - Remove generic local Plan copies to inherit future toolkit updates.
  - Keep only deliberate, focused project overrides in the nearest applicable `AGENTS.md`.
- Leave the canonical checkpoint rules in `.agent/PLANS.md`.
- Make no installer, runtime, skill, public-interface, or version change.
- Validate the documentation and run one native checkpoint review before the local toolkit commit.

## CP2 — One-Time `~/Projects` Audit

- Inventory instruction files again immediately before editing. Fetch each distinct Git remote once.
- For remote-backed repositories, require the working branch to contain the current upstream head. Fast-forward only clean, non-divergent branches. Do not stash, reset, rebase, or overwrite unrelated work.
- Exclude the toolkit’s canonical `.agent/PLANS.md`.
- Ignore these dirty historical Meridian worktrees entirely:
  - `meridian-task-063e`
  - `meridian-task-063e-rebuild`
  - `meridian-task-063f`
  - `meridian-task-063f-rebuild`
  - `meridian-task-084a2`
- Audit Meridian `main` and the three clean task worktrees separately. Fetch the shared remote only once.

For each eligible project:

- Archive every untracked or non-Git Plan copy, with its original path and SHA-256 hash, under `~/.local/share/codex-practical-kit/audits/cpk-048/`.
- Remove obsolete `.agent/PLANS.md` copies. Tracked copies remain recoverable from Git; archived copies remain recoverable from the audit directory.
- Preserve Meridian’s production-complete checkpoint requirement in its root `AGENTS.md` before removing its customized Plan copy.
- Remove stale generic planning, review, progress, coordination, and publication rules from project `AGENTS.md` files.
- Preserve project-specific product, security, compatibility, build, versioning, release-evidence, and human-approval rules at their existing scope.
- Remove every reference to a deleted local Plan file. Do not copy toolkit lifecycle or checkpoint rules into another local owner.
- Create a documentation branch in each independent repository. Use existing clean Meridian task branches.
- Stage only `AGENTS.md` and `.agent/PLANS.md`, run one native instruction/configuration review, and create one local commit. Do not push or increment project versions.
- Stop only the affected repository if it has divergence, unexpected tracked changes, newer conflicting remote instructions, or an uncertain project-specific rule. Continue the read-only audit of other repositories and report the blocked repository.

## Validation and Publication

- Confirm the initial inventory: 25 stale Plan copies outside the toolkit.
- Expect 20 eligible copies to be removed. The five excluded dirty Meridian worktrees remain unchanged and must be reported.
- Confirm eligible repositories contain no stale `.agent/PLANS.md` routes or copied toolkit lifecycle rules.
- Confirm every Git commit changes only approved instruction paths and contains its refreshed upstream where applicable.
- Confirm no external repository was pushed.
- Run the complete toolkit checks and one final native review of the full toolkit candidate.
- Apply review closure, install the reviewed toolkit into the live environment, and require Doctor to report `Result: ready`.
- Resume publication of toolkit version `0.23.2` through the existing CPK-047 publication gates. External audit commits remain local.

## Prior Plan Reconciliation

- CPK-042 is carried. Semantic checkpoint guidance remains single-owned by the canonical Plan contract.
- The final CPK-047 Plan is carried. Its completed checkpoints and publication rules remain unchanged.
- CPK-048 is a new corrective task on the existing unpublished branch. It does not rewrite earlier checkpoint commits.

<!-- cpk-plan-spec: docs/plans/cpk-048-shared-instruction-reconciliation.md -->
</proposed_plan>
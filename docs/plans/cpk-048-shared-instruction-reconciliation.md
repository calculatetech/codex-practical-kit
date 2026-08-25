# Reconcile shared agent and Plan instructions

This ExecPlan is the durable CPK-048 implementation specification. Maintain it according to `.agent/PLANS.md`.

## Purpose

The toolkit installs global agent and ExecPlan instructions. Repository files can override those instructions, but the installer does not update repository-owned files.

Older repositories contain copied Plan contracts and generic lifecycle rules. Those copies can hide current checkpoint guidance or conflict with maintained skills.

Correct the documentation and the eligible projects before publication of version `0.23.2`.

## Product boundary

[ExecPlan rules](../../.agent/PLANS.md) remain the only shared Plan contract. [Rule ownership](../../assets/skills/toolkit-maintainer/SKILL.md) prevents duplicate toolkit owners. [Git isolation](../../assets/skills/delivery-lifecycle/references/git-isolation.md) protects user work during the project audit.

The task adds no migrator, Doctor check, skill, runtime behavior, dependency, or version change. Repository-specific product, build, security, and release rules remain in their nearest `AGENTS.md` file.

## Decisions

- Document the global instruction scope and repository override priority in the README.
- Remove generic repository Plan copies instead of maintaining duplicate contracts.
- Preserve Meridian's production-complete checkpoint rule in its root `AGENTS.md`.
- Remove only generic toolkit lifecycle rules from project `AGENTS.md` files.
- Archive untracked and non-Git Plan copies before removal.
- Ignore the five dirty Meridian worktrees that the user identified as historical artifacts.
- Create local documentation commits in eligible Git repositories. Do not push them.
- Keep toolkit version `0.23.2` because its tag has not reached GitHub.

## Checkpoints

### CP1 — Document shared instruction precedence

Update the README. Explain the global files, repository override priority, manual maintenance boundary, and safe removal of generic copies.

Run documentation checks and one checkpoint native review. Create one local toolkit checkpoint commit.

### CP2 — Reconcile eligible projects

Work from `/home/mbeutler/Projects`. Inventory Plan copies with:

    find /home/mbeutler/Projects -path '*/.agent/PLANS.md' -type f -print | sort

Before edits, this command must show the toolkit file and 25 copies. Exclude these five dirty Meridian worktrees:

- `meridian-task-063e`
- `meridian-task-063e-rebuild`
- `meridian-task-063f`
- `meridian-task-063f-rebuild`
- `meridian-task-084a2`

Refresh each distinct Git remote once with `git fetch --prune`. Operate only when `git status --short` shows no unexpected tracked change. Fast-forward a clean selected base branch with `git merge --ff-only @{upstream}`. Then require `git merge-base --is-ancestor @{upstream} HEAD` to succeed. Use the `cpk-048-instruction-reconciliation` branch in independent repositories. Use the existing branch in each eligible Meridian worktree.

Archive each untracked or non-Git Plan copy under `/home/mbeutler/.local/share/codex-practical-kit/audits/cpk-048/`. Preserve its path relative to `/home/mbeutler/Projects`. Record its SHA-256 value before removal. Run `sha256sum` on the source and archive. Both values must match.

Remove 20 eligible generic Plan copies. Move real project rules to the nearest `AGENTS.md`, then remove stale generic lifecycle text. Run the inventory command again. It must show only the toolkit file and the five excluded worktree files.

In each Git candidate, stage only `AGENTS.md` and `.agent/PLANS.md`. Run `git diff --cached --check`; it must produce no output. Create a synthetic commit from the staged tree, then run `codex review --commit <synthetic-commit>`. If the review has no applicable finding, create one local documentation commit. Preserve unrelated untracked files. Do not push external repositories.

From `/home/mbeutler/Projects/codex-practical-kit`, run:

    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

The test command must report success. The other commands must produce no error. Run one final native review of the complete toolkit candidate. Apply review closure, run `./install.sh`, then run `./doctor.sh`. Doctor must report `Result: ready`. Continue toolkit publication only after these results.

## Validation

- Confirm that the toolkit still has one canonical `.agent/PLANS.md`.
- Confirm that 20 eligible copied Plan files are removed and five dirty Meridian worktrees remain unchanged.
- Confirm that archived files have matching SHA-256 values.
- Confirm that eligible `AGENTS.md` files contain no stale local Plan route or copied toolkit lifecycle rule.
- Confirm that external commits change only `AGENTS.md` and `.agent/PLANS.md`.
- Run the complete toolkit test, syntax, link, manifest, and diff checks.
- Install the reviewed toolkit and require Doctor to report `Result: ready`.

## Prior Plan reconciliation

Record: `.agent/plan-history/plan-summary.20260823T052048899607Z.c539b46a7e5fa56092a382fef046fd00d4271c42c4fda8e0f0e2216ce94df122.md`

Status: carried

Reason: CPK-042 remains authoritative for semantic checkpoints and final native review.

Record: `.agent/plan-history/plan-summary.20260825T173129857080Z.a3ee26a1802fb85c5a0a100ccb3c33c1a6fff358bd20b65636adc61f8d0de377.md`

Status: carried

Reason: The final CPK-047 publication and integration rules remain authoritative.

Record: `.agent/plan-history/plan-summary.20260825T183857932150Z.47ec1ac118b8c6c23f961b4099708aacc7031581a744bc389e6795e1c2007796.md`

Status: carried

Reason: This record is the accepted CPK-048 implementation contract.

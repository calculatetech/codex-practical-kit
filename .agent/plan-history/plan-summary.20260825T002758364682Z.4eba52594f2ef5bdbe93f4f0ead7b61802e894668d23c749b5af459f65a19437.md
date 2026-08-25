<proposed_plan>
# CPK-046 — RepoWise Worktree Recovery

## Damage assessment

- Preserve `8a0b82e`; it is valid repository-local work. Local `main`, `origin/main`, the live toolkit, and the shared Git hook all remain unchanged.
- No damaged work was committed or published. The rejected work is confined to `task/cpk-046-repowise-worktree-bootstrap` and its worktree.
- The staged candidate adds duplicate repository ownership logic, redirects linked worktrees to the primary checkout, introduces an undocumented Git 2.31 requirement, and leaves version `0.23.0` unchanged. Delete it rather than salvage it.
- The foreign session also created `/tmp/.git` and `/tmp/.codex`. `/tmp/.git` caused Plan History to mistake temporary directories for repositories; the assessment then generated `/tmp/.agent`.
- Unreachable review objects are harmless and can expire through normal Git maintenance.

## Checkpoint 1 — Containment and authority

- Record the incident evidence in ignored test-results storage. Then remove the rejected worktree, its branch, the three verified `/tmp` marker directories, and the named assessment temp repositories and logs. Report that the discarded staged work is not recoverable.
- Create `cpk-046-repowise-worktree-recovery` from `8a0b82e`. Do not modify tracked files on `main`.
- Add one canonical Delivery Lifecycle rule: failures in shared tooling, dependencies, live installations, or other repositories authorize read-only diagnosis only. Agents must obtain explicit user authority before modifying another repository.
- Change Repository Knowledge’s ambiguous “restore the code graph” instruction to route to that authority owner and stop with a portable diagnostic when in-scope recovery fails.
- Add a focused rule-owner test that blocks duplicate cross-repository authority rules.
- Add a Design Preflight exemption for strict simplifications: no independent challenger is required when the correction deletes or rejects the starting design, uses an existing upstream/native capability, and adds no interface, persistent state, or broader behavior.
- Review this checkpoint once and commit it separately.

## Checkpoint 2 — Minimal RepoWise correction

- Upgrade the owned RepoWise installation from `0.41.0` to `0.45.0` and bump the toolkit bugfix version from `0.23.0` to `0.23.1`.
- Permit an in-place forced upgrade only when the outdated executable is the exact toolkit-owned path recorded by the install manifest. Continue rejecting unowned or differently located installations.
- Pass the actual linked-worktree root to RepoWise. RepoWise 0.45 already creates a separate worktree index, seeds it from the base checkout, and leaves the base unchanged. Do not add the rejected primary-checkout resolver. [RepoWise worktree guidance](https://github.com/repowise-dev/repowise/blob/main/docs/scale/WORKTREES.md), [RepoWise changelog](https://github.com/repowise-dev/repowise/blob/main/docs/CHANGELOG.md)
- Make Doctor resolve the shared hook directory with `git rev-parse --git-path hooks`. Do not use `--path-format`. Git defines hooks as common worktree data and runs them from the active working tree. [Git hooks](https://git-scm.com/docs/githooks), [Git repository layout](https://git-scm.com/docs/gitrepository-layout)
- Reject `remove-repo` from a linked worktree before any mutation because uninstalling its shared hook would disable sibling worktrees. Keep ordinary-checkout removal unchanged.
- Preserve the existing watcher compatibility patch, keyless operation, empty-directory behavior, and Windows launcher repair.
- Update the dependency lock, license declaration to `AGPL-3.0-or-later`, documentation, roadmap, checksums, and manifest. Add no new command, configuration, state marker, wrapper hook, or LLM dependency.
- Review this checkpoint once, then run one final whole-candidate coherency review.

## Validation and delivery

- Prove owned `0.41.0` upgrades to `0.45.0`; matching installations are reused; unowned mismatches stop safely.
- Exercise setup, bootstrap, Doctor, watcher indexing, hook-driven commit updates, and MCP startup in real ordinary and linked worktrees.
- Confirm linked worktree changes update its index without modifying the base index.
- Confirm linked removal stops before changing configuration, indexes, or the shared hook.
- Retain tests for empty/non-Git directories, Windows launchers, Plan History repository detection, routing, and unique rule ownership.
- Run the complete test suite, compilation checks, shell and PowerShell checks, checksum validation, and the final native review.
- After clean review, update the live toolkit and repeat Doctor plus linked-worktree MCP smoke tests. Do not publish without a separate publication request.

## Prior Plan reconciliation

Carry forward these records without superseding them:

- `.agent/plan-history/plan-summary.20260822T050100617085Z.fd7dfe4c94e461a1824112794d31e1372d316ccf79eed8a3937d2754c1157e40.md`
- `.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md`
- `.agent/plan-history/plan-summary.20260823T052048899607Z.c539b46a7e5fa56092a382fef046fd00d4271c42c4fda8e0f0e2216ce94df122.md`
- `.agent/plan-history/plan-summary.20260824T031427928859Z.f30d03e6b396d05f07f5ce7eebc8b8e8b81e2b1cfe8ebc739342a6e444ca6968.md`
- `.agent/plan-history/plan-summary.20260824T135017227348Z.7cfbec79d5ce39f1a1d436a31dccfe0669c616f252b6793d4b90dc2b34ad13d6.md`
- `.agent/plan-history/plan-summary.20260824T164719361941Z.f1479c9effab9071b8ccaa86dce1dbee407b79647c6bb7d542aea8c75caae32b.md`

Preflight: ready — the replacement is strictly simpler than the rejected candidate; the unnecessary independent challenge was canceled.

Review: not started — planning only.

Docs: planned — ExecPlan, roadmap, RepoWise behavior, dependency, and authority documentation.

<!-- cpk-plan-spec: docs/plans/cpk-046-repowise-worktree-recovery.md -->
</proposed_plan>
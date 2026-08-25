<proposed_plan>
# CPK-046 — RepoWise Worktree Recovery

## Damage assessment

- Preserve `8a0b82e`; it is valid repository-local work. Local `main`, `origin/main`, the live toolkit, and the shared Git hook remain unchanged.
- No damaged work was committed or published. The rejected work is confined to `task/cpk-046-repowise-worktree-bootstrap` and its worktree.
- Delete the staged candidate rather than salvage its duplicate ownership logic, primary-checkout redirection, and undocumented Git requirement.
- Remove the verified `/tmp/.git`, `/tmp/.codex`, and `/tmp/.agent` debris. Leave unreachable review objects to normal Git maintenance.

## Checkpoint 1 — Containment and authority

- Record the incident evidence in ignored test-results storage. Then remove the rejected worktree, its branch, and the exact verified temporary paths.
- Create `cpk-046-repowise-worktree-recovery` from `8a0b82e`. Do not modify tracked files on `main`.
- Create the CPK-046 ExecPlan. Copy and link every applicable unlinked Plan History record beside it before implementation.
- Add one Delivery Lifecycle rule requiring explicit user authority before modifying another repository because shared tooling failed.
- Make Repository Knowledge route failures to that owner and stop with a portable diagnostic.
- Add a unique-owner test for the authority rule.
- Exempt strict simplifications from independent design challenges when they use existing upstream or native behavior and add no interface, state, or broader behavior.
- Run one checkpoint native review and commit the accepted checkpoint.

## Checkpoint 2 — Minimal RepoWise correction

- Upgrade the toolkit-owned RepoWise installation from `0.41.0` to `0.45.0`. Bump the toolkit bugfix version from `0.23.0` to `0.23.1`.
- Force an upgrade only for the exact toolkit-owned path recorded by the install manifest. Reject unowned mismatches.
- Pass the actual worktree root to RepoWise and rely on its native linked-worktree support. Do not add a primary-checkout resolver. [RepoWise worktrees](https://github.com/repowise-dev/repowise/blob/main/docs/scale/WORKTREES.md), [RepoWise changelog](https://github.com/repowise-dev/repowise/blob/main/docs/CHANGELOG.md)
- Resolve hooks with `git rev-parse --git-path hooks`. Do not use `--path-format`. [Git hooks](https://git-scm.com/docs/githooks)
- Reject `remove-repo` from linked worktrees before mutation because their hook is shared. Keep ordinary-checkout removal unchanged.
- Preserve the watcher patch, keyless operation, empty-directory behavior, and Windows launcher repair.
- Update the dependency lock, license declaration, documentation, roadmap, checksums, and manifest. Add no new command, state marker, wrapper hook, or LLM dependency.
- Run one checkpoint native review and commit the accepted checkpoint.
- Run one final native review of the complete staged candidate. Do not perform a separate coherency review.

## Validation and delivery

- Test owned upgrades, matching-version reuse, unowned conflicts, Windows launchers, and empty/non-Git directories.
- Exercise setup, bootstrap, Doctor, watcher indexing, hook-driven commits, and MCP startup in real ordinary and linked worktrees.
- Confirm each linked worktree has its own index and does not modify the base index.
- Confirm linked removal stops before changing configuration, indexes, or the shared hook.
- Run the complete test suite, compilation, shell and PowerShell checks, rule-owner checks, and checksum validation.
- After a clean final native review, update the live toolkit and repeat Doctor plus linked-worktree MCP smoke tests.
- Do not publish without a separate publication request.

## Prior Plan reconciliation

The six earlier Plan History records remain carried.

Record: `.agent/plan-history/plan-summary.20260825T002758364682Z.4eba52594f2ef5bdbe93f4f0ead7b61802e894668d23c749b5af459f65a19437.md`  
Status: superseded  
Reason: The user clarified that coherency reviews have been replaced with native reviews.  
Replacement: Use checkpoint native reviews followed by one final native review of the complete candidate. All other decisions remain carried.

Preflight: ready — this correction is strictly simpler than the rejected candidate.

Review: not started — planning only.

Docs: planned — ExecPlan, roadmap, RepoWise behavior, dependency, and authority documentation.

<!-- cpk-plan-spec: docs/plans/cpk-046-repowise-worktree-recovery.md -->
</proposed_plan>
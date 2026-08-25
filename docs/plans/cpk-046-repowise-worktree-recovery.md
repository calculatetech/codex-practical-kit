# Recover RepoWise Worktree Support

This ExecPlan is a living specification until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

A Codex session in another repository tried to repair this toolkit without user authority. The rejected repair also replaced RepoWise’s linked-worktree model with duplicate primary-checkout logic. This change keeps repository scope explicit and uses RepoWise’s native worktree support.

The release version is `0.23.1`. Work occurs on branch `cpk-046-repowise-worktree-recovery` from commit `8a0b82e54dcefa5780c4869d8412e7b4158f2659`.

## Surprises & Discoveries

- The rejected branch contained no commit and never changed the live installation or remote branch.
- RepoWise `0.45.0` supports linked worktrees and resolves their shared hook directory through Git.
- A linked-worktree hook is shared. Removing it from one linked worktree would disable maintenance for its siblings.
- The accepted Plan initially used unlinked storage because this specification did not exist.

## Decision Log

- Preserve `8a0b82e` as valid repository-local work.
- Delete the rejected custom worktree resolver and rely on RepoWise `0.45.0`.
- Let Delivery Lifecycle own cross-repository mutation authority. Repository Knowledge only routes to that owner.
- Skip an independent preflight challenger for a strict simplification that adds no interface, state, dependency, or broader behavior.
- Reject `remove-repo` in a linked worktree before mutation.
- Keep the existing watcher patch, keyless operation, empty-directory behavior, and Windows launcher repair.
- Use checkpoint native reviews and one final native review. A separate coherency review does not exist.
- Run semantic trace closure only for executable production-code behavior with a real runnable entry point. Written instructions use deterministic checks and native review.

## Context and Orientation

`assets/skills/delivery-lifecycle/references/delivery-lifecycle.md` owns delivery authority. `assets/skills/repository-knowledge/SKILL.md` owns RepoWise lookup routing. `assets/skills/design-preflight/SKILL.md` owns the strict-simplification challenge exemption. `assets/runtime/repowise_bootstrap.py` starts RepoWise. `kit.py` installs and diagnoses it. `tests/test_kit.py` verifies behavior and rule ownership.

Applicable immutable Plan records:

- `.agent/plan-history/plan-summary.20260822T050100617085Z.fd7dfe4c94e461a1824112794d31e1372d316ccf79eed8a3937d2754c1157e40.md`
- `.agent/plan-history/plan-summary.20260822T065923051937Z.4415ee79c8b0327ba824768113192b4f60662d355fb4931876ec995a214a5526.md`
- `.agent/plan-history/plan-summary.20260823T052048899607Z.c539b46a7e5fa56092a382fef046fd00d4271c42c4fda8e0f0e2216ce94df122.md`
- `.agent/plan-history/plan-summary.20260824T031427928859Z.f30d03e6b396d05f07f5ce7eebc8b8e8b81e2b1cfe8ebc739342a6e444ca6968.md`
- `.agent/plan-history/plan-summary.20260824T135017227348Z.7cfbec79d5ce39f1a1d436a31dccfe0669c616f252b6793d4b90dc2b34ad13d6.md`
- `.agent/plan-history/plan-summary.20260824T164719361941Z.f1479c9effab9071b8ccaa86dce1dbee407b79647c6bb7d542aea8c75caae32b.md`
- `.agent/plan-history/plan-summary.20260825T002758364682Z.4eba52594f2ef5bdbe93f4f0ead7b61802e894668d23c749b5af459f65a19437.md`
- `.agent/plan-history/plan-summary.20260825T002911279202Z.940432714b78524077326cf1dea7571142fa6038e878a2fb7e884024bc8775a8.md`

The first CPK-046 record is superseded only where it names a final coherency review. The second record replaces that term with the toolkit’s final native review. All other decisions are carried.

## Product Boundary

[Delivery Lifecycle](../../assets/skills/delivery-lifecycle/references/delivery-lifecycle.md) limits write authority to the current repository and repositories explicitly named by the user. [Repository Knowledge](../../assets/skills/repository-knowledge/SKILL.md) must report an out-of-scope tooling failure instead of repairing another repository.

The supported runtime is a normal Git checkout or a normal linked worktree. Bare-backed worktrees retain upstream behavior. The implementation adds no new command, configuration, state marker, wrapper hook, LLM dependency, or primary-checkout resolver.

## Boundary Inventory

| Boundary | Condition and contrast | Entry points | Required oracle | Scenario |
| --- | --- | --- | --- | --- |
| B1 | A failure in the current or explicitly named repository permits in-scope work. The same failure in another repository permits read-only diagnosis only. | Delivery Lifecycle and Repository Knowledge failure handling. | The authority rule occurs only in Delivery Lifecycle. Repository Knowledge reports failure and routes to it. | S1 |
| B2 | A correction that rejects a larger design, uses an existing capability, and broadens no behavior skips the challenger. A correction that adds an interface, state, dependency, fallback, or supported behavior keeps the challenger. | Design Preflight correction entry gate. | Both sides remain explicit. Only the strict simplification receives the exception. | S2 |
| B3 | A manifest-owned outdated RepoWise command upgrades. An unowned mismatch stops. | Core installation and runtime discovery on POSIX and Windows. | Only the owned path changes and the final command reports `0.45.0`. | S3 |
| B4 | A normal linked worktree uses its own index and Git's shared hook path. A normal checkout keeps its existing behavior. | Setup, automatic bootstrap, Doctor, watcher, MCP, and post-commit maintenance. | Linked changes reach the linked index without changing the base index. Both repository forms remain ready. | S4 |
| B5 | `remove-repo` in a linked worktree stops before mutation. The same command in a normal checkout removes only managed integration. | POSIX and PowerShell removal launchers through `kit.py`. | Linked configuration, index, and shared hook remain unchanged. Normal removal still succeeds. | S5 |
| B6 | Executable production-code behavior with a real runnable entry point uses trace closure. Written instructions, tests, documentation, and static configuration do not. | Scenario Discrimination before native review. | Instruction-only work uses deterministic checks and native review without a semantic trace loop. Runtime behavior keeps trace closure. | S6 |

No source clause is deferred or a contract gap. Bare-backed worktrees are opaque upstream behavior and receive no toolkit-specific promise.

## Scenario Proof

| Scenario | Discriminator | Minimal contrast | Production path and terminal oracle | Runnable check |
| --- | --- | --- | --- | --- |
| S1 | Repository write authority | Same tooling failure inside task scope and in an unnamed repository | Failure to Delivery Lifecycle authority; only the in-scope repository can change | `test_tool_failure_does_not_expand_repository_write_scope` |
| S2 | Correction shape | Strict deletion/upstream reuse and a correction that adds one listed moving part | Design Preflight entry gate; only the strict simplification skips the challenger | `test_strict_simplifications_skip_the_preflight_challenger` |
| S3 | Manifest ownership | Outdated command at the recorded fixed path and the same version elsewhere | `ensure_repowise`; owned command upgrades and unowned command raises conflict | Focused owned-upgrade and unowned-mismatch runtime tests |
| S4 | Repository form | Normal checkout and linked worktree from the same base | Launcher to RepoWise hook, watcher, MCP, and separate index state | Real linked-worktree setup, Doctor, watcher, MCP, and commit smoke tests |
| S5 | Removal repository form | Normal checkout and linked worktree | `remove_repo`; linked form stops before the first mutation and normal form completes | Focused removal tests with configuration, index, and hook oracles |
| S6 | Review source type | Executable production behavior and written instruction behavior | Scenario Discrimination gate; only the executable side invokes semantic trace closure | `test_boundary_trace_closure_blocks_native_review` |

## Plan of Work

### CP1 — Containment and authority

Add one cross-repository write-authority guard to Delivery Lifecycle. Route Repository Knowledge failures to it. Add the strict-simplification challenge exception to Design Preflight. Limit semantic trace closure to executable production-code behavior. Verify that each rule has one owner, update the focused tests and documentation, run one checkpoint native review, and commit the accepted checkpoint.

### CP2 — Minimal RepoWise correction

Pin RepoWise `0.45.0`. Upgrade only the manifest-recorded toolkit-owned executable. Resolve hooks with `git rev-parse --git-path hooks`. Reject linked-worktree removal before mutation. Preserve existing runtime behavior, update the authoritative documentation and dependency records, and regenerate the manifest. Run one checkpoint native review and commit the accepted checkpoint. Then run one final native review of the complete candidate.

## Validation

- Prove one-owner routing for cross-repository authority and strict-simplification challenge behavior.
- Prove owned upgrades, matching-version reuse, unowned conflicts, Windows repair, and empty-directory behavior.
- Exercise setup, bootstrap, Doctor, watcher indexing, hook commits, and MCP startup in real normal and linked worktrees.
- Confirm that a linked worktree has its own index and does not modify the base index.
- Confirm that linked removal stops before configuration, index, or hook mutation.
- Run the complete Python suite, compilation checks, shell and PowerShell checks, rule-owner checks, and checksum validation.
- Install the reviewed candidate and repeat Doctor plus linked-worktree MCP smoke tests before review closure.

## Outcomes & Retrospective

RepoWise uses its upstream linked-worktree model. A tooling failure cannot silently authorize edits in another repository. The toolkit has one native review sequence and no separate coherency review.

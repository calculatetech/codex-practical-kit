# Make preflight adversarial and research-backed

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, Design Preflight first obtains an independent scenario derivation and then challenges the coordinator's actual decisions. Qualifying architecture, algorithm, protocol, and systems choices must use the pinned NeuroArxiv skill before an approach is selected. Read-only research and review can use available platform capacity, while only one write-capable implementation subagent can run at a time.

## Progress

- [x] (2026-08-19) Accepted the CPK-035 plan and created the isolated task branch.
- [x] (2026-08-19) Activated CPK-035 as the sole roadmap task.
- [x] (2026-08-19) Implemented the two-phase preflight challenge and concurrency correction.
- [x] (2026-08-19) Bundled pinned NeuroArxiv and made its qualifying research gate mandatory.
- [x] (2026-08-19) Updated tests and documentation, then forward-tested both workflows.
- [x] (2026-08-19) Passed final validation and a clean full review of staged tree `7d4caa6bfdabbca8f92818ffef1bdd5610a7c869`.

## Surprises & Discoveries

- Observation: The existing upstream staging and install loops are already data-driven.
  Evidence: `kit.py` downloads every skill in `upstream.lock.json` and installs every name in `UPSTREAM_SKILLS`.
- Observation: NeuroArxiv borrows ADHD's isolated-reader pattern but has a narrower research purpose.
  Evidence: The pinned upstream skill applies separate paper readers to arXiv research and does not provide general ideation guidance.
- Observation: The informed preflight phase rejected a plausible but unsupported operator-timing exclusion.
  Evidence: The same challenger classified the post-cutoff save as an unsupported assumption, invalid exclusion, and unresolved contract gap after it received the incomplete coordinator card.
- Observation: The bundled workflow completed a real narrow systems search within platform capacity by running isolated readers in waves.
  Evidence: Sequential arXiv API fetches returned four papers. The workflow selected a durable database state machine after four paper-specific abstract reads.

## Decision Log

- Decision: Use the same fresh challenger for an unanchored first pass and an informed adversarial second pass.
  Rationale: The first pass preserves independent derivation. The second pass can test the coordinator's assumptions and exclusions instead of echoing them.
  Date/Author: 2026-08-19 / user and Codex
- Decision: Bundle NeuroArxiv unchanged at commit `b5d20efa12dd1ba177ce890d56809d2e027f8055` and remove ADHD and NeuroArxiv from optional metadata.
  Rationale: The existing pinned upstream mechanism supplies provenance and safe ownership without adding a dependency or copying upstream source into this repository.
  Date/Author: 2026-08-19 / user and Codex
- Decision: Restrict one concurrent write-capable implementation subagent, not read-only agents.
  Rationale: Parallel independent research and review are useful; concurrent writers create task-state and working-tree conflicts.
  Date/Author: 2026-08-19 / user and Codex

## Outcomes & Retrospective

Implementation, forward testing, documentation, validation, and review are complete. The clean reviewer reported no findings.

## Context and Orientation

The task branch is `cpk-035-adversarial-preflight-research`. Its base branch is `main`, and its base commit is `038a3b8c6e9459d49845d1d42aa83be1f99b1cc7`.

`assets/skills/design-preflight/SKILL.md` owns preflight procedure, and `assets/skills/design-preflight/references/preflight-review.md` owns challenger output. `assets/skills/research-first/SKILL.md` owns research selection. `assets/skills/delivery-lifecycle/references/coordination.md` owns agent roles. `kit.py` and `upstream.lock.json` own bundled-skill installation and provenance. `tests/test_kit.py` protects the installed interface.

NeuroArxiv is an upstream skill that searches the arXiv API, assigns papers to isolated read-only agents, compares their evidence, and selects one path. A write-capable implementation subagent can edit files. A read-only agent can research or review but cannot edit files.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). Toolkit rule files, routes, lock metadata, installer behavior, tests, and documentation are `composes`. Installed copies, user-managed ADHD, and tenant repository code are `opaque`. The toolkit must not adopt, overwrite, install, or remove user-managed ADHD.

## Scenario Proof

This task changes static policy and installation behavior, not product runtime behavior. The runtime Scenario Proof gate does not apply to the toolkit implementation itself.

The preflight forward check must show that Phase 1 receives no coordinator card and that Phase 2 receives it and reports a seeded omission. The research forward check must show a qualifying open systems choice performs a real arXiv fetch through isolated readers, records citations and paper limitations, and selects one path. Structural tests must prove the research gate, fetch-failure stop, routine-work skip, concurrency boundary, exact upstream pin, conflict safety, and ADHD non-ownership.

## Plan of Work

Revise Design Preflight to run a two-phase challenge with one fresh read-only challenger. Extend the review interface with a `preflight-adversary` Phase 2 result and require dispositions for supported and rejected findings.

Revise Research First to route qualifying open, costly architecture, algorithm, protocol, and systems choices through NeuroArxiv before selection. A failed required arXiv fetch stops selection. Retain official documentation and other primary sources for questions outside arXiv's scope.

Add NeuroArxiv to `UPSTREAM_SKILLS` and to the lock at the accepted commit, blobs, and MIT license. Remove ADHD and NeuroArxiv from optional metadata. Do not add ADHD to obsolete or managed skills. Update routing and user documentation, then update the manifest.

## Concrete Steps

Work in `/home/mbeutler/Projects/codex-practical-kit`.

Run the focused integration tests, all skill validators, `./run-tests.sh`, shell syntax checks, `git diff --check`, and `sha256sum --check MANIFEST.sha256`. Record detailed results in `.agent/test-results/cpk-035-adversarial-preflight-research.md` and never stage that file.

## Validation and Acceptance

Tests must fail if the exact NeuroArxiv pin, skill blob, license blob, install destination, required research trigger, fetch-failure stop, two-phase challenge packet, or one-writer boundary is removed. Installation tests must preserve an unrelated user-managed ADHD directory and reject an unowned NeuroArxiv destination.

A fresh read-only forward test must apply the two challenge phases and find a seeded omission only after receiving the incomplete card. A separate clean-context forward test must apply the candidate research rule to a qualifying systems choice and return real arXiv citations, paper limitations, and one selected path.

One clean-context reviewer must inspect the staged candidate from base commit `038a3b8c6e9459d49845d1d42aa83be1f99b1cc7`.

## Idempotence and Recovery

The edits and validation commands are safe to repeat. The installer uses its existing staged download and ownership checks. If a command fails, stop and report it unless an in-scope correction is clear.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, and `.vscode/`. They are untracked environment state outside this task.

The NeuroArxiv forward test cited arXiv `2608.03836`, `1911.11286`, `2302.04500`, and `2102.10185`. The readers used abstracts only. The selected test path was a durable database state machine with atomic claims and an idempotent effect ledger. This is validation evidence for the workflow, not an architecture decision for the toolkit.

## Interfaces and Dependencies

The bundled upstream skill is `neuroarxiv`, pinned at commit `b5d20efa12dd1ba177ce890d56809d2e027f8055`. Its `SKILL.md` Git blob is `cc47304c76f7cb53aa4e8a324702dc8e4f1d5639`; its `LICENSE` Git blob is `aaf95a45d3b11d68387ab0c3a0cee964a4ecd98c`; its license is MIT. No Node CLI or package dependency is bundled.

The Phase 2 JSON result uses reviewer `preflight-adversary`. Each finding records its kind, source, coordinator claim, counterexample, wrong terminal result, required card change, and supported-model classification. Empty findings are valid.

Revision note: Created from the accepted CPK-035 plan and verified upstream NeuroArxiv metadata.
Revision note: Recorded implementation and both clean-context forward tests.
Revision note: Recorded final validation, clean staged-tree review, and task closure.

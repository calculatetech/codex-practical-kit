<proposed_plan>
# CPK-047 — Repair Worktree Handoffs, Preflight, and Publication

## Summary

Correct three related process defects in version `0.23.2`.

First, relocate pending Plan History records from the source worktree to the task worktree. Do not leave duplicate untracked files in local `main`.

Then bound preflight and reconcile publication state.

Official documentation defines `codex review` as local review. It defines `@codex review` as GitHub PR review. [Local review](https://learn.chatgpt.com/docs/developer-commands?surface=cli#codex-review), [PR review](https://learn.chatgpt.com/docs/third-party/github#request-a-codex-review)

Create branch `cpk-047-bounded-preflight-publication` from synchronized `main`. Use three checkpoint commits.

## CP1 — Transfer Pending Plan History

Update the canonical Plan History owner.

- Before work starts in another worktree, enumerate every worktree in the same Git repository.
- Find every applicable untracked central record and specification-sibling record.
- Copy each record to the same relative path in the task worktree.
- Compare the source and destination bytes.
- If the bytes match, remove the redundant untracked source copy.
- If the bytes differ, retain both records and stop.
- If the destination copy fails, retain the source and stop.
- Never remove a tracked record, collision record, unrelated record, or unique record.
- Keep central and specification-sibling records together in the task worktree. They have different purposes and are not redundant.
- Preserve record contents, event identity, timestamps, and filenames.
- Define this operation as relocation. It does not remove Plan history because the verified destination remains.
- Make the sequence repeatable. A partial copy can leave a harmless duplicate for the next attempt.
- Do not change the Plan capture hook. It cannot know which future worktree will implement the Plan.
- Do not add a helper, database, manifest, or new runtime state.

Add a focused owner test for discovery, copy, byte comparison, safe removal, collision retention, and tracked-file protection.

Review and commit CP1 before the other checkpoints.

## CP2 — Bound Preflight

- Build one source packet before the challenger starts.
- Include the accepted outcome, explicit requirements, product specifications, composing owners, path gates, state writers, and direct checks.
- Interpret “complete source set” as complete within the accepted task boundary.
- Permit expansion for authoritative product evidence or a direct composing-owner relationship.
- Require each expansion to name its source, relevance basis, and evidence.
- Do not expand for reachability, opaque owners, deferred work, future use cases, or unrelated lifecycles.
- Add `source_scope` to the Phase 1 result. Include `initial_sources` and evidence-backed `expansions`.
- Keep one challenger identity for both phases and one coordinator comparison.
- Put generic task liveness in Coordination. Elapsed time cannot authorize a duplicate delegated task.
- Route an actual challenger error to the existing one-attempt Supported Model rule.
- Add no numeric timeout, automatic retry, cancellation system, or durable challenger state.

Review and commit CP2 as a checkpoint.

## CP3 — Reconcile Publication

Before publication classifies worktree state, apply the Plan History handoff from CP1.

- Do not classify verified Plan History duplicates as unrelated files.
- Preserve all other untracked files.
- Stop for an untracked file only when Git reports an actual overwrite conflict.
- Stop for staged or unstaged tracked changes before the local-main update.

Keep local native review and GitHub PR review as separate cumulative gates.

- Apply Review Closure and freeze tracked records before the task commit.
- Record the frozen local task head.
- Push the task branch.
- Require the remote task branch and PR head to equal the local task head.
- Request `@codex review` for that exact PR head.
- Do not use a clean local review to satisfy the GitHub review gate.
- Apply local correction and review rules before each correction push.
- Reset PR review and CI eligibility after each push.

After GitHub completes the squash merge:

1. Record the GitHub merge commit.
2. Fetch `origin`.
3. Find the worktree that contains local `main`.
4. Apply the Plan History handoff before the clean-state gate.
5. Require no staged or unstaged tracked changes.
6. Run `git merge --ff-only origin/main`.
7. If no worktree contains `main`, switch the clean publishing worktree to `main`.
8. Fast-forward `main` there.
9. Prove that local `main` equals `origin/main`.
10. Prove that the head contains the recorded merge commit and published result.
11. Monitor required post-merge CI for that head.

Stop on tracked changes, divergence, checkout conflicts, actual untracked-path conflicts, or a failed fast-forward. Do not stash, reset, rebase, or remove unrelated files.

## Validation and Delivery

- Test Plan History relocation before any unexpected-file or clean-state decision.
- Test byte-identical relocation, different-content preservation, partial-copy recovery, and tracked-record protection.
- Test bounded preflight sources, evidence-backed expansion, one live challenger, and no automatic restart.
- Test cumulative review gates, exact task and PR heads, local-main fast-forward, and safe-stop behavior.
- Keep each rule in one canonical owner.
- Use deterministic instruction checks. Do not add variable clean-context traces.
- Run the focused checks, full suite, skill validators, link checks, platform checks, manifest validation, and `git diff --check`.
- Bump the committed source version from `0.23.1` to `0.23.2`.
- Run one final native review from the task base after all checkpoints.
- Apply Review Closure and create the final closure commit.
- Install the reviewed toolkit in the live environment. Require Doctor to report `Result: ready`.
- Do not publish without a later publication request.

## Prior Plan Reconciliation

Record: `.agent/plan-history/plan-summary.20260825T172626414955Z.9eaf7888a286b18f69d5a94869ee99522214d23dd715a553664a2041108fced3.md`  
Status: superseded  
Reason: The publication checkpoint did not first relocate pending Plan History records from the `main` worktree.  
Replacement: Add CP1 relocation before preflight and publication. Apply that owner before publication classifies worktree state.  
Scope: unfinished subtasks CP1 and CP2.

Carry the CPK-035 two-phase challenger design, CPK-042 checkpoint process, CPK-043 PR gate, CPK-044 finding gate, and final CPK-046 review process.

Use a branch because this task has one writable implementation stream.

Preflight: ready — CP1 is a strict simplification of the existing copy and byte-comparison handoff.

Review: not started — planning only.  
Docs: planned — update Plan History, Coordination, Design Preflight, Publication, CPK-047, roadmap, version, tests, and checksums.

<!-- cpk-plan-spec: docs/plans/cpk-047-bounded-preflight-publication.md -->
</proposed_plan>
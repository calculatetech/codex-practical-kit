<proposed_plan>
# CPK-047 — Bound Preflight and Reconcile Publication

## Summary

Correct two process defects in version `0.23.2`.

Limit preflight to evidence that can change the accepted outcome. Keep one challenger until it completes or reports an error.

Require separate local and PR reviews. After a remote merge, fast-forward local `main` before publication ends.

Official OpenAI documentation defines `codex review` as a local target review. It defines `@codex review` as a GitHub PR review. [Local review](https://learn.chatgpt.com/docs/developer-commands?surface=cli#codex-review), [PR review](https://learn.chatgpt.com/docs/third-party/github#request-a-codex-review)

Create branch `cpk-047-bounded-preflight-publication` from synchronized `main`. Use two checkpoint commits because the fixes have separate owners.

## CP1 — Bound Preflight

- Build one source packet before the challenger starts.
- Include the accepted outcome, explicit requirements, relevant product specifications, direct composing owners, path gates, state writers, and direct checks.
- Interpret “complete source set” as complete within the accepted task boundary.
- Permit expansion for authoritative product evidence or a direct composing-owner relationship.
- Require each expansion to name its source, relevance basis, and evidence.
- Do not expand for reachability, opaque owners, deferred work, future use cases, or unrelated lifecycles.
- Add `source_scope` to the Phase 1 result. Include `initial_sources` and evidence-backed `expansions`.
- Keep one challenger identity for both phases and one coordinator comparison.
- Put generic task liveness in Coordination. Elapsed time cannot authorize a duplicate delegated task.
- Route an actual challenger error to the existing one-attempt Supported Model rule. Stop and report the error.
- Add no numeric timeout, retry, cancellation system, or durable challenger state.

Review CP1 with checkpoint mode. Commit it after the focused checks and clean review.

## CP2 — Preserve Publication State

- Keep native local review and GitHub PR review as separate cumulative gates.
- Apply Review Closure, freeze tracked records, and create the local task commit before publication.
- Record the frozen local task head. Do not require its tree to equal the pre-closure review tree.
- After the push, require the remote task branch and PR head to equal the local task head.
- Request `@codex review` for that exact PR head. A clean local review cannot satisfy this gate.
- Apply existing local correction and review rules before each correction push.
- Reset PR review and CI eligibility after every push.

After GitHub completes the squash merge:

1. Record the GitHub merge commit.
2. Fetch `origin`.
3. Find the worktree that contains local `main`.
4. Require no staged or unstaged tracked changes in that worktree.
5. Run `git merge --ff-only origin/main` in that worktree.
6. If no worktree contains `main`, switch the clean publishing worktree to `main`.
7. Fast-forward `main` there.
8. Prove that local `main` equals `origin/main`.
9. Prove that this head contains the recorded merge commit and published result.
10. Monitor required post-merge CI for the integrated head.

Stop on dirty tracked state, checkout conflicts, divergence, or a failed fast-forward. Do not stash, reset, rebase, retry, or change untracked files.

## Validation and Delivery

- Extend the focused preflight test for bounded sources, evidence-backed expansion, one live challenger, and no automatic restart.
- Extend the publication test for cumulative review gates, exact task and PR heads, local-main fast-forward, and safe-stop behavior.
- Keep each new rule in one canonical owner. Add no duplicate review, failure, or Git-isolation rules.
- Use deterministic instruction checks. Do not add variable clean-context traces or executable-production trace closure.
- Run the focused checks, full suite, skill validators, link checks, shell checks, PowerShell checks, manifest validation, and `git diff --check`.
- Bump the committed source version from `0.23.1` to `0.23.2`.
- Review and commit CP2 as a checkpoint.
- Run one final native review from the task base.
- Apply Review Closure and create the final closure commit.
- Install the reviewed toolkit in the live environment. Require Doctor to report `Result: ready`.
- Do not publish without a later publication request.

## Assumptions and Prior Plan Reconciliation

- Use semantic scope instead of file, source, action, or time limits.
- Keep the CPK-035 two-phase challenger design. Clarify that its complete source set is task-boundary complete.
- Carry the CPK-042 checkpoint plan record unchanged.
- Carry the CPK-043 plan record. Clarify its current-head PR review and local integration requirements.
- Carry the CPK-044 plan record. Local native review and finding adjudication remain unchanged.
- Carry the final CPK-046 plan record. Use deterministic checks and one final native review.
- Direct publication, tags, releases, cleanup, non-GitHub providers, and destructive recovery remain unchanged.
- Use a normal branch because this task has one writable implementation stream.
- Do not add a skill, dependency, parser, publication script, daemon, database, or runtime state machine.

Preflight: ready — use one evidence-bounded challenger and reconcile exact publication heads through local `main`.

Review: not started — planning only.  
Docs: planned — update the canonical rule owners, CPK-047 ExecPlan, roadmap, version, and checksums.

<!-- cpk-plan-spec: docs/plans/cpk-047-bounded-preflight-publication.md -->
</proposed_plan>
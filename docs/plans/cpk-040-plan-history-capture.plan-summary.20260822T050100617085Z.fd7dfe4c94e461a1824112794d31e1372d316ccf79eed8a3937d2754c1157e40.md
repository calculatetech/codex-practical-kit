<proposed_plan>
# CPK-040 — Save Plans at Acceptance

## Summary

A prompt such as `Implement the plan.` must save the preceding Plan before implementation begins.

Do not add semantic acceptance detection. Every next `UserPromptSubmit` saves the preceding completed Plan. Therefore, acceptance and revision prompts both preserve history.

Release this bugfix as `0.19.1`.

## Diagnostic First Action

Before fetching, branching, editing, installing, or creating files:

- Inspect this chat’s rollout at `/home/mbeutler/.codex/sessions/2026/08/13/rollout-2026-08-13T20-56-24-019ffdc5-27d6-7583-9a3b-7499d22ed915.jsonl`.
- Confirm the latest accepted Plan has:
  - A completed `Plan` item.
  - An assistant response containing the exact `<proposed_plan>` envelope.
  - A matching `task_complete` with `last_agent_message: null`.
  - A following acceptance turn.
- Confirm that no corresponding `.agent/plan-history` or specification-sibling record exists.
- Inspect the installed hook configuration and generated Codex hook schemas.
- Record the redacted event sequence and observed failure in the CPK-040 ExecPlan after creating the branch.
- Recover the exact accepted Plan from this rollout into repository and sibling history before other tracked edits.

## Implementation

- Create branch `cpk-040-plan-history-capture` from `ec07371a`. Do not implement on `main`.
- Keep the existing `Stop` capture for compatibility.
- Add one standard-library reverse transcript reader:
  - Inspect only the newest completed turn.
  - Use the raw assistant response as the saved content.
  - Use the completed `Plan` item as the completion discriminator.
  - Derive thread and turn identity from rollout fields.
  - Stop immediately when the newest completed turn is not a Plan.
  - Do not backfill older pre-fix Plans.
- Run transcript capture before:
  - Every `UserPromptSubmit`, regardless of current permission mode.
  - `SessionStart` for `resume`, `compact`, and `clear`.
  - `SessionEnd`, using the event and `transcript_path` exposed by Codex 0.149.
- Always write repository Plans to `.agent/plan-history/`.
- Also write exact sibling copies for all valid specification markers.
- Preserve the existing non-Git global fallback.
- Preserve each hook’s output contract. Emit one valid response per hook.
- Update only the canonical `plan-history` rule owner and affected product documentation.
- Bump the committed version from `0.19.0` to `0.19.1`.

## Automated Checks

- Add a redacted fixture copied from this chat’s real Plan and acceptance sequence.
- Add a focused acceptance check:
  - Supply a transcript ending with a completed Plan.
  - Invoke `UserPromptSubmit` with `Implement the plan.`
  - Verify that the exact Plan exists before the hook returns.
- Check revision prompts, default permission mode, and Unicode exactness.
- Check `SessionStart`, `SessionEnd`, direct `Stop`, clear-session identity, retries, equal-content turns, and collision preservation.
- Check central discovery, valid siblings, explicit `none`, invalid markers, and hook-specific warning output.
- Check bounded reads with large prefixes, non-Plan suffixes, no-Plan transcripts, CRLF, and Windows paths.
- Update installer and doctor checks for `SessionEnd`.
- Add an opt-in live app-server test:
  - Start a real Plan turn through `collaborationMode.mode = "plan"`.
  - Read its raw response from the generated rollout.
  - Start a default turn with `Implement the plan.`
  - Verify that the installed hook saves the response before any agent tool action.
  - Interrupt the acceptance turn and clean the temporary repository.
- Keep the live check outside the default suite because it requires authentication, network access, and model usage.

## Delivery

- Run focused checks, the full suite, shell checks, and rule-owner checks.
- Run scope-bound adversarial review.
- After review passes, run `python3 kit.py install --repo .` and `python3 kit.py doctor --repo .`.
- Run the live Plan acceptance check against the installed toolkit.
- Create one local checkpoint commit. Do not publish without a later request.
- Finalize roadmap state before the commit. Do not write progress state after it.

## Prior Plan Reconciliation

Record: `docs/plans/cpk-036-plan-history.md`  
Status: superseded  
Reason: Codex 0.149 completes Plan turns without the expected `Stop` hook. Specification-only records are also not globally discoverable.  
Replacement: Save the newest completed Plan during the next `UserPromptSubmit`, including an implementation acceptance prompt. Also capture during supported session lifecycle events and retain `Stop` compatibility.

## Assumptions

- Acceptance is not detected from prompt wording. The lifecycle boundary is authoritative.
- Historical Plans missed before this repair are not bulk-imported.
- Crashes that bypass every lifecycle event remain outside the supported model.
- App-server Plan invocation is a test facility, not automatic mode switching in an active chat.
- No daemon, database, mutable cursor, dependency, or unrelated-session scan is added.

Preflight: ready — this chat supplies the production event sequence and the acceptance-path regression fixture.

Review: not started — planning only.  
Docs: planned — correct the Plan capture and discovery contract.

<!-- cpk-plan-spec: docs/plans/cpk-040-plan-history-capture.md -->
</proposed_plan>
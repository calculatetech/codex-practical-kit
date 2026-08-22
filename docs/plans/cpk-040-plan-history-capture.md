# Save Plans at acceptance

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose

An implementation acceptance prompt must save the preceding completed Plan before implementation work starts. Later agents must find every saved repository Plan in `.agent/plan-history/` without knowing its specification path.

## Progress

- [x] (2026-08-22) Inspected this chat rollout before fetching, branching, editing, installing, or creating task files.
- [x] (2026-08-22) Confirmed the accepted Plan, null `last_agent_message`, following acceptance turn, missing history record, and missing managed `SessionEnd` hook.
- [x] (2026-08-22) Created branch `cpk-040-plan-history-capture` from `ec07371a49480b10c5f5e6625624fcf329e3fd4a`.
- [x] (2026-08-22) Preserved the accepted Plan in repository and sibling history with byte-for-byte comparison to the rollout.
- [x] (2026-08-22) Implemented transcript capture, central discovery storage, lifecycle hooks, and the `0.19.1` version.
- [x] (2026-08-22) Passed the focused checks and all 79 default Python checks.
- [x] (2026-08-22) Updated the canonical Plan history rules and affected user documentation.
- [x] (2026-08-22) Completed clean full and test-delta reviews.
- [x] (2026-08-22) Installed version `0.19.1`, passed Doctor, and passed the live Codex acceptance check.
- [x] (2026-08-22) Corrected and reviewed the managed `SessionEnd` timeout after Codex reported its 3-second maximum.

## Prior Plan Reconciliation

Record: `docs/plans/cpk-036-plan-history.md`

Status: superseded

Reason: Codex 0.149 completes Plan turns without the expected `Stop` hook. Specification-only records are also not globally discoverable.

Replacement: Save the newest completed Plan during the next `UserPromptSubmit`, including an implementation acceptance prompt. Also capture during supported session lifecycle events and retain `Stop` compatibility.

The accepted CPK-040 response is recovered from this chat rollout and linked beside this ExecPlan.

## Plan Deviations

- The accepted Plan contains the literal opening envelope tag in its diagnostic text. The existing count-based validator rejects that normal Plan. The shared validator must recognize the outer boundary without rejecting tag text inside the Plan.
- The current hook cannot perform the required manual recovery until that shared validator is corrected. Run recovery immediately after the correction and before unrelated runtime work.
- The live client must declare the Codex `experimentalApi` capability. It waits for the managed `hook/completed` event because `turn/started` occurs before prompt hooks.
- Official Codex documentation caps `SessionEnd` at 3 seconds. The first candidate incorrectly reused the 10-second timeout from other hooks.

## Production Evidence

The source rollout is `/home/mbeutler/.codex/sessions/2026/08/13/rollout-2026-08-13T20-56-24-019ffdc5-27d6-7583-9a3b-7499d22ed915.jsonl`.

Thread `019ffdc5-27d6-7583-9a3b-7499d22ed915` contains completed Plan turn `01a027d1-1ffc-7463-8292-00d9b3ffde26`. The turn has a completed `Plan` item, an assistant `final_answer`, and `task_complete` with `last_agent_message: null`. Turn `01a027d4-0287-7322-9b03-d2e78bc26d8f` then starts with `Implement the plan.`. The installed hook did not create a repository or sibling record.

The assistant turn also contains commentary messages. Therefore, transcript selection must require the final-answer envelope. Turn identity alone is not sufficient.

## Product Boundary

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). The task composes the managed hook, hook installer, immutable record writer, and canonical Plan history skill. Codex rollout and hook schemas are opaque platform owners. Repository history and valid specification siblings are terminal file owners.

The supported model is one current Codex session in a Git repository. The next prompt, session start, or clean session end supplies the current transcript. Historical all-session recovery, crashes that bypass every lifecycle event, daemons, databases, mutable cursors, dependencies, and automatic mode switching are excluded.

## Scenario Proof

| Scenario | Discriminator and contrast | Production path | Required oracle | Runnable check | Result |
| --- | --- | --- | --- | --- | --- |
| Acceptance capture | Completed Plan followed by `Implement the plan.` versus no completed Plan | `UserPromptSubmit` to transcript reader to record writer | Exact Plan exists before hook return | Real-rollout fixture acceptance test | Passed |
| Structural envelope | Outer envelope with an inline opening-tag mention versus incomplete outer envelope | shared Plan validator | Valid outer envelope passes; incomplete response fails | focused validator test | Passed |
| Lifecycle capture | default prompt, resume, compact, clear, and session end | managed hook event to transcript reader | Latest completed Plan is saved without changing hook output shape | hook subprocess tests | Passed |
| Turn selection | Final Plan response versus commentary and newer non-Plan turn | reverse rollout reader | Only the newest completed turn can produce a record | observed-shape selection tests | Passed |
| Event identity | Stop replay versus transcript replay; equal text from distinct turns | shared session and turn identity to immutable writer | Same turn is idempotent; distinct turns remain distinct | identity and collision tests | Passed |
| Discovery and association | linked, none, invalid, and mixed markers | central history plus sibling writers | Every repository Plan has a central record and every valid sibling | association tests | Passed |
| Bounded read | large prefix, non-Plan suffix, and no-Plan transcript | reverse reader to newest completed turn | Old transcript content is not repeatedly scanned | large-prefix and newest-non-Plan checks | Passed |
| Live acceptance | app-server Plan turn followed by acceptance | real Codex to installed hook | Raw final response is saved when the synchronous prompt hook completes | opt-in live test | Passed |

## Plan of Work

Correct the shared envelope validator first. Recover the accepted Plan through that owner. Then add one standard-library reverse transcript reader and call it from `UserPromptSubmit`, `SessionStart`, and `SessionEnd`. Keep direct `Stop` capture.

Always write repository Plans to `.agent/plan-history/`. Also write each valid specification sibling. Preserve the existing global fallback for non-Git paths and every hook output contract.

Update the installer, Doctor, canonical Plan history instructions, user documentation, and committed version. Add no dependency or background process.

## Validation and Acceptance

Run focused hook and installer checks, the full suite, shell checks, rule-owner checks, and `git diff --check`. Finalize documentation before adversarial review.

After clean review, install the candidate with `python3 kit.py install --repo .` and run `python3 kit.py doctor --repo .`. Run the opt-in app-server acceptance check against the installed toolkit.

## Idempotence and Recovery

The session and original turn form the immutable event identity. An exact retry writes nothing. Different content for one identity creates a collision record. The reader inspects only the newest completed turn and does not backfill older missed Plans.

## Interfaces and Dependencies

The managed hook set adds `SessionEnd`. Repository Plan capture always adds a central discovery record and can add specification siblings. No public command or dependency is added. The version changes from `0.19.0` to `0.19.1`.

## Outcomes

The accepted Plan from this chat is now exact and discoverable in both required locations. The installed toolkit captures a real Codex Plan during the following prompt hook. Doctor reports version `0.19.1` ready.

The full review was clean. A later test-only delta corrected the app-server capability and observation boundary. Its delta review was also clean.

The final installer delta gives `SessionEnd` its documented 3-second maximum through one shared timeout owner. Its review was clean. Live installation, Doctor, and a fresh Codex app-server startup passed without the clamp warning.

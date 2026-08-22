<proposed_plan>
# CPK-041 — Explain Code Consequences Before Decisions

## Summary

Material code decisions must explain their visible result and implementation shape before asking the user to choose.

Simple English will control the wording. The decision-handoff rule will control the required facts.

Release this feature as version `0.20.0`.

## Implementation Changes

- Create branch `cpk-041-implementation-aware-decisions` from the reviewed CPK-040 commit.
- Keep `decision-handoffs.md` as the single rule owner. Add no new skill.
- Route Design Preflight questions through this owner.
- Require the `simple-english` skill before drafting the decision brief or choice widget.
- Keep the existing decision labels and material-choice boundary.

For each option, require these facts:

- `What you get`: Explain the visible behavior in plain language.
- `Code change`: State whether the option reuses, extends, replaces, or adds an owner.
- `Source`: Name the plain code role, followed by its file or symbol.
- `New moving parts`: Name new state, callbacks, workers, storage, queues, or state machines. State when none are added.
- `Tests and maintenance`: State the new proof cases, compatibility effects, and ongoing lifecycle obligations.

Do not estimate line counts. Classify the change as local, multi-owner, or a new subsystem.

Investigate each option before asking. If source does not prove an impact, label it `unknown` and explain the missing evidence.

Show the complete brief before `request_user_input`. The widget only collects the choice and never serves as the sole explanation.

After selection, record the chosen behavior and implementation shape in the active ExecPlan.

## Interfaces and Records

- The installed decision-handoff contract gains source-backed implementation consequences.
- No CLI, runtime API, dependency, or persistent product state changes.
- Create the CPK-041 ExecPlan and make CPK-041 the only Active roadmap task.
- Keep CPK-008’s trigger, fixed labels, and exclusions. Extend its incomplete definition of an option’s “effect.”
- Keep CPK-040 Plan capture unchanged.

## Test Plan

- Prove that Design Preflight routes material questions to the decision-handoff owner.
- Prove that the owner invokes Simple English for the brief and widget.
- Prove that each option includes visible behavior, code shape, source, moving parts, and maintenance effects.
- Prove that the widget cannot replace the complete brief.
- Prove that routine questions and discoverable facts remain concise.
- Prove that unsupported code-impact claims use `unknown`.
- Prove that the rule requires no line estimate or new skill.
- Run the full toolkit suite, rule-owner checks, link checks, manifest checks, and diff checks.
- Run scope-bound adversarial review.
- Install the reviewed toolkit and run Doctor.
- Use a clean Codex planning session to repeat the supplied paging decision. Confirm that the new brief is understandable before the choice widget appears.
- Create one local checkpoint commit. Do not publish without a later request.

## Assumptions

- “Code shape only” means structural impact without line estimates.
- Source anchors use a plain role first and a file or symbol second.
- Material technical choices receive the full brief. Minor preferences do not.
- CPK-041 uses a branch because it has one implementation stream and no parallel writers.

## Prior Plan Reconciliation

- CPK-008 is carried. Its material-choice trigger, labels, and exclusions remain authoritative.
- CPK-040 is carried. Its Plan capture and delivery constraints remain unchanged.

<!-- cpk-plan-spec: docs/plans/cpk-008-decision-handoffs.md -->
</proposed_plan>
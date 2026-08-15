# Playground

Use a disposable repository or a branch that you can reset.

The goal is not to prove that the kit is universally better. The goal is to learn whether it helps your real work.

## 1. Plain explanation

Ask Codex:

```text
Explain how this repository starts. Use plain language. Tell me which file runs first and what it calls next.
```

Look for:

- The answer starts with the main path.
- Technical terms have short definitions.
- Commands and identifiers stay exact.
- The response does not become an essay.

## 2. Ponytail bug fix

Give Codex a small bug with two or more callers.

Ask:

```text
Find the root cause. Use Ponytail full. Make the smallest correct fix and leave one focused check.
```

Look for:

- Codex reads callers before editing.
- It fixes one shared owner instead of every symptom.
- It adds no speculative abstraction or dependency.
- It does not remove validation or error handling.

## 3. Design preflight

Choose a multi-file change with unclear ownership or a public interface.

Ask:

```text
Use design-preflight. Find the existing owner. Define the behavior floor and implementation ceiling. Do not implement yet.
```

Look for:

- The card cites the current execution path.
- Authority and projections are separate.
- The card states the supported operating model.
- Exceptional conditions pass all four true or false checks.
- The result names one smallest implementation.
- Duplicate ownership in supported normal use stops the work.

## 4. ExecPlan handoff

After an accepted preflight, ask:

```text
Put the accepted preflight into one ExecPlan. Do not create another task plan. Keep exact checks and the scope ceiling.
```

Look for:

- One ExecPlan, not separate brief, plan, and task systems.
- Clear required behavior and scope ceiling.
- Checks name the production break they can catch.
- The implementation stops at the stated ceiling.

## 5. Clean-context review

Make a non-trivial code change.

Ask:

```text
Run adversarial-review. Use one fresh subagent. Do not give it the implementation conversation. Apply the supported-model gate.
```

Look for:

- The reviewer gets the actual diff and source.
- Every finding has four true supported-model results.
- Findings include a concrete trigger, path, and wrong outcome.
- Environmental speculation is dropped.
- Fixes use Ponytail and target one root cause.
- Each new pass uses fresh context.
- A third counted production-code-defect pass stops instead of creating another patch.

## 6. Roadmap lifecycle

In a repository with `docs/roadmap.md`, ask Codex to implement one planned task.

Look for:

- The task becomes the only Active task before the first implementation edit.
- Task order, scope, and blockers change when the work changes.
- Documentation is final before review.
- The task stays Active until review is clean. Then it moves to a terminal section.
- Installation and repository setup never create or replace the roadmap.

## 7. Architecture breaker

Create or choose a change with two writers or unclear state authority.

Ask for Design Preflight or Adversarial Review.

Look for:

- The agent identifies the duplicate owner or writer.
- It does not add guards to every caller.
- It stops and asks for the ownership decision.

## 8. Research

Choose one real technical decision.

Ask:

```text
Use research-first. Check this repository first. Compare no more than four real options. Use primary sources. Pick one and state when we must revisit it.
```

Look for:

- Existing project choices appear before new tools.
- Sources are current and relevant.
- Facts and inference are separate.
- The answer selects one option instead of producing a shopping list.

## 9. Property testing, optional

Choose a parser, serializer, validator, normalizer, or state transition function.

Install the Trail of Bits `property-based-testing` plugin or ask Codex to apply the technique directly.

Look for:

- Properties are stated before examples.
- Generated cases include boundaries and malformed inputs.
- The check finds a case that hand-written examples missed, or proves the existing cases sufficient.

## 10. Documentation guard

Make a behavior or configuration change and do not mention documentation.

Look for:

- Codex updates the existing authoritative document, or gives one short reason that no update is needed.
- The final response has a `Docs:` line.
- No filler document appears only to satisfy the hook.
- No documentation changes occur after review or commit.

## Keep a simple score

After each real task, record:

```text
Task:
Preflight used: yes / no / not needed
Useful RepoWise context: yes / no / unavailable
Unneeded code avoided:
Missed edge case before review:
Validated production-code defects by pass: 0 / 1 / 2 / 3-stop
Architecture breaker fired: yes / no
Docs stayed correct: yes / no
Explanation was clear: yes / no
Extra turns caused by the kit:
Estimated turns saved later:
Would I keep this setup: yes / no
```

Ten real tasks will teach more than one generated toy application.

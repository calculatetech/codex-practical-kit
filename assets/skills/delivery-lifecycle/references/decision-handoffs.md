<!-- cpk-rule-owner: decision-handoffs -->
<!-- cpk-rule-guard: A material decision changes scope, architecture, authority, exposure, or the delivered result. -->
<!-- cpk-rule-guard: Use these labels in order: `Decision`, `Term`, `Trigger`, `Likelihood`, `Current exposure`, `Options`, `Recommendation`, and `Question`. -->
<!-- cpk-rule-guard: Before a material technical decision, explain each option's visible result, code shape, source, new parts, proof, and maintenance cost. -->
<!-- cpk-rule-guard: Show the complete decision brief before an interactive choice tool. The tool only collects the answer. -->
<!-- cpk-rule-guard: Ask at most three independent material questions in one batch. -->

# Decision handoffs

A material decision changes scope, architecture, authority, exposure, or the delivered result.

Before you request direction, investigate discoverable facts. Exclude unsupported conditions.

Order material questions by their prerequisites. Ask a dependent question only after its prerequisite is settled. Ask at most three independent material questions in one batch.

After each reply or source discovery, reassess the remaining questions. Keep partial answers and remove settled or obsolete questions. Ask only the next unresolved material choices. Stop the interview when the required behavior, scope, and acceptance are settled.

Do not use a full handoff for discoverable facts, routine values, status questions, or minor preferences.

Apply `simple-english` before you draft the decision brief or interactive choice text.

Use these labels in order: `Decision`, `Term`, `Trigger`, `Likelihood`, `Current exposure`, `Options`, `Recommendation`, and `Question`.

Use `Term` only when the reader needs a definition.

Define the term before you use it elsewhere.

Treat an internal code term as unfamiliar when the user cannot see it in the product.

Define it before use, or replace it with the visible behavior.

For `Likelihood`, use `already present`, `likely`, `unlikely`, or `unknown`. Give the supporting evidence. Do not invent a numeric probability.

For `Current exposure`, use `yes`, `no`, or `unknown`. Give one factual reason.

Give two or three practical options. Do not add a filler option.

Before a material technical decision, explain each option's visible result, code shape, source, new parts, proof, and maintenance cost.

Use these fields for each option:

- `What you get`: Explain the visible behavior in plain language.
- `Code change`: State whether the option reuses, extends, replaces, or adds a code owner. Classify it as local, multi-owner, or a new subsystem.
- `Source`: Name the code role in plain language. Then give its file or symbol in parentheses.
- `New moving parts`: Name new state, callbacks, workers, storage, queues, state machines, or lifecycles. If none exist, state that fact.
- `Tests and maintenance`: State the required proof, compatibility effect, and ongoing lifecycle work.

Do not estimate line counts. Use the structural impact instead.

Investigate each option against current source before you ask. If source cannot prove an impact, write `unknown` and name the missing evidence.

Show the complete decision brief before an interactive choice tool. The tool only collects the answer.

Keep the tool question and option descriptions short. Do not make the user infer implementation consequences from the tool text or an earlier technical diagnostic.

Recommend one option. If evidence does not distinguish them, select the smallest reversible option that meets the requirement.

If no real choice exists, state the required action. Do not ask for direction.

End each decision brief with one exact question.

After the user selects a material technical option, record its visible behavior and implementation shape in the active ExecPlan before implementation.

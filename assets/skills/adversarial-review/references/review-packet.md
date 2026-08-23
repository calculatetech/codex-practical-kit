# Review packet

Keep the packet factual and compact.

## Intent

Quote or link the accepted requirement, ExecPlan, specification, or user request.

## Scope

- Review mode: `full | checkpoint | delta | coherence`
- Base revision:
- Previous reviewed tree, or `none`:
- Current staged tree:
- Diff command:
- Changed paths:
- Excluded paths and reason:

## Checkpoint

- Stable subtask identifier, or `none`:
- Previous accepted checkpoint, or `none`:
- Pre-stage tracked-change classification:
- `git diff --quiet` result:
- Prior validated findings:
- Prior finding disposition:
- Direct impact added for a delta review:
- Checkpoint invalidation reason, or `none`:

## Product boundary

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](../../design-preflight/references/scope-boundaries.md)

## Task boundary facts

- Authoritative product specification:
- Current production use cases:
- Inherited-specification conflicts resolved:

| Relevant owner | Classification | Linked product fact |
| --- | --- | --- |
|  |  |  |

- Changed production entry points:
- Task-visible outcomes:

## Diff

Give the reviewer the actual relevant diff. Do not replace it with prose.

## Execution path

List exact source locations for:

- Entry point.
- Outcome owner.
- State owner.
- Readers and writers.
- Callers and callees.
- External, process, thread, FFI, database, or provider boundaries.

Write `unknown` when the source does not establish a fact.

## Verification already run

Copy the accepted Scenario Proof mapping. For every retained scenario, include its discriminator, contrast, production path, required oracle, actual runnable test or command, and result. An aggregate suite result is supporting evidence only.

Apply [Scenario discrimination](../../design-preflight/references/scenario-discrimination.md) to the mapping.

For each command, include:

- Command.
- Exit status.
- Short result.
- Which behavior it can fail on.

## Project standards

Include only the AGENTS, CLAUDE, lint, test, architecture, or API rules that govern the reviewed files.

## RepoWise observations

Apply [Repository knowledge](../../repository-knowledge/SKILL.md).

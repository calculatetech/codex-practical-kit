# Review record

Keep the record factual and compact. Native discovery receives only the synthetic commit.

## Native discovery target

- Accepted intent:
- Intent source:
- Review mode: `full | checkpoint | delta | final`
- Task base:
- Previous reviewed candidate, or `none`:
- Previous accepted checkpoint, or `none`:
- Selected parent:
- Current staged tree:
- Synthetic commit:
- Pre-review `git diff --quiet` result:
- Post-review staged tree:
- Post-review `git diff --quiet` result:
- Native command result:

The synthetic commit message contains only Accepted intent and Intent source. Do not send this complete record to native discovery. Do not add exclusions, scenario conclusions, findings, correction directions, or preferred outcomes to the native input.

## Checkpoint

- Stable subtask identifier, or `none`:
- Pre-stage tracked-change classification:
- Prior validated findings:
- Prior finding disposition:
- Direct impact added for a delta review:
- Checkpoint invalidation reason, or `none`:

## Product boundary

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](../../design-preflight/references/scope-boundaries.md)

## Coordinator adjudication

- Authoritative product specification:
- Current production use cases:
- Inherited-specification conflicts resolved:

| Relevant owner | Classification | Linked product fact |
| --- | --- | --- |
|  |  |  |

- Changed production entry points:
- Task-visible outcomes:
- Supported-model result:
- Finding adjudication records:
- Atomic correction result:

Read cited source and relevant callers before adjudication. Write `unknown` when source does not establish a fact.

## Verification already run

Record the accepted Scenario Proof mapping and result when one exists.

## Scenario discrimination

<!-- cpk-rule-route-only: scenario-discrimination -->
[Scenario discrimination](../../design-preflight/references/scenario-discrimination.md)

## Project standards

List only rules that govern the reviewed files.

## RepoWise observations

Apply [Repository knowledge](../../repository-knowledge/SKILL.md). Record the indexed revision and freshness.

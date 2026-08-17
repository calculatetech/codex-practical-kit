# Preflight card

Keep the complete card under 80 lines.

## Goal

State one observable outcome.

## Product boundary

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](scope-boundaries.md)

## Task boundary facts

- Authoritative product specification:
- Current production use cases:
- Inherited-specification conflicts:

| Relevant owner | Classification | Linked product fact |
| --- | --- | --- |
|  |  |  |

## Supported operating model

<!-- cpk-rule-route-only: supported-model -->
[Supported model](supported-model.md)

## Existing owner

- Entry point:
- Outcome owner:
- Authoritative state:
- Readers and writers:
- Boundaries:

Cite source. Write `unknown` when source does not prove a claim.

## Normal-use behavior floor

List the task-specific `applicable` behavior and `contract-gap` results from Supported model.

## Scope ceiling

List work that must not exist. Include excluded conditions, abstractions, dependencies, services, and rewrites.

## Smallest implementation

Name the existing owner to change and the minimum supporting edits.

## Scenario Proof

Apply [Scenario discrimination](scenario-discrimination.md) to every retained scenario. Apply [Owner composition](owner-composition.md) and [Full-set results](full-set-results.md) when they are applicable.

For each runtime outcome classified `composes`, record:

- Requirement and source.
- Entry point, relevant gates, and terminal owner.
- Applicable input-domain, path-and-transition, and collection cases.
- Expected result, or `undefined — decision required`.
- One short reason for each inapplicable lens.

Do not create a Cartesian product of inputs.

Before implementation, complete the first six columns for each retained scenario. Before review, record the actual runnable test or command and its result.

| Scenario | Discriminator | Contrast | Production path | Required oracle | Runnable test or command | Result |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Checks

List supporting commands. Do not replace the scenario mapping with an aggregate test count or suite result.

## Open decisions

List only decisions that can change the implementation. Do not list excluded risks.

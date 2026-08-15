# Preflight card

Keep the complete card under 80 lines.

## Goal

State one observable outcome.

## Product boundary

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](../../codex-practical-kit-rules/references/scope-boundaries.md)

## Task boundary facts

- Authoritative product specification:
- Current production use cases:
- Inherited-specification conflicts:

| Relevant owner | Classification | Linked product fact |
| --- | --- | --- |
|  |  |  |

## Supported operating model

<!-- cpk-rule-route-only: supported-model -->
[Supported model](../../codex-practical-kit-rules/references/supported-model.md)

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

Apply [Owner composition](../../codex-practical-kit-rules/references/owner-composition.md) and [Full-set results](../../codex-practical-kit-rules/references/full-set-results.md) when they are applicable.

For each runtime outcome classified `composes`, record:

- Requirement and source.
- Entry point, relevant gates, and terminal owner.
- Applicable input-domain, path-and-transition, and collection cases.
- Expected result, or `undefined — decision required`.
- One runnable check for each retained case.
- One short reason for each inapplicable lens.

Do not create a Cartesian product of inputs.

## Checks

List exact commands and normal-use scenarios. Each check must name the behavior that it can fail on.

## Open decisions

List only decisions that can change the implementation. Do not list excluded risks.

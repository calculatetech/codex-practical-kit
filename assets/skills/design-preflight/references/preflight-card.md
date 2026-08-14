# Preflight card

Keep the complete card under 80 lines.

## Goal

State one observable outcome.

## Supported operating model

State the users, writers, platform, and normal environment. List an exceptional condition only when the task includes it.

## Existing owner

- Entry point:
- Outcome owner:
- Authoritative state:
- Readers and writers:
- Boundaries:

Cite source. Write `unknown` when source does not prove a claim.

## Normal-use behavior floor

List only behavior that passes all four checks:

- It occurs in supported normal use.
- The project controls it.
- The condition or planned trigger is feasible without fault injection.
- An explicit requirement defines the result.

## Scope ceiling

List work that must not exist. Include excluded conditions, abstractions, dependencies, services, and rewrites.

## Smallest implementation

Name the existing owner to change and the minimum supporting edits.

## Scenario Proof

For each runtime outcome, record:

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

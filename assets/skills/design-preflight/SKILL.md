---
name: design-preflight
description: >
  Define the normal-use behavior floor and implementation ceiling before a
  non-trivial change. Use repository evidence, exclude unsupported conditions,
  and challenge the design once only when ownership or scope remains unclear.
license: MIT
---

# Design preflight

Understand the normal path before implementation. Do not turn possible environmental conditions into requirements.

## Use this skill when

Use it for a multi-file change, a public interface, persistent product state, an external service, or unclear ownership.

Skip it for a small change with one proven owner and one direct check.

## Supported-model gate

Write the project's declared operating model first. Include only conditions that occur in that model or that the user explicitly requested.

For each proposed requirement, answer:

1. Does the condition occur during supported normal use?
2. Does the project control the condition and result?
3. Can the current path reproduce the problem without fault injection?
4. Does an explicit requirement define the expected result?

Keep the requirement only when all answers are `true`.

Do not add I/O faults, permissions, links, concurrency, interruption, retry, restart, recovery, submodules, or outside influence by default.

## Define the change

Read the entry point, outcome owner, state owner, callers, checks, and documentation. Use RepoWise only when its current index gives useful leads.

Write one preflight card from `references/preflight-card.md`. It must contain:

- One required outcome.
- The existing owner.
- The normal-use behavior floor.
- The hard scope ceiling.
- Applicable failures only.
- Exact checks.

Use a Task Brief when the accepted card needs a durable handoff. Do not create a second specification owner.

## Optional challenge

The coordinator owns the preflight. Spawn one fresh read-only reviewer only when normal-use ownership or scope remains unclear.

Give that reviewer the card, exact source, and supported model. Do not ask for speculative failure discovery.

Apply the supported-model gate to every response. Revise the card once. Do not start a review loop.

## Stop condition

Stop for human direction only when supported normal use has duplicate authority, duplicate writers, or an unresolved public contract.

Finish with:

- `Preflight: ready — <smallest implementation path>.`
- `Preflight: stopped — architecture decision required: <decision>.`

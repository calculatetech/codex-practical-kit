---
name: task-brief
description: >
  Create one small implementation brief for a multi-file feature, stateful
  behavior, failure-prone change, or unclear task. Define the goal, required
  behavior, forbidden scope, checks, and unknowns without creating a full
  specification system. Use the accepted design preflight as input. Do not use
  for a small obvious fix.
license: MIT
---

# Task brief

Use the smallest contract that prevents guessing and scope creep.

## Do not use this for

- A typo.
- A one-line configuration change.
- A local bug with a clear root cause and one obvious check.

## Before the brief

For non-trivial work, use `design-preflight` first. Put its accepted outcome into this brief. Do not preserve a second preflight document unless it records a durable architecture decision.

## Brief format

Keep the complete brief under 80 lines.

### Goal

One outcome. State who benefits and what changes.

### Existing owner

Name the entry point, operation owner, authoritative state, and important boundaries. Cite source paths. Write `unknown` when the source does not prove a claim.

### Must work

List the observable behavior that the implementation must provide. Include an exceptional condition only when supported normal use can encounter it.

Apply four true or false checks. The condition must occur in normal use, be project-controlled, reproduce without fault injection, and violate an explicit requirement.

### Must not change

List protected behavior and the scope ceiling. Name services, abstractions, dependencies, rewrites, duplicate owners, and speculative extension points that are not authorized.

### Checks

List the smallest commands or scenarios that prove the required behavior. Each check must name the production break that it can catch. Do not use vague text such as “test thoroughly.”

### Unknowns

List only unknowns that can change the implementation. Resolve a safe default when possible.

## Handoff

After the brief is accepted or the safe defaults are clear:

1. Use Ponytail.
2. Implement only the `Must work` items.
3. Respect `Must not change` as a hard ceiling.
4. Run the `Checks`.
5. Use `docs-maintainer` before review.
6. Use `adversarial-review` with one fresh reviewer.

Do not create separate spec, plan, preflight, and task files for the same work.

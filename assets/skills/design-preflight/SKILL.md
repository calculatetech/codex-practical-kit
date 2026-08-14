---
name: design-preflight
description: >
  Define the normal-use behavior floor and implementation ceiling before a
  non-trivial change. Derive runtime scenarios systematically, use one
  independent planning challenge, exclude unsupported conditions, and stop on
  unresolved normal-use contracts.
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
3. Can the condition or planned trigger occur without fault injection?
4. Does an explicit requirement define the expected result?

Keep the requirement only when all answers are `true`.

Do not add I/O faults, permissions, links, concurrency, interruption, retry, restart, recovery, submodules, or outside influence by default.

## Define the change

Read the entry point, outcome owner, state owner, callers, checks, and documentation. Use RepoWise only when its current index gives useful leads.

For non-trivial runtime behavior, derive a Scenario Proof with three lenses:

- Input domain: applicable presence, syntax, semantic validity, range boundaries, and explicit relationships.
- Path and transition: selectors, filters, transformations, controlled boundaries, state changes, and terminal obligations.
- Collection semantics: supported empty input, one record, duplicates, a duplicate prefix with a later counterexample, and every record that owes a result.

Use source predicates and requirements. Select the minimum cases that exercise each distinct outcome or disprove an invariant. Do not create a Cartesian product.

When success depends on every matching record, use the complete set or an operation that preserves the full-set result. Do not limit raw records before grouping, deduplication, or aggregation. Test duplicate prefix values followed by a later counterexample.

Write one preflight card from `references/preflight-card.md`. It must contain:

- One required outcome.
- The existing owner.
- The normal-use behavior floor.
- The hard scope ceiling.
- Applicable failures only.
- The Scenario Proof for non-trivial runtime behavior.
- Exact checks.

Every non-trivial runtime preflight requires one task ExecPlan. Merge the accepted card into it before implementation. For other ExecPlan work, do the same. Do not preserve a second planning artifact.

## Independent challenge

The coordinator owns the preflight. For non-trivial runtime behavior, spawn one fresh read-only planning challenger with no inherited task conversation. A small change that skips Design Preflight also skips this challenge.

Give the challenger raw requirements, the supported model, exclusions, exact source, entry and terminal owners, selectors, filters, state writers, and current tests.

Do not give it the coordinator's card, Scenario Proof, implementation, known edge cases, prior diagnostics, reviewer corrections, severity, or preferred outcome.

Require the JSON in `references/preflight-review.md`. Compare its independent result with the coordinator's derivation once. Merge supported scenarios into the card and ExecPlan. Do not start a review loop.

For scenario applicability, require normal use, project control, a feasible trigger without fault injection, and an explicit result. Record a contract gap when the first three answers are `true` but no explicit result exists. Exclude the result when any of the first three answers is `false`.

For a non-runtime preflight, use this same single challenge only when normal-use ownership or scope remains unclear.

## Stop condition

Stop for human direction when supported normal use has duplicate authority, duplicate writers, or an unresolved public contract. Do not invent an outcome for a contract gap.

Finish with:

- `Preflight: ready — <smallest implementation path>.`
- `Preflight: stopped — architecture decision required: <decision>.`

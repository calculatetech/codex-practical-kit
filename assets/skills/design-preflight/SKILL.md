---
name: design-preflight
description: >
  Define the normal-use behavior floor and implementation ceiling before a
  non-trivial change. Use automatically before implementation or an accepted
  review correction for a multi-file change, public interface, persistent
  product state, external service, or unclear ownership. Use even when Plan
  Mode was not requested and the user did not name this skill.
license: MIT
---

<!-- cpk-rule-owner: design-preflight -->
<!-- cpk-rule-guard: Use the same fresh read-only challenger for an unanchored derivation and an informed adversarial challenge. -->

# Design preflight

Understand the normal path before implementation. Do not turn possible environmental conditions into requirements.

## Phase mode

<!-- cpk-rule-route-only: implementation-modes -->
[Implementation modes](../delivery-lifecycle/references/implementation-modes.md)

## Repository context

<!-- cpk-rule-route-only: repository-knowledge -->
[Repository Knowledge](../repository-knowledge/SKILL.md)

## Entry gate

Apply the trigger in this skill description before the first implementation edit. Plan Mode and an explicit skill request are not prerequisites.

Apply the same entry gate to an accepted correction. Runtime paths, retained state, reopening sources, terminal owners, event ordering, and shared-signal classification are common examples, not an exhaustive gate.

Skip it for a small change with one proven owner and one direct check. The small-change exception still applies to an accepted correction unless the task adds or changes a behavioral boundary.

## Scope gate

<!-- cpk-rule-route-only: scope-boundaries -->
[Scope boundaries](references/scope-boundaries.md)

## Supported-model gate

<!-- cpk-rule-route-only: supported-model -->
[Supported model](references/supported-model.md)

## Define the change

Read the entry point, outcome owner, state owner, callers, checks, and documentation.

For non-trivial runtime behavior, derive a Scenario Proof with three lenses:

- Input domain: applicable presence, syntax, semantic validity, range boundaries, and explicit relationships.
- Path and transition: selectors, filters, transformations, controlled boundaries, state changes, and terminal obligations.
- Collection semantics: supported empty input, one record, duplicates, a duplicate prefix with a later counterexample, and every record that owes a result.

Apply [Scenario discrimination](references/scenario-discrimination.md) to every retained scenario. Apply [Owner composition](references/owner-composition.md) to the path-and-transition lens. Apply [Full-set results](references/full-set-results.md) to collection semantics.

Use Scenario discrimination to inventory every authoritative source clause when the task adds or changes a behavioral boundary. Merge the accepted inventory into the task ExecPlan.

Close each retained path-and-transition scenario over every supported event that can act on its state until the required terminal result. Do not split one stateful sequence into component scenarios.

Use source predicates and requirements. Select the minimum cases that exercise each distinct outcome or disprove an invariant. Do not create a Cartesian product.

Write one preflight card from `references/preflight-card.md`. It must contain:

- One required outcome.
- The product boundary source and owner classifications.
- The existing owner.
- The normal-use behavior floor.
- The hard scope ceiling.
- Applicable failures only.
- The Scenario Proof for non-trivial runtime behavior.
- A discriminator, contrast, planned production path, required oracle, and runnable check for each retained scenario.

Every non-trivial runtime preflight requires one task ExecPlan. Merge the accepted card into it before implementation. For other ExecPlan work, do the same. Do not preserve a second planning artifact.

## Two-phase challenge

The coordinator owns the preflight. For non-trivial runtime behavior or a task that adds or changes a behavioral boundary, spawn one fresh read-only planning challenger with no inherited task conversation. Use the same fresh read-only challenger for an unanchored derivation and an informed adversarial challenge. A small change that skips Design Preflight also skips this challenge.

For an accepted correction that passes the entry gate, spawn one fresh read-only planning challenger even when the correction is not runtime behavior.

### Phase 1: independent derivation

Give the challenger raw requirements, the complete authoritative source set, the supported model, exact source, owners, selectors, filters, state writers, current tests, and applicable focused rule links. Require it to enumerate source clauses before it derives scenarios.

Keep Phase 1 unanchored. Do not give it the coordinator's card, decisions, assumptions, exclusions, Scenario Proof, implementation, known edge cases, prior diagnostics, reviewer corrections, severity, research result, or preferred outcome.

Give a correction challenger the accepted finding, original requirements, current source, and current tests. Do not give it the coordinator's preferred fix in Phase 1. Require it to derive the smallest complete correction and the runnable checks before implementation.

Require the Phase 1 JSON in `references/preflight-review.md`.

### Phase 2: adversarial challenge

After Phase 1, give the same challenger the coordinator's complete card and Scenario Proof. Include decisions, assumptions, exclusions, diagnostics, known edge cases, and the research result when one exists.

Require the Phase 2 JSON in `references/preflight-review.md`. The challenger must look for missing scenarios, unsupported assumptions, invalid exclusions, weak proof cases, and contract gaps. It must challenge the coordinator's actual claims, not repeat Phase 1.

Compare both results with the coordinator's derivation once. Merge each supported finding into the card and ExecPlan. Record a source-backed rationale for each rejected finding. Stop on an unresolved contract gap. Do not start a review loop. Empty finding arrays are valid.

Use the canonical classifications. Merge `applicable` scenarios. Record `contract-gap` scenarios. Omit `excluded` scenarios.

Before implementation, each retained scenario must have a planned runnable check and oracle. Before review, update the mapping with the actual test or command and its result. A suite pass or test count does not replace this mapping.

For an initial non-runtime preflight that changes no behavioral boundary, use this same single challenge only when normal-use ownership or scope remains unclear.

## Human decision

<!-- cpk-rule-route-only: decision-handoffs -->
[Decision handoffs](../delivery-lifecycle/references/decision-handoffs.md)

## Stop condition

Stop for human direction when supported normal use has duplicate authority, duplicate writers, or an unresolved public contract. Do not invent an outcome for a contract gap.

Finish with:

- `Preflight: ready — <smallest implementation path>.`
- `Preflight: stopped — architecture decision required: <decision>.`

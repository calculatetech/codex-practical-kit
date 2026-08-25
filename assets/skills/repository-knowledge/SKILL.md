---
name: repository-knowledge
description: >
  Use RepoWise for every new repository lookup throughout a task, including
  after no-llm-provider or automatic compaction. Resolve symbols, paths,
  owners, callers, callees, and relationships before broad source exploration.
license: MIT
---

<!-- cpk-rule-owner: repository-knowledge -->
<!-- cpk-rule-guard: Use RepoWise before broad repository exploration. -->
<!-- cpk-rule-guard: Resolve exact identifiers through `search_codebase(mode="symbol")` and `get_symbol` before native search. -->
<!-- cpk-rule-guard: A verified `get_symbol` body is source confirmation; do not read it again. -->
<!-- cpk-rule-guard: After `no-llm-provider`, do not call `get_answer` again in the same Codex session. -->
<!-- cpk-rule-guard: After `no-llm-provider`, continue each new lookup through indexed RepoWise tools. -->
<!-- cpk-rule-guard: If RepoWise fails, stop and report the missing code graph. -->
<!-- cpk-rule-guard: Use RepoWise for each new repository lookup throughout a task. -->

# Repository knowledge

Use RepoWise before broad repository exploration.

Use RepoWise for each new repository lookup throughout a task. Initial orientation does not satisfy a later lookup.

Reuse a verified result that is already in context. Do not repeat an indexed lookup without a new question or changed source.

For an unfamiliar repository, call `get_overview` once.

Route by the target you have:

- Resolve exact identifiers through `search_codebase(mode="symbol")` and `get_symbol` before native search.
- Use `get_context` for known paths, modules, callers, callees, ownership, or structure. Batch related targets.
- Use `get_answer` only for conceptual how or why questions.

When `get_answer` reports `no-llm-provider`, use its complete candidate set to select a symbol or path. Prefer an exact symbol or path over a generic page. `no-llm-provider` means that synthesis is unavailable. RepoWise is still available.

After `no-llm-provider`, continue each new lookup through indexed RepoWise tools. After `no-llm-provider`, do not call `get_answer` again in the same Codex session. For each later conceptual question, use `search_codebase` with automatic routing. Then use `get_context` or `get_symbol` for the selected path or symbol. A new session can use a provider that the user configured later.

Automatic compaction does not end this route. Apply this skill again before the next repository lookup and keep it active until the task ends.

If an indexed lookup has no useful result, make one more query with the strongest known identifier or path. Then use focused native search. Preserve ambiguous exact candidates until path, signature, caller, or task evidence resolves them.

A verified `get_symbol` body is source confirmation; do not read it again. Use its continuation when it is truncated. Read a focused source range when RepoWise reports approximate bounds or when the task needs non-indexed text or wider edit context. Treat inferred relationships as leads until source confirms the relevant behavior.

Automatic startup and watch updates keep normal work current. If RepoWise still reports a stale index, run `repowise update --index-only --no-agents --no-workspace` once before relying on absence or relationships.

Record the indexed revision and freshness in a review packet. A stale index cannot prove absence.

If RepoWise fails, stop and report the missing code graph.

## Write authority

<!-- cpk-rule-route-only: delivery-lifecycle -->
[Delivery lifecycle](../delivery-lifecycle/references/delivery-lifecycle.md)

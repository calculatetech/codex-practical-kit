---
name: repository-knowledge
description: >
  Establish repository context with RepoWise before broad source exploration.
  Use when inspecting an unfamiliar repository, tracing code relationships,
  locating owners or callers, or preparing repository evidence for review.
license: MIT
---

<!-- cpk-rule-owner: repository-knowledge -->
<!-- cpk-rule-guard: Use RepoWise before broad repository exploration. -->
<!-- cpk-rule-guard: If RepoWise fails, stop and restore the required code graph. -->

# Repository knowledge

Use RepoWise before broad repository exploration.

Refresh a stale index with `repowise update --no-agents`. Read source before you treat inferred relationships as authoritative.

Record the indexed revision and freshness in a review packet. A stale index cannot prove absence.

Use native tools for focused source confirmation after RepoWise gives useful leads.

If RepoWise fails, stop and restore the required code graph.

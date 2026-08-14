---
name: docs-maintainer
description: >
  Keep repository documentation correct after code changes. Inspect the actual
  diff, find the authoritative document, update only what became wrong, use
  Simple English, finalize roadmap state before review, and report when no
  documentation change is needed. Use before review and commit for any change
  that affects behavior, setup, commands, configuration, public interfaces,
  operations, or architecture.
license: MIT
---

# Documentation maintainer

Keep the documentation true. Do not write documentation to prove that you wrote documentation.

## Process

1. Read the complete candidate and the files that own the changed behavior.
2. Identify the authoritative document for that behavior.
3. Check these surfaces when relevant:
   - README and getting-started steps.
   - User commands and examples.
   - Configuration names, defaults, and environment variables.
   - Public API and error behavior.
   - Runbooks, migrations, recovery steps, and operational limits.
   - Architecture or decision records for durable design changes.
4. Update the smallest existing document that owns the fact.
5. Remove or correct stale statements instead of adding a second explanation.
6. Use the `simple-english` skill in pragmatic mode.
7. Keep code, commands, paths, identifiers, and quoted errors exact.
8. Make sure that examples can still run as written.
9. If `docs/roadmap.md` exists, finish all other documentation first.
10. Use `roadmap-maintainer` for the terminal task transition.
11. Reread the final roadmap. Do not change its lifecycle fields through this skill.
12. Finish before adversarial review and commit.

After a clean review, do not change documentation. If any candidate file changes, that clean review is invalid and commit is blocked until the complete candidate is reviewed again.

## RepoWise

If RepoWise is available, use its context, decision, risk, or affected-test views to find related documentation and owners. Treat the result as evidence, not authority. Read the source before you change a durable claim.

## Do not update documentation when

- The change is internal and does not alter behavior, setup, interfaces, operations, or maintenance.
- An existing comment or test is the correct and sufficient owner.
- The only possible addition is a duplicate description of the code.

## Finish

Return exactly one documentation status line in the final response:

- `Docs: updated <paths or topic>.`
- `Docs: no change needed — <short reason>.`

---
name: research-first
description: >
  Research a technical choice before implementation when the choice is
  unfamiliar, current, high-impact, safety-sensitive, or costly to reverse.
  Check the repository first, prefer primary sources, compare a small number of
  real options, and record a durable decision only when the project needs it.
license: MIT
---

# Research first

Research must reduce uncertainty. It must not create ceremony.

## Use this skill when

- The task depends on a library, standard, product, law, protocol, or tool that can have changed.
- The choice affects architecture, persistence, concurrency, security, recovery, compatibility, or long-term maintenance.
- The problem is unfamiliar and a plausible existing solution can remove custom code.
- A wrong choice is expensive to reverse.

Do not use this skill for a routine fix with a clear local answer.

## Process

1. Read the current repository first.
   - Find the existing owner, dependency, pattern, and constraint.
   - Use RepoWise when its current index can answer the repository question.
2. Write the exact question in one sentence.
3. List the constraints that decide the answer.
4. Inspect two to four viable options. Do not create a long catalog.
5. Prefer these sources in this order:
   - Official documentation and current source code.
   - Standards and specifications.
   - Original research papers, including arXiv when relevant.
   - Maintainer issue and pull-request discussions.
   - Reputable secondary analysis only when primary sources do not answer the question.
6. Check dates, versions, licenses, maintenance, and failure modes.
7. Select one option. State why it wins for this repository.
8. Name the rejected options and the condition that can change the decision.
9. Apply Ponytail. Reuse an existing solution when it satisfies the constraints.

## Durable note

Create `docs/research/<short-name>.md` only when the decision will matter after this task. Use these headings:

- Question
- Repository constraints
- Options
- Evidence
- Decision
- Rejected options
- Revisit when
- Sources

For a temporary or small decision, keep the result in the response.

## Output

Start with the selected option. Use Simple English. Link each material factual claim to a source. Separate facts from inference.

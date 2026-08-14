---
name: roadmap-maintainer
description: >
  Create and maintain the repository roadmap at docs/roadmap.md. Use when the
  user asks to initialize a roadmap, accepts or reorders work, starts an
  implementation task, changes its scope or status, accepts residual risk, or
  completes work. Keep permanent task identifiers and at most one active task.
license: MIT
---

# Roadmap maintainer

Keep `docs/roadmap.md` accurate at each work transition. This file is the human interface for accepted work.

## Authority

- Use `docs/roadmap.md` as the only roadmap authority.
- Do not keep another backlog, task ledger, or roadmap.
- Preserve human notes and accepted decisions unless the user changes them.
- Make roadmap lifecycle edits through this skill. Other skills can request or verify an edit, but they do not own task status.

If the repository has no `docs/roadmap.md`, continue normal work without one. Create it only when the user explicitly requests roadmap initialization.

## Initialize

1. Read repository instructions and existing documentation.
2. Get a short project prefix from the user unless one is unambiguous in those sources.
3. Refuse to replace an existing `docs/roadmap.md`.
4. Copy `assets/roadmap-template.md` to `docs/roadmap.md`.
5. Replace every placeholder before completion.
6. Add only work that the user accepted or that current evidence requires.

Use identifiers in the form `<PREFIX>-NNN`, with at least three digits. Allocate the next number above the highest identifier ever recorded for that prefix. Never fill gaps, rename an identifier, erase task history, or reuse a number.

## Update lifecycle

Update the roadmap when one of these events occurs:

- The user accepts a new task or idea.
- Accepted priority or order changes.
- Implementation starts.
- Accepted scope changes.
- Work becomes blocked or resumes.
- The user accepts a residual risk.
- Validation establishes a terminal candidate.

Plan-only, audit-only, review-only, and documentation-only work does not become Active.

Before the first implementation edit:

1. Reread `docs/roadmap.md`.
2. Apply an exact-context patch that moves the intended task to Active.
3. If the context changed, reread the file and stop for coordination.
4. Reread the result.
5. Start implementation only when the intended task is the sole Active task.

If a different task is Active, do not replace it. Stop and request coordination.

Keep blocked implementation Active. Add the concrete blocker or remaining outcome to its text. When work resumes, use the same identifier.

Record newly discovered work only when it is authorized or supported by concrete evidence. Give it the next permanent identifier and place it in the correct planned section. Do not implement it without authorization.

## Finish a task

Documentation must be final before review and commit.

1. Let Docs Maintainer finish all non-roadmap documentation.
2. Move the Active task to one terminal section.
3. Use Completed when no accepted limitation remains.
4. Use Accepted residual risk when bounded work is complete and the user accepts a documented limitation.
5. Use Declined when the user intentionally does not support the work.
6. Never put one identifier in more than one terminal section.
7. Reread the complete roadmap and make sure that no task is incorrectly Active.
8. Let Docs Maintainer verify the final roadmap without changing its lifecycle fields.
9. Include the final roadmap in the candidate that receives review.

If validation fails, keep the task Active and record the blocker. Do not claim a terminal state.

If review finds a validated defect, that candidate is rejected. Move the task back to Active, make the correction, and finalize all documentation before the next review pass.

After a clean review, do not change code, tests, configuration, documentation, the roadmap, or the checksum manifest. Commit that exact candidate.

## Template

Use `assets/roadmap-template.md`. Keep its section order and status meanings. A repository can add short usage rules, but it must preserve one Active section, the Declined section, and permanent task identifiers.

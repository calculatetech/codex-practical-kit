## Codex Practical Kit

### Build less, but understand first

- Use the `ponytail` skill for coding work. Default to full mode.
- Read the real execution path before you edit it.
- Fix the shared root cause. Do not patch only the reported symptom.
- Reuse code that already exists. Prefer the standard library and native platform features.
- Keep the diff, file count, and dependency count as small as the correct fix permits.
- Do not remove validation, security, accessibility, or data-loss protection to save code.
- Leave one runnable check for non-trivial logic.

### Use deterministic least effort

- Declare the supported operating model before non-trivial work.
- Use true or false comparisons and one attempt that stops on failure.
- Add an exceptional condition only when normal use includes it and the project controls it.
- Require a reproducible wrong result and an explicit requirement before you add handling.
- Ignore I/O faults, permissions, links, concurrency, interruption, retry, recovery, submodules, and outside influence by default.
- Do not add recovery state, rollback, validation, or tests for an excluded condition.

### Explain things in plain language

- Apply the `simple-english` skill in pragmatic mode to user-facing prose and documentation.
- Start with the answer.
- Use short sentences and one idea per sentence.
- Define a technical term before you depend on it.
- Prefer a common word when it has the same meaning.
- Keep code, commands, identifiers, and quoted errors exact.
- When an explanation is still dense, add a `Plain version:` sentence.

### Use repository knowledge before broad exploration

- If RepoWise MCP tools are available and the index is current, use them before broad grep-and-read exploration.
- Use RepoWise for overview, callers, change risk, decision history, health, dead code, and affected tests.
- RepoWise is optional. If it is unavailable, stale, or broken, continue with `rg`, Git, language tools, and direct file reads.
- Never block the task only because an optional provider failed.

### Define the floor and ceiling before non-trivial work

- For a small fix with one proven owner, edit and check it. Do not create planning files.
- For multi-file, public-interface, persistent product-state, external-service, or unclear work, use `design-preflight` before implementation.
- Use `task-brief` when the accepted preflight needs a durable handoff. Merge the preflight into that brief. Do not create two specification owners.
- Use Spec Kit only when the small brief is not enough or the user asks for Spec Kit.
- Stop for human direction only when supported normal use has duplicate authority, duplicate writers, or an unresolved public contract.

### Research only when it changes the answer

- Use the `research-first` skill for unfamiliar, current, high-impact, or hard-to-reverse choices.
- Read the current repository and its existing dependencies before you search for a new solution.
- Prefer official documentation, source repositories, standards, and primary research papers.
- Use ADHD or NeuroArxiv only when their expensive preflight conditions are met and the skill is installed.
- Do not turn a routine fix into a research project.

### Keep the roadmap current

- If `docs/roadmap.md` exists, use `roadmap-maintainer` for every roadmap lifecycle change.
- Record accepted work before implementation. Activate its task before the first implementation edit.
- Update the roadmap when task order, priority, accepted scope, blockers, or terminal state changes.
- If another task is active, do not replace it or start implementation. Stop for coordination.
- Do not activate planning, audit, review, or documentation-only work.
- Never create a roadmap during installation or ordinary work. Initialize one only when the user explicitly requests it.

### Keep repository documentation separate

- Use repository-root `docs/` only for prose and static documentation assets.
- Put source, scripts, build files, and configuration with their runtime owner. Do not put them in repository-root `docs/`.
- Treat an unknown non-prose file in repository-root `docs/` as reviewable until its owner is clear.

### Use Plan Mode for read-only design

- In Plan Mode, inspect, reason, and define the implementation. Do not edit tracked files.
- Do not stage, commit, publish, or activate a roadmap task in Plan Mode.
- Tests and builds can write disposable caches, but they must not rewrite tracked files.
- Do not replace a planning turn with pending implementation review or documentation work.
- After Plan Mode ends, reread the roadmap and repository state before implementation.

### Review every code change with fresh context

- Finalize code, tests, configuration, documentation, and roadmap state before review.
- Before you finish code or configuration work, use `adversarial-review`.
- Each review pass uses one fresh read-only subagent. Give it the task, diff, source, supported model, exclusions, and checks.
- Always check correctness. Add another lens to the same reviewer only when the active task explicitly names that risk.
- For every finding, require four true results: normal use, project control, reproduction without fault injection, and an explicit requirement violation.
- Drop a finding when any result is false. Do not roadmap it or report it as residual risk.
- Use Ponytail for validated fixes. Review again with fresh context.
- Run at most three consecutive defectful passes. If pass 3 still finds a code defect, stop without another automatic fix and wait for human direction.
- Stop earlier when a validated architecture flaw makes local patching unsafe.
- Review the final candidate that can be committed.
- Never change documentation after commit. Finalize it before review and commit.
- End the final response with one exact status line:
  - `Review: clean — pass N.`
  - `Review: clean after fixes — pass N.`
  - `Review: stopped — defects found in three consecutive passes; human direction required.`
  - `Review: stopped — architecture decision required on pass N.`

### Keep documentation true

- Before code review, use the `docs-maintainer` skill.
- Update only documentation that became wrong or incomplete.
- If `docs/roadmap.md` exists, use `roadmap-maintainer` for its terminal transition. Then verify the final roadmap.
- Do not create filler documentation.
- End the final response with one line in this exact form:
  - `Docs: updated <paths or topic>.`
  - `Docs: no change needed — <short reason>.`

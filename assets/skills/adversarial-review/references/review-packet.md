# Review packet

Keep the packet factual and compact.

## Intent

Quote or link the accepted requirement, ExecPlan, specification, or user request.

## Scope

- Base revision:
- Current revision or working tree:
- Changed paths:
- Excluded paths and reason:

## Diff

Give the reviewer the actual relevant diff. Do not replace it with prose.

## Execution path

List exact source locations for:

- Entry point.
- Outcome owner.
- State owner.
- Readers and writers.
- Callers and callees.
- External, process, thread, FFI, database, or provider boundaries.

Write `unknown` when the source does not establish a fact.

## Verification already run

For each command, include:

- Command.
- Exit status.
- Short result.
- Which behavior it can fail on.

## Project standards

Include only the AGENTS, CLAUDE, lint, test, architecture, or API rules that govern the reviewed files.

## RepoWise observations

Apply [Repository knowledge](../../codex-practical-kit-rules/references/repository-knowledge.md).

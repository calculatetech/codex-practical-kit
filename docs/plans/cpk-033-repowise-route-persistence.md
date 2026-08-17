# Keep RepoWise active for the full task

This ExecPlan is a living document until review closure. Maintain it under the global `PLANS.md` rules.

## Purpose / Big Picture

Codex must continue to use RepoWise for each new repository lookup. A missing synthesis provider or an automatic compaction must not change that route. A fresh Codex session demonstrates the result by using indexed retrieval for separate questions without an explicit RepoWise request.

## Progress

- [x] (2026-08-17 08:32Z) Created branch `cpk-033-repowise-route-persistence` from reviewed commit `306577a53136`.
- [x] (2026-08-17 08:32Z) Completed Design Preflight and one independent planning challenge.
- [x] (2026-08-17 08:34Z) Added focused contract tests and captured the expected pre-change errors.
- [x] (2026-08-17 08:37Z) Corrected the owner, activation metadata, persistent router, and compact continuation.
- [x] (2026-08-17 08:39Z) Completed skill validation, focused checks, documentation, and the 40-test suite.
- [x] (2026-08-17 08:40Z) Completed a clean first full review and review closure.

## Surprises & Discoveries

- Observation: RepoWise remained available after Codex stopped using it.
  Evidence: The Meridian transcript contains successful `search_codebase` and `get_symbol` calls before and after the drift.
- Observation: `no-llm-provider` has no route for later conceptual questions.
  Evidence: The owner forbids another `get_answer` call but does not name an indexed replacement for the next question.
- Observation: The current long-lived Codex process uses an older plain RepoWise MCP command.
  Evidence: New managed sessions use the bootstrap command and watcher. The existing process started before the current configuration.

## Decision Log

- Decision: Keep the complete lookup rule in `repository-knowledge`.
  Rationale: This skill is the existing unique owner. AGENTS and the hook remain route-only surfaces.
  Date/Author: 2026-08-17 / Codex
- Decision: Use official skill metadata, AGENTS routing, and `SessionStart` compact context together.
  Rationale: Skill metadata declares the MCP dependency. AGENTS supplies the persistent default. The hook restores the route after compaction.
  Date/Author: 2026-08-17 / Codex
- Decision: Do not block native commands or parse transcripts.
  Rationale: OpenAI documents tool hooks as guardrails and does not define transcript format as a stable interface.
  Date/Author: 2026-08-17 / Codex
- Decision: Use version `0.17.1`.
  Rationale: This task corrects the published behavior of version `0.17.0`.
  Date/Author: 2026-08-17 / Codex

## Outcomes & Retrospective

Version `0.17.1` keeps RepoWise active after a missing synthesis provider and automatic compaction. The skill has an explicit MCP dependency. Focused tests and all 40 repository tests pass. The first full correctness review was clean.

## Context and Orientation

`assets/skills/repository-knowledge/SKILL.md` owns repository lookup behavior. `assets/AGENTS.block.md` routes applicable work to skills. `assets/hooks/session_start.py` supplies Codex context after startup, resume, clear, or compaction. `tests/test_kit.py` protects installation and rule ownership.

OpenAI documents progressive skill loading at `https://developers.openai.com/codex/skills`. It documents session instruction discovery at `https://developers.openai.com/codex/guides/agents-md`. It documents compact continuation context at `https://developers.openai.com/codex/hooks`.

## Product Boundary

The user requirement and the observed Meridian transcript are authoritative. Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md). The repository-knowledge skill owns lookup selection. The managed AGENTS block owns routing. The Session Start hook owns post-compaction context. RepoWise runtime, model-provider setup, and native-command enforcement are outside this task.

The supported model has one user and one Codex writer in a normal local Git repository. A RepoWise index and MCP server are available. A synthesis provider is optional. Existing Codex sessions do not reload changed instructions or configuration.

## Scenario Proof

This task changes executable hook behavior and live agent instructions. It does not change product data or retained runtime state.

Before compaction, a new lookup selects repository-knowledge and uses RepoWise. After `no-llm-provider`, the current candidate set remains usable. Each later conceptual question uses raw indexed search. Exact results use indexed context or symbol bodies. One stronger indexed query precedes focused native fallback.

After compaction, `SessionStart` adds a route-only developer instruction before the immediate continuation. The next new repository lookup selects repository-knowledge again. A focused hook test provides the oracle.

## Plan of Work

First, add focused tests for skill metadata, the no-provider transition, the AGENTS route, and compact continuation. Record the expected pre-change errors.

Then, update the repository-knowledge description and owner body. Add `agents/openai.yaml` with implicit invocation and the named RepoWise MCP dependency. Strengthen the AGENTS route without copying query rules. Add compact-specific context to the existing hook.

Update the smallest RepoWise document with no-provider and restart behavior. Set the source version to `0.17.1`. Regenerate the manifest after all tracked content is final.

## Concrete Steps

Work in `/home/mbeutler/Projects/codex-practical-kit` on branch `cpk-033-repowise-route-persistence`.

Run the focused contract tests before and after implementation. Then run `./run-tests.sh`, `git diff --check`, and `sha256sum --check MANIFEST.sha256`. Store detailed results in ignored file `.agent/test-results/cpk-033-repowise-route-persistence.md`.

Stage the complete candidate and run Adversarial Review. After a clean result, apply review closure. Install the reviewed candidate with `./install.sh`. Then run `./doctor.sh --repo .` and a fresh Codex forward test.

## Validation and Acceptance

The focused tests must prove four outcomes. The skill declares the `repowise` MCP dependency. The no-provider state retains indexed routing. A compact event restores the skill route. The complete rule has one owner.

The fresh forward test must ask separate conceptual and exact repository questions without naming RepoWise. After one `no-llm-provider` result, later conceptual questions must use `search_codebase`. Exact results must use `get_context` or `get_symbol`. Broad native search cannot occur before the bounded indexed fallback.

The complete test suite and manifest checks must pass. Doctor must report version `0.17.1` and `Result: ready` from the reviewed candidate.

## Idempotence and Recovery

The tests, installer, and Doctor are repeatable. If a required operation fails, stop and report the exact error. Do not add retries or speculative recovery.

## Artifacts and Notes

Keep detailed validation and review evidence only in the ignored task result. Keep the tracked ExecPlan final before the task commit.

## Interfaces and Dependencies

The `repository-knowledge` skill gains standard `agents/openai.yaml` metadata. It names the existing `repowise` MCP server. The Session Start hook changes only its developer context for `source: compact`. No dependency or public command changes.

Revision note (2026-08-17): Created from the accepted CPK-033 plan, official Codex documentation, transcript evidence, and the independent preflight challenge.

Revision note (2026-08-17): Recorded the implemented behavior, validation results, and clean first full review.

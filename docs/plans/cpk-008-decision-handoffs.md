# Make material decisions operator-readable

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, Codex explains a material choice before it requests direction. The operator sees why the choice matters, its current effect, practical options, and one recommendation. Simple English keeps the handoff clear. The new policy controls which facts the handoff contains.

## Progress

- [x] (2026-08-14 03:58Z) Compared Simple English with the accepted CPK-008 outcome.
- [x] (2026-08-14 03:58Z) Created `cpk-008-decision-handoffs` and activated CPK-008.
- [x] (2026-08-14 03:58Z) Completed Design Preflight and selected toolkit version `0.9.0`.
- [x] (2026-08-14 04:01Z) Added the material-decision trigger and compact handoff contract.
- [x] (2026-08-14 04:01Z) Added one focused consistency check and updated all version owners.
- [x] (2026-08-14 04:01Z) Completed validation, documentation maintenance, and the review-ready roadmap update.
- [x] (2026-08-14 04:03Z) Completed a clean adversarial review on pass 1 and recorded review closure.

## Surprises & Discoveries

- Observation: Simple English changes style but does not define decision content.
  Evidence: Its skill controls vocabulary, sentence structure, term definitions, and procedural order.
- Observation: The installed agent policy already owns every rule that can stop for human direction.
  Evidence: `assets/AGENTS.block.md` contains the architecture, publication, review, and supported-model stop rules.

## Decision Log

- Decision: Apply the full handoff to material decisions.
  Rationale: These choices change scope, architecture, authority, exposure, or the delivered result.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Skip the full handoff for discoverable facts, routine values, status questions, and minor preferences.
  Rationale: Extra structure makes small questions harder to read without improving the decision.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Use compact labels in one fixed order.
  Rationale: The operator can scan each required fact before the final question.
  Date/Author: 2026-08-14 / user
- Decision: Reuse Simple English without changing its upstream skill.
  Rationale: Simple English owns wording. The installed agent policy owns decision behavior.
  Date/Author: 2026-08-14 / Codex
- Decision: Use qualitative likelihood and do not invent percentages.
  Rationale: The repository does not contain a numeric risk model.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

CPK-008 is complete. The installed policy, session reminder, README, and operating manual now define one compact material-decision handoff. All 28 tests pass. Python compilation, shell syntax checks, diff checks, and manifest checks pass. Adversarial review pass 1 found no defects. Publication is not authorized; the branch remains local.

## Context and Orientation

The task uses branch `cpk-008-decision-handoffs`. Its base branch is `main`, and its base commit is `21151472b263fdd9ec412104cc838e879b8f3839`. The isolation form is a normal branch in the existing checkout. The target toolkit version is `0.9.0` because this task adds a feature during initial development.

`assets/AGENTS.block.md` owns the installed behavior policy. `assets/hooks/session_start.py` gives compact session guidance. `docs/OPERATING-MANUAL.md` owns the full user procedure. `README.md` gives the short workflow. `tests/test_kit.py` checks policy propagation.

A material decision is a user choice that changes scope, architecture, authority, exposure, or the delivered result. Current exposure states whether the repository or operator is affected now. A reversible choice is a choice that the operator can change later without losing work.

The supported model has one personal user and one Codex writer. It uses normal local filesystems and Git. If an operation fails, Codex stops and reports the error. The task excludes I/O faults, permissions, links, concurrency, interruption, retry, recovery, submodules, and outside writers.

## Normal-Use Behavior Floor

Before a material decision, Codex investigates every discoverable fact. It includes only conditions from supported normal use. It then presents `Decision`, optional `Term`, `Trigger`, `Likelihood`, `Current exposure`, `Options`, `Recommendation`, and `Question` in that order.

The `Term` label appears only when the handoff uses an unfamiliar term. `Likelihood` uses `already present`, `likely`, `unlikely`, or `unknown`, with evidence. `Current exposure` uses `yes`, `no`, or `unknown`, with one factual reason.

The handoff gives two or three practical options. Each option states its effect. The recommendation names one option and gives a reason. If evidence does not distinguish the options, Codex recommends the smallest reversible option that satisfies the requirement. The final question asks for the exact direction needed.

Codex does not invent numeric probabilities. It does not present filler options. If no real choice exists, it states the required action instead of requesting direction.

Routine facts and minor inputs stay concise. A file name, path, status request, or discoverable repository fact does not receive the full handoff.

## Scope Ceiling

Do not add a new skill, modify Simple English, change its upstream lock, add a parser, add a response generator, add telemetry, add risk scoring, or add a service. Do not change the authority rules that decide when Codex must stop. Do not require the format for routine questions.

## Plan of Work

Add one material-decision section to the installed agent policy. Add one compact Session Start reminder. Add the full procedure and one representative example to the operating manual. Add a short summary to the README.

Add one focused consistency check. Update the source version, user version statements, and checksum manifest after all content is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-008-decision-handoffs`.

Run:

    ./run-tests.sh
    python3 -m py_compile kit.py tests/test_kit.py assets/hooks/session_start.py
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record detailed results in `.agent/test-results/cpk-008-decision-handoffs.md`. Keep CPK-008 Active and mark validation complete with review pending. Finalize documentation before one fresh read-only adversarial review.

## Validation and Acceptance

The focused check must prove that each policy owner agrees on the material trigger, exclusions, fixed labels, qualitative likelihood, option effects, and recommendation order.

Acceptance includes five scenarios. An architecture choice receives the full handoff. An unfamiliar term is defined before use. A routine path request stays concise. Missing likelihood evidence produces `unknown`. A material choice gives option effects and a recommendation before the final question.

## Idempotence and Recovery

The policy has no persistent runtime state. Validation commands can run again. If a command fails, stop and report the error. Do not add retry or recovery behavior.

## Artifacts and Notes

Preserve the existing untracked `.claude/`, `.codex/`, `.mcp.json`, `.repowise/`, `.vscode/`, and root `AGENTS.md` paths. `MANIFEST.sha256` covers the distributed files and this ExecPlan.

## Interfaces and Dependencies

No public command or dependency changes. The installed agent contract gains one response format for material decisions. The toolkit version becomes `0.9.0`.

Revision note: Created from the accepted Plan Mode result and Design Preflight. Updated after implementation, validation, documentation maintenance, and clean review closure.

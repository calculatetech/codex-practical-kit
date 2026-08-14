# Diagnose severe defects at review stop gates

This ExecPlan is a living document. Maintain it according to the repository's `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, every validated finding that causes a review stop gets its own human decision block. A severe stop also runs one fresh read-only model diagnostic. The diagnostic retraces how the defect entered and escaped the work. It produces a portable summary, then the coordinator halts for human action.

## Progress

- [x] (2026-08-14 20:14Z) Reproduced the missing communication path in the third-defect breaker.
- [x] (2026-08-14 20:14Z) Selected a fresh diagnostic subagent as the model-query mechanism.
- [x] (2026-08-14 20:14Z) Defined the supported model, severe trigger, stop formatter, and halt boundary.
- [x] (2026-08-14 20:14Z) Created stacked branch `cpk-021-severe-defect-stop-diagnostics` and activated CPK-021.
- [x] (2026-08-14 20:43Z) Implemented the stop formatter and diagnostic skill.
- [x] (2026-08-14 20:43Z) Forward-tested the diagnostic skill with a duplicate-prefix severe defect.
- [x] (2026-08-14 20:43Z) Validated the complete pre-review candidate.
- [x] (2026-08-14 20:49Z) Completed clean-context review with no findings. Prepared the candidate for a local checkpoint.

## Surprises & Discoveries

- Observation: The reviewer JSON format and the human decision format have no routing rule between them.
  Evidence: `adversarial-review` defines reviewer JSON and a final status line. It does not define per-finding stop output.
- Observation: The toolkit already has the required model-query mechanism.
  Evidence: Adversarial Review uses one fresh read-only subagent per pass. A diagnostic can use the same coordinator capability after the reviewer closes.

## Decision Log

- Decision: Define P0 and P1 findings as severe on any pass. Also treat an implementation defect on the third counted pass as severe.
  Rationale: P0 and P1 indicate high immediate impact. A third counted defect indicates a repeated process failure even when severity is P2.
  Date/Author: 2026-08-14 / Codex
- Decision: Render one complete decision handoff for each stop-causing finding.
  Rationale: A cumulative handoff hides each trigger, exposure, option set, recommendation, and required answer.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Query a fresh read-only subagent for diagnosis.
  Rationale: This reuses the installed clean-context model path and adds no API key, service, CLI recursion, or runtime dependency.
  Date/Author: 2026-08-14 / Codex
- Decision: Run the diagnostic before the final halt, then prohibit all implementation activity.
  Rationale: The user needs the evidence summary before choosing a correction.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Keep version 0.11.0.
  Rationale: No `0.11.0` tag or GitHub release exists. A local checkpoint does not change the version.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

Implementation, validation, forward-testing, and clean-context review are complete. The first correctness pass found no validated defects. Publication is not authorized. The candidate is ready for a local checkpoint.

## Context and Orientation

The task uses branch `cpk-021-severe-defect-stop-diagnostics`. Its base branch is `cpk-020-protect-full-set-invariants`, and its base commit is `8f542e45e295`. The branch is stacked because CPK-020 is not integrated into `main`.

`assets/skills/adversarial-review/SKILL.md` owns review validation and stop behavior. `references/finding-format.md` owns reviewer JSON. The global communication rule in `assets/AGENTS.block.md` owns the human decision labels. No file currently connects these owners at a stop gate.

The new `assets/skills/defect-diagnostic/` skill owns clean-context defect reconstruction. `kit.py` owns custom-skill installation. The coordinator remains the only agent that can spawn and close the diagnostic subagent.

## Normal-Use Behavior Floor

After the coordinator validates findings, a P0 or P1 finding stops automatic correction on any pass. An implementation defect on the third counted pass also stops automatic correction.

At either severe stop, close the reviewer. Present each stop-causing finding in its own `Decision`, optional `Term`, `Trigger`, `Likelihood`, `Current exposure`, `Options`, `Recommendation`, and `Question` block. Do not combine findings into one handoff.

Run `defect-diagnostic` automatically. Give one fresh read-only subagent the raw requirement, implementation diff, source, checks, review history, and finding evidence. Omit reviewer fix directions. Do not give it the coordinator's diagnosis or proposed fix. The subagent retraces the decision sequence and produces the summary in the skill reference.

After the summary, halt. Do not edit, test, review, commit, publish, run CI, change task state, or create follow-up work. Wait for explicit human direction.

## Scope Ceiling

Do not restore a Stop hook. Do not call `codex exec`, the OpenAI API, or an external model service. Do not add credentials, a runtime script, persistent incident storage, automatic toolkit edits, or a diagnostic review loop. Do not trigger the automatic halt for P2 findings before the third counted pass.

## Plan of Work

Add a stop-finding formatter reference to Adversarial Review. Update its breaker so each stop finding uses that formatter. Add the severe trigger, diagnostic call, and mandatory halt.

Create the `defect-diagnostic` skill with one portable output reference and standard UI metadata. Add it to the custom-skill installer. Add focused tests for installation, implicit invocation metadata, per-finding formatting, automatic triggers, and the halt boundary.

Update the managed global policy, Session Start summary, README, review guide, and operating manual. Regenerate `MANIFEST.sha256` after content is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-021-severe-defect-stop-diagnostics`.

Run:

    python3 /home/mbeutler/.codex/skills/.system/skill-creator/scripts/quick_validate.py assets/skills/defect-diagnostic
    python3 -m unittest tests.test_kit.IntegrationTests.test_review_stop_diagnostics_are_per_finding_and_mandatory
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record results in `.agent/test-results/cpk-021-severe-defect-stop-diagnostics.md`. Never stage that file.

## Validation and Acceptance

The focused test must fail if the stop path combines findings, omits a communication label, skips the diagnostic trigger, permits a severe automatic fix, or omits the final halt. It must also fail if the new skill is absent from installation.

A clean-context forward test must produce a chronological defect trace and portable toolkit-correction summary from raw evidence. The test must not edit files or propose automatic implementation after the halt.

## Idempotence and Recovery

The skill and policy edits are static. Repeating validation is safe. Stop and report the first command failure. Do not add retry or recovery behavior.

## Artifacts and Notes

Preserve `.mcp.json`, `.repowise/`, and `.vscode/`. They are untracked environment state outside this task.

## Interfaces and Dependencies

`defect-diagnostic` is a new custom skill. It uses the coordinator's existing subagent capability. It has no code dependency or external service.

Revision note: Created after third-pass findings were returned as a cumulative status instead of separate human decision handoffs.

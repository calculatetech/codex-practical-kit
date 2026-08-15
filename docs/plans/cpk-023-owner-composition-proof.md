# Enforce single rule ownership

This ExecPlan is a living document. Maintain it in accordance with `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, the managed `AGENTS.md` is a compact router. It links an agent to the complete rule file that applies to the current task. The Session Start hook does not inject another policy copy. A runnable ownership check fails when a protected rule appears outside its sole live owner.

## Progress

- [x] (2026-08-15 04:15Z) Proved that local `main` and `origin/main` equal `7e8190d7194605d917c1b03afd3e9a25253a2b42`.
- [x] (2026-08-15 04:15Z) Created `cpk-023-owner-composition-proof` and activated CPK-023.
- [x] (2026-08-15 04:30Z) Implemented and validated the first copied-policy design.
- [x] (2026-08-15 05:10Z) Stopped after three counted review passes exposed repeated propagation defects.
- [x] (2026-08-15 05:20Z) Completed the severe-defect diagnostic and obtained human direction.
- [x] (2026-08-15 05:35Z) Replaced the design with focused rule owners and an AGENTS router.
- [x] (2026-08-15 06:15Z) Implemented the replacement architecture and its ownership check.
- [x] (2026-08-15 06:20Z) Finalized documentation, validation, and roadmap state.
- [x] (2026-08-15 07:00Z) Corrected the three replacement-review pass-1 defects and repeated full validation.
- [x] (2026-08-15 07:25Z) Completed replacement review pass 2. It found two P2 ownership-check defects.
- [x] (2026-08-15 07:35Z) Moved the remaining one-attempt copies to a canonical route and made the link-only check cover the complete section.
- [x] (2026-08-15 07:40Z) Repeated skill, unit, shell, hook, diff, and checksum validation after the pass-2 corrections.
- [x] (2026-08-15 08:05Z) Rejected the replacement pass-3 finding because the internal Playground exercise is not a supported normal-use rule surface.
- [x] (2026-08-15 08:10Z) Corrected the Playground exercise wording and removed it from the distribution manifest.
- [x] (2026-08-15 08:15Z) Repeated skill, unit, shell, hook, diff, checksum, and manifest-scope validation.
- [x] (2026-08-15 08:45Z) Limited review stop accounting to executable production code by human direction.
- [x] (2026-08-15 08:50Z) Bound each marked route to a resolved file that declares the same owner.
- [x] (2026-08-15 09:00Z) Validated the production-code gate and complete route invariant.
- [x] (2026-08-15 09:20Z) Completed fresh review. It found one non-counting ExecPlan housekeeping issue.
- [x] (2026-08-15 09:25Z) Replaced the copied supported-model text with its canonical link.
- [x] (2026-08-15 09:30Z) Validated the housekeeping correction.
- [x] (2026-08-15 09:40Z) Completed fresh review pass 5 with no findings.
- [x] (2026-08-15 09:45Z) Prepared the reviewed candidate for the authorized local checkpoint commit.

## Surprises & Discoveries

- Observation: The old tests required identical policy sentences in several files.
  Evidence: `tests/test_kit.py` calls AGENTS, Session Start, PLANS, skills, and documentation policy owners and asserts the same text in each one.
- Observation: Compactness made the copied rules lose required facts.
  Evidence: Each review correction expanded one copy and left another copy incomplete.
- Observation: The installer already owns a complete skill-copy lifecycle.
  Evidence: Custom skills support conflict detection, reinstall, uninstall, and doctor checks through manifest schema 1.
- Observation: The committed source version is `0.11.0`.
  Evidence: The branch changes `KIT_VERSION` to `0.11.1`, which is the correct bug-fix increment.
- Observation: A repository-level rule link cannot safely use invocation defaults after a custom-path installation.
  Evidence: `setup-repo` has no path options, while the global AGENTS router already owns the required link.
- Observation: Link migration must remove semantic copies, not only exact guard phrases.
  Evidence: Replacement review pass 1 found the four supported-model checks restated in Design Preflight and its card.
- Observation: Moving a policy requires a fact-by-fact transfer from every former live owner.
  Evidence: Replacement review pass 1 found accepted pull-request gates that were absent from the new publication owner.
- Observation: A fixed list of current manuals can omit a live rule copy.
  Evidence: Replacement review pass 2 found the one-attempt rule in `docs/REMOVE-CBM.md`, which the ownership scan did not include.
- Observation: A marker-level parser does not protect prose before the marker.
  Evidence: Replacement review pass 2 inserted ordinary prose between a section heading and its route marker without invalidating the original check.
- Observation: A distributed-file checksum does not make an internal exercise a live agent rule surface.
  Evidence: The user rejected the replacement pass-3 finding because `PLAYGROUND.md` is a special-case exercise and does not affect supported real-world usage.
- Observation: Executable test logic is not executable production code.
  Evidence: The user clarified that tests and fixtures can require correction but cannot increment the review breaker or trigger a stop.

## Decision Log

- Decision: Use one managed rule package with focused Markdown references.
  Rationale: The existing skill lifecycle installs and removes the package without a second file-management system.
  Date/Author: 2026-08-15 / User and Codex
- Decision: Make the managed AGENTS block a trigger-and-link router.
  Rationale: Agents can read only the complete rule that applies to the current task.
  Date/Author: 2026-08-15 / User and Codex
- Decision: Treat Session Start as an activation notice only.
  Rationale: Session Start cannot become another policy owner.
  Date/Author: 2026-08-15 / User and Codex
- Decision: Protect canonical rules with unique owner markers and owner-local guard phrases.
  Rationale: One generic check can reject copied live policy without copying expected policy into the test.
  Date/Author: 2026-08-15 / Codex
- Decision: Keep version `0.11.1`.
  Rationale: This work corrects the failed CPK-023 bug fix. It does not add a user capability.
  Date/Author: 2026-08-15 / User and Codex
- Decision: Count only defects in executable production code for review stop gates.
  Rationale: Tests, fixtures, documentation, configuration, dependencies, manifests, and housekeeping do not run as production code.
  Date/Author: 2026-08-15 / User

## Outcomes & Retrospective

The first implementation is rejected. It strengthened the required rule but made every policy copy another authority.

The replacement installs 12 focused shared-rule files. AGENTS is a 25-line router, and Session Start is one activation notice. Existing skills and the active ExecPlan link shared rules instead of copying them. One generic check rejects duplicate owners, copied guards, extra route content, missing targets, and wrong-owner targets. The review breaker counts only executable production-code defects. All seven custom skills and all 27 tests pass. Fresh review pass 5 found no findings.

## Context and Orientation

The task uses branch `cpk-023-owner-composition-proof`. Its base is `main` at `7e8190d7194605d917c1b03afd3e9a25253a2b42`.

`assets/AGENTS.block.md` is the source for the global managed block. `assets/hooks/session_start.py` supplies startup context. `kit.py` stages custom skills before it writes AGENTS. `tests/test_kit.py` owns installer and policy checks.

The new package lives at `assets/skills/codex-practical-kit-rules/`. Its reference files are the only live owners of shared toolkit rules. Existing skill files remain the owners of their specialized procedures. Historical ExecPlans and diagnostics are records, not live instruction sources.

## Design Preflight

The required outcome is one complete owner for each live rule and an installed router that reaches that owner. The project controls the rule sources, installer, generated links, tests, and documentation.

Apply [Supported model](../../assets/skills/codex-practical-kit-rules/references/supported-model.md). This task also supports installation with distinct Codex and skills directories.

This is a non-runtime policy architecture change. The user resolved the ownership contract. A planning challenger is not required.

The implementation ceiling excludes a policy parser, generated documentation system, new dependency, manifest schema change, or semantic prose classifier. One stdlib test will scan explicit owner and guard markers.

Preflight: ready — reuse the custom-skill lifecycle, render direct AGENTS links, and enforce unique live owners.

## Plan of Work

First, create the focused rule package. Move each accepted shared policy into one file. Add a short package `SKILL.md` that tells agents to read only the reference selected by AGENTS. Add owner and guard comments to each canonical file.

Next, replace the managed AGENTS content with a short route table. Render the skills and PLANS paths during installation. Replace the Session Start policy copy with one activation notice.

Then, remove copied shared rules from PLANS, custom skills, templates, README, the operating manual, and the design rationale. Link to the canonical source instead. Keep operational commands and product facts that are not agent rules.

Finally, replace every propagation test with single-owner content checks, link-resolution checks, and one general duplication guard. Update source version statements and checksums. Finalize documentation before review.

## Concrete Steps

Work in `/home/mbeutler/Projects/codex-practical-kit`.

Run:

    python3 /home/mbeutler/.codex/skills/.system/skill-creator/scripts/quick_validate.py assets/skills/codex-practical-kit-rules
    python3 -m unittest tests.test_kit.InstallerTests.test_global_agents_profile_is_compact_and_subagent_safe
    python3 -m unittest tests.test_kit.IntegrationTests.test_rule_owners_are_unique
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record detailed output in `.agent/test-results/cpk-023-owner-composition-proof.md`. Do not stage that ignored file.

## Validation and Acceptance

The installed AGENTS block must contain only routing text and links. Each rendered link must target the configured installation paths and exist after installation. Session Start must contain no expanded policy.

Each live owner identifier must occur once. Each owner-local guard phrase must occur only in that owner across current policy and documentation surfaces. Historical task records are excluded.

The canonical owner-composition rule must preserve the three accepted composed runtime obligations. It must link the full-set rule instead of copying it.

The full unit suite, skill validation, shell syntax, diff, and checksum checks must pass. One fresh adversarial reviewer must find no supported normal-use defect before commit.

## Idempotence and Recovery

Reinstall replaces only toolkit-owned skill directories and the managed AGENTS block. Uninstall removes only manifest-recorded destinations. If any command fails, stop and report it.

## Artifacts and Notes

Preserve the existing untracked `.claude/`, `.codex/`, `.mcp.json`, `.repowise/`, `.vscode/`, and root `AGENTS.md` paths. They are environment state outside this task.

## Interfaces and Dependencies

The installed AGENTS contract changes from embedded policy to absolute local links. The installer adds one managed rule package. No CLI, configuration schema, external service, or dependency changes. The toolkit version becomes `0.11.1`.

Revision note: Replaced the rejected copied-policy design after the third review defect and human direction.
Revision note: Recorded the validated replacement candidate and fresh-review readiness.
Revision note: Recorded the three replacement-review pass-1 findings and correction scope.
Revision note: Recorded the shared-owner corrections and repeated validation before replacement review pass 2.
Revision note: Recorded the two replacement-review pass-2 findings and their shared-check corrections.
Revision note: Recorded the rejected pass-3 finding and the user-defined Playground scope.
Revision note: Recorded the production-code-only stop gate and the corrected route invariant.
Revision note: Replaced the active plan's copied supported-model text after a non-counting housekeeping finding.
Revision note: Recorded the clean final review result.

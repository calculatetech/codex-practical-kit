# Require the RepoWise code graph

This ExecPlan is a living document. Maintain it according to the repository's `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, Codex waits for RepoWise to initialize before a session starts. The first session in an unindexed Git repository no longer continues without the code graph. Toolkit instructions treat RepoWise as required repository knowledge, not an optional provider.

## Progress

- [x] (2026-08-14 16:32Z) Reproduced the first-start timing and confirmed that RepoWise completed after Codex omitted the pending optional server.
- [x] (2026-08-14 16:32Z) Verified the official Codex `required` and `startup_timeout_sec` MCP settings.
- [x] (2026-08-14 16:32Z) Defined the behavior floor, scope ceiling, and target version.
- [x] (2026-08-14 16:32Z) Activated CPK-016 on an isolated task branch.
- [x] (2026-08-14 16:58Z) Added required RepoWise startup and removed optional-provider guidance.
- [x] (2026-08-14 16:58Z) Updated focused tests, documentation, and version owners.
- [x] (2026-08-14 16:58Z) Passed 26 tests, Python compilation, shell syntax checks, and the diff check.
- [x] (2026-08-14 17:16Z) Updated checksums and completed clean-context review after two fixes on pass 3.

## Surprises & Discoveries

- Observation: Automatic initialization succeeded even though Codex displayed an MCP startup warning.
  Evidence: Codex omitted a pending optional server at 12:24:45. RepoWise finished 24.9 seconds later and completed the MCP handshake at 12:25:12.
- Observation: The managed table already gives RepoWise a 1,800-second startup timeout.
  Evidence: `repowise_config_block()` writes `startup_timeout_sec = 1800`, but it does not write `required = true`.
- Observation: Review pass 1 found fallback guidance in `docs/OPTIONAL-REVIEW-TOOLS.md`.
  Evidence: The guide told users to continue with native tools when RepoWise failed. The candidate now uses the required stop-and-restore policy.
- Observation: Review pass 2 found an optional RepoWise heading in the bundled review packet.
  Evidence: The packet now labels the section `RepoWise observations`, and the policy test covers the file.

## Decision Log

- Decision: Set `required = true` in the managed RepoWise MCP table.
  Rationale: Official Codex configuration defines this flag as the startup and resume gate for an enabled MCP server. The existing timeout bounds the wait.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Remove fallback guidance from toolkit-owned agent instructions and current documentation.
  Rationale: The user made the code graph a mandatory toolkit component. Continuing without it contradicts that requirement.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Use version `0.11.0`.
  Rationale: Required RepoWise startup is a breaking behavior change before version 1.0.0.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

Version 0.11.0 makes RepoWise a required MCP server and keeps the 1,800-second startup bound. Toolkit guidance now stops when the graph is unavailable. All 26 tests and required checks pass. Review pass 3 is clean after two consistency fixes.

Publication status: A local checkpoint commit is authorized. Push is not authorized for CPK-016.

## Context and Orientation

The task uses branch `cpk-016-required-repowise`. Its base branch is `cpk-015-config-toml-hooks`, and its base commit is `2bd33d71f886a759ef2ebf667c6b960498bfd9c9`. This stacked branch is necessary because CPK-015 is published but is not integrated into `main`. The isolation form is a normal branch in the existing checkout. The target version is `0.11.0`.

`kit.py` renders the global RepoWise MCP table in `repowise_config_block()`. Its bootstrap command initializes an absent index before it starts the MCP server. The table already sets `startup_timeout_sec = 1800`.

Codex treats an MCP server as optional unless its table sets `required = true`. The official configuration reference says that a required enabled server gates startup and resume. The timeout controls how long Codex waits for initialization.

`assets/AGENTS.block.md`, `assets/hooks/session_start.py`, and `kit.py:repowise_agents_block()` currently tell agents to fall back when RepoWise is unavailable. `README.md`, `docs/REPOWISE.md`, and `docs/WHY-THIS-SHAPE.md` repeat that optional model.

The supported operating model has one personal user and one Codex writer on a normal local filesystem. RepoWise 0.41.0 is installed by the toolkit. The automatic bootstrap owns index creation and Git-hook installation.

## Normal-Use Behavior Floor

The managed global MCP table contains `required = true` and `startup_timeout_sec = 1800`. Codex waits for first-time index creation and MCP initialization before it starts or resumes a session. If initialization fails or exceeds the timeout, Codex startup fails instead of continuing without the graph.

Toolkit-owned instructions require current RepoWise knowledge before broad repository exploration. If the index is stale, the agent refreshes it. Source remains the correctness authority.

## Scope Ceiling

Do not redesign the bootstrap command, add polling, add retry or recovery, change RepoWise, or change Codex. Do not make generated RepoWise prose mandatory. Do not remove direct source verification. Do not change repository opt-out commands in this task.

## Plan of Work

Add `required = true` to `repowise_config_block()` next to the existing startup timeout. Update doctor to require the flag. Add a focused assertion to the existing install test.

Replace optional-provider wording in the current toolkit-owned agent instructions and documentation. State that a stale index must be refreshed and that source remains authoritative. Update version owners to `0.11.0`.

Regenerate `MANIFEST.sha256` after code and documentation are final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-016-required-repowise`.

Run:

    python3 -m unittest tests.test_kit.InstallerTests.test_install_preserves_global_config_and_uninstall_removes_owned_block
    ./run-tests.sh
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record current results in `.agent/test-results/cpk-016-required-repowise.md`. Keep CPK-016 Active and mark validation complete before review.

## Validation and Acceptance

The focused install test must fail if the generated global RepoWise table omits `required = true` or the existing timeout. The full suite and compilation must pass. Shell syntax, diff, and manifest checks must pass.

The candidate must contain no current toolkit instruction that calls RepoWise optional or tells an agent to continue without it.

## Idempotence and Recovery

The managed marker block replaces its prior contents on reinstall. Repeated installation produces one required RepoWise table. If initialization fails, Codex applies its configured required-server failure. The toolkit does not retry or recover.

## Artifacts and Notes

Preserve the untracked `.mcp.json`, `.repowise/`, and `.vscode/` paths. Never stage `.agent/test-results/`.

## Interfaces and Dependencies

No new dependency or command is required. The public configuration change is `mcp_servers.repowise.required = true`. The existing `startup_timeout_sec = 1800` remains the wait bound.

Revision note: Created after the user made RepoWise mandatory and local logs confirmed the optional-server startup race.

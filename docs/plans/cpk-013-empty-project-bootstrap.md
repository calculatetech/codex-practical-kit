# Bootstrap empty project folders

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, a user can create an empty project folder and start Codex in it. The RepoWise MCP startup command initializes Git, builds the RepoWise index, and installs the post-commit hook. Codex does not initialize Git when a non-Git folder contains any entry.

## Progress

- [x] (2026-08-14 10:51Z) Reproduced the empty-folder startup path and identified the Git lookup fallback.
- [x] (2026-08-14 10:51Z) Accepted automatic Git initialization for empty folders only.
- [x] (2026-08-14 10:51Z) Created `cpk-013-empty-project-bootstrap`, activated CPK-013, and completed Design Preflight.
- [x] (2026-08-14 10:53Z) Added the empty-folder bootstrap branch and its focused check.
- [x] (2026-08-14 10:53Z) Updated version owners and RepoWise documentation.
- [x] (2026-08-14 10:53Z) Completed validation, documentation maintenance, and the review-ready roadmap update.
- [x] (2026-08-14 10:56Z) Completed a clean adversarial review on pass 1 and recorded review closure.

## Surprises & Discoveries

- Observation: RepoWise itself starts in a non-Git folder, but it creates only an empty database instead of a usable project index.
  Evidence: The startup log for `/home/mbeutler/Projects/techconnect` reported no `.repowise` directory, then the MCP handshake succeeded.
- Observation: The `codex_apps` server did not reproduce a failure.
  Evidence: The startup log and a live restart showed successful initialization.
- Observation: The official OpenAI documentation search returned no accessible MCP startup page in this session.
  Evidence: The official-domain search and direct page request returned no page content.

## Decision Log

- Decision: Run `git init` only when Git lookup fails and the current folder contains no entries.
  Rationale: The user starts Codex in empty folders to create projects, but also uses Codex in non-project folders that must stay unchanged.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Treat hidden entries as content.
  Rationale: A folder with any entry is not completely empty.
  Date/Author: 2026-08-14 / Codex
- Decision: Use version `0.9.1`.
  Rationale: CPK-013 corrects the RepoWise bootstrap behavior in the current feature line.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

CPK-013 is complete. Empty non-Git folders now enter the existing Git and RepoWise setup path. Non-empty non-Git folders remain unchanged. All 29 tests pass. Python compilation, shell syntax checks, diff checks, and manifest checks pass. Adversarial review pass 1 found no defects. Publication is not authorized; the branch remains local.

## Context and Orientation

The task uses branch `cpk-013-empty-project-bootstrap`. Its base branch is `main`, and its base commit is `e266ded5ca894df2f460ce93e9799f1c2a61e17d`. The isolation form is a normal branch in the existing checkout. The target toolkit version is `0.9.1`.

`kit.py` owns the global RepoWise MCP command. Its `repowise_bootstrap()` function first asks Git for the repository root. Current code starts a generic RepoWise MCP server when that lookup fails. Therefore, it never reaches the existing index and hook setup path in a new empty folder.

`tests/test_kit.py` executes the generated shell command with a fake RepoWise executable. `README.md` and `docs/REPOWISE.md` own the user-visible startup behavior. `CODEX-INSTALL-PROMPT.md` and `kit.py` own the current version statements.

The supported model has one personal user and one Codex writer on a normal local filesystem. The current directory is the Codex workspace. Git and the pinned RepoWise command are installed. A completely empty folder has no visible or hidden entries.

## Normal-Use Behavior Floor

If the current directory is already in a Git repository, preserve the current behavior. Initialize RepoWise when its index is absent, install the hook, and start the MCP server for the repository root.

If the current directory is not in Git and is completely empty, run `git init` once. Then use the same repository bootstrap path.

If the current directory is not in Git and contains any entry, do not initialize Git, RepoWise, or a hook. Start the generic RepoWise MCP server without a project root.

If one command fails, stop and report the error. Do not add retry or recovery behavior.

## Scope Ceiling

Do not infer workspace trust. Codex owns trust. Do not initialize Git in a non-empty folder. Do not inspect parent intent, add an allowlist, change `codex_apps`, change RepoWise, add dependencies, or add recovery behavior. Do not repair folders changed by an earlier startup.

## Plan of Work

Change `repowise_bootstrap()` in `kit.py`. When Git root lookup fails, use `ls -A` to test whether the current directory has one entry. Run quiet `git init` only when the result is empty. Then resolve the new Git root and continue through the existing RepoWise initialization and hook commands.

Add one focused test in `tests/test_kit.py`. Prove that an empty non-Git folder gains `.git` and uses the full RepoWise path. Prove that a non-empty non-Git folder does not gain `.git` and uses only the generic MCP command.

Update the existing RepoWise sections in `README.md` and `docs/REPOWISE.md`. Update the toolkit version owners and checksum manifest after all content is final.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-013-empty-project-bootstrap`.

Run:

    python3 -m unittest tests.test_kit.RepoWiseRuntimeTests.test_bootstrap_initializes_only_empty_non_git_directory
    ./run-tests.sh
    python3 -m py_compile kit.py tests/test_kit.py assets/hooks/session_start.py
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Record detailed results in `.agent/test-results/cpk-013-empty-project-bootstrap.md`. Keep CPK-013 Active and mark validation complete with review pending. Finalize documentation before one fresh read-only adversarial review.

## Validation and Acceptance

The focused check must fail if an empty non-Git folder does not gain `.git`, if RepoWise does not initialize, or if the hook does not install. It must fail if a non-empty non-Git folder gains `.git` or runs RepoWise initialization.

The full suite must pass. Python compilation, shell syntax, diff, and manifest checks must pass.

## Idempotence and Recovery

After `git init`, later MCP starts use the existing Git repository path. RepoWise initialization remains conditional on `.repowise`. If a command fails, stop and report it. Do not retry or repair partial state.

## Artifacts and Notes

Preserve the existing untracked `.claude/`, `.codex/`, `.mcp.json`, `.repowise/`, `.vscode/`, and root `AGENTS.md` paths in this toolkit checkout. The diagnostic folder `/home/mbeutler/Projects/techconnect` already contains a RepoWise database from the reported startup and is outside this implementation scope.

## Interfaces and Dependencies

No new public command or dependency is required. The generated POSIX shell command continues to use Git, RepoWise, and standard `ls`. The toolkit version becomes `0.9.1`.

Revision note: Created from the accepted empty-folder rule and Design Preflight. Updated after implementation, validation, documentation maintenance, and clean review closure.

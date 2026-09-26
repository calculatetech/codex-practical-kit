# Resolve the Codex command on Windows

This ExecPlan records the scope and validation for CPK-060. Maintain it according to `.agent/PLANS.md` until review closure.

## Purpose

The Windows installer and Doctor must run the npm-installed Codex command. Python cannot start the extensionless `codex` name directly when only the Windows npm command shim is available.

## Scope

Resolve `codex` with the Python standard library on Windows and reuse that path for plugin installation and Doctor checks. Keep the existing command name on macOS and Linux. Isolate Git test fixtures from the host's line-ending conversion so the Windows suite verifies repository bytes consistently.

This bug fix publishes version `0.24.1`. It adds no dependency, configuration option, or new installation path.

## Progress

- [x] Reproduced the Windows command lookup failure.
- [x] Added one shared Windows command resolver and its regression check.
- [x] Isolated Git fixtures from global `core.autocrlf` settings.
- [x] Passed the complete test suite, installer, and Doctor on Windows.
- [x] Completed adversarial review. Publication continues through the protected pull-request workflow.

## Plan history reconciliation

No Plan Mode record applies to CPK-060. The task began from the user's direct bug report and publication request.

## Validation and acceptance

Run from the repository root:

    pwsh -File .\run-tests.ps1
    pwsh -File .\install.ps1
    pwsh -File .\doctor.ps1
    git diff --check

Require every manifest checksum to match. Require Doctor to report `Result: ready` for toolkit version `0.24.1` and the installed Codex CLI.

## Outcome

On Windows, the toolkit uses the executable path returned by `shutil.which("codex")`. Native plugin installation and Doctor use the resolved npm `.CMD` shim. Other platforms keep the existing `codex` command. Final adversarial review found no actionable defect.

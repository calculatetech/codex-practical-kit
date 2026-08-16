<!-- cpk-rule-owner: supported-model -->
<!-- cpk-rule-guard: Require normal use, project control, a reproducible wrong result, and an explicit requirement before adding handling. -->
<!-- cpk-rule-guard: Exclude I/O faults, permissions, links, concurrency, interruption, retry, restart, recovery, submodules, outside influence, and hostile completion markers by default. -->
<!-- cpk-rule-guard: Attempt an operation once. If it fails, stop and report the error. -->

# Supported model

Declare the supported operating model before non-trivial work.

The default model has one personal user and one Codex writer. It uses normal local filesystems and Git.

Require normal use, project control, a reproducible wrong result, and an explicit requirement before adding handling.

For a proposed requirement or review finding, answer these questions with `true` or `false`:

1. Does the trigger occur during supported normal use?
2. Does the project control the trigger and result?
3. Can current behavior reproduce the trigger without fault injection?
4. Does an explicit requirement define the expected result?

Classify the result:

- `applicable`: all four answers are `true`.
- `contract-gap`: the first three answers are `true`, and the fourth answer is `false`.
- `excluded`: one of the first three answers is `false`.

Exclude I/O faults, permissions, links, concurrency, interruption, retry, restart, recovery, submodules, outside influence, and hostile completion markers by default.

Use true or false checks for deterministic operations. Attempt an operation once. If it fails, stop and report the error.

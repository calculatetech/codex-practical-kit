# Remove the invalid Stop context limit

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose

Codex must load the managed Stop hook without a configuration warning. The installer must keep `additionalContextLimit` on context-producing hooks and omit it from Stop.

## Progress

- [x] (2026-08-19) Confirmed the warning in the installed configuration and the shared hook generator.
- [x] (2026-08-19) Confirmed the event restriction in the official OpenAI Hooks documentation.
- [x] (2026-08-19) Completed the small-change preflight and activated CPK-037.
- [x] (2026-08-19) Corrected generation and detection, and added the upgrade check.
- [x] (2026-08-19) Passed 51 tests, all skill validators, shell syntax checks, and diff checks.
- [x] (2026-08-19) Passed clean-context adversarial review and closed CPK-037.

## Decision Log

- Decision: Keep one managed hook generator and vary only the event-specific field.
  Rationale: Stop cannot emit additional context. Session Start and User Prompt Submit still use the configured limit.
  Date/Author: 2026-08-19 / Codex

## Context

The task branch is `cpk-037-stop-hook-context-limit`. Its base is `cpk-036-plan-history` commit `442c95f687c880bc07eb6434f7cc6cb01d5562ee`. The isolation form is one stacked local task branch.

`kit.py` generates managed hook TOML and detects existing managed handlers. `tests/test_kit.py` verifies installation and upgrades. The official Hooks documentation states that Codex warns when `additionalContextLimit` appears on an event that cannot emit additional context.

## Product Boundary

The installer owns only its marked hook block. It must preserve unrelated handlers and configuration. This correction does not change Stop execution or Plan history storage.

## Scenario Proof

| Scenario | Discriminator | Contrast | Production path | Required oracle | Runnable test or command | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Generate current hooks | Hook event | Stop versus Session Start and User Prompt Submit | `hooks_config_block` to TOML parser | Stop has no limit; the other managed hooks have `1200` | `test_reinstall_accepts_existing_config_toml_hook` | Passed |
| Upgrade the faulty block | Existing Stop field | Legacy managed block versus corrected block | `install_hooks` removes and regenerates the marked block | Reinstalled Stop has no limit and no duplicate handler | `test_reinstall_removes_stop_context_limit` | Passed |

## Scope Ceiling

Do not add a new hook format, parser, service, dependency, or event registry. Do not change unrelated user configuration.

## Validation

Run the focused installer tests, `./run-tests.sh`, `git diff --check`, and `sha256sum --check MANIFEST.sha256`. Store detailed results in `.agent/test-results/cpk-037-stop-hook-context-limit.md`.

## Outcomes

The installer now omits `additionalContextLimit` from Stop. It retains the limit on Session Start and User Prompt Submit. Reinstallation also removes the invalid field from the prior managed block.

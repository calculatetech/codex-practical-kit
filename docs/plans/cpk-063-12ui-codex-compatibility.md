# Stop reinstalling incompatible 12UI hooks

This ExecPlan is a living specification until review closure. Follow `.agent/PLANS.md`.

## Purpose / Big Picture

After removing the incompatible 12UI Git plugin, users must be able to install or apply toolkit updates without restoring its startup warning. The toolkit retains its website-only instruction for separately installed 12UI skills.

## Context and Orientation

`kit.py` owns check, apply, install, and Doctor commands. `upstream.lock.json` declares managed components. `native_plugin_status`, `install_core`, and `apply_updates` select native plugins. Doctor currently requires both Ponytail and the incompatible 12UI Git package. `tests/test_updates.py` exercises the commands through external-system fakes and real shell launchers. `tests/test_ponytail.py` covers native installation.

The task branch is `cpk-063-12ui-codex-compatibility`, based on `cpk-062-managed-update-application-12ui` at `62c549376f2f53a48484ddba49bad607feb426cf`. One writer uses the current checkout. Local main and origin/main match. Preserve the user's applied upstream pins and unrelated untracked files.

## Product Boundary

Follow [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) and [Supported model](../../assets/skills/design-preflight/references/supported-model.md). The authoritative source is the user's request to update the toolkit after removing the incompatible Git plugin. This explicitly supersedes CPK-062's automatic 12UI Git installation and refresh decision. No immutable Plan history record applies to this focused correction.

Managed inventory, native plugin selection, Doctor, documentation, and website routing compose the result. Codex plugin internals, upstream packages, and separately installed 12UI are opaque owners. The normal model is one personal user with a selected Codex home and normal Git files. The ceiling excludes editing plugin caches, creating a fork or adapter, downgrading 12UI, installing a replacement automatically, and removing user plugins.

## Decision Log

- Decision: remove 12UI from managed runtime inventory and native plugin operations. Keep Ponytail as the managed native plugin.
  Rationale: 12UI 0.2.108's `hooks/hooks.json` contains `modules`, which Codex 0.160.0 rejects. Its README identifies the module as a Claude Code pane. The separately installed directory plugin has its own lifecycle.
- Decision: retain the website-only routing instruction unchanged and document separately installed 12UI.
  Rationale: the user still wants 12UI for websites. Removing an incompatible package does not require changing that use restriction.
- Decision: use the strict-simplification challenger exemption.
  Rationale: this correction deletes an unsupported installation path and adds no interface, persistent state, dependency, fallback, or supported use case. Native review and trace closure still apply.
- Decision: preserve the user's already-applied runtime and skill pins.
  Rationale: those source-lock changes are an existing application result, not a request to downgrade installed tools.

## Boundary Inventory and Scenario Proof

Follow [Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md), [Owner composition](../../assets/skills/design-preflight/references/owner-composition.md), and [Full-set results](../../assets/skills/design-preflight/references/full-set-results.md).

Every request clause is mapped below. The startup warning is evidence for B1. The user already removed the package, so automatic uninstall is outside scope. Unrelated plugins and upstream workflow internals are opaque.

| Boundary | Source and invariant | Contrast and required oracle | Entry points and exact named check |
| --- | --- | --- | --- |
| B1 | User correction: toolkit commands must not restore the incompatible 12UI package. | 12UI absent versus a separately installed disabled 12UI with user data. Install and apply succeed, never add or refresh 12UI, and preserve existing state. | `main` install, apply, Doctor; `ComposedUpdateTests.test_12ui_is_unmanaged_across_install_apply_and_doctor` |
| B2 | Retained website-only restriction. | Installed router retains website scope and rejects native-app scope, regardless of plugin presence. | Same composed check as B1. |
| B3 | Managed update completeness and existing launcher behavior remain supported. | Managed components still update, and a Ponytail operation error stops after one attempt. 12UI is absent from the report and provider requests. | Check/apply Bash and PowerShell launchers; `ComposedUpdateTests.test_update_launchers_run_complete_actions_and_propagate_failures` |

Presence, preservation, and repeated install/apply sequences are applicable input and transition cases. B3 covers every remaining managed record. Unsupported failure models and unrelated plugin operations are excluded.

## Plan of Work

One atomic subtask, CP1, removes managed 12UI from `upstream.lock.json`, status selection, install, apply, and Doctor. Delete its special package-source validator and status wrapper. Adapt existing command and launcher tests to preserve separately installed 12UI as an external plugin. Retain Ponytail's official-source checks and update failure checks. Add the B1 composed regression using real command owners and only external fakes.

Update README, installation prompt, and third-party notices to explain the directory-installed plugin and removal of the old Git package. Keep completed plans unchanged. Regenerate distribution checksums after final documentation. Review the complete task from its base, then perform roadmap closure and one local commit.

## Concrete Steps and Acceptance

From the repository root, run:

    PYTHONPATH=tests python3 -m unittest test_updates test_ponytail
    ./run-tests.sh
    sh -n apply-updates.sh check-updates.sh doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

Run B1 and B3 individually and retain their exact results in ignored `.agent/test-results/CPK-063.md`. Require no 12UI native mutation or provider query, preservation of existing 12UI state, the website-only router, and Doctor success with 12UI absent. Perform the required fresh trace closure before native review. After a clean review, update the roadmap and matching checksum, freeze tracked records, and commit locally. Reinstall the corrected toolkit and require Doctor to report ready.

## Idempotence and Dependencies

Install and apply remain repeatable under their existing ownership rules. The correction uses Python's standard library and existing native commands. Attempt each external operation once and report an error. No new dependency or plugin format is introduced.

## Outcomes & Retrospective

The toolkit no longer installs, queries, refreshes, or requires the incompatible Git package. Separately installed 12UI retains its state, and the website-only router continues to apply. Managed version facts come from the source lock, including the user's applied pins.

This correction removes the unsupported package path instead of maintaining a modified plugin cache. The package host and hook format must agree before a third-party Git package enters managed installation.

## Surprises & Discoveries

The latest upstream package and installed package both contain `{"hooks": {}, "modules": ["./register.mjs"]}`. The [upstream README](https://github.com/just-every/12ui-plugin) describes the pane as a Claude Code feature. [OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins) distinguishes local Git marketplaces from the shared directory. The existing curated 12UI cache has no `hooks/hooks.json`.

The change supersedes automatic Git-package installation because that path produces a startup warning on the supported host.

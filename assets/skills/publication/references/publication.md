<!-- cpk-rule-owner: publication -->
<!-- cpk-rule-guard: Direct integration is allowed only when protected `main` does not require a pull request. -->
<!-- cpk-rule-guard: Mark the pull request ready only after the current-head review is clean. -->
<!-- cpk-rule-guard: Treat each review comment as a candidate finding. Apply Adversarial Review before you use its severity or change the candidate. -->
<!-- cpk-rule-guard: Before merge, require successful checks for the latest head. Require no requested changes and GitHub mergeability. -->
<!-- cpk-rule-guard: Publication does not authorize tag creation, a GitHub release, or cleanup. -->
<!-- cpk-rule-guard: Before Codex Practical Kit publication, use the Windows PowerShell launchers on Windows and the shell launchers elsewhere. Require `Result: ready`. -->

# Publication

## Tracked state

<!-- cpk-rule-route-only: delivery-lifecycle -->
[Delivery lifecycle](../../delivery-lifecycle/references/delivery-lifecycle.md)

## PR findings

<!-- cpk-rule-route-only: adversarial-review -->
[Adversarial Review](../../adversarial-review/SKILL.md)

## Procedure

Before Codex Practical Kit publication, use the Windows PowerShell launchers on Windows and the shell launchers elsewhere. Require `Result: ready`.

On Windows, run `pwsh -File .\install.ps1` and `pwsh -File .\doctor.ps1`. On macOS or Linux, run `./install.sh` and `./doctor.sh`. Run the commands from the reviewed candidate.

Direct integration is allowed only when protected `main` does not require a pull request.

If protected `main` requires a pull request, make sure that all PR-mode gates are available. Require CI checks and resolved conversations.

CI must contain at least one workflow. Its workflows must supply every required check.

PR mode is active when protected `main` requires a pull request and every PR-mode gate is available.

Before you push the task branch, prove that task-branch pushes and draft pull requests cannot start hosted CI.

Prove that pull-request readiness can start every required CI check.

If protected `main` requires a pull request and a PR-mode gate is absent, stop. Do not use direct integration.

When direct integration is allowed, `publish` authorizes branch push, merge to `main`, integration verification, and required post-merge CI.

When PR mode is active, use a pull request for every change, including bounded documentation.

One explicit `publish` request authorizes branch push, draft creation, readiness, monitoring, in-scope fixes, squash merge, and integration verification.

Push the task branch. Open a draft pull request. Verify its base, head, scope, title, and body.

Post `@codex review`. Keep the pull request draft while Codex reviews the current head.

Treat each review comment as a candidate finding. Apply Adversarial Review before you use its severity or change the candidate.

Follow the Adversarial Review result. Apply Delivery Lifecycle to each accepted correction.

A current-head review is clean when it completes with no retained applicable finding.

A Codex thumbs-up reaction is sufficient evidence of a clean review. It is not the only clean result.

Respond to each excluded finding with its boundary evidence. Resolve its conversation. An excluded finding does not block readiness.

If a correction needs a push, keep the pull request draft. If it is ready, convert it to draft before the push.

Each push resets the required CI and Codex review gates. Post `@codex review` again for the new head.

Mark the pull request ready only after the current-head review is clean. Hosted CI can start after readiness.

If hosted CI starts while the pull request is draft, stop and report the repository configuration error.

Before merge, require successful checks for the latest head. Require no requested changes and GitHub mergeability.

Respond to every conversation. Push a required fix before you resolve its conversation. Resolve all conversations before merge.

Squash-merge after all gates pass. Verify that `main` contains the result. Then monitor required post-merge CI.

Publication ends after verified integration.

Commit and push do not authorize a pull request or release.

Publication does not authorize tag creation, a GitHub release, or cleanup.

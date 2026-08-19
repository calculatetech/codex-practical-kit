<!-- cpk-rule-owner: publication -->
<!-- cpk-rule-guard: PR mode is active only when protected `main` requires pull requests, required CI checks, and resolved conversations. -->
<!-- cpk-rule-guard: Before merge, require successful checks for the latest head. Require no requested changes and GitHub mergeability. -->
<!-- cpk-rule-guard: Publication does not authorize tag creation, a GitHub release, or cleanup. -->
<!-- cpk-rule-guard: Before Codex Practical Kit publication, use the Windows PowerShell launchers on Windows and the shell launchers elsewhere. Require `Result: ready`. -->

# Publication

## Tracked state

<!-- cpk-rule-route-only: delivery-lifecycle -->
[Delivery lifecycle](../../delivery-lifecycle/references/delivery-lifecycle.md)

## Procedure

Before Codex Practical Kit publication, use the Windows PowerShell launchers on Windows and the shell launchers elsewhere. Require `Result: ready`.

On Windows, run `pwsh -File .\install.ps1` and `pwsh -File .\doctor.ps1`. On macOS or Linux, run `./install.sh` and `./doctor.sh`. Run the commands from the reviewed candidate.

PR mode is active only when protected `main` requires pull requests, required CI checks, and resolved conversations.

CI must contain at least one workflow. Its workflows must supply every required check. If any condition is false, PR mode is off.

If PR mode is off, use direct integration. Do not create a pull request.

When PR mode is off, `publish` authorizes branch push, merge to `main`, integration verification, and required post-merge CI.

When PR mode is active, use a pull request for every change, including bounded documentation.

One explicit `publish` request authorizes branch push, draft creation, readiness, monitoring, in-scope fixes, squash merge, and integration verification.

Push the task branch. Open a draft pull request. Verify its base, head, scope, title, and body. Then mark it ready.

Use the configured automatic Codex review. Do not request the review manually.

Before merge, require successful checks for the latest head. Require no requested changes and GitHub mergeability.

Require a Codex thumbs-up reaction after the latest push. Each push resets the required CI and Codex review gates.

Respond to every conversation. Push a required fix before you resolve its conversation. Resolve all conversations before merge.

Apply the validation and pre-commit review rules to an in-scope code fix.

If feedback changes accepted scope, stop for human direction. If feedback requires an architecture decision, stop for human direction.

Squash-merge after all gates pass. Verify that `main` contains the result. Then monitor required post-merge CI.

Publication ends after verified integration.

Commit and push do not authorize a pull request or release.

Publication does not authorize tag creation, a GitHub release, or cleanup.

<!-- cpk-rule-owner: delivery-lifecycle -->
<!-- cpk-rule-guard: Finalize substantive documentation before review. -->
<!-- cpk-rule-guard: Keep detailed results in one ignored `.agent/test-results/` file per task. -->
<!-- cpk-rule-guard: Freeze every tracked task record before the task commit, CI, push, pull request, merge, or publication. -->
<!-- cpk-rule-guard: Invoke Design Preflight before implementation or an accepted review correction when its trigger matches, even outside Plan Mode. -->

# Delivery lifecycle

Do not perform unrelated refactors, dependency updates, formatting, or fixes.

Invoke Design Preflight before implementation or an accepted review correction when its trigger matches, even outside Plan Mode.

Validate every implementation with relevant tests and linting. Add one runnable check for non-trivial logic.

Keep detailed results in one ignored `.agent/test-results/` file per task. Never stage that file.

If `docs/roadmap.md` exists, use Roadmap Maintainer before implementation and at each lifecycle transition.

Use Docs Maintainer for behavior, setup, command, configuration, interface, operation, or architecture changes.

Use repository-root `docs/` for prose and static documentation assets. Keep source, scripts, builds, and configuration with their runtime owner.

Finalize substantive documentation before review.

Run Adversarial Review after source, tests, dependencies, migrations, configuration, or substantive documentation changes.

Do not start review after a commit, push, pull request, or CI action. Report a missed pre-commit review.

After clean review, apply Review Closure.

Freeze every tracked task record before the task commit, CI, push, pull request, merge, or publication.

After the freeze, record delivery progress and results only in Git, GitHub, the ignored task result, and the final response.

A substantive correction reopens the candidate. Finalize its applicable documentation, validation, review, and closure before the next freeze.

End the final response with one `Review:` status and one `Docs:` status from the applicable skills.

## Design gate

<!-- cpk-rule-route-only: design-preflight -->
[Design Preflight](../../design-preflight/SKILL.md)

## Repository context

<!-- cpk-rule-route-only: repository-knowledge -->
[Repository Knowledge](../../repository-knowledge/SKILL.md)

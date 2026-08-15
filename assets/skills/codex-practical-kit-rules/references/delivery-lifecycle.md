<!-- cpk-rule-owner: delivery-lifecycle -->
<!-- cpk-rule-guard: Finalize documentation and roadmap content before review and commit. -->
<!-- cpk-rule-guard: Keep detailed results in one ignored `.agent/test-results/` file per task. -->

# Delivery lifecycle

Do not perform unrelated refactors, dependency updates, formatting, or fixes.

Validate every implementation with relevant tests and linting. Add one runnable check for non-trivial logic.

Keep detailed results in one ignored `.agent/test-results/` file per task. Never stage that file.

If `docs/roadmap.md` exists, use Roadmap Maintainer before implementation and at each lifecycle transition.

Use Docs Maintainer for behavior, setup, command, configuration, interface, operation, or architecture changes.

Use repository-root `docs/` for prose and static documentation assets. Keep source, scripts, builds, and configuration with their runtime owner.

Finalize documentation and roadmap content before review and commit.

Run Adversarial Review after source, tests, dependencies, migrations, configuration, or substantive documentation changes.

Do not start review after a commit, push, pull request, or CI action. Report a missed pre-commit review.

Do not change documentation after the task commit.

End the final response with one `Review:` status and one `Docs:` status from the applicable skills.

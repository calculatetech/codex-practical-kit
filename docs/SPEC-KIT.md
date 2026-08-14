# Optional Spec Kit

Spec Kit is optional behavior input. ExecPlan remains the implementation owner.

Use Design Preflight first. Put accepted decisions into one ExecPlan.

The ExecPlan records:

- Goal.
- Existing owner.
- Must work.
- Must not change.
- Checks.
- Unknowns.

Add Spec Kit when the task needs more behavior detail. Good signals include:

- A new application.
- A feature with several user stories.
- Several teams or reviewers.
- A long implementation with durable plan and task artifacts.
- A need for repeatable specification commands across many repositories.

## Install

Use the current official installation guide. A typical Codex skills-mode setup is:

```bash
uv tool install specify-cli
specify init --here --integration codex --integration-options="--skills"
```

Run `specify integration list` first when the installed release changes its integration names or options.

## One owner rule

Do not use Spec Kit artifacts as a second implementation tracker.

When Spec Kit supplies the behavior specification:

- Its specification is the durable behavior source.
- The ExecPlan owns implementation decisions and progress.
- Design Preflight reviews the Spec Kit artifacts and feeds accepted decisions into the ExecPlan.
- Ponytail controls implementation size.
- Adversarial Review checks the completed diff against the Spec Kit intent.
- SimpleEnglish controls prose.
- Docs Maintainer checks public documentation.
- RepoWise remains repository evidence, not the specification owner.

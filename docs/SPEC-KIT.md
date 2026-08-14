# Optional Spec Kit

Spec Kit is not the default glue.

Use Design Preflight first. Put the accepted result into one Task Brief when the work needs a durable handoff.

That small path asks for:

- Goal.
- Existing owner.
- Must work.
- Must not change.
- Checks.
- Unknowns.

Add Spec Kit when one brief is no longer enough. Good signals include:

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

Do not use Task Brief and Spec Kit as two parallel specifications for the same work.

When Spec Kit owns the work:

- Its specification is the durable behavior source.
- Its plan and tasks own implementation progress.
- Design Preflight reviews the Spec Kit artifacts instead of creating another brief.
- Ponytail controls implementation size.
- Adversarial Review checks the completed diff against the Spec Kit intent.
- SimpleEnglish controls prose.
- Docs Maintainer checks public documentation.
- RepoWise remains repository evidence, not the specification owner.

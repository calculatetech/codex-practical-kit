# Optional review and pre-implementation tools

The core kit does not install these tools.

Add one only when a real task needs its specialty.

## Compound Engineering

Source: https://github.com/EveryInc/compound-engineering-plugin

Best fit:

- Full risk-selected multi-agent code review.
- Multi-persona review of requirements and implementation plans.
- Cross-model adversarial review.
- Durable solution notes after a bug is solved.

Why it is not bundled:

- It is a complete engineering workflow with many skills.
- It overlaps Ponytail, ExecPlan, docs maintenance, research, and the kit review loop.
- The core `ce-code-review` skill has a large support tree and helper scripts.

Install when you want the full workflow:

```bash
codex plugin marketplace add EveryInc/compound-engineering-plugin
codex plugin add compound-engineering@compound-engineering-plugin
```

The kit borrowed these ideas, not its code:

- Structured and deduplicated findings.
- Clean review context.

The core kit adds a supported-model gate and uses one reviewer. Install Compound Engineering only when a task explicitly needs broader review.

License: MIT.

## Superpowers

Source: https://github.com/obra/superpowers

Best fit:

- Strict design approval before implementation.
- Test-first development.
- Fresh implementer and reviewer subagents per task.
- Durable task ledgers for long sessions.

The kit uses its clean-context review-packet idea. It does not install the full workflow because that would add more ceremony than most tasks need.

License: MIT.

## Trail of Bits Skills

Source: https://github.com/trailofbits/skills

The marketplace supports Codex.

```bash
codex plugin marketplace add trailofbits/skills
codex plugin list
codex plugin add <plugin-name>@trailofbits
```

Useful plugins:

### `audit-context-building`

Use when the code is unfamiliar or a previous review produced findings that nobody can judge. It records per-function assumptions, promises, and dependencies before the defect hunt starts.

### `property-based-testing`

Use for parsers, serialization pairs, validators, normalization, state machines, data structures, and mathematical logic.

It generates many inputs from stated properties. This often finds boundary cases before review.

### `differential-review`

Use for security-sensitive diffs. It adds Git history, blast radius, test gaps, and concrete attack scenarios.

### `spec-to-code-compliance`

Use when a durable specification exists and the change is critical. It checks each requirement separately and performs a reverse sweep for undocumented behavior.

### `sharp-edges`

Use before public or security-sensitive API design. It looks for dangerous defaults, silent failures, confusing parameters, and easy misuse.

### `second-opinion`

Use when a different model or harness is available. It runs an external Codex or Gemini review for stronger independence.

### `mutation-testing`

Use when the language is supported and the test suite looks green but weak. It changes production code deliberately and measures whether tests notice.

Why these are not bundled:

- They are specialized.
- Several require extra tools or long runs.
- The marketplace license is CC BY-SA 4.0. The kit does not copy the skill text.

## RepoWise

RepoWise is the kit's required repository context provider.

Read the canonical [Repository knowledge](../assets/skills/repository-knowledge/SKILL.md) rule when a task uses it.

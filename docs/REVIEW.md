# Supported-model review

Review protects the behavior that the project supports. It does not expand the project.

## Order

```text
implementation
  -> checks
  -> documentation
  -> roadmap terminal state
  -> one fresh correctness reviewer
  -> commit
```

Documentation must be final before review and commit.

## Finding gate

For each finding, answer:

1. Does the trigger occur during supported normal use?
2. Does the project control the trigger and result?
3. Does current code reliably produce the wrong result without fault injection?
4. Does the result violate an explicit requirement?

All answers must be true. Drop the finding if one answer is false. Do not add it to the roadmap or residual-risk list.

## Default exclusions

The toolkit supports one personal user, one Codex writer, normal local filesystems, and normal Git.

Do not review these conditions unless the active task includes one:

- I/O faults.
- Permission changes.
- Link topology.
- Concurrent or outside writers.
- Interrupted or partial operations.
- Retry, restart, or recovery.
- Git submodules.
- Hostile or contradictory completion-marker text.

## One reviewer

Each pass uses one new clean-context reviewer. The reviewer receives the actual diff, relevant source, project rules, checks, supported model, and exclusions.

Always use the correctness lens. Add another lens to the same reviewer only when the active task explicitly names that risk.

Do not use a separate refuter. The coordinator reads the cited source and applies the four true or false checks.

## Three passes

A validated P0, P1, or P2 correctness defect makes the pass defectful.

For pass 1 or 2, fix the smallest shared cause with Ponytail. Add one focused check. Finalize documentation again. Then use a new reviewer.

If pass 3 finds a validated defect, stop. Wait for human direction.

## Final markers

```text
Review: clean — pass 1.
Docs: no change needed — behavior is unchanged.
```

```text
Review: clean after fixes — pass 2.
Docs: updated README.md.
```

```text
Review: stopped — defects found in three consecutive passes; human direction required.
Docs: no change needed — implementation is not accepted.
```

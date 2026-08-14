# Supported-model review

Review protects the behavior that the project supports. It does not expand the project.

## Order

```text
implementation
  -> checks
  -> documentation
  -> roadmap ready-for-review state
  -> one fresh correctness reviewer
  -> review closure
  -> commit
```

Documentation must be final before review and commit.

Review closure records the review result, moves the reviewed roadmap task to its terminal state, and updates matching integrity metadata. These changes do not require another review.

A change to behavior, tests, configuration, requirements, or the supported model invalidates review. Use a fresh reviewer for the corrected candidate.

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

## Three-defect breaker

A validated P0, P1, or P2 correctness defect in executable source, tests, migrations, dependencies, or runtime, build, or security configuration makes a counted implementation-defect pass.

If no severe stop applies, fix each validated in-scope finding. Use the smallest shared correction. Add one focused check. Finalize documentation again. Then use a new reviewer.

Documentation and review-housekeeping findings remain actionable, but they neither increment nor reset the three-defect count.

These results cause a severe stop:

- A validated P0 or P1 finding on any pass.
- An architecture flaw that makes a local patch unsafe.
- An implementation defect on the third consecutive counted pass.

At every stop, present each validated stop finding as a separate decision handoff. Do not combine findings into one handoff.

For a severe stop, close the reviewer. Run one clean-context `defect-diagnostic`. Present its portable summary. Then halt for human direction.

After the halt, do not edit, run checks, start review, commit, publish, run CI, change task state, or create follow-up work.

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
Review: stopped — implementation defects found in three counted passes; human direction required.
Docs: no change needed — implementation is not accepted.
```

```text
Review: stopped — severe defect diagnostic complete; human direction required.
Docs: no change needed — implementation is not accepted.
```

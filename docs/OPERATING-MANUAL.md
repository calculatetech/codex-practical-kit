# Operating manual

## Small change

Read the real execution path. Fix the shared cause. Run one focused check. Finalize documentation and roadmap state. Then run one review.

## Non-trivial change

Use Design Preflight for a multi-file change, public interface, persistent product state, external service, or unclear owner.

State the supported operating model. Define the normal-use behavior floor and hard scope ceiling.

For each exceptional condition, require four true answers:

1. Does it occur during supported normal use?
2. Does the project control it?
3. Does current code reproduce it without fault injection?
4. Does it violate an explicit requirement?

If one answer is false, exclude the condition.

## Roadmap lifecycle

Use `docs/roadmap.md` as the only roadmap authority. Record accepted work before implementation. Make one task Active before its first implementation edit.

Update the roadmap when scope, order, priority, blocking state, or terminal state changes.

Use Declined for work that the user intentionally does not support. Do not report excluded review findings as residual risk.

## Plan Mode

Plan Mode is read-only. Do not edit tracked files, stage, commit, publish, or activate a roadmap task.

The Stop hook returns immediately in Plan Mode. After Plan Mode ends, reread the repository and roadmap before implementation.

## Review

Finalize documentation and roadmap state before review. Use one fresh read-only correctness reviewer per pass.

Give the reviewer the task, diff, source, supported model, exclusions, and completed checks.

Apply the four true or false checks to each finding. Drop a finding when one answer is false.

Use another lens only when the active task names that risk. Do not spawn a separate refuter.

Passes 1 and 2 can cause a focused correction. If pass 3 finds a validated defect, stop for human direction.

## Stop hook

The hook compares plain Git status with the Session Start baseline.

Equal status permits Stop. Documentation changes require a current Docs marker. Other changes require current clean Review and Docs markers.

The hook is a reminder. It does not prove commit identity or invalidate earlier messages after each content edit.

## Installation

The installer copies skills to the shared skills directory. The install manifest lists the copied names that the toolkit owns.

Reinstallation replaces manifest-owned copies only in the recorded skills directory. An unrecorded destination is a conflict. Move or remove the conflict before installation.

The `0.2.1` upgrade removes recorded skill links and writes ordinary copies.

## Uninstall

Uninstall uses the manifest's recorded skills and Codex directories. It removes those copied skills and the managed instruction and hook blocks.

If the manifest is absent, uninstall changes nothing. Use `--purge` to remove toolkit files.

A successful uninstall removes the manifest. A second uninstall changes nothing.

If an operation fails, the command stops and reports the error. The toolkit does not retry or repair partial work.

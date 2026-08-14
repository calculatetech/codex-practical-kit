# Why this shape

The toolkit solves one narrow problem. It helps Codex do useful work without adding speculative machinery.

## Before code

Design Preflight defines the supported operating model, normal-use behavior, owner, scope ceiling, and exact checks.

The four true or false checks prevent possible conditions from becoming automatic requirements.

One ExecPlan records durable implementation decisions and progress. Plan Mode and Design Preflight feed it instead of creating competing records.

## During code

Ponytail reuses existing code and native features. It stops at the first solution that satisfies the accepted task.

The toolkit policy adds deterministic least effort. Operations try once and report failure. Exceptional behavior needs explicit authorization.

## Before review

Docs Maintainer makes user documentation true. Roadmap Maintainer records the final task state.

Both finish before review and commit. Documentation never changes after the task commit.

## Review

One fresh reviewer checks correctness in the supported model. The coordinator drops every finding that fails one true or false check.

The three-defect breaker stops recursive implementation correction after three counted passes. Documentation and review-housekeeping findings remain actionable, but they neither increment nor reset the three-defect count.

## Repository knowledge

RepoWise provides leads about callers, decisions, and tests. The kit requires its code graph, initializes it on first start, and updates it after commits. Source remains authoritative.

## What the toolkit does not become

The toolkit does not become a service, database, proof system, transaction manager, recovery framework, or universal risk model.

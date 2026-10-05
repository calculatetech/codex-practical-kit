# Set the managed-update publication version

This ExecPlan is a living specification until review closure. Follow `.agent/PLANS.md`.

## Purpose / Big Picture

Users must be able to identify the combined managed-update feature and 12UI compatibility correction as toolkit version `0.25.0`. Publication carries CPK-061, CPK-062, and CPK-063 together without changing their final behavior.

## Context and Orientation

`kit.py::KIT_VERSION` owns the toolkit identity. `IntegrationTests.test_lifecycle_skills_and_version` checks that identity. `MANIFEST.sha256` records distribution file checksums. The managed update commands and retained website-only routing are documented in README and the completed CPK-061 through CPK-063 specifications.

The metadata task uses branch `cpk-064-publish-managed-updates` from `cpk-063-12ui-codex-compatibility` at `4a5a657a9f01ce11de33ed9759db05450164aefe`. One writer uses the primary checkout. Local main and origin/main match at `00f3af7e9e91fdb7ddd31c529863c616522cdd82`. No applicable Plan Mode record or untracked Plan handoff applies to this publication.

## Product Boundary

The source is the user's explicit `publish` request. Follow [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md), [Versioning](../../assets/skills/publication/references/versioning.md), and [Publication](../../assets/skills/publication/references/publication.md).

Version identity, its existing check, and distribution checksums compose this metadata task. Completed runtime behavior is opaque and retains its accepted result. Publication uses the existing protected-main pull-request workflow. No owner is promoted from deferred behavior. The model is one personal user and one writer with normal local files and Git.

The ceiling excludes new runtime behavior, dependency changes, unrelated fixes, tag creation, a GitHub release, and branch or worktree cleanup. Design Preflight uses its small-change exception: one proven version owner and one direct existing check. No behavioral boundary or non-trivial runtime path changes.

## Decision Log

- Decision: use source version `0.25.0`.
  Rationale: committed version `0.24.1` precedes the new explicit update check and apply commands. This publication includes a feature, not only the later compatibility fix.
- Decision: keep the completed CPK-061 through CPK-063 commits and specifications unchanged.
  Rationale: version preparation is a new metadata task. It does not rewrite completed implementation decisions.
- Decision: publish through a draft pull request and squash integration.
  Rationale: main requires a pull request, `toolkit-tests`, and resolved conversations. The existing CI workflow starts on readiness and main pushes, not task-branch pushes or draft creation.

## Plan of Work

One atomic metadata subtask, CP1, changes `kit.py::KIT_VERSION` and its existing assertion to `0.25.0`. Add this specification and its roadmap entry, then update distribution checksums. Existing README and installation guidance contain no current toolkit version literal that needs replacement.

Validate and review the metadata task from its base. The previous task commits retain their recorded local review gates. Follow the linked publication procedure for the combined pull request, hosted review, required CI, squash merge, and local main integration.

## Concrete Steps

Run from `/home/mbeutler/Projects/codex-practical-kit`:

    PYTHONPATH=tests python3 -m unittest test_kit.IntegrationTests.test_lifecycle_skills_and_version -v
    ./run-tests.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

After local review and its closure, run `./install.sh` and `./doctor.sh` from the frozen candidate before pushing the task branch.

## Validation and Acceptance

Require the existing version check and required repository checks to pass. Doctor must report toolkit version `0.25.0` and `Result: ready`. The hosted review must cover the current pull-request head. Publication finishes with local main equal to origin/main and containing the recorded squash result.

## Idempotence and Dependencies

Version preparation uses the existing constant and test. It adds no dependency or interface. Preserve unrelated untracked files. Use the existing Git and GitHub operations, and report an operation failure without inventing recovery.

## Outcomes & Retrospective

The source and selected installation identify the managed-update feature and compatible 12UI ownership model as version `0.25.0`. The toolkit retains the user's applied component pins and separately installed 12UI state.

# Define version increments

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

After this change, Codex selects one predictable toolkit version for each deliverable change. Version `0.x` identifies initial development. Version `1.0.0` identifies the first production-ready release. Normal `0.x` releases remain visible as full GitHub releases.

## Progress

- [x] (2026-08-14 02:48Z) Compared the current repository with Semantic Versioning and GitHub release guidance.
- [x] (2026-08-14 02:48Z) Integrated CPK-004, created `cpk-005-version-policy`, and activated CPK-005.
- [x] (2026-08-14 02:51Z) Reconciled the distributed version and release-boundary rules.
- [x] (2026-08-14 02:51Z) Added one focused policy check and set version `0.7.0`.
- [x] (2026-08-14 02:51Z) Finalized documentation, the ready-for-review roadmap state, and the checksum manifest. All 26 tests and lint checks pass.
- [x] (2026-08-14 02:54Z) Corrected the P2 omission from review pass 1. Repeated all 26 tests and lint checks successfully.
- [x] (2026-08-14 02:56Z) Completed fresh adversarial review. Pass 2 was clean after the pass-1 policy correction. Applied review closure.

## Surprises & Discoveries

- Observation: The repository has no Git tags, GitHub releases, or tracked CI workflow.
  Evidence: `git tag`, `gh release list`, and `git ls-tree HEAD .github` returned no entries.
- Observation: Semantic Versioning separates initial development from a suffixed prerelease.
  Evidence: Version `0.y.z` is initial development. A suffix such as `-beta.1` has lower precedence than its normal version.
- Observation: GitHub excludes prereleases from its latest full release API.
  Evidence: GitHub defines the latest release as a published release that is not a draft or prerelease.
- Observation: Review pass 1 found that the full policy owners omitted the required `0.1.0` starting value.
  Evidence: They defined the `0.MINOR.PATCH` pattern but did not define its first value.

## Decision Log

- Decision: Start initial development at `0.1.0` and reserve `1.0.0` for the first production-ready public contract.
  Rationale: This matches the user policy and Semantic Versioning.
  Date/Author: 2026-08-14 / user and Codex
- Decision: During initial development, increment the minor number for a feature or breaking change. Increment the patch number for a bug fix or published checkpoint in the same feature line.
  Rationale: This gives each pre-1.0 number one stable project meaning.
  Date/Author: 2026-08-14 / user and Codex
- Decision: Do not change the version for a local Git checkpoint commit.
  Rationale: A local checkpoint is not a distributed toolkit release.
  Date/Author: 2026-08-14 / Codex
- Decision: Do not use alpha or beta suffixes by default.
  Rationale: Version `0.x` already states initial development. Suffixes add value only for public testing of one target version.
  Date/Author: 2026-08-14 / Codex
- Decision: Publish normal `0.x` versions as full GitHub releases.
  Rationale: GitHub excludes prereleases from the latest full release result.
  Date/Author: 2026-08-14 / Codex
- Decision: Use source version `X.Y.Z` and Git tag `vX.Y.Z`.
  Rationale: Semantic Versioning identifies `v1.2.3` as a common tag name for semantic version `1.2.3`.
  Date/Author: 2026-08-14 / Codex

## Outcomes & Retrospective

The toolkit now has one version policy from `0.1.0` through production releases. All 26 tests and lint checks pass. Review pass 1 found one omitted starting value, which the corrected test now prevents. Fresh review pass 2 was clean. The final local task-branch commit is authorized next. Push, pull request creation, tag creation, release publication, merge, and cleanup remain unauthorized.

## Context and Orientation

The task uses branch `cpk-005-version-policy`. Its base branch is `main`, and its base commit is `46e83562459cf81c97be353bcc21340d46a54919`. The isolation form is a normal branch in the existing checkout.

`kit.py` owns the current version in `KIT_VERSION`. `README.md` and `CODEX-INSTALL-PROMPT.md` show the current version to users. `assets/AGENTS.block.md` owns the distributed agent policy. `assets/hooks/session_start.py` gives compact session guidance. `.agent/PLANS.md` owns ExecPlan requirements. `docs/OPERATING-MANUAL.md` owns the complete user procedure. `tests/test_kit.py` checks propagation. `MANIFEST.sha256` covers distributed files.

A published feature checkpoint is a coherent subset of one feature line that users can install. It is different from a local checkpoint commit. A prerelease suffix is an identifier such as `-alpha.1` or `-beta.1` that marks public testing of a specific future version.

## Plan of Work

Add one version-policy section to the distributed AGENTS block. Define pre-1.0 feature, fix, checkpoint, and breaking-change increments. Define post-1.0 Semantic Versioning increments. State that documentation-only work and local checkpoint commits do not change the toolkit version unless the user authorizes a release.

Select the target version when implementation scope is fixed. Record it in the ExecPlan. Update `KIT_VERSION`, the README current-version statement, and the installation prompt before validation and review. Regenerate the checksum manifest after these files are final.

Use alpha only for incomplete public testing. Use beta only after feature scope is complete and validation continues. Mark only suffixed versions as GitHub prereleases. Publish normal `0.x` versions as full releases so GitHub can identify a latest release.

Define one release boundary. The semantic version in `kit.py` must equal the Git tag without its `v` prefix. The tag must identify the exact integrated commit. A version becomes consumed when its tag reaches GitHub. Do not move or reuse a consumed version. If publication fails before the remote tag exists, correct the candidate without another version increment. If publication fails after the remote tag exists, preserve the tag and stop for human direction.

Add one focused consistency check. Do not add a version command, release script, changelog generator, tag automation, or GitHub workflow. CPK-006 owns publication behavior.

## Concrete Steps

Work from `/home/mbeutler/Projects/codex-practical-kit` on `cpk-005-version-policy`.

Run:

    ./run-tests.sh
    python3 -m py_compile kit.py tests/test_kit.py assets/hooks/session_start.py
    sh -n doctor.sh install.sh run-tests.sh setup-repo.sh uninstall.sh
    git diff --check
    sha256sum --check MANIFEST.sha256

After validation, keep CPK-005 Active and mark review pending. Run one fresh read-only adversarial review on the cumulative diff from the base commit. After a clean result, apply only review closure and make the final local branch commit. Do not push CPK-005.

## Validation and Acceptance

The focused check must prove that the full policy, compact session rule, ExecPlan rule, and current-version owners agree.

Acceptance includes these examples. A feature changes `0.6.2` to `0.7.0`. A bug fix changes `0.7.0` to `0.7.1`. A published checkpoint in the same feature line changes `0.7.1` to `0.7.2`. A local checkpoint commit does not change the version. A pre-1.0 breaking change changes `0.7.2` to `0.8.0`. The first production-ready release is `1.0.0`. A post-1.0 breaking change increments the major number.

## Idempotence and Recovery

Version selection occurs once after task scope is fixed. If validation, review, merge, or CI fails before the remote tag exists, keep the selected version and correct the candidate. If a remote tag exists, treat its version as consumed. Stop after an operation error. Do not retry, move a tag, or reuse a consumed version.

## Artifacts and Notes

Record detailed results in `.agent/test-results/cpk-005-version-policy.md`. This ignored file is not part of the candidate. Preserve the existing untracked `.claude/`, `.codex/`, `.mcp.json`, `.repowise/`, `.vscode/`, and root `AGENTS.md` paths.

Research sources:

- Semantic Versioning 2.0.0: https://semver.org/
- GitHub release management: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository
- GitHub latest release API: https://docs.github.com/en/rest/releases/releases#get-the-latest-release
- GitHub immutable releases: https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases

## Interfaces and Dependencies

No public command or dependency changes. The installed agent policy gains version selection and release-boundary rules. The toolkit version becomes `0.7.0`.

Revision note: Created from the accepted preparation result, official guidance, and Design Preflight. Updated after implementation and validation to record the review-ready candidate. Updated after review pass 1 to add the required `0.1.0` starting value.

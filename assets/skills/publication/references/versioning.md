<!-- cpk-rule-owner: versioning -->
<!-- cpk-rule-guard: Before `1.0.0`, increment the minor number for a feature or breaking change. -->
<!-- cpk-rule-guard: A version is consumed when its tag reaches GitHub. -->

# Versioning

Read the committed source version before you select the next version.

Start initial development at `0.1.0`. Use `0.MINOR.PATCH` during initial development. Version `1.0.0` is the first production-ready release.

Before `1.0.0`, increment the minor number for a feature or breaking change. Reset the patch number to zero.

Before `1.0.0`, increment the patch number for a bug fix or a published checkpoint in the same feature line.

A published feature checkpoint is a coherent subset that users can install.

After `1.0.0`, increment the major number for a breaking change. Increment the minor number for a feature. Increment the patch number for a fix.

A local checkpoint commit does not change the version.

Unreleased documentation, comments, formatting, plans, tests, and review closure do not change it either.

Select the target version after task scope is fixed. Record it in the task ExecPlan. Update source-version references and checksums before validation.

Do not use alpha or beta suffixes by default. Use an alpha suffix for incomplete public testing. Use a beta suffix after feature scope is complete.

Mark only a suffixed test version as a GitHub prerelease.

Publish a normal `0.x` version as a full GitHub release.

Use source version `X.Y.Z` and Git tag `vX.Y.Z`.

The tag must identify the exact integrated commit. Do not move or reuse the tag.

A version is consumed when its tag reaches GitHub.

If publication fails before the remote tag exists, keep the selected version and correct the candidate.

If publication fails after the remote tag exists, preserve the tag and stop for human direction.

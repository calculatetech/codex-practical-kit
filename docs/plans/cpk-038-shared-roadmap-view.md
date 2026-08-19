# Keep one live roadmap view across worktrees

This ExecPlan is a living document until review closure. Maintain it according to `.agent/PLANS.md`.

## Purpose

Users must be able to keep one roadmap file open while Codex works in linked Git worktrees. `docs/roadmap.md` remains the only roadmap authority. The toolkit generates a stable, read-only projection in the primary checkout after an actual roadmap edit.

## Progress

- [x] (2026-08-19) Recovered the accepted Plan Mode response and stored it beside this ExecPlan.
- [x] (2026-08-19) Completed adversarial design preflight and official Codex hook research.
- [x] (2026-08-19) Created the isolated `cpk-038-shared-roadmap-view` worktree from CPK-037.
- [x] (2026-08-19) Implemented the managed edit hooks and generated view lifecycle.
- [x] (2026-08-19) Updated the roadmap authority and user documentation.
- [x] (2026-08-19) Passed 57 tests, Python compilation, shell syntax, skill validation, diff checks, and manifest checksums.
- [x] (2026-08-19) Corrected the parent-path collision from full review pass 1.
- [x] (2026-08-19) Completed delta and coherence review, then closed the task.

## Prior Plan Reconciliation

- `docs/plans/cpk-038-shared-roadmap-view.plan-summary.20260819T195712262086Z.manual-recovery.md`: carried. The Plan history hook did not create its normal record, so the exact completed response was recovered from the thread before implementation.

## Plan Deviations

No accepted decision has changed.

## Surprises and Discoveries

- Observation: The patch path can identify a linked worktree even when hook `cwd` identifies the original checkout.
  Evidence: The first focused implementation test used the linked worktree as `cwd`. Self-review reproduced the real `../linked/docs/roadmap.md` form and required target-owned root discovery.
- Observation: A user-owned `.codex` file is a collision before `.codex/roadmap-view.md` exists.
  Evidence: Full review pass 1 showed that directory creation failed only after the exclusion changed. The collision guard now checks the parent path first.

## Decision Log

- Decision: Generate `.codex/roadmap-view.md` only after an exact roadmap edit changes the source bytes.
  Rationale: Session startup does not prove which worktree is authoritative.
  Date/Author: 2026-08-19 / Codex
- Decision: Pair `PreToolUse` and `PostToolUse` fingerprints instead of interpreting tool output.
  Rationale: The official hook contract defines the tool input but does not define one stable success shape for `tool_response`.
  Date/Author: 2026-08-19 / Codex
- Decision: Keep global uninstall repository-agnostic, but let `remove-repo` delete owned projection state.
  Rationale: Global installation has no safe list of every repository touched by runtime hooks.
  Date/Author: 2026-08-19 / Codex

## Context

The task worktree is `/home/mbeutler/Projects/codex-practical-kit-cpk-038` on branch `cpk-038-shared-roadmap-view`. It is stacked on CPK-037 commit `4ae47a1c5dffc2cc6e8d2a690f8041e4b54b2d82`, which already restricts `additionalContextLimit` to context-producing hooks.

`assets/hooks/session_start.py` dispatches all current managed hook events. `kit.py` installs and detects the marked `config.toml` hook block. `tests/test_kit.py` exercises installation and hook payloads. The official Codex Hooks documentation defines `PreToolUse` and `PostToolUse` support for `apply_patch`, including `cwd`, `tool_use_id`, and `tool_input.command`.

## Product Boundary

`docs/roadmap.md` remains the only roadmap authority and the only agent write target. `.codex/roadmap-view.md` is a generated human projection. The supported model is one active roadmap writer in a normal non-bare Git repository. Manual edits, concurrent writers, deletion or rename synchronization, symlinked layouts, submodules, retries, and recovery are excluded.

## Scenario Proof

| Scenario | Discriminator | Production path | Required oracle | Runnable check | Result |
| --- | --- | --- | --- | --- | --- |
| First roadmap creation | Absent file becomes present | Pre-hook fingerprint to post-hook projection | Owned view and exclusion appear with unchanged source bytes | focused hook test | Passed |
| Linked-worktree update | Source checkout differs from primary checkout | Exact patch path to shared Git directory | Primary view contains linked-worktree roadmap, not primary source | focused hook test | Passed |
| Failed or no-op patch | Source fingerprint does not change | Paired hook state | Existing view and exclusion remain byte-identical | focused hook test | Passed |
| Complete patch scan | Lookalike precedes exact operation | Full operation parser | Later exact roadmap operation refreshes the view | focused hook test | Passed |
| Unrelated or lookalike edit | Resolved target differs | Exact normalized path guard | No projection state changes | focused hook test | Passed |
| User-owned collision | Destination or parent path is user-owned | Collision check before exclusion | File, exclusion, and Git visibility stay unchanged; one warning appears | focused hook tests | Passed |
| Hook lifecycle | Managed versus unrelated handlers | Install, reinstall, uninstall | Exact managed matchers are present once; unrelated hooks remain | installer tests | Passed |
| Repository removal | Owned versus user-owned projection | `remove-repo` cleanup | Only owned view and exclusion block are removed | integration test | Passed |

## Implementation

Reuse the existing hook script and Python standard library. Parse all `*** Add File:` and `*** Update File:` headers from `tool_input.command`. Resolve them against `cwd`, and retain only the exact roadmap under that worktree root.

On `PreToolUse`, store the source fingerprint in temporary state keyed by the session and tool-use identifiers. On `PostToolUse`, remove that state, compare the live source, and continue only when the bytes changed. Resolve the primary checkout from the absolute shared Git directory. Check destination ownership before adding a marked block to the common `info/exclude`. Replace the owned view with a generated banner plus source content. Emit no output on success and one `systemMessage` on an applicable failure.

Add managed `PreToolUse` and `PostToolUse` groups with matcher `^apply_patch$`. Preserve unrelated hooks. Keep `additionalContextLimit` only on Session Start and User Prompt Submit.

Teach `remove-repo` to remove the owned view and marked exclusion block. Do not enumerate repositories during global uninstall.

Update Roadmap Maintainer as the sole rule owner. Add a short user procedure that tells users to open the generated view and edit only the tracked roadmap.

## Validation

Run focused installer and hook tests, `./run-tests.sh`, Python compilation, shell syntax checks, `git diff --check`, and `sha256sum --check MANIFEST.sha256`. Store detailed results in `.agent/test-results/cpk-038-shared-roadmap-view.md`.

## Outcomes

The implementation is complete and validated. Full review pass 1 found one P2 collision defect. The correction passed delta review, and the complete task passed final coherence review.

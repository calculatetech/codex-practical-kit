# Restore finished-thread archival

This ExecPlan follows [`.agent/PLANS.md`](../../.agent/PLANS.md).

## Purpose / Big Picture

Coordinators must archive finished delegated threads as the user requested. They must not require an unrelated agent-close operation before archival.

The user clarified the original request on October 5, 2026: “I specically said to archive threads, not close_agent in the original request.” This clarification supplies the accepted result. It rejects the closure requirement introduced in CPK-061.

## Context and Orientation

`assets/skills/delivery-lifecycle/references/coordination.md` owns the live coordination rule. `tests/test_kit.py` contains three direct checks for terminal cleanup, archive targeting, and required follow-ups. `MANIFEST.sha256` records package contents.

Native archival changes persisted thread history. The exposed tool accepts an explicit thread identifier and can archive descendants. Toolkit code does not implement that operation or control agent capacity.

## Decision Log

- Decision: Restore archival in the existing rule and delete the invented closure prerequisite.
  Rationale: The user explicitly rejected the substitution. There is no evidence that closure was necessary to fulfill the request.
- Decision: Preserve finished-target and required-follow-up safeguards.
  Rationale: Archival can affect descendants. A returned turn does not prove that a complete assignment finished.
- Decision: Keep completed CPK-061 records unchanged and supersede their closure decision here.
  Rationale: Historical evidence must not hide the incorrect substitution. This correction replaces only CPK-061-B, B5, and S7 closure requirements. Component-update behavior and all other boundaries remain unchanged.
- Decision: Use the strict-simplification challenger exemption in [Design Preflight](../../assets/skills/design-preflight/SKILL.md).
  Rationale: The correction deletes an invented prerequisite and uses existing native archival. It adds no interface, persistent state, dependency, fallback, or supported behavior.
- Decision: Keep the existing publication branch `cpk-064-publish-managed-updates` from corrective base `635cebb34e37859567c886aac638384f51a33f0f` in the primary checkout.
  Rationale: This is one corrective write stream within the authorized draft publication. No Plan Mode record applies to this correction.

## Product Boundary and Supported Model

Apply [Scope boundaries](../../assets/skills/design-preflight/references/scope-boundaries.md) and [Supported model](../../assets/skills/design-preflight/references/supported-model.md). The user clarification is the authoritative product source.

The canonical coordination rule and its direct tests compose this result. Existing delegation rules and the two-phase challenger requirement remain opaque and unchanged. Native archival implementation, thread identifiers, and platform capacity also remain opaque.

Normal use has one personal user, one writer, captured terminal results, and an exposed native archive tool. The rule must preserve unfinished assignments and descendants. Do not add closure, capacity-release claims, fallback tools, thread-limit handling, bulk archival, direct session deletion, or Codex state-file edits. No owner is promoted from deferred behavior.

## Boundary Inventory and Checks

Apply [Scenario discrimination](../../assets/skills/design-preflight/references/scenario-discrimination.md). The clauses below exhaust the clarification and the composing cleanup rule. These are instruction boundaries, not executable production-code entry points. Native archival semantics remain opaque. Trace closure does not apply.

| Boundary | Source and discriminator | Contrast and required oracle | Instruction path and check |
| --- | --- | --- | --- |
| B1 | User clarification and terminal-result clause: capture, then archive | Archive a captured finished assignment, not a close-only substitute. The rule orders capture before native archival and contains no close operation or capacity prerequisite. | Canonical coordination owner. `test_coordination_cleans_terminal_agent_threads` |
| B2 | Existing archive-target clause: exact finished subtree | Explicit finished identifier, not a coordinator default. The rule waits for every descendant to finish with no required follow-up and forbids direct session or state edits. | Canonical coordination owner. `test_coordination_archive_targets_preserve_active_work` and B1 check |
| B3 | Existing assignment-completion clause: whole assignment | A Phase 1 return with Phase 2 owed, not full completion. The same agent remains available for required follow-ups. The challenger requirement remains unchanged. | Coordination and Design Preflight owners. `test_coordination_cleanup_preserves_required_followups` |

All three boundaries are mapped. The rest of coordination is unchanged and opaque. The clarification's explanation of why the user accepted the discrepancy is non-boundary context. Agent-capacity changes are outside scope.

## Plan of Work

CPK-065-A is one atomic instruction correction. Edit the canonical cleanup paragraph and remove its closure guard. Order result capture before native archival with an explicit finished identifier. Preserve descendant protection and the existing required-follow-up rule. Update the first direct test to reject the substituted close operation and capacity claim. Keep the other two tests unchanged.

The allowed edits are the canonical owner, its direct test, this specification, the roadmap, and matching manifest entries. The full review and local commit boundary is this complete corrective task from its recorded base. Existing completed runtime work retains its prior review evidence.

## Concrete Steps and Acceptance

Run from `/home/mbeutler/Projects/codex-practical-kit`:

    PYTHONPATH=tests python3 -m unittest test_kit.IntegrationTests.test_coordination_cleans_terminal_agent_threads test_kit.IntegrationTests.test_coordination_archive_targets_preserve_active_work test_kit.IntegrationTests.test_coordination_cleanup_preserves_required_followups -v
    ./run-tests.sh
    sha256sum --check MANIFEST.sha256
    git diff --check

The first direct test must reject the old closure rule. All three checks must pass with the corrected rule. The complete suite must pass, apart from its existing platform-specific skip. Update only changed manifest records and add this specification. Finalize documentation before the native review. Keep detailed results in ignored `.agent/test-results/CPK-065.md`.

## Idempotence and Recovery

Source edits are ordinary Git changes. Preserve unrelated untracked files and completed history. Do not archive live threads as a test. Stop and report a failed operation rather than inventing recovery.

## Interfaces and Dependencies

No runtime interface or dependency changes. The existing native archival tool remains responsible for thread history.

Plan note: This correction restores the original archive request and explicitly supersedes only the mistaken closure requirement.

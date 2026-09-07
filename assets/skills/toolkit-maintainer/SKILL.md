---
name: toolkit-maintainer
description: >
  Maintain Codex Practical Kit rules, routers, skills, and rule-owner tests.
  Use when adding, moving, deleting, or revising toolkit instructions or when
  changing AGENTS routing and canonical rule ownership.
license: MIT
---

<!-- cpk-rule-owner: rule-ownership -->
<!-- cpk-rule-guard: Audit applicable live instructions for conflicts and duplicate requirements when changing guidance. -->
<!-- cpk-rule-guard: A live toolkit rule has exactly one authoritative file. -->
<!-- cpk-rule-guard: A router names an applicable skill or links to a rule owner. It does not summarize the rule. -->
<!-- cpk-rule-guard: A `cpk-rule-route-only` section contains only its marker and one Markdown link. -->

# Rule ownership

A live toolkit rule has exactly one authoritative file.

A router names an applicable skill or links to a rule owner. It does not summarize the rule. Documentation also links to the owner instead of copying instructions.

Each owner declares one unique `cpk-rule-owner` comment. Add `cpk-rule-guard` comments for distinctive requirements that must not occur in another live file.

A `cpk-rule-route-only` section contains only its marker and one Markdown link. Put the marker directly below a level-two heading.

Current AGENTS content, Session Start content, PLANS, skills, references, README, and current manuals are live surfaces. Tests scan these surfaces.

Completed ExecPlans, roadmap history, diagnostics, test records, and source tests are records. They are not live rule owners.

An active ExecPlan records task facts and decisions. It links a general toolkit rule instead of copying that rule.

When a rule changes, edit its owner. Update links only when the owner path changes.

Audit applicable live instructions for conflicts and duplicate requirements when changing guidance. Include the routes and linked skills that can affect the requested result. Preserve deliberate repository overrides and upstream skill ownership. Correct toolkit-owned conflicts in the existing owner instead of adding another instruction layer.

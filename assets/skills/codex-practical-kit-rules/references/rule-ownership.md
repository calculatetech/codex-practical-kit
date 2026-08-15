<!-- cpk-rule-owner: rule-ownership -->
<!-- cpk-rule-guard: A live toolkit rule has exactly one authoritative file. -->
<!-- cpk-rule-guard: A router links to a rule owner and does not summarize its rule. -->
<!-- cpk-rule-guard: A `cpk-rule-route-only` section contains only its marker and one Markdown link. -->

# Rule ownership

A live toolkit rule has exactly one authoritative file.

A router links to a rule owner and does not summarize its rule. Documentation also links to the owner instead of copying instructions.

Each owner declares one unique `cpk-rule-owner` comment. Add `cpk-rule-guard` comments for distinctive requirements that must not occur in another live file.

A `cpk-rule-route-only` section contains only its marker and one Markdown link. Put the marker directly below a level-two heading.

Current AGENTS content, Session Start content, PLANS, skills, references, README, and current manuals are live surfaces. Tests scan these surfaces.

Completed ExecPlans, roadmap history, diagnostics, test records, and source tests are records. They are not live rule owners.

An active ExecPlan records task facts and decisions. It links a general toolkit rule instead of copying that rule.

When a rule changes, edit its owner. Update links only when the owner path changes.

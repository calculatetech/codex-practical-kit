<!-- cpk-rule-owner: implementation-modes -->
<!-- cpk-rule-guard: Keep normal mode active through accepted test scope. -->
<!-- cpk-rule-guard: Return to normal mode before each read-only review pass. -->

# Implementation modes

Keep normal mode active through accepted test scope.

Use normal mode for requirements, planning, research, Scenario Proof, test-scope definition, and read-only review. Fix each required behavior, oracle, and planned runnable check before implementation.

Use Ponytail full while writing test code, production code, or an accepted review correction. Return to normal mode before each read-only review pass.

An explicit user mode selection overrides these defaults. Treat a natural-language request to work without, disable, or exclude Ponytail as normal mode for the named scope.

Do not modify Ponytail to enforce this policy. Select its documented mode at the phase boundary.

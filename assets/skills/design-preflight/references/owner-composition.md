<!-- cpk-rule-owner: owner-composition -->
<!-- cpk-rule-guard: Each nonterminal retained-work state names its entry owner, retained state, supported reopening sources, and terminal owner. -->
<!-- cpk-rule-guard: Each applicable shared-owner event states whether it preserves, advances, or clears the active gate. -->
<!-- cpk-rule-guard: Component checks do not satisfy a composed scenario. -->
<!-- cpk-rule-guard: A scenario set is open while a supported event can still act on retained state. -->
<!-- cpk-rule-guard: For an unordered stream, include the smallest counterexample ordering that can change the terminal result. -->
<!-- cpk-rule-guard: When one signal has multiple causes, exercise each cause under predicates that select different outcomes. -->

# Owner composition

Apply this rule to non-trivial runtime behavior. Combine only states and events that share an owner or mutable state.

Each nonterminal retained-work state names its entry owner, retained state, supported reopening sources, and terminal owner.

Add one composed runnable check that reaches each supported reopening without an unrelated event. Include deadline-driven reopening when the required result depends on a deadline.

A scenario set is open while a supported event can still act on retained state. Continue the event sequence until the terminal owner produces the required oracle. Include a later command, wake, retry, or completion when it can change retained work.

For an unordered stream, include the smallest counterexample ordering that can change the terminal result. Do not test every event permutation.

Each applicable shared-owner event states whether it preserves, advances, or clears the active gate.

When one signal has multiple causes, exercise each cause under predicates that select different outcomes. Do not infer the cause from incidental state that can coexist with another cause.

Add one composed runnable check for each distinct gate outcome. A new wake cannot clear an existing retry gate unless the requirement permits it.

For every production entry point to one authoritative result, identify the shared owner and required side effects.

Apply [Full-set results](full-set-results.md) to the affected records. Add one runnable production-path check for each entry point.

An explicit tombstone, absence response, and change-feed absence must reach the same authoritative absence owner when they promise the same result.

Component checks do not satisfy a composed scenario.

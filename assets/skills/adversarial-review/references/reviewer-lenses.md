# Reviewer lenses

## Correctness

Always check the supported normal path:

- The requested result occurs.
- Inputs and outputs keep their documented meaning.
- Setup and cleanup agree.
- A branch does not report success before the result exists.
- Tests exercise the real owner.

## Optional lenses

Add one of these lenses to the same reviewer only when the active task names it:

- Security for an explicit trust boundary.
- API contract for an external interface.
- Migration for a declared data change.
- Performance for a measured resource problem.

Do not review excluded conditions. Do not attack assumptions that define the supported operating model.

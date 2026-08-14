# Stop-hook task-boundary hotfix

Version 0.2.0 kept one Git baseline for the full Codex session.

The Stop continuation ran the review, but the hook exited immediately when `stop_hook_active` was true. It did not accept the reviewed Git state.

A later `/plan` turn still saw the old code diff. The hook then replaced the planning flow with the previous task review prompt.

## Fix in version 0.2.1

The hook now:

- Records review and documentation evidence before it handles `stop_hook_active`.
- Binds evidence to the exact changed code state.
- Advances the accepted Git checkpoint after clean evidence.
- Advances the checkpoint after documentation-only turns.
- Does not start a Stop continuation in `/plan` mode.
- Migrates an existing version 0.2.0 session-state file when it next records evidence.

## Recover from an affected session

1. Stop the misplaced review cycle.
2. Keep any valid working-tree changes.
3. Exit the affected Codex session.
4. Install version 0.2.1.
5. Start a new Codex session.
6. Open `/hooks` if Codex asks you to review the changed hook.

Do not resume the old session. Its current continuation was already created by the version 0.2.0 hook.

## Upgrade

```bash
./run-tests.sh
./install.sh
./doctor.sh
```

The doctor output must show:

```text
[OK] kit version: 0.2.1
```

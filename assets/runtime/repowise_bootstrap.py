#!/usr/bin/env python3
"""Prepare RepoWise and keep its watcher beside the MCP server."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

INIT_ARGS = [
    "init",
    "--yes",
    "--no-codex",
    "--no-agents",
    "--no-editor-setup",
    "--no-distill-hook",
    "--no-claude-md",
    "--no-workspace",
    "--no-prose",
]
WATCH_PATCH = (
    "from repowise.cli.commands import watch_cmd as w;"
    "original=w._event_paths;"
    "w._event_paths=lambda event,root:set() if getattr(event,'event_type','') in "
    "{'opened','closed','closed_no_write'} else original(event,root);"
    "w.watch_command.main(args=__import__('sys').argv[1:],standalone_mode=False)"
)


def git_root(cwd: Path) -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    return Path(result.stdout.strip()).resolve() if result.returncode == 0 else None


def run_setup(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, env=repowise_env(), stdout=sys.stderr, check=True)


def repowise_env() -> dict[str, str]:
    env = os.environ.copy()
    env["REPOWISE_SKIP_EDITOR_SETUP"] = "1"
    return env


def has_head(root: Path) -> bool:
    return (
        subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def watch_command(repowise: str, platform: str | None = None) -> list[str]:
    if (platform or sys.platform) == "win32":
        return [repowise, "watch"]

    launcher = Path(repowise).resolve()
    try:
        first_line = launcher.read_bytes().splitlines()[0].decode("utf-8").strip()
    except (IndexError, OSError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"Cannot read the RepoWise launcher at {launcher}: {exc}") from exc
    if not first_line.startswith("#!"):
        raise RuntimeError(f"RepoWise launcher has no Python shebang: {launcher}")
    words = shlex.split(first_line[2:])
    if not words:
        raise RuntimeError(f"RepoWise launcher has an empty shebang: {launcher}")
    command = words[1:] if Path(words[0]).name == "env" else words
    if command[:1] in (["-S"], ["--split-string"]):
        command = command[1:]
    elif command and command[0].startswith("-S"):
        command = [*shlex.split(command[0][2:]), *command[1:]]
    elif command and command[0].startswith("--split-string="):
        command = [*shlex.split(command[0].split("=", 1)[1]), *command[1:]]
    interpreter, *interpreter_args = command
    if not Path(interpreter).name.startswith("python"):
        tool_python = launcher.parent / "python"
        if not tool_python.is_file():
            return [repowise, "watch"]
        interpreter = str(tool_python)
        interpreter_args = []
    return [interpreter, *interpreter_args, "-c", WATCH_PATCH]


def stop_watcher(
    watcher: subprocess.Popen[bytes], platform: str | None = None
) -> None:
    if (platform or sys.platform) == "win32":
        taskkill = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "taskkill.exe"
        subprocess.run(
            [str(taskkill), "/PID", str(watcher.pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    else:
        try:
            watcher.terminate()
        except OSError:
            pass
    watcher.wait()


def bootstrap(repowise: str, cwd: Path) -> int:
    root = git_root(cwd)
    if root is None:
        if any(cwd.iterdir()):
            return subprocess.run(
                [repowise, "mcp"], cwd=cwd, env=repowise_env(), check=False
            ).returncode
        run_setup(["git", "init", "--quiet"], cwd)
        root = git_root(cwd)
        if root is None:
            raise RuntimeError("Git did not create a repository")

    initialized = not (root / ".repowise").is_dir()
    if initialized:
        run_setup([repowise, *INIT_ARGS, str(root)], root)
    run_setup([repowise, "hook", "install", str(root), "--no-workspace"], root)
    if has_head(root) and not initialized:
        run_setup(
            [
                repowise,
                "update",
                "--index-only",
                "--no-agents",
                "--no-workspace",
                str(root),
            ],
            root,
        )

    command = [
        *watch_command(repowise),
        "--index-only",
        "--no-workspace",
        str(root),
    ]
    with (root / ".repowise" / ".update.log").open("a", encoding="utf-8") as log:
        watcher = subprocess.Popen(
            command,
            cwd=root,
            env=repowise_env(),
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        time.sleep(1)
        status = watcher.poll()
        if status is not None:
            watcher.wait()
            return status or 1
        try:
            return subprocess.run(
                [repowise, "mcp", str(root)],
                cwd=root,
                env=repowise_env(),
                check=False,
            ).returncode
        finally:
            if watcher.poll() is None:
                stop_watcher(watcher)
            else:
                watcher.wait()


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: repowise_bootstrap.py <repowise-command>", file=sys.stderr)
        return 2
    try:
        return bootstrap(args[0], Path.cwd())
    except subprocess.CalledProcessError as exc:
        return exc.returncode
    except (OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

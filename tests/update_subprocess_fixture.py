"""External-system fixture loaded by launcher subprocess tests."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.parse
import urllib.request
import urllib.error


FIXTURE = Path(os.environ["CPK_UPDATE_FIXTURE"])
STATE = FIXTURE / "plugins.json"
CALLS = FIXTURE / "calls.jsonl"
REAL_RUN = subprocess.run
SKILLS = {
    "neuroarxiv": {
        "repository": "UditAkhourii/neuroarxiv",
        "commit": "1" * 40,
        "files": {
            "skills/neuroarxiv/SKILL.md": b"# neuroarxiv selected\n",
            "LICENSE": b"MIT neuroarxiv\n",
        },
    },
    "simple-english": {
        "repository": "AminBlg/SimpleEnglish",
        "commit": "2" * 40,
        "files": {
            "skills/simple-english/SKILL.md": b"# simple English selected\n",
            "LICENSE": b"MIT simple English\n",
        },
    },
}


class Response:
    def __init__(self, value):
        self.body = value if isinstance(value, bytes) else json.dumps(value).encode()

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


def blob(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def urlopen(request, timeout=60):
    if timeout != 60:
        raise AssertionError(timeout)
    url = request.full_url
    record(["http", url], None)
    if load_state().get("fail_http"):
        raise urllib.error.URLError("fixture offline")
    if url == "https://pypi.org/pypi/repowise/json":
        return Response({"info": {"version": "9.9.9"}})
    releases = {
        "/repos/astral-sh/uv/releases/latest": "v8.8.8",
        "/repos/DietrichGebert/ponytail/releases/latest": "v4.12.0",
        "/repos/just-every/12ui-plugin/releases/latest": "design-v0.2.107",
    }
    for suffix, tag in releases.items():
        if url.endswith(suffix):
            return Response({"tag_name": tag})
    if url.startswith("https://astral.sh/uv/"):
        return Response(b"fixture installer\n")
    for item in SKILLS.values():
        repository = item["repository"]
        if f"/repos/{repository}/commits?per_page=1" in url:
            return Response([{"sha": item["commit"]}])
        if f"/repos/{repository}/git/trees/" in url:
            return Response(
                {
                    "truncated": False,
                    "tree": [
                        {"type": "blob", "path": path, "sha": blob(data)}
                        for path, data in item["files"].items()
                    ],
                }
            )
        prefix = f"https://raw.githubusercontent.com/{repository}/"
        if url.startswith(prefix):
            path = urllib.parse.urlsplit(url).path.lstrip("/").split("/", 3)[3]
            return Response(item["files"][path])
    raise AssertionError(f"Unexpected HTTP request: {url}")


def load_state():
    return json.loads(STATE.read_text())


def save_state(state):
    STATE.write_text(json.dumps(state, sort_keys=True))


def record(command, home):
    with CALLS.open("a") as stream:
        stream.write(json.dumps({"command": command, "home": home}) + "\n")


def plugin(name, enabled=True):
    marketplace = "ponytail" if name == "ponytail" else "12ui-plugin"
    plugin_name = "ponytail" if name == "ponytail" else "12ui-design"
    repository = (
        "https://github.com/DietrichGebert/ponytail.git"
        if name == "ponytail" else "https://github.com/just-every/12ui-plugin.git"
    )
    package_source = (
        {"source": "git", "url": repository}
        if name == "ponytail"
        else {"source": "local", "path": "."}
    )
    return {
        "name": plugin_name,
        "pluginId": f"{plugin_name}@{marketplace}",
        "installed": True,
        "version": "fixture",
        "enabled": enabled,
        "source": package_source,
        "marketplaceSource": {"sourceType": "git", "source": repository},
    }


def run(command, *args, **kwargs):
    command = [str(value) for value in command]
    executable = Path(command[0]).name
    if executable == "git":
        return REAL_RUN(command, *args, **kwargs)
    home = (kwargs.get("env") or os.environ).get("CODEX_HOME")
    record(command, home)
    if executable == "node":
        return subprocess.CompletedProcess(command, 0, "v22.0.0\n", "")
    if executable in {"sh", "pwsh"} and kwargs.get("input") is not None:
        target = Path(kwargs["env"]["UV_INSTALL_DIR"])
        target.mkdir(parents=True, exist_ok=True)
        suffix = ".exe" if executable == "pwsh" else ""
        (target / f"uv{suffix}").write_text("fixture")
        return subprocess.CompletedProcess(command, 0, "", "")
    if executable in {"uv", "uv.exe"}:
        if command[1:] == ["--version"]:
            return subprocess.CompletedProcess(command, 0, "uv 8.8.8\n", "")
        if command[1:3] == ["tool", "install"]:
            target = Path(kwargs["env"]["UV_TOOL_BIN_DIR"])
            target.mkdir(parents=True, exist_ok=True)
            suffix = ".exe" if executable.endswith(".exe") else ""
            (target / f"repowise{suffix}").write_text("fixture")
        return subprocess.CompletedProcess(command, 0, "", "")
    if executable in {"repowise", "repowise.exe"}:
        return subprocess.CompletedProcess(command, 0, "RepoWise 9.9.9\n", "")
    if executable != "codex":
        raise AssertionError(f"Unexpected process: {command}")
    if command[1:] == ["--version"]:
        return subprocess.CompletedProcess(command, 0, "codex-cli fixture\n", "")
    if command[1:] == ["login", "status"]:
        return subprocess.CompletedProcess(command, 0, "Logged in\n", "")
    state = load_state()
    values = command[2:-1]
    if values == ["marketplace", "list"]:
        output = {"marketplaces": state["marketplaces"]}
    elif values[:2] == ["list", "--marketplace"]:
        output = {
            "installed": [
                item for item in state["installed"]
                if item["pluginId"].endswith("@" + values[2])
            ]
        }
    elif values[:2] == ["marketplace", "add"]:
        name = "ponytail" if "ponytail" in values[2].lower() else "12ui-plugin"
        repository = (
            "https://github.com/DietrichGebert/ponytail.git"
            if name == "ponytail" else "https://github.com/just-every/12ui-plugin.git"
        )
        state["marketplaces"].append(
            {"name": name, "marketplaceSource": {"sourceType": "git", "source": repository}}
        )
        output = {"added": True}
    elif values[:1] == ["add"]:
        state["installed"].append(plugin("ponytail" if values[1].startswith("ponytail@") else "12ui"))
        output = {"installed": True}
    elif values[:2] == ["marketplace", "upgrade"]:
        if state.get("fail") == values[2]:
            return subprocess.CompletedProcess(command, 1, "", "fixture upgrade failed")
        for item in state["installed"]:
            if item["pluginId"].endswith("@" + values[2]):
                item["version"] = "refreshed"
                cache = Path(home) / "plugins" / "cache" / values[2] / "revision"
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_text("refreshed")
        output = {"upgraded": values[2]}
    else:
        raise AssertionError(f"Unexpected Codex command: {command}")
    save_state(state)
    return subprocess.CompletedProcess(command, 0, json.dumps(output), "")


urllib.request.urlopen = urlopen
subprocess.run = run

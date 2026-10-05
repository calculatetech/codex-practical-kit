"""Focused checks for explicit managed-update application."""

import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.parse
from unittest import mock

import kit


ROOT = Path(__file__).resolve().parents[1]


class ApplyUpdateTests(unittest.TestCase):
    def paths(self, root: Path) -> kit.InstallPaths:
        return kit.InstallPaths(root / "home", root / "codex", root / "skills", root / "kit")

    def runtime_lock(self, *, repowise="9.9.9", uv="8.8.8"):
        lock = copy.deepcopy(kit.load_lock())
        lock["runtime_tools"]["repowise"]["version"] = repowise
        lock["runtime_tools"]["uv"]["version"] = uv
        lock["runtime_tools"]["uv"]["installers"] = {
            "posix": {"url": f"https://astral.sh/uv/{uv}/install.sh", "sha256": "a" * 64},
            "windows": {"url": f"https://astral.sh/uv/{uv}/install.ps1", "sha256": "b" * 64},
        }
        return lock

    def test_apply_repowise_selected_version(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            uv = paths.home / "bin/uv"
            repowise = paths.home / ".local/bin/repowise"
            uv.parent.mkdir(parents=True)
            uv.write_text("uv")
            repowise.parent.mkdir(parents=True)
            repowise.write_text("old")
            kit.write_file(
                kit.manifest_path(paths),
                json.dumps({"repowise": str(repowise)}),
            )
            calls = []

            def run(command, **_kwargs):
                calls.append(command)
                if command == [str(repowise), "--version"]:
                    return subprocess.CompletedProcess(command, 0, "RepoWise 1.0.0\n", "")
                if command[:3] == [str(uv), "tool", "install"]:
                    repowise.write_text("new")
                return subprocess.CompletedProcess(command, 0, "", "")

            with mock.patch.object(kit, "load_lock", return_value=self.runtime_lock()), mock.patch.object(
                kit, "find_runtime_command", return_value=str(repowise)
            ), mock.patch.object(kit, "run", side_effect=run):
                result = kit.ensure_repowise(paths, str(uv), force_install=True)

            self.assertEqual(result, str(repowise))
            self.assertIn([str(uv), "tool", "install", "--force", "repowise==9.9.9"], calls)

    def test_apply_reuses_current_external_repowise(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            repowise = Path(temp) / "external/repowise"
            repowise.parent.mkdir()
            repowise.write_text("repowise")
            calls = []

            def run(command, **_kwargs):
                calls.append(command)
                return subprocess.CompletedProcess(command, 0, "RepoWise 9.9.9\n", "")

            with mock.patch.object(kit, "load_lock", return_value=self.runtime_lock()), mock.patch.object(
                kit, "find_runtime_command", return_value=str(repowise)
            ), mock.patch.object(kit, "run", side_effect=run):
                result = kit.ensure_repowise(paths, "uv", force_install=True)

            self.assertEqual(result, str(repowise))
            self.assertEqual(calls, [[str(repowise), "--version"]])

    def _assert_uv_platform(self, windows: bool):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            body = b"windows installer" if windows else b"posix installer"
            calls = []

            def run(command, **kwargs):
                calls.append((command, kwargs["input_text"]))
                target = Path(kwargs["env"]["UV_INSTALL_DIR"])
                target.mkdir(parents=True)
                (target / ("uv.exe" if windows else "uv")).write_text("uv")
                return subprocess.CompletedProcess(command, 0, "", "")

            with mock.patch.object(kit, "load_lock", return_value=self.runtime_lock()), mock.patch.object(
                kit, "is_windows", return_value=windows
            ), mock.patch.object(kit, "find_runtime_command", return_value="old-uv"), mock.patch.object(
                kit, "run", side_effect=run
            ):
                result = kit.ensure_uv(paths, force=True, installer_bytes=body)

            self.assertEqual(Path(result).name, "uv.exe" if windows else "uv")
            self.assertEqual(calls[0][1], body.decode())
            self.assertEqual(calls[0][0][0], "pwsh" if windows else "sh")

    def test_apply_uv_posix(self):
        self._assert_uv_platform(False)

    def test_apply_uv_windows(self):
        self._assert_uv_platform(True)

    def test_apply_complete_skill_revision(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paths = self.paths(root)
            destination = paths.skills_home / "demo"
            kit.write_file(destination / "obsolete.md", "old")
            lock = self.runtime_lock()
            lock["skills"] = {
                "demo": {
                    "repository": "https://github.com/example/demo",
                    "commit": "1" * 40,
                    "license": "MIT",
                    "root": "skills/demo",
                    "license_path": "LICENSE",
                    "files": [
                        {"path": "skills/demo/SKILL.md", "destination": "demo/SKILL.md", "git_blob_sha1": "0" * 40},
                        {"path": "skills/demo/obsolete.md", "destination": "demo/obsolete.md", "git_blob_sha1": "9" * 40},
                    ],
                }
            }
            commit_url = kit.github_api_url("https://github.com/example/demo", "commits?per_page=1")
            tree_url = kit.github_api_url("https://github.com/example/demo", f"git/trees/{'2' * 40}?recursive=1")

            def fetch(url):
                if url.endswith("/repowise/json"):
                    return {"info": {"version": "9.9.9"}}
                if url == commit_url:
                    return [{"sha": "2" * 40}]
                if url == tree_url:
                    return {
                        "truncated": False,
                        "tree": [
                            {"type": "blob", "path": "skills/demo/SKILL.md", "sha": "a" * 40},
                            {"type": "blob", "path": "skills/demo/new.md", "sha": "b" * 40},
                            {"type": "blob", "path": "LICENSE", "sha": "c" * 40},
                            {"type": "blob", "path": "unrelated.txt", "sha": "d" * 40},
                        ],
                    }
                self.fail(url)

            with mock.patch.object(kit, "load_lock", return_value=lock), mock.patch.object(
                kit, "release_identity", side_effect=lambda repository: "v8.8.8" if repository.endswith("/uv") else "release"
            ), mock.patch.object(kit, "fetch_json", side_effect=fetch), mock.patch.object(
                kit, "download_url", return_value=b"installer"
            ), mock.patch.object(
                kit, "download_file", side_effect=lambda url, _blob: url.rsplit("/", 1)[-1].encode()
            ):
                candidate, _lines, payloads = kit.managed_candidates(include_payloads=True)

            self.assertEqual(
                [item["destination"] for item in candidate["skills"]["demo"]["files"]],
                ["demo/LICENSE", "demo/SKILL.md", "demo/new.md"],
            )
            self.assertNotIn("skill:demo/obsolete.md", payloads)
            stage_lock = {
                "skills": {
                    "demo": {
                        "repository": "https://github.com/example/demo",
                        "commit": "2" * 40,
                        "license": "MIT",
                        "files": [
                            {"path": "skills/demo/SKILL.md", "destination": "demo/SKILL.md", "git_blob_sha1": "1" * 40},
                            {"path": "skills/demo/new.md", "destination": "demo/new.md", "git_blob_sha1": "2" * 40},
                        ],
                    }
                }
            }
            payloads = {"skill:demo/SKILL.md": b"new skill", "skill:demo/new.md": b"new file"}
            stage = root / "stage"
            stage.mkdir()
            with mock.patch.object(kit, "ALL_SKILLS", ("demo",)):
                records = kit.stage_upstream_skills(stage, stage_lock, payloads)
                installed = kit.install_skills(paths, stage, {"demo"})

            self.assertEqual(records["demo"]["commit"], "2" * 40)
            self.assertEqual(installed, [{"name": "demo"}])
            self.assertEqual(
                {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()},
                {"SKILL.md", "new.md"},
            )
            self.assertFalse((destination / "obsolete.md").exists())

    def _run_install_plugins(self, states, *, refresh):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        paths = self.paths(Path(temp.name))
        calls = []

        def stage(destination):
            for name in kit.UPSTREAM_SKILLS:
                kit.write_file(destination / name / "SKILL.md", name)
            return {}

        with mock.patch.object(kit, "stage_upstream_skills", side_effect=stage), mock.patch.object(
            kit, "ensure_repowise_runtime", return_value=("uv", "repowise")
        ), mock.patch.object(kit, "codex_plugin", side_effect=lambda _paths, *args: calls.append(args) or {}):
            kit.install_core(
                mock.Mock(),
                paths,
                refresh_plugins=refresh,
                plugin_states=states,
            )
        return paths, calls

    def test_apply_native_plugins_preserves_user_state(self):
        disabled = {"installed": True, "enabled": False, "user": "keep"}
        states = {"ponytail": (True, disabled)}
        paths, calls = self._run_install_plugins(states, refresh=True)
        self.assertEqual(
            calls,
            [("marketplace", "upgrade", "ponytail")],
        )
        self.assertFalse(disabled["enabled"])
        self.assertEqual(disabled["user"], "keep")
        self.assertTrue((paths.codex_home / "AGENTS.md").is_file())

    def test_install_ponytail_absent_or_existing(self):
        absent = {"ponytail": (False, None)}
        _paths, calls = self._run_install_plugins(absent, refresh=False)
        self.assertEqual(
            calls,
            [("marketplace", "add", "DietrichGebert/ponytail"), ("add", "ponytail@ponytail")],
        )
        existing = {"ponytail": (True, {"installed": True, "enabled": False})}
        _paths, calls = self._run_install_plugins(existing, refresh=False)
        self.assertEqual(calls, [])
        existing_marketplace = {"ponytail": (True, None)}
        _paths, calls = self._run_install_plugins(existing_marketplace, refresh=True)
        self.assertEqual(
            calls,
            [
                ("marketplace", "upgrade", "ponytail"),
                ("add", "ponytail@ponytail"),
            ],
        )

    def test_12ui_policy_is_website_only(self):
        text = (ROOT / "assets/AGENTS.block.md").read_text()
        self.assertEqual(text.count("cpk-rule-guard: Use 12ui-design only for website projects."), 1)
        self.assertIn("Use 12ui-design only for website projects", text)
        self.assertIn("Do not use it for native apps or other UI work", text)
        self.assertNotIn("all non-trivial UI", text.lower())

    def test_update_set_cardinality_and_late_record(self):
        lock = kit.load_lock()
        responses = {
            "repowise": lock["runtime_tools"]["repowise"]["version"],
            "uv": "v" + lock["runtime_tools"]["uv"]["version"],
            "ponytail": "v4.12.0",
        }

        def release(repository):
            for name in ("ponytail", "uv"):
                if repository == lock["runtime_tools"][name]["repository"]:
                    return responses[name]
            self.fail(repository)

        def fetch(url):
            if url.endswith("/repowise/json"):
                return {"info": {"version": responses["repowise"]}}
            for component in lock["skills"].values():
                if url == kit.github_api_url(component["repository"], "commits?per_page=1"):
                    return [{"sha": component["commit"]}]
            self.fail(url)

        with mock.patch.object(kit, "release_identity", side_effect=release), mock.patch.object(
            kit, "fetch_json", side_effect=fetch
        ):
            _candidate, lines, _payloads = kit.managed_candidates()
        self.assertEqual(len(lines), len(lock["runtime_tools"]) + len(lock["skills"]))
        self.assertTrue(all("same identity" in line or "Codex-owned plugin" in line for line in lines))
        responses["repowise"] = "99.0.0"
        with mock.patch.object(kit, "release_identity", side_effect=release), mock.patch.object(
            kit, "fetch_json", side_effect=fetch
        ):
            _candidate, changed, _payloads = kit.managed_candidates()
        self.assertEqual(sum("upstream differs" in line for line in changed), 1)

    def test_update_actions_stop_once_on_error(self):
        with mock.patch.object(kit, "managed_candidates", side_effect=kit.KitError("offline")), mock.patch.object(
            kit, "write_file"
        ) as write, mock.patch.object(kit, "install_core") as install:
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                status = kit.main(["apply-updates"])
        self.assertEqual(status, 2)
        self.assertEqual(stderr.getvalue().count("ERROR:"), 1)
        write.assert_not_called()
        install.assert_not_called()

    def test_update_source_safety_uses_kit_root(self):
        with tempfile.TemporaryDirectory(prefix="toolkit source ") as source_temp, tempfile.TemporaryDirectory(
            prefix="caller repo "
        ) as caller_temp:
            source = Path(source_temp)
            caller = Path(caller_temp)
            (source / "upstream.lock.json").write_text("{}\n")
            for root in (source, caller):
                subprocess.run(["git", "init", "-q", str(root)], check=True)
                subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
                subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            subprocess.run(["git", "-C", str(source), "add", "upstream.lock.json"], check=True)
            subprocess.run(["git", "-C", str(source), "commit", "-qm", "base"], check=True)
            previous = Path.cwd()
            paths = self.paths(source)
            try:
                os.chdir(caller)
                with mock.patch.object(kit, "ROOT", source):
                    kit.require_clean_update_source(paths)
                    (source / "upstream.lock.json").write_text('{"changed": true}\n')
                    with self.assertRaisesRegex(kit.KitError, "modified or untracked"):
                        kit.require_clean_update_source(paths)
                    kit.write_file(
                        paths.install_root / "upstream.lock.json",
                        (source / "upstream.lock.json").read_bytes(),
                    )
                    kit.require_clean_update_source(paths)
            finally:
                os.chdir(previous)

    def test_apply_reconciles_stale_installed_skill(self):
        self.test_apply_complete_skill_revision()

    @unittest.skipIf(os.name == "nt", "POSIX launchers require a POSIX host")
    def test_bash_update_launchers_complete_path(self):
        with tempfile.TemporaryDirectory(prefix="update launchers ") as temp:
            for script in ("check-updates.sh", "apply-updates.sh"):
                success = subprocess.run([str(ROOT / script), "--help"], cwd=temp, text=True, capture_output=True)
                failure = subprocess.run([str(ROOT / script), "--not-an-option"], cwd=temp, text=True, capture_output=True)
                self.assertEqual(success.returncode, 0, success.stderr)
                self.assertEqual(failure.returncode, 2)

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell 7 is not installed")
    def test_powershell_update_launchers_complete_path(self):
        with tempfile.TemporaryDirectory(prefix="update launchers ") as temp:
            shim = Path(temp) / "python"
            shim.symlink_to(sys.executable)
            env = {**os.environ, "PATH": temp + os.pathsep + os.environ["PATH"]}
            for script in ("check-updates.ps1", "apply-updates.ps1"):
                success = subprocess.run(["pwsh", "-NoProfile", "-File", str(ROOT / script), "--help"], cwd=temp, env=env, text=True, capture_output=True)
                failure = subprocess.run(["pwsh", "-NoProfile", "-File", str(ROOT / script), "--not-an-option"], cwd=temp, env=env, text=True, capture_output=True)
                self.assertEqual(success.returncode, 0, success.stderr)
                self.assertEqual(failure.returncode, 2)


class ComposedUpdateTests(unittest.TestCase):
    """Exercise the real update entry point with only external systems faked."""

    class Response:
        def __init__(self, value):
            self.body = value if isinstance(value, bytes) else json.dumps(value).encode()

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return self.body

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="composed updates ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "toolkit source"
        shutil.copytree(
            ROOT,
            self.source,
            ignore=shutil.ignore_patterns(".git", ".repowise", ".mcp.json", ".vscode", "__pycache__"),
        )
        subprocess.run(["git", "init", "-q", str(self.source)], check=True)
        subprocess.run(["git", "-C", str(self.source), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(self.source), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(self.source), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.source), "commit", "-qm", "candidate"], check=True)
        self.paths = kit.InstallPaths(
            self.root / "home",
            self.root / "selected codex",
            self.root / "installed skills",
            self.root / "installed kit",
        )
        self.default_home = self.root / "default codex"
        kit.write_file(self.default_home / "sentinel", "unchanged")
        self.default_before = (self.default_home / "sentinel").read_bytes()
        self.process_calls = []
        self.http_calls = []
        self.plugin_state = {
            "marketplaces": [
                {"name": "unrelated", "root": "keep"},
                {
                    "name": "ponytail",
                    "marketplaceSource": {
                        "sourceType": "git",
                        "source": "https://github.com/DietrichGebert/ponytail.git",
                    },
                },
            ],
            "installed": [self.plugin("ponytail", enabled=False, user="keep")],
        }
        self.fail_upgrade = None
        self.repowise_version = "9.9.9"
        self.skill_payloads = {
            "neuroarxiv": {
                "skills/neuroarxiv/SKILL.md": b"# neuroarxiv selected\n",
                "skills/neuroarxiv/references/paper.md": b"selected paper\n",
                "LICENSE": b"MIT neuroarxiv\n",
            },
            "simple-english": {
                "skills/simple-english/SKILL.md": b"# simple English selected\n",
                "skills/simple-english/references/new.md": b"selected reference\n",
                "LICENSE": b"MIT simple English\n",
            },
        }
        self.skill_commits = {"neuroarxiv": "1" * 40, "simple-english": "2" * 40}
        self.real_subprocess_run = subprocess.run
        git = shutil.which("git")
        self.assertIsNotNone(git)
        self.patches = [
            mock.patch.object(kit, "ROOT", self.source),
            mock.patch.object(kit.urllib.request, "urlopen", side_effect=self.urlopen),
            mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(self.default_home), "PATH": str(Path(git).parent)},
            ),
        ]
        for patch in self.patches:
            patch.start()
            self.addCleanup(patch.stop)

    @staticmethod
    def plugin(name, *, enabled, user=None):
        marketplace = "ponytail" if name == "ponytail" else "12ui-plugin"
        plugin_name = "ponytail" if name == "ponytail" else "12ui-design"
        repository = (
            "https://github.com/DietrichGebert/ponytail.git"
            if name == "ponytail"
            else "https://github.com/just-every/12ui-plugin.git"
        )
        package_source = (
            {"source": "git", "url": repository}
            if name == "ponytail"
            else {"source": "local", "path": "."}
        )
        record = {
            "name": plugin_name,
            "pluginId": f"{plugin_name}@{marketplace}",
            "installed": True,
            "version": "old",
            "enabled": enabled,
            "source": package_source,
            "marketplaceSource": {"sourceType": "git", "source": repository},
        }
        if user is not None:
            record["user"] = user
        return record

    def urlopen(self, request, timeout=60):
        self.assertEqual(timeout, 60)
        url = request.full_url
        self.http_calls.append(url)
        if url == "https://pypi.org/pypi/repowise/json":
            return self.Response({"info": {"version": "9.9.9"}})
        if url.endswith("/repos/astral-sh/uv/releases/latest"):
            return self.Response({"tag_name": "v8.8.8"})
        if url.endswith("/repos/DietrichGebert/ponytail/releases/latest"):
            return self.Response({"tag_name": "v4.12.0"})
        if url.endswith("/repos/just-every/12ui-plugin/releases/latest"):
            return self.Response({"tag_name": "design-v0.2.107"})
        if url.startswith("https://astral.sh/uv/"):
            return self.Response(b"fixture installer\n")
        for name, repository in (
            ("neuroarxiv", "UditAkhourii/neuroarxiv"),
            ("simple-english", "AminBlg/SimpleEnglish"),
        ):
            if f"/repos/{repository}/commits?per_page=1" in url:
                return self.Response([{"sha": self.skill_commits[name]}])
            if f"/repos/{repository}/git/trees/" in url:
                tree = [
                    {"type": "blob", "path": path, "sha": kit.git_blob_sha1(data)}
                    for path, data in self.skill_payloads[name].items()
                ]
                return self.Response({"truncated": False, "tree": tree})
            raw_prefix = f"https://raw.githubusercontent.com/{repository}/"
            if url.startswith(raw_prefix):
                # Remove the owner, repository, and commit path segments.
                path = urllib.parse.urlsplit(url).path.lstrip("/").split("/", 3)[3]
                return self.Response(self.skill_payloads[name][path])
        self.fail(f"Unexpected HTTP request: {url}")

    def fake_run(self, command, **kwargs):
        command = [str(item) for item in command]
        self.process_calls.append((command, (kwargs.get("env") or {}).get("CODEX_HOME")))
        executable = Path(command[0]).name
        if executable == "git":
            return self.real_subprocess_run(command, **kwargs)
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
                self.repowise_version = command[-1].split("==", 1)[1]
            return subprocess.CompletedProcess(command, 0, "", "")
        if executable in {"repowise", "repowise.exe"}:
            return subprocess.CompletedProcess(command, 0, f"RepoWise {self.repowise_version}\n", "")
        if executable != "codex":
            self.fail(f"Unexpected process: {command}")
        if command[1:] == ["--version"]:
            return subprocess.CompletedProcess(command, 0, "codex-cli fixture\n", "")
        if command[1:] == ["login", "status"]:
            return subprocess.CompletedProcess(command, 0, "Logged in\n", "")
        args = command[2:-1]
        if args == ["marketplace", "list"]:
            output = {"marketplaces": self.plugin_state["marketplaces"]}
        elif args[:2] == ["list", "--marketplace"]:
            marketplace = args[2]
            output = {
                "installed": [
                    item for item in self.plugin_state["installed"]
                    if item["pluginId"].endswith("@" + marketplace)
                ]
            }
        elif args[:2] == ["marketplace", "add"]:
            source = args[2]
            name = "ponytail" if "ponytail" in source.lower() else "12ui-plugin"
            repository = (
                "https://github.com/DietrichGebert/ponytail.git"
                if name == "ponytail" else "https://github.com/just-every/12ui-plugin.git"
            )
            self.plugin_state["marketplaces"].append(
                {"name": name, "marketplaceSource": {"sourceType": "git", "source": repository}}
            )
            output = {"added": True}
        elif args[:1] == ["add"]:
            name = "ponytail" if args[1].startswith("ponytail@") else "12ui"
            self.plugin_state["installed"].append(self.plugin(name, enabled=True))
            output = {"installed": True}
        elif args[:2] == ["marketplace", "upgrade"]:
            marketplace = args[2]
            if self.fail_upgrade == marketplace:
                return subprocess.CompletedProcess(command, 1, "", "fixture upgrade failed")
            for item in self.plugin_state["installed"]:
                if item["pluginId"].endswith("@" + marketplace):
                    item["version"] = "refreshed"
                    cache = self.paths.codex_home / "plugins" / "cache" / marketplace / "revision"
                    kit.write_file(cache, "refreshed")
            output = {"upgraded": marketplace}
        else:
            self.fail(f"Unexpected Codex command: {command}")
        return subprocess.CompletedProcess(command, 0, json.dumps(output), "")

    def cli(self, command):
        args = [
            command,
            "--home", str(self.paths.home),
            "--codex-home", str(self.paths.codex_home),
            "--skills-home", str(self.paths.skills_home),
            "--install-root", str(self.paths.install_root),
        ]
        if command == "check-updates":
            args = [command]
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(subprocess, "run", side_effect=self.fake_run), contextlib.redirect_stdout(
            stdout
        ), contextlib.redirect_stderr(stderr):
            status = kit.main(args)
        return status, stdout.getvalue(), stderr.getvalue()

    def commit_source_lock(self):
        subprocess.run(["git", "-C", str(self.source), "add", "upstream.lock.json"], check=True)
        changed = subprocess.run(
            ["git", "-C", str(self.source), "diff", "--cached", "--quiet"]
        ).returncode
        if changed:
            subprocess.run(["git", "-C", str(self.source), "commit", "-qm", "selected lock"], check=True)

    def test_apply_main_reconciles_complete_installation_and_plugins(self):
        first_call = len(self.process_calls)
        status, stdout, stderr = self.cli("apply-updates")
        self.assertEqual((status, stderr), (0, ""))
        self.assertIn("Managed component updates applied.", stdout)
        selected = json.loads((self.source / "upstream.lock.json").read_text())
        self.assertEqual(selected["runtime_tools"]["repowise"]["version"], "9.9.9")
        self.assertEqual(selected["runtime_tools"]["uv"]["version"], "8.8.8")
        self.assertEqual(set(selected["runtime_tools"]), {"ponytail", "repowise", "uv"})
        self.assertEqual(set(selected["skills"]), set(self.skill_payloads))
        self.assertFalse(
            any(name in url for name in selected["optional_tools"] for url in self.http_calls)
        )
        self.assertEqual(self.http_calls.count("https://pypi.org/pypi/repowise/json"), 1)
        for name in ("ponytail", "uv"):
            self.assertEqual(
                self.http_calls.count(
                    kit.github_api_url(selected["runtime_tools"][name]["repository"], "releases/latest")
                ),
                1,
            )
        for name, component in selected["skills"].items():
            self.assertEqual(
                self.http_calls.count(
                    kit.github_api_url(component["repository"], "commits?per_page=1")
                ),
                1,
                name,
            )
        for name, files in self.skill_payloads.items():
            installed = {
                path.relative_to(self.paths.skills_home / name).as_posix(): path.read_bytes()
                for path in (self.paths.skills_home / name).rglob("*") if path.is_file()
            }
            expected = {
                ("LICENSE" if path == "LICENSE" else path.removeprefix(f"skills/{name}/")): data
                for path, data in files.items()
            }
            self.assertEqual(installed, expected)
        manifest = json.loads(kit.manifest_path(self.paths).read_text())
        self.assertEqual(
            {name: item["commit"] for name, item in manifest["upstream"].items()},
            self.skill_commits,
        )
        self.assertFalse(any(item["name"] == "12ui-design" for item in self.plugin_state["installed"]))
        ponytail = next(item for item in self.plugin_state["installed"] if item["name"] == "ponytail")
        self.assertFalse(ponytail["enabled"])
        self.assertEqual(ponytail["user"], "keep")
        router = (self.paths.codex_home / "AGENTS.md").read_text()
        self.assertIn("Use 12ui-design only for website projects", router)
        self.assertNotIn("all non-trivial UI", router.lower())
        self.assertEqual((self.default_home / "sentinel").read_bytes(), self.default_before)
        self.assertEqual(self.cli("doctor")[0], 0)
        first_processes = [call[0] for call in self.process_calls[first_call:]]
        self.assertEqual(
            [
                call[-1]
                for call in first_processes
                if Path(call[0]).name.startswith("uv") and call[1:3] == ["tool", "install"]
            ],
            ["repowise==9.9.9"],
        )
        self.assertEqual(
            [call[4] for call in first_processes if call[1:4] == ["plugin", "marketplace", "upgrade"]],
            ["ponytail"],
        )
        self.assertEqual(
            sum(call[1:3] == ["plugin", "add"] and call[3] == "12ui-design@12ui-plugin" for call in first_processes),
            0,
        )
        self.assertEqual(
            sum(call[1:4] == ["plugin", "marketplace", "add"] and call[4] == "just-every/12ui-plugin" for call in first_processes),
            0,
        )

        stale = self.paths.skills_home / "simple-english"
        (stale / "SKILL.md").write_text("stale")
        (stale / "obsolete.md").write_text("obsolete")
        status, stdout, stderr = self.cli("apply-updates")
        self.assertEqual((status, stderr), (0, ""))
        self.assertIn("Managed component updates applied.", stdout)
        self.assertEqual((stale / "SKILL.md").read_bytes(), self.skill_payloads["simple-english"]["skills/simple-english/SKILL.md"])
        self.assertFalse((stale / "obsolete.md").exists())
        router = (self.paths.codex_home / "AGENTS.md").read_text()
        self.assertIn("Use 12ui-design only for website projects", router)
        self.assertNotIn("all non-trivial UI", router.lower())
        upgrades = [
            call[0][4] for call in self.process_calls
            if call[0][1:4] == ["plugin", "marketplace", "upgrade"]
        ]
        self.assertEqual(upgrades, ["ponytail", "ponytail"])
        self.assertEqual(
            (self.paths.codex_home / "plugins/cache/ponytail/revision").read_text(),
            "refreshed",
        )
        self.assertFalse((self.paths.codex_home / "plugins/cache/12ui-plugin").exists())
        self.assertTrue(
            all(
                home == str(self.paths.codex_home)
                for command, home in self.process_calls
                if command[:2] == ["codex", "plugin"]
            )
        )
        self.assertEqual(self.plugin_state["marketplaces"][0], {"name": "unrelated", "root": "keep"})
        self.assertEqual(self.cli("doctor")[0], 0)

    def test_apply_matches_complete_repowise_version(self):
        self.assertEqual(self.cli("apply-updates")[0], 0)
        for action in ("install", "apply-updates"):
            for version in ("9.9.9", "19.9.9", "9.9.9.post1"):
                with self.subTest(action=action, reported_version=version):
                    self.repowise_version = version
                    self.assertEqual(self.cli("doctor")[0], 0 if version == "9.9.9" else 1)
                    before = len(self.process_calls)
                    status, stdout, stderr = self.cli(action)
                    self.assertEqual((status, stderr), (0, ""))
                    self.assertIn("Core kit installed." if action == "install" else "Managed component updates applied.", stdout)
                    installs = [
                        command for command, _home in self.process_calls[before:]
                        if command[1:3] == ["tool", "install"]
                    ]
                    self.assertEqual(len(installs), 0 if version == "9.9.9" else 1)
                    if installs:
                        self.assertEqual(installs[0][-1], "repowise==9.9.9")
                    self.assertEqual(self.repowise_version, "9.9.9")
                    selected = json.loads((self.source / "upstream.lock.json").read_text())
                    self.assertEqual(selected["runtime_tools"]["repowise"]["version"], "9.9.9")
                    self.assertEqual(
                        (self.source / "upstream.lock.json").read_bytes(),
                        (self.paths.install_root / "upstream.lock.json").read_bytes(),
                    )
                    self.assertEqual(self.cli("doctor")[0], 0)

    def test_12ui_is_unmanaged_across_install_apply_and_doctor(self):
        candidate, _lines, _payloads = kit.managed_candidates(include_payloads=True)
        kit.write_file(
            self.source / "upstream.lock.json",
            json.dumps(candidate, indent=2, sort_keys=True) + "\n",
        )
        self.commit_source_lock()
        # Retained Codex listing shape, independent of the toolkit's request generator.
        curated = {
            "pluginId": "12ui-design@openai-curated-remote",
            "name": "12ui-design",
            "marketplaceName": "openai-curated-remote",
            "version": "0.2.65",
            "installed": True,
            "enabled": False,
            "source": {"source": "remote", "id": "plugins_6a8915941e8c8191ae58d10e41cc322f"},
            "user": "keep",
        }
        cache = self.paths.codex_home / "plugins/cache/openai-curated-remote/12ui-design/0.2.65/skills/12ui-design/SKILL.md"
        for existing in (False, True):
            with self.subTest(existing_12ui=existing):
                if existing:
                    self.plugin_state["installed"].append(copy.deepcopy(curated))
                    kit.write_file(cache, "# separately installed 12UI\n")
                    kit.write_file(
                        self.paths.codex_home / "config.toml",
                        kit.read_text(self.paths.codex_home / "config.toml")
                        + '\n[plugins."12ui-design@openai-curated-remote"]\nenabled = false\n',
                    )
                before = len(self.process_calls)
                http_before = len(self.http_calls)
                for command in ("check-updates", "install", "apply-updates", "install", "doctor"):
                    status, stdout, stderr = self.cli(command)
                    self.assertEqual((status, stderr), (0, ""), command)
                    if command == "check-updates":
                        self.assertNotIn("12ui", stdout.lower())
                    elif command == "install":
                        self.assertIn("Ponytail: native Codex plugin", stdout)
                        self.assertNotIn("12UI", stdout)
                    elif command == "doctor":
                        self.assertIn("Result: ready", stdout)
                        self.assertNotIn("12UI", stdout)
                plugins = [
                    item for item in self.plugin_state["installed"]
                    if item["name"] == "12ui-design"
                ]
                self.assertEqual(plugins, [curated] if existing else [])
                if existing:
                    self.assertEqual(cache.read_bytes(), b"# separately installed 12UI\n")
                    self.assertIn(
                        '[plugins."12ui-design@openai-curated-remote"]\nenabled = false',
                        (self.paths.codex_home / "config.toml").read_text(),
                    )
                router = (self.paths.codex_home / "AGENTS.md").read_text()
                self.assertIn("Use 12ui-design only for website projects", router)
                self.assertIn("Do not use it for native apps or other UI work", router)
                self.assertFalse(
                    any("12ui" in argument.lower() for command, _home in self.process_calls[before:] for argument in command)
                )
                self.assertFalse(any("12ui" in url.lower() for url in self.http_calls[http_before:]))
                self.assertFalse((self.paths.codex_home / "plugins/cache/12ui-plugin").exists())
                self.assertEqual((self.default_home / "sentinel").read_bytes(), self.default_before)

    def test_apply_main_stops_after_first_operation_error(self):
        self.assertEqual(self.cli("apply-updates")[0], 0)
        self.fail_upgrade = "ponytail"
        before = len(self.process_calls)
        status, stdout, stderr = self.cli("apply-updates")
        calls = self.process_calls[before:]
        self.assertEqual(status, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr.count("ERROR:"), 1)
        self.assertIn("fixture upgrade failed", stderr)
        self.assertNotIn("Managed component updates applied.", stderr)
        self.assertEqual(
            [call[0][4] for call in calls if call[0][1:4] == ["plugin", "marketplace", "upgrade"]],
            ["ponytail"],
        )
        self.assertEqual(
            sum(
                call[0][1:5] == ["plugin", "marketplace", "upgrade", "ponytail"]
                for call in calls
            ),
            1,
        )
        self.assertEqual(
            calls[-1][0][1:5],
            ["plugin", "marketplace", "upgrade", "ponytail"],
        )
        self.assertFalse(any(Path(call[0][0]).name.startswith("uv") for call in calls))

    def test_failed_first_apply_leaves_source_retryable(self):
        before = (self.source / "upstream.lock.json").read_bytes()
        self.fail_upgrade = "ponytail"
        self.assertEqual(self.cli("apply-updates")[0], 2)
        self.assertEqual((self.source / "upstream.lock.json").read_bytes(), before)
        self.fail_upgrade = None
        self.assertEqual(self.cli("apply-updates")[0], 0)

    def test_apply_main_windows_runtime_branch(self):
        with mock.patch.object(kit, "is_windows", return_value=True):
            status, _stdout, stderr = self.cli("apply-updates")
            self.assertEqual((status, stderr), (0, ""))
            self.assertTrue((self.paths.home / ".local/bin/uv.exe").is_file())
            self.assertTrue((self.paths.home / ".local/bin/repowise.exe").is_file())
            self.assertTrue(any(Path(call[0][0]).name == "pwsh" for call in self.process_calls))
            manifest = json.loads(kit.manifest_path(self.paths).read_text())
            self.assertEqual(set(manifest["upstream"]), set(self.skill_payloads))
            for name, files in self.skill_payloads.items():
                self.assertEqual(
                    {
                        path.relative_to(self.paths.skills_home / name).as_posix()
                        for path in (self.paths.skills_home / name).rglob("*") if path.is_file()
                    },
                    {
                        "LICENSE" if path == "LICENSE" else path.removeprefix(f"skills/{name}/")
                        for path in files
                    },
                )
            self.assertEqual(self.cli("doctor")[0], 0)

    @unittest.skipIf(os.name == "nt", "combined launcher parity requires a POSIX host")
    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell 7 is not installed")
    def test_update_launchers_run_complete_actions_and_propagate_failures(self):
        fixture = self.root / "launcher fixture"
        fixture.mkdir()
        state = {
            "marketplaces": [
                {"name": "unrelated", "root": "keep"},
                {
                    "name": "ponytail",
                    "marketplaceSource": {
                        "sourceType": "git",
                        "source": "https://github.com/DietrichGebert/ponytail.git",
                    },
                }
            ],
            "installed": [self.plugin("ponytail", enabled=False)],
        }
        state["installed"][0]["user"] = "keep-ponytail"
        (fixture / "plugins.json").write_text(json.dumps(state))
        site = self.root / "fixture site"
        site.mkdir()
        (site / "sitecustomize.py").write_text(
            "from tests import update_subprocess_fixture\n"
        )
        binaries = self.root / "fixture bin"
        binaries.mkdir()
        for name in ("python", "python3"):
            (binaries / name).symlink_to(sys.executable)
        for name in ("node", "codex"):
            path = binaries / name
            path.write_text("#!/bin/sh\nexit 99\n")
            path.chmod(0o755)
        real_path = os.environ["PATH"]
        env = {
            **os.environ,
            "CPK_UPDATE_FIXTURE": str(fixture),
            "PYTHONPATH": os.pathsep.join((str(site), str(ROOT))),
            "PATH": os.pathsep.join((str(binaries), real_path)),
            "CODEX_HOME": str(self.default_home),
        }
        def options(paths):
            return [
                "--home", str(paths.home),
                "--codex-home", str(paths.codex_home),
                "--skills-home", str(paths.skills_home),
                "--install-root", str(paths.install_root),
            ]

        def invoke(script, *extra):
            command = [str(self.source / script), *extra]
            if script.endswith(".ps1"):
                command = ["pwsh", "-NoProfile", "-File", *command]
            return subprocess.run(
                command,
                cwd=self.root,
                env=env,
                text=True,
                capture_output=True,
            )

        def calls():
            path = fixture / "calls.jsonl"
            return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

        def clear_calls():
            (fixture / "calls.jsonl").unlink(missing_ok=True)

        def snapshot(paths):
            roots = (self.source, paths.home, paths.codex_home, paths.skills_home, paths.install_root, self.default_home)
            result = {}
            for root in roots:
                if not root.exists():
                    continue
                for path in root.rglob("*"):
                    if path.is_file() and ".git" not in path.parts:
                        result[str(path)] = path.read_bytes()
            result["plugin-state"] = (fixture / "plugins.json").read_bytes()
            return result

        def expected_check_output():
            lock = json.loads((self.source / "upstream.lock.json").read_text())
            lines = ["Managed component updates:"]
            lines.extend(
                (
                    "- ponytail: Codex-owned plugin; upstream release v4.12.0; use the Codex plugin manager",
                    (
                        f"- repowise: toolkit pin {lock['runtime_tools']['repowise']['version']}; "
                        f"upstream release 9.9.9; "
                        + ("same identity" if lock["runtime_tools"]["repowise"]["version"] == "9.9.9" else "upstream differs")
                    ),
                    (
                        f"- uv: toolkit pin {lock['runtime_tools']['uv']['version']}; upstream release v8.8.8; "
                        + ("same identity" if lock["runtime_tools"]["uv"]["version"] == "8.8.8" else "upstream differs")
                    ),
                    (
                        f"- neuroarxiv: toolkit revision {lock['skills']['neuroarxiv']['commit']}; "
                        f"upstream revision {'1' * 40}; "
                        + ("same identity" if lock["skills"]["neuroarxiv"]["commit"] == "1" * 40 else "upstream differs")
                    ),
                    (
                        f"- simple-english: toolkit revision {lock['skills']['simple-english']['commit']}; "
                        f"upstream revision {'2' * 40}; "
                        + ("same identity" if lock["skills"]["simple-english"]["commit"] == "2" * 40 else "upstream differs")
                    ),
                )
            )
            return "\n".join(lines) + "\n"

        def assert_ready(paths):
            lock = json.loads((self.source / "upstream.lock.json").read_text())
            self.assertEqual(lock["runtime_tools"]["repowise"]["version"], "9.9.9")
            self.assertEqual(lock["runtime_tools"]["uv"]["version"], "8.8.8")
            self.assertEqual(set(lock["runtime_tools"]), {"ponytail", "repowise", "uv"})
            self.assertEqual(set(lock["skills"]), {"neuroarxiv", "simple-english"})
            expected_files = {
                "neuroarxiv": {
                    "LICENSE": b"MIT neuroarxiv\n",
                    "SKILL.md": b"# neuroarxiv selected\n",
                },
                "simple-english": {
                    "LICENSE": b"MIT simple English\n",
                    "SKILL.md": b"# simple English selected\n",
                },
            }
            for name, expected in expected_files.items():
                actual = {
                    path.relative_to(paths.skills_home / name).as_posix(): path.read_bytes()
                    for path in (paths.skills_home / name).rglob("*") if path.is_file()
                }
                self.assertEqual(actual, expected)
            manifest = json.loads(kit.manifest_path(paths).read_text())
            self.assertEqual(
                manifest["upstream"],
                {
                    name: {
                        "repository": lock["skills"][name]["repository"],
                        "commit": lock["skills"][name]["commit"],
                        "license": lock["skills"][name]["license"],
                    }
                    for name in expected_files
                },
            )
            self.assertEqual(
                (paths.install_root / "upstream.lock.json").read_bytes(),
                (self.source / "upstream.lock.json").read_bytes(),
            )
            router = (paths.codex_home / "AGENTS.md").read_text()
            self.assertIn("Use 12ui-design only for website projects", router)
            self.assertNotIn("all non-trivial UI", router.lower())
            self.assertTrue((paths.home / ".local/bin/uv").is_file())
            self.assertTrue((paths.home / ".local/bin/repowise").is_file())
            doctor = invoke("doctor.sh", *options(paths))
            self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
            self.assertIn("Result: ready", doctor.stdout)

        before = snapshot(self.paths)
        clear_calls()
        bash_check = invoke("check-updates.sh")
        self.assertEqual(bash_check.returncode, 0, bash_check.stderr)
        self.assertEqual(bash_check.stdout, expected_check_output())
        self.assertEqual(snapshot(self.paths), before)
        self.assertFalse(
            any("12ui" in item["command"][1].lower() for item in calls() if item["command"][0] == "http")
        )

        clear_calls()
        bash_apply = invoke("apply-updates.sh", *options(self.paths))
        self.assertEqual(bash_apply.returncode, 0, bash_apply.stderr)
        self.assertEqual(bash_apply.stdout, "Managed component updates applied.\n")
        assert_ready(self.paths)
        bash_calls = calls()
        bash_urls = [item["command"][1] for item in bash_calls if item["command"][0] == "http"]
        self.assertFalse(any("12ui" in url.lower() for url in bash_urls))
        lock = json.loads((self.source / "upstream.lock.json").read_text())
        self.assertFalse(any(name in url for name in lock["optional_tools"] for url in bash_urls))
        for name, component in lock["skills"].items():
            commit_url = kit.github_api_url(component["repository"], "commits?per_page=1")
            self.assertEqual(bash_urls.count(commit_url), 1, name)
            tree_url = kit.github_api_url(
                component["repository"],
                f"git/trees/{lock['skills'][name]['commit']}?recursive=1",
            )
            self.assertEqual(bash_urls.count(tree_url), 1, name)
        self.assertEqual(bash_urls.count("https://pypi.org/pypi/repowise/json"), 1)
        for name in ("ponytail", "uv"):
            self.assertEqual(
                bash_urls.count(
                    kit.github_api_url(lock["runtime_tools"][name]["repository"], "releases/latest")
                ),
                1,
                name,
            )
        self.assertEqual(sum(url.startswith("https://astral.sh/uv/8.8.8/") for url in bash_urls), 2)
        mutations = [
            item["command"][2:-1] for item in bash_calls
            if item["command"][:2] == ["codex", "plugin"]
            and item["command"][2] in {"add", "marketplace"}
        ]
        self.assertEqual(
            [item for item in mutations if item[:2] == ["marketplace", "upgrade"]],
            [["marketplace", "upgrade", "ponytail"]],
        )
        self.assertEqual(
            [item for item in mutations if item[:2] == ["marketplace", "add"]],
            [],
        )
        self.assertEqual(
            [item for item in mutations if item[:1] == ["add"]],
            [],
        )
        self.assertEqual(
            sum(
                item["command"][1:4] == ["tool", "install", "--force"]
                for item in bash_calls if Path(item["command"][0]).name == "uv"
            ),
            1,
        )

        main_state = json.loads((fixture / "plugins.json").read_text())
        main_ponytail = next(item for item in main_state["installed"] if item["name"] == "ponytail")
        self.assertFalse(main_ponytail["enabled"])
        self.assertEqual(main_ponytail["user"], "keep-ponytail")
        self.assertEqual(main_state["marketplaces"][0], {"name": "unrelated", "root": "keep"})
        self.assertEqual(
            (self.paths.codex_home / "plugins/cache/ponytail/revision").read_text(),
            "refreshed",
        )
        self.assertTrue(
            all(
                item["home"] == str(self.paths.codex_home)
                for item in bash_calls if item["command"][:2] == ["codex", "plugin"]
            )
        )
        self.assertEqual((self.default_home / "sentinel").read_bytes(), self.default_before)
        bash_paths = kit.InstallPaths(
            self.root / "bash install home",
            self.root / "bash install codex",
            self.root / "bash install skills",
            self.root / "bash install kit",
        )
        (fixture / "plugins.json").write_text(json.dumps({"marketplaces": [], "installed": []}))
        clear_calls()
        bash_install = invoke("install.sh", *options(bash_paths))
        self.assertEqual(bash_install.returncode, 0, bash_install.stderr)
        assert_ready(bash_paths)
        state = json.loads((fixture / "plugins.json").read_text())
        self.assertFalse(any(item["name"] == "12ui-design" for item in state["installed"]))
        state["installed"].append(self.plugin("12ui", enabled=False, user="keep-bash"))
        (fixture / "plugins.json").write_text(json.dumps(state))
        clear_calls()
        self.assertEqual(invoke("install.sh", *options(bash_paths)).returncode, 0)
        state = json.loads((fixture / "plugins.json").read_text())
        self.assertEqual(sum(item["name"] == "12ui-design" for item in state["installed"]), 1)
        self.assertFalse(next(item for item in state["installed"] if item["name"] == "12ui-design")["enabled"])
        self.assertEqual(next(item for item in state["installed"] if item["name"] == "12ui-design")["user"], "keep-bash")
        self.assertFalse(
            any(
                item["command"][2] == "add" or item["command"][2:4] == ["marketplace", "upgrade"]
                for item in calls() if item["command"][:2] == ["codex", "plugin"]
            )
        )
        self.assertEqual(invoke("doctor.sh", *options(bash_paths)).returncode, 0)

        powershell_paths = kit.InstallPaths(
            self.root / "powershell install home",
            self.root / "powershell install codex",
            self.root / "powershell install skills",
            self.root / "powershell install kit",
        )
        (fixture / "plugins.json").write_text(json.dumps({"marketplaces": [], "installed": []}))
        clear_calls()
        powershell_install = invoke("install.ps1", *options(powershell_paths))
        self.assertEqual(powershell_install.returncode, 0, powershell_install.stderr)
        assert_ready(powershell_paths)
        state = json.loads((fixture / "plugins.json").read_text())
        self.assertFalse(any(item["name"] == "12ui-design" for item in state["installed"]))
        state["installed"].append(self.plugin("12ui", enabled=False, user="keep-powershell"))
        (fixture / "plugins.json").write_text(json.dumps(state))
        clear_calls()
        self.assertEqual(invoke("install.ps1", *options(powershell_paths)).returncode, 0)
        state = json.loads((fixture / "plugins.json").read_text())
        self.assertEqual(sum(item["name"] == "12ui-design" for item in state["installed"]), 1)
        self.assertFalse(next(item for item in state["installed"] if item["name"] == "12ui-design")["enabled"])
        self.assertEqual(next(item for item in state["installed"] if item["name"] == "12ui-design")["user"], "keep-powershell")
        self.assertFalse(
            any(
                item["command"][2] == "add" or item["command"][2:4] == ["marketplace", "upgrade"]
                for item in calls() if item["command"][:2] == ["codex", "plugin"]
            )
        )
        self.assertEqual(invoke("doctor.ps1", *options(powershell_paths)).returncode, 0)

        (fixture / "plugins.json").write_text(json.dumps(main_state))
        self.commit_source_lock()
        before = snapshot(self.paths)
        clear_calls()
        powershell_check = invoke("check-updates.ps1")
        self.assertEqual(powershell_check.returncode, 0, powershell_check.stderr)
        self.assertEqual(powershell_check.stdout, expected_check_output())
        self.assertEqual(snapshot(self.paths), before)
        self.assertFalse(
            any("12ui" in item["command"][1].lower() for item in calls() if item["command"][0] == "http")
        )

        stale = self.paths.skills_home / "simple-english"
        (stale / "SKILL.md").write_text("stale")
        (stale / "obsolete.md").write_text("obsolete")
        state = json.loads((fixture / "plugins.json").read_text())
        state["installed"].append(self.plugin("12ui", enabled=False, user="keep-apply"))
        (fixture / "plugins.json").write_text(json.dumps(state))
        clear_calls()
        powershell_apply = invoke("apply-updates.ps1", *options(self.paths))
        self.assertEqual(powershell_apply.returncode, 0, powershell_apply.stderr)
        self.assertEqual(powershell_apply.stdout, "Managed component updates applied.\n")
        assert_ready(self.paths)
        self.assertEqual((stale / "SKILL.md").read_text(), "# simple English selected\n")
        self.assertFalse((stale / "obsolete.md").exists())
        state = json.loads((fixture / "plugins.json").read_text())
        installed_12ui = next(item for item in state["installed"] if item["name"] == "12ui-design")
        self.assertFalse(installed_12ui["enabled"])
        self.assertEqual(installed_12ui["user"], "keep-apply")
        self.assertEqual(
            next(item for item in state["installed"] if item["name"] == "ponytail")["user"],
            "keep-ponytail",
        )
        self.assertEqual(state["marketplaces"][0], {"name": "unrelated", "root": "keep"})
        power_calls = calls()
        power_urls = [
            item["command"][1] for item in power_calls if item["command"][0] == "http"
        ]
        self.assertEqual(power_urls.count("https://pypi.org/pypi/repowise/json"), 1)
        for name in ("ponytail", "uv"):
            self.assertEqual(
                power_urls.count(
                    kit.github_api_url(lock["runtime_tools"][name]["repository"], "releases/latest")
                ),
                1,
                name,
            )
        for name, component in lock["skills"].items():
            self.assertEqual(
                power_urls.count(
                    kit.github_api_url(component["repository"], "commits?per_page=1")
                ),
                1,
                name,
            )
            self.assertEqual(
                power_urls.count(
                    kit.github_api_url(
                        component["repository"],
                        f"git/trees/{component['commit']}?recursive=1",
                    )
                ),
                1,
                name,
            )
        self.assertEqual(sum(url.startswith("https://astral.sh/uv/8.8.8/") for url in power_urls), 2)
        upgrades = [
            item["command"][4] for item in power_calls
            if item["command"][1:4] == ["plugin", "marketplace", "upgrade"]
        ]
        self.assertEqual(upgrades, ["ponytail"])
        self.assertEqual(
            sum(
                item["command"][1:] == ["--version"]
                for item in power_calls if Path(item["command"][0]).name.startswith("repowise")
            ),
            2,
        )
        self.assertFalse(
            any(
                item["command"][1:3] == ["tool", "install"]
                for item in power_calls if Path(item["command"][0]).name == "uv"
            )
        )
        self.assertTrue(
            all(
                item["home"] == str(self.paths.codex_home)
                for item in power_calls if item["command"][:2] == ["codex", "plugin"]
            )
        )
        self.assertEqual((self.default_home / "sentinel").read_bytes(), self.default_before)
        self.assertEqual((self.paths.codex_home / "plugins/cache/ponytail/revision").read_text(), "refreshed")
        self.assertFalse((self.paths.codex_home / "plugins/cache/12ui-plugin").exists())
        self.assertFalse(any("12ui" in url.lower() for url in power_urls))

        self.commit_source_lock()
        state = json.loads((fixture / "plugins.json").read_text())
        state["fail_http"] = True
        (fixture / "plugins.json").write_text(json.dumps(state))
        for script in ("check-updates.sh", "check-updates.ps1"):
            clear_calls()
            failed = invoke(script)
            self.assertEqual(failed.returncode, 2)
            self.assertEqual(failed.stdout, "")
            self.assertEqual(failed.stderr.count("ERROR:"), 1)
            self.assertIn("fixture offline", failed.stderr)
            self.assertEqual(len(calls()), 1)
            self.assertEqual(calls()[0]["command"][0], "http")
        state["fail_http"] = False
        state["fail"] = "ponytail"
        (fixture / "plugins.json").write_text(json.dumps(state))
        for script in ("apply-updates.sh", "apply-updates.ps1"):
            clear_calls()
            failed = invoke(script, *options(self.paths))
            self.assertEqual(failed.returncode, 2)
            self.assertNotIn("Managed component updates applied.", failed.stdout + failed.stderr)
            self.assertEqual(failed.stderr.count("ERROR:"), 1)
            self.assertIn("fixture upgrade failed", failed.stderr)
            failed_calls = calls()
            failed_upgrade = [
                item for item in failed_calls
                if item["command"][1:5] == ["plugin", "marketplace", "upgrade", "ponytail"]
            ]
            self.assertEqual(len(failed_upgrade), 1)
            self.assertEqual(failed_calls[-1], failed_upgrade[0])


if __name__ == "__main__":
    unittest.main()

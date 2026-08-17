import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]

import kit


class GitFixture:
    def __init__(self, root: Path):
        self.root = root
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)

    def commit(self, path: str, text: str):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        subprocess.run(["git", "add", path], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "test"], cwd=self.root, check=True)


class MarkerTests(unittest.TestCase):
    def test_managed_block_round_trip(self):
        original = "before\nafter\n"
        installed = kit.marker_block(original, "# start", "# end", "managed")
        self.assertEqual(kit.remove_marker_block(installed, "# start", "# end"), original)

    def test_managed_block_replacement_preserves_backslashes(self):
        updated = kit.marker_block(
            "# start\nold\n# end\n",
            "# start",
            "# end",
            kit.repowise_config_block(
                "/tmp/repowise", watcher=["/tmp/repowise", "watch"]
            ),
        )
        self.assertEqual(
            tomllib.loads(updated)["mcp_servers"]["repowise"]["args"][1],
            kit.repowise_bootstrap(
                "/tmp/repowise", watcher=["/tmp/repowise", "watch"]
            ),
        )


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.runtime = mock.patch.object(
            kit,
            "ensure_repowise_runtime",
            return_value=("/usr/bin/uv", "/usr/bin/repowise"),
        )
        self.watcher = mock.patch.object(
            kit,
            "repowise_watch_command",
            return_value=["/usr/bin/python3", "-c", kit.REPOWISE_WATCH_PATCH],
        )
        self.runtime.start()
        self.watcher.start()

    def tearDown(self):
        self.watcher.stop()
        self.runtime.stop()

    def paths(self, base: Path) -> kit.InstallPaths:
        return kit.InstallPaths(
            base / "home", base / "codex", base / "skills", base / "kit"
        )

    def source(self, base: Path) -> Path:
        source = base / "source"
        for name in kit.ALL_SKILLS:
            skill = source / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(name + "\n", encoding="utf-8")
        return source

    def test_global_agents_profile_is_compact_and_subagent_safe(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            agents = paths.codex_home / "AGENTS.md"
            agents.parent.mkdir(parents=True)
            agents.write_text("# User preference\n- Keep me.\n")

            kit.install_global_agents(paths)

            installed = agents.read_text()
            self.assertTrue(installed.startswith("# User preference\n- Keep me.\n"))
            self.assertLess(len(installed.splitlines()), 40)
            self.assertIn((paths.codex_home / "PLANS.md").as_posix(), installed)
            for skill in (
                "delivery-lifecycle",
                "repository-knowledge",
                "design-preflight",
                "adversarial-review",
                "publication",
                "toolkit-maintainer",
            ):
                self.assertIn(f"`{skill}`", installed)
            self.assertIn(
                "Every new repository lookup throughout a task: `repository-knowledge`.",
                installed,
            )
            self.assertNotIn("{{", installed)
            self.assertNotIn("Only the active coordinator can delegate", installed)
            self.assertNotIn("codex-practical-kit-rules", installed)

    def test_reinstall_accepts_existing_config_toml_hook(self):
        def fake_stage(destination: Path):
            for name in kit.UPSTREAM_SKILLS:
                skill = destination / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(name + "\n")
            return {}

        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            hook_root = paths.install_root / "hooks"
            hook_root.mkdir(parents=True)
            for name in ("stop_gate.py", "stop_docs.py", "session_end.py", "hook_common.py"):
                (hook_root / name).write_text("old\n")
            cache = hook_root / "__pycache__"
            cache.mkdir()
            (cache / "stop_gate.cpython-314.pyc").write_text("old\n")

            config_path = paths.codex_home / "config.toml"
            config_path.parent.mkdir(parents=True)
            existing_hook = kit.hooks_config_block(paths, ("SessionStart",)).replace(
                "hooks.SessionStart", 'hooks."SessionStart"'
            )
            original = (
                "\n\n[[hooks.PreToolUse]]\n"
                'matcher = "shell"\n\n'
                "[[hooks.PreToolUse.hooks]]\n"
                'type = "command"\n'
                'command = "python /tmp/user.py"\n\n'
                + existing_hook
                + "\n\n\n"
            )
            config_path.write_text(original, encoding="utf-8")

            with mock.patch.object(kit, "stage_upstream_skills", fake_stage):
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)

            config_text = config_path.read_text()
            hooks = tomllib.loads(config_text)["hooks"]
            self.assertEqual(set(hooks), {"PreToolUse", "SessionStart", "UserPromptSubmit"})
            self.assertEqual(
                hooks["PreToolUse"][0]["hooks"][0]["command"],
                "python /tmp/user.py",
            )
            self.assertEqual(len(hooks["SessionStart"]), 1)
            self.assertEqual(len(hooks["UserPromptSubmit"]), 1)
            self.assertIn(kit.HOOKS_START, config_text)
            self.assertIn(kit.HOOKS_END, config_text)
            self.assertFalse((paths.codex_home / "hooks.json").exists())
            self.assertEqual(
                {path.name for path in hook_root.iterdir()}, {"session_start.py"}
            )

            kit.uninstall_core(Namespace(purge=False), paths)
            remaining = tomllib.loads(config_path.read_text())["hooks"]
            self.assertEqual(set(remaining), {"PreToolUse", "SessionStart"})
            self.assertNotIn(kit.HOOKS_START, config_path.read_text())

    def test_plan_mode_prompt_selects_normal_mode(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            script = paths.install_root / "hooks" / "session_start.py"
            script.parent.mkdir(parents=True)
            script.write_bytes((ROOT / "assets" / "hooks" / "session_start.py").read_bytes())
            hooks = tomllib.loads(kit.hooks_config_block(paths))["hooks"]
            command = hooks["UserPromptSubmit"][0]["hooks"][0]["command"]

            def run(event):
                return subprocess.run(
                    command,
                    shell=True,
                    input=json.dumps(event),
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout

            self.assertEqual(
                run({"hook_event_name": "UserPromptSubmit", "permission_mode": "plan"}),
                "normal mode\n",
            )
            self.assertEqual(
                run({"hook_event_name": "UserPromptSubmit", "permission_mode": "default"}),
                "",
            )

    def test_reinstall_removes_duplicate_managed_hooks(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            config = paths.codex_home / "config.toml"
            kit.install_hooks(paths)
            config.write_text(config.read_text() + "\n\n" + kit.hooks_config_block(paths) + "\n")

            kit.install_hooks(paths)

            text = config.read_text()
            hooks = tomllib.loads(text)["hooks"]
            for event in kit.MANAGED_HOOK_EVENTS:
                self.assertEqual(len(hooks[event]), 1)
            self.assertNotIn(kit.HOOKS_START, text)

    def test_session_start_still_announces_router(self):
        contexts = {}
        for source in ("startup", "compact"):
            result = subprocess.run(
                ["python3", str(ROOT / "assets" / "hooks" / "session_start.py")],
                input=json.dumps(
                    {
                        "hook_event_name": "SessionStart",
                        "permission_mode": "default",
                        "source": source,
                    }
                ),
                text=True,
                capture_output=True,
                check=True,
            )
            output = json.loads(result.stdout)
            self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SessionStart")
            contexts[source] = output["hookSpecificOutput"]["additionalContext"]

        self.assertIn("Codex Practical Kit is active", contexts["startup"])
        self.assertNotIn("repository-knowledge", contexts["startup"])
        self.assertIn("repository-knowledge", contexts["compact"])
        self.assertIn("until the task ends", contexts["compact"])

    def test_copy_reinstall_and_uninstall(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            paths = self.paths(base)
            source = self.source(base)
            records = kit.install_skills(paths, source, set())
            self.assertEqual(records, [{"name": name} for name in kit.ALL_SKILLS])
            self.assertFalse((paths.skills_home / kit.ALL_SKILLS[0]).is_symlink())
            (paths.skills_home / kit.ALL_SKILLS[0] / "SKILL.md").write_text("changed\n")
            kit.install_skills(paths, source, set(kit.ALL_SKILLS))
            self.assertEqual(
                (paths.skills_home / kit.ALL_SKILLS[0] / "SKILL.md").read_text(),
                kit.ALL_SKILLS[0] + "\n",
            )
            paths.install_root.mkdir(parents=True)
            plans = paths.codex_home / "PLANS.md"
            plans.parent.mkdir(parents=True)
            plans.write_text("managed\n", encoding="utf-8")
            (paths.install_root / "install-manifest.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "codex_home": str(paths.codex_home),
                        "skills_home": str(paths.skills_home),
                        "plans_file": str(plans),
                        "skills": records,
                    }
                ),
                encoding="utf-8",
            )
            other = kit.InstallPaths(
                home=paths.home,
                codex_home=base / "other-codex",
                skills_home=base / "other-skills",
                install_root=paths.install_root,
            )
            for name in kit.ALL_SKILLS:
                skill = other.skills_home / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text("user\n", encoding="utf-8")
            self.assertTrue(kit.uninstall_core(Namespace(purge=False), other))
            self.assertTrue(all(not (paths.skills_home / name).exists() for name in kit.ALL_SKILLS))
            self.assertTrue(all((other.skills_home / name).exists() for name in kit.ALL_SKILLS))
            self.assertFalse(plans.exists())
            self.assertFalse((paths.install_root / "install-manifest.json").exists())
            self.assertFalse(kit.uninstall_core(Namespace(purge=False), other))

    def test_install_manages_global_plans_and_rejects_unowned_file(self):
        def fake_stage(destination: Path):
            for name in kit.UPSTREAM_SKILLS:
                skill = destination / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(name + "\n")
            return {name: {"commit": "test"} for name in kit.UPSTREAM_SKILLS}

        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp) / "custom paths")
            with mock.patch.object(kit, "stage_upstream_skills", fake_stage):
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)
            plans = paths.codex_home / "PLANS.md"
            plans_text = plans.read_text()
            self.assertEqual(plans_text, (ROOT / ".agent" / "PLANS.md").read_text())
            for target in re.findall(r"]\(([^)]+)\)", plans_text):
                if "://" not in target:
                    self.assertTrue(Path(target.strip("<>")).is_absolute(), target)
            agents = (paths.codex_home / "AGENTS.md").read_text()
            targets = re.findall(r"]\(<([^>]+)>\)", agents)
            self.assertTrue(targets)
            self.assertTrue(all(Path(target).is_file() for target in targets))
            manifest = json.loads((paths.install_root / "install-manifest.json").read_text())
            self.assertEqual(manifest["plans_file"], str(plans))
            plans.write_text("changed\n")
            with mock.patch.object(kit, "stage_upstream_skills", fake_stage):
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)
            self.assertEqual(plans.read_text(), (ROOT / ".agent" / "PLANS.md").read_text())
            self.assertTrue(kit.uninstall_core(Namespace(purge=False), paths))
            self.assertFalse(plans.exists())

        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            plans = paths.codex_home / "PLANS.md"
            plans.parent.mkdir(parents=True)
            plans.write_text("user\n")
            with mock.patch.object(
                kit, "stage_upstream_skills", fake_stage
            ), self.assertRaises(kit.KitError):
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)
            self.assertEqual(plans.read_text(), "user\n")
            self.assertFalse((paths.codex_home / "AGENTS.md").exists())

    def test_changed_skills_home_conflict_stops_before_skill_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            paths = self.paths(base)
            conflict = paths.skills_home / kit.ALL_SKILLS[0]
            conflict.mkdir(parents=True)
            (conflict / "SKILL.md").write_text("user\n")
            paths.install_root.mkdir(parents=True)
            (paths.install_root / "install-manifest.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "skills_home": str(base / "other-skills"),
                        "skills": [{"name": name} for name in kit.ALL_SKILLS],
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(
                kit, "stage_upstream_skills", return_value={}
            ), self.assertRaises(kit.KitError):
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)
            self.assertEqual((conflict / "SKILL.md").read_text(), "user\n")

    def test_v021_recorded_links_upgrade_to_copies(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            paths = self.paths(base)
            old = paths.install_root / "skills"
            old.mkdir(parents=True)
            paths.skills_home.mkdir()
            records = []
            for name in (*kit.ALL_SKILLS, *kit.OBSOLETE_SKILLS):
                target = old / name
                target.mkdir()
                (target / "SKILL.md").write_text("old\n")
                (paths.skills_home / name).symlink_to(target, target_is_directory=True)
                records.append(
                    {
                        "name": name,
                        "destination": str(paths.skills_home / name),
                        "source": str(target),
                        "method": "symlink",
                        "digest": "old",
                        "backup": None,
                    }
                )
            (paths.install_root / "install-manifest.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "kit_version": "0.2.1",
                        "skills_home": str(paths.skills_home),
                        "skills": records,
                    }
                )
            )

            def fake_stage(destination: Path):
                for name in kit.UPSTREAM_SKILLS:
                    skill = destination / name
                    skill.mkdir(parents=True)
                    (skill / "SKILL.md").write_text(name + "\n")
                return {name: {"commit": "test"} for name in kit.UPSTREAM_SKILLS}

            with mock.patch.object(kit, "stage_upstream_skills", fake_stage):
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)

            self.assertTrue(all((paths.skills_home / name).is_dir() for name in kit.ALL_SKILLS))
            self.assertTrue(all(not (paths.skills_home / name).is_symlink() for name in kit.ALL_SKILLS))
            self.assertTrue(all(not (paths.skills_home / name).exists() for name in kit.OBSOLETE_SKILLS))
            self.assertFalse((paths.install_root / "skills").exists())
            manifest = json.loads((paths.install_root / "install-manifest.json").read_text())
            self.assertEqual(manifest["skills"], [{"name": name} for name in kit.ALL_SKILLS])
            self.assertEqual(manifest["plans_file"], str(paths.codex_home / "PLANS.md"))

    def test_absent_uninstall_is_no_op(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            plans = paths.codex_home / "PLANS.md"
            plans.parent.mkdir(parents=True)
            plans.write_text("user\n")
            self.assertFalse(kit.uninstall_core(Namespace(purge=True), paths))
            self.assertEqual(plans.read_text(), "user\n")

    def test_install_preserves_global_config_and_uninstall_removes_owned_block(self):
        def fake_stage(destination: Path):
            for name in kit.UPSTREAM_SKILLS:
                skill = destination / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(name + "\n")
            return {}

        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            config = paths.codex_home / "config.toml"
            config.parent.mkdir(parents=True)
            config.write_text('[mcp_servers.other]\ncommand = "other"\n')
            with mock.patch.object(kit, "stage_upstream_skills", fake_stage):
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)
            installed = config.read_text()
            self.assertIn("mcp_servers.other", installed)
            self.assertIn(kit.HOOKS_START, installed)
            self.assertIn('default_tools_approval_mode = "approve"', installed)
            self.assertIn("required = true", installed)
            self.assertIn("startup_timeout_sec = 1800", installed)
            self.assertIn("hook install", installed)
            self.assertTrue(kit.uninstall_core(Namespace(purge=False), paths))
            self.assertEqual(config.read_text(), '[mcp_servers.other]\ncommand = "other"\n')

    def test_unowned_global_repowise_config_is_a_conflict(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            config = paths.codex_home / "config.toml"
            config.parent.mkdir(parents=True)
            config.write_text('[mcp_servers.repowise]\ncommand = "user"\n')
            with mock.patch.object(
                kit, "stage_upstream_skills", return_value={}
            ), self.assertRaises(kit.KitError):
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)
            self.assertEqual(config.read_text(), '[mcp_servers.repowise]\ncommand = "user"\n')


class RepoWiseRuntimeTests(unittest.TestCase):
    def paths(self, base: Path) -> kit.InstallPaths:
        return kit.InstallPaths(
            base / "home", base / "codex", base / "skills", base / "kit"
        )

    def test_watch_command_uses_repowise_python_and_filters_read_events(self):
        with tempfile.TemporaryDirectory() as temp:
            launcher = Path(temp) / "repowise"
            launcher.write_text(f"#!{sys.executable}\n")

            command = kit.repowise_watch_command(str(launcher))

        self.assertEqual(command[:2], [sys.executable, "-c"])
        for event in ("opened", "closed", "closed_no_write"):
            self.assertIn(event, command[2])

    def test_runtime_pins_match_lock_file(self):
        runtime = json.loads((ROOT / "upstream.lock.json").read_text())["runtime_tools"]
        self.assertEqual(runtime["uv"]["version"], kit.UV_VERSION)
        self.assertEqual(runtime["uv"]["installer_url"], kit.UV_INSTALLER_URL)
        self.assertEqual(runtime["uv"]["installer_sha256"], kit.UV_INSTALLER_SHA256)
        self.assertEqual(runtime["repowise"]["version"], kit.REPOWISE_VERSION)

    def test_missing_uv_runs_verified_installer_once(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))

            def fake_run(command, **kwargs):
                self.assertEqual(command, ["sh"])
                self.assertEqual(kwargs["input_text"], "installer")
                destination = Path(kwargs["env"]["UV_INSTALL_DIR"])
                destination.mkdir(parents=True)
                (destination / "uv").write_text("uv")
                return subprocess.CompletedProcess(command, 0, "", "")

            with mock.patch.object(
                kit, "find_runtime_command", return_value=None
            ), mock.patch.object(
                kit, "download_sha256", return_value=b"installer"
            ) as download, mock.patch.object(kit, "run", side_effect=fake_run) as run:
                uv = kit.ensure_uv(paths)
            self.assertEqual(uv, str(paths.home / ".local" / "bin" / "uv"))
            download.assert_called_once_with(kit.UV_INSTALLER_URL, kit.UV_INSTALLER_SHA256)
            run.assert_called_once()

    def test_download_rejects_wrong_sha256(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return b"wrong"

        with mock.patch.object(kit.urllib.request, "urlopen", return_value=Response()):
            with self.assertRaises(kit.KitError):
                kit.download_sha256("https://example.invalid/uv.sh", "0" * 64)

    def test_missing_repowise_installs_persistent_tool(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            commands = []

            def fake_run(command, **kwargs):
                commands.append(command)
                if command[1:3] == ["tool", "install"]:
                    destination = Path(kwargs["env"]["UV_TOOL_BIN_DIR"])
                    destination.mkdir(parents=True)
                    (destination / "repowise").write_text("repowise")
                return subprocess.CompletedProcess(command, 0, "", "")

            with mock.patch.object(
                kit, "find_runtime_command", return_value=None
            ), mock.patch.object(kit, "run", side_effect=fake_run):
                repowise = kit.ensure_repowise(paths, "/usr/bin/uv")
            self.assertEqual(repowise, str(paths.home / ".local" / "bin" / "repowise"))
            self.assertEqual(
                commands,
                [
                    ["/usr/bin/uv", "tool", "install", "repowise==0.41.0"],
                    ["/usr/bin/uv", "tool", "update-shell"],
                ],
            )

    def test_different_repowise_version_stops_install(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            with mock.patch.object(
                kit, "find_runtime_command", return_value="/usr/bin/repowise"
            ), mock.patch.object(
                kit, "command_version", return_value="RepoWise 0.40.0"
            ), mock.patch.object(kit, "run") as run, self.assertRaises(kit.KitError):
                kit.ensure_repowise(paths, "/usr/bin/uv")
            run.assert_not_called()

    def test_bootstrap_initializes_once_and_always_installs_hook(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            GitFixture(root).commit("sample.py", "value = 1\n")
            log = Path(temp) / "calls"
            fake = Path(temp) / "repowise"
            fake.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$*\" >> \"$CALL_LOG\"\n"
                "if [ \"$1\" = init ]; then\n"
                "  for LAST do :; done\n"
                "  mkdir -p \"$LAST/.repowise\"\n"
                "elif [ \"$1\" = update ] && ! git rev-parse --verify HEAD >/dev/null 2>&1; then\n"
                "  exit 7\n"
                "elif [ \"$1\" = watch ]; then\n"
                "  printf '%s\\n' \"$$\" >> \"$WATCH_PID_LOG\"\n"
                "  trap 'exit 0' HUP INT TERM\n"
                "  while :; do sleep 1; done\n"
                "fi\n"
            )
            fake.chmod(0o755)
            env = os.environ.copy()
            env["CALL_LOG"] = str(log)
            watcher_pids = Path(temp) / "watcher-pids"
            env["WATCH_PID_LOG"] = str(watcher_pids)
            script = kit.repowise_bootstrap(str(fake), watcher=[str(fake), "watch"])
            first = subprocess.run(
                ["/bin/sh", "-c", script],
                cwd=root,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                ["/bin/sh", "-c", script], cwd=root, env=env, check=True
            )
            calls = log.read_text().splitlines()
            self.assertEqual(sum(line.startswith("init ") for line in calls), 1)
            self.assertEqual(sum(line.startswith("hook install ") for line in calls), 2)
            self.assertEqual(
                sum(line.startswith("update --index-only ") for line in calls), 2
            )
            self.assertEqual(
                sum(line.startswith("watch --index-only ") for line in calls), 2
            )
            self.assertEqual(sum(line.startswith("mcp ") for line in calls), 2)
            self.assertEqual(first.stdout, "")
            self.assertLess(
                calls.index(
                    "update --index-only --no-agents --no-workspace " + str(root)
                ),
                calls.index("watch --index-only --no-workspace " + str(root)),
            )
            self.assertLess(
                calls.index("watch --index-only --no-workspace " + str(root)),
                calls.index("mcp " + str(root)),
            )
            for pid in map(int, watcher_pids.read_text().splitlines()):
                with self.assertRaises(ProcessLookupError):
                    os.kill(pid, 0)

    def test_bootstrap_initializes_only_empty_non_git_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "calls"
            fake = root / "repowise"
            fake.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$*\" >> \"$CALL_LOG\"\n"
                "if [ \"$1\" = init ]; then\n"
                "  for LAST do :; done\n"
                "  mkdir -p \"$LAST/.repowise\"\n"
                "elif [ \"$1\" = update ] && ! git rev-parse --verify HEAD >/dev/null 2>&1; then\n"
                "  exit 7\n"
                "elif [ \"$1\" = watch ]; then\n"
                "  trap 'exit 0' HUP INT TERM\n"
                "  while :; do sleep 1; done\n"
                "fi\n"
            )
            fake.chmod(0o755)
            env = os.environ.copy()
            env["CALL_LOG"] = str(log)
            script = kit.repowise_bootstrap(str(fake), watcher=[str(fake), "watch"])

            empty = root / "empty"
            empty.mkdir()
            subprocess.run(["/bin/sh", "-c", script], cwd=empty, env=env, check=True)
            self.assertTrue((empty / ".git").is_dir())
            empty_calls = log.read_text().splitlines()
            self.assertEqual(sum(line.startswith("init ") for line in empty_calls), 1)
            self.assertEqual(sum(line.startswith("hook install ") for line in empty_calls), 1)
            self.assertEqual(sum(line.startswith("update --index-only ") for line in empty_calls), 0)
            self.assertEqual(sum(line.startswith("watch --index-only ") for line in empty_calls), 1)
            self.assertIn(f"mcp {empty}", empty_calls)

            log.write_text("")
            nonempty = root / "nonempty"
            nonempty.mkdir()
            (nonempty / ".keep").write_text("")
            subprocess.run(["/bin/sh", "-c", script], cwd=nonempty, env=env, check=True)
            self.assertFalse((nonempty / ".git").exists())
            self.assertEqual(log.read_text().splitlines(), ["mcp"])

    def test_bootstrap_stops_when_watcher_fails_to_start(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            GitFixture(root)
            (root / ".repowise").mkdir()
            log = root / "calls"
            fake = root / "repowise"
            fake.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$*\" >> \"$CALL_LOG\"\n"
                "if [ \"$1\" = watch ]; then exit 7; fi\n"
            )
            fake.chmod(0o755)
            env = os.environ.copy()
            env["CALL_LOG"] = str(log)

            result = subprocess.run(
                [
                    "/bin/sh",
                    "-c",
                    kit.repowise_bootstrap(
                        str(fake), watcher=[str(fake), "watch"]
                    ),
                ],
                cwd=root,
                env=env,
                check=False,
            )

            self.assertEqual(result.returncode, 7)
            self.assertFalse(
                any(line.startswith("mcp ") for line in log.read_text().splitlines())
            )


class IntegrationTests(unittest.TestCase):
    def test_setup_skips_catch_up_before_first_commit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            GitFixture(root)
            calls = []

            def fake_repowise(repo: Path, *args: str, **_kwargs):
                calls.append(args)
                if args and args[0] == "init":
                    (repo / ".repowise").mkdir(exist_ok=True)
                return subprocess.CompletedProcess([], 0, "", "")

            paths = kit.InstallPaths(
                root, root / "codex", root / "skills", root / "kit"
            )
            with mock.patch.object(
                kit, "repowise_command", fake_repowise
            ), mock.patch.object(
                kit,
                "ensure_repowise_runtime",
                return_value=("/usr/bin/uv", "/usr/bin/repowise"),
            ), mock.patch.object(
                kit,
                "repowise_watch_command",
                return_value=["/usr/bin/python3", "-c", kit.REPOWISE_WATCH_PATCH],
            ):
                kit.setup_repo(Namespace(repo=str(root), prose=False), paths)

            self.assertTrue(any(call[0] == "init" for call in calls))
            self.assertFalse(any(call[0] == "update" for call in calls))

    def test_setup_preserves_roadmap_and_unrelated_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            git = GitFixture(root)
            git.commit("AGENTS.md", "# Project rules\n")
            (root / ".codex").mkdir()
            (root / ".codex" / "config.toml").write_text(
                '[mcp_servers.other]\ncommand = "other"\n', encoding="utf-8"
            )
            (root / "docs").mkdir()
            (root / "docs" / "roadmap.md").write_text("sentinel\n", encoding="utf-8")

            calls = []

            def fake_repowise(repo: Path, *args: str, **_kwargs):
                calls.append(args)
                if args and args[0] == "init":
                    (repo / ".repowise").mkdir(exist_ok=True)
                return subprocess.CompletedProcess([], 0, "", "")

            paths = kit.InstallPaths(root, root / "codex", root / "skills", root / "kit")
            with mock.patch.object(kit, "repowise_command", fake_repowise), mock.patch.object(
                kit, "ensure_repowise_runtime", return_value=("/usr/bin/uv", "/usr/bin/repowise")
            ), mock.patch.object(
                kit,
                "repowise_watch_command",
                return_value=["/usr/bin/python3", "-c", kit.REPOWISE_WATCH_PATCH],
            ):
                kit.setup_repo(Namespace(repo=str(root), prose=False), paths)
            self.assertIn("mcp_servers.other", (root / ".codex" / "config.toml").read_text())
            self.assertTrue(any(call[:2] == ("hook", "install") for call in calls))
            self.assertIn(
                (
                    "update",
                    "--index-only",
                    "--no-agents",
                    "--no-workspace",
                    str(root),
                ),
                calls,
            )
            self.assertEqual((root / "docs" / "roadmap.md").read_text(), "sentinel\n")
            self.assertEqual((root / "AGENTS.md").read_text(), "# Project rules\n")
            with mock.patch.object(kit, "repowise_command", fake_repowise), mock.patch.object(
                kit, "ensure_repowise_runtime", return_value=("/usr/bin/uv", "/usr/bin/repowise")
            ):
                kit.remove_repo(Namespace(repo=str(root), delete_index=False), paths)
            self.assertEqual((root / "AGENTS.md").read_text(), "# Project rules\n")
            self.assertIn("enabled = false", (root / ".codex" / "config.toml").read_text())
            self.assertTrue(any(call[:2] == ("hook", "uninstall") for call in calls))

    def test_roadmap_contract_and_router(self):
        rules = (ROOT / "assets" / "AGENTS.block.md").read_text()
        template = (
            ROOT / "assets" / "skills" / "roadmap-maintainer" / "assets" / "roadmap-template.md"
        ).read_text()
        self.assertIn("`roadmap-maintainer`", rules)
        self.assertEqual(template.count("## Active"), 1)
        self.assertIn("## Declined", template)

    def test_tracked_task_records_freeze_before_delivery(self):
        delivery = (
            ROOT / "assets" / "skills" / "delivery-lifecycle" / "references" / "delivery-lifecycle.md"
        ).read_text()
        roadmap = (ROOT / "assets" / "skills" / "roadmap-maintainer" / "SKILL.md").read_text()
        plans = (ROOT / ".agent" / "PLANS.md").read_text()
        closure = (
            ROOT
            / "assets"
            / "skills"
            / "adversarial-review"
            / "references"
            / "review-closure.md"
        ).read_text()
        publication = (
            ROOT / "assets" / "skills" / "publication" / "references" / "publication.md"
        ).read_text()

        freeze = (
            "Freeze every tracked task record before the task commit, CI, push, pull request, merge, "
            "or publication."
        )
        self.assertIn(freeze, delivery)
        for content in (roadmap, plans, closure, publication):
            self.assertNotIn(freeze, content)

        self.assertNotIn("review is pending", roadmap)
        self.assertNotIn("Validation establishes a review candidate", roadmap)
        self.assertIn("An ExecPlan is a living document until review closure", plans)
        self.assertIn("Do not write a readiness or authorization statement", plans)
        self.assertIn("Do not add a `Progress` item for a delivery action", plans)
        self.assertIn("limited to four updates", closure)
        self.assertNotIn("publication status", closure)
        self.assertIn("cpk-rule-route-only: delivery-lifecycle", publication)

    def test_execplan_is_the_only_durable_task_model(self):
        rules = (ROOT / "assets" / "AGENTS.block.md").read_text()
        plans = (ROOT / ".agent" / "PLANS.md").read_text()
        preflight = (ROOT / "assets" / "skills" / "design-preflight" / "SKILL.md").read_text()
        self.assertIn("{{PLANS_FILE}}", rules)
        self.assertIn("cpk-rule-owner: execplans", plans)
        self.assertNotIn("Task Brief", preflight)
        self.assertNotIn("task-brief", kit.ALL_SKILLS)

    def test_rule_owners_are_unique(self):
        live = [
            ROOT / ".agent" / "PLANS.md",
            ROOT / "assets" / "AGENTS.block.md",
            ROOT / "assets" / "hooks" / "session_start.py",
            ROOT / "README.md",
            ROOT / "CODEX-INSTALL-PROMPT.md",
            *(path for path in sorted((ROOT / "docs").glob("*.md")) if path.name != "roadmap.md"),
            *sorted((ROOT / "assets" / "skills").rglob("*.md")),
        ]
        owner_pattern = re.compile(r"<!-- cpk-rule-owner: ([a-z0-9-]+) -->")
        guard_pattern = re.compile(r"<!-- cpk-rule-guard: (.+?) -->")
        section_pattern = re.compile(r"^## [^\n]+\n(.*?)(?=^## |\Z)", re.DOTALL | re.MULTILINE)
        route_pattern = re.compile(r"<!-- cpk-rule-route-only: ([a-z0-9-]+) -->")
        owners = {}
        guards = []

        for path in live:
            content = path.read_text()
            found = owner_pattern.findall(content)
            self.assertLessEqual(len(found), 1, path)
            if not found:
                continue
            owner = found[0]
            self.assertNotIn(owner, owners)
            owners[owner] = path
            owner_guards = guard_pattern.findall(content)
            self.assertTrue(owner_guards, path)
            for guard in owner_guards:
                self.assertGreaterEqual(content.count(guard), 2, (path, guard))
                guards.append((path, guard))

        expected = {
            "routing",
            "execplans",
            "coordination",
            "supported-model",
            "scope-boundaries",
            "decision-handoffs",
            "repository-knowledge",
            "delivery-lifecycle",
            "implementation-modes",
            "git-isolation",
            "full-set-results",
            "owner-composition",
            "review-closure",
            "publication",
            "versioning",
            "rule-ownership",
            "design-preflight",
            "adversarial-review",
            "docs-maintainer",
            "roadmap-maintainer",
            "research-first",
            "defect-diagnostic",
        }
        self.assertEqual(set(owners), expected)

        def assert_route(path, owner, line):
            match = re.fullmatch(r"\[[^]]+\]\((?:<)?([^)>]+)(?:>)?\)", line)
            self.assertIsNotNone(match, (path, line))
            target = (path.parent / match.group(1)).resolve()
            self.assertTrue(target.is_file(), (path, target))
            self.assertEqual(owner_pattern.findall(target.read_text()), [owner], (path, target, owner))

        for path in live:
            checked_routes = 0
            for body in section_pattern.findall(path.read_text()):
                routes = route_pattern.findall(body)
                if not routes:
                    continue
                checked_routes += len(routes)
                self.assertEqual(len(routes), 1, (path, body))
                owner = routes[0]
                self.assertIn(owner, owners, (path, owner))
                lines = [line for line in body.splitlines() if line.strip()]
                self.assertEqual(len(lines), 2, (path, body))
                self.assertEqual(lines[0], f"<!-- cpk-rule-route-only: {owner} -->")
                assert_route(path, owner, lines[1])
            self.assertEqual(checked_routes, len(route_pattern.findall(path.read_text())), path)

        card = (ROOT / "assets" / "skills" / "design-preflight" / "references" / "preflight-card.md").read_text()
        mutated = card.replace(
            "## Supported operating model\n\n",
            "## Supported operating model\n\nExpanded shared rule.\n\n",
            1,
        )
        mutated_body = next(
            body
            for body in section_pattern.findall(mutated)
            if route_pattern.findall(body) == ["supported-model"]
        )
        self.assertEqual(len([line for line in mutated_body.splitlines() if line.strip()]), 3)

        prompt = (ROOT / "CODEX-INSTALL-PROMPT.md").read_text()
        prompt_body = next(body for body in section_pattern.findall(prompt) if route_pattern.search(body))
        prompt_lines = [line for line in prompt_body.splitlines() if line.strip()]
        with self.assertRaises(AssertionError):
            assert_route(ROOT / "CODEX-INSTALL-PROMPT.md", "supported-model", "[Missing](missing.md)")
        with self.assertRaises(AssertionError):
            assert_route(
                ROOT / "CODEX-INSTALL-PROMPT.md",
                "supported-model",
                prompt_lines[1].replace("supported-model.md", "rule-ownership.md"),
            )

        contents = {path: path.read_text() for path in live}
        for owner_path, guard in guards:
            for path, content in contents.items():
                if path != owner_path:
                    self.assertNotIn(guard, content, (owner_path, path, guard))

    def test_rule_routes_are_complete_and_links_resolve(self):
        agents = (ROOT / "assets" / "AGENTS.block.md").read_text()
        skill_routes = {
            "delivery-lifecycle": (
                "coordination.md",
                "delivery-lifecycle.md",
                "implementation-modes.md",
                "git-isolation.md",
                "decision-handoffs.md",
            ),
            "design-preflight": (
                "scope-boundaries.md",
                "supported-model.md",
                "owner-composition.md",
                "full-set-results.md",
            ),
            "adversarial-review": ("review-closure.md",),
            "publication": ("publication.md", "versioning.md"),
        }
        for skill, references in skill_routes.items():
            self.assertIn(f"`{skill}`", agents)
            skill_text = (ROOT / "assets" / "skills" / skill / "SKILL.md").read_text()
            for reference in references:
                self.assertIn(reference, skill_text)
        for skill in ("repository-knowledge", "toolkit-maintainer"):
            self.assertIn(f"`{skill}`", agents)
        self.assertNotIn("codex-practical-kit-rules", agents)

        link_pattern = re.compile(r"]\((?:<)?([^)>]+\.md)(?:>)?\)")
        link_sources = [
            ROOT / "README.md",
            ROOT / "docs" / "OPERATING-MANUAL.md",
            ROOT / "docs" / "REMOVE-CBM.md",
            ROOT / "docs" / "REPOWISE.md",
            ROOT / "docs" / "REVIEW.md",
            ROOT / "docs" / "SPEC-KIT.md",
            ROOT / "docs" / "WHY-THIS-SHAPE.md",
            *sorted((ROOT / "assets" / "skills").rglob("*.md")),
        ]
        for path in link_sources:
            for target in link_pattern.findall(path.read_text()):
                if "{{" in target or Path(target).is_absolute():
                    continue
                self.assertTrue((path.parent / target).resolve().is_file(), (path, target))

    def test_runtime_scenario_preflight_has_one_rule_owner(self):
        skill = (ROOT / "assets" / "skills" / "design-preflight" / "SKILL.md").read_text()
        card = (
            ROOT / "assets" / "skills" / "design-preflight" / "references" / "preflight-card.md"
        ).read_text()
        result = (
            ROOT / "assets" / "skills" / "design-preflight" / "references" / "preflight-review.md"
        ).read_text()
        lens = (
            ROOT / "assets" / "skills" / "adversarial-review" / "references" / "reviewer-lenses.md"
        ).read_text()
        owner = (
            ROOT
            / "assets"
            / "skills"
            / "design-preflight"
            / "references"
            / "owner-composition.md"
        ).read_text()

        self.assertIn("For non-trivial runtime behavior, derive a Scenario Proof", skill)
        self.assertIn("with no inherited task conversation", skill)
        self.assertIn("Do not give it the coordinator's card", skill)
        self.assertIn('"reviewer": "normal-use-scenarios"', result)
        self.assertIn('"contract_gaps"', result)
        self.assertEqual(owner.count("<!-- cpk-rule-guard:"), 6)
        self.assertIn("full-set-results.md", owner)
        for route in (skill, card, result, lens):
            self.assertIn("owner-composition.md", route)
            self.assertIn("full-set-results.md", route)

    def test_default_mode_preflight_and_repowise_continue_through_corrections(self):
        root = ROOT / "assets" / "skills"
        delivery = (
            root / "delivery-lifecycle" / "references" / "delivery-lifecycle.md"
        ).read_text()
        preflight = (root / "design-preflight" / "SKILL.md").read_text()
        composition = (
            root / "design-preflight" / "references" / "owner-composition.md"
        ).read_text()
        review = (root / "adversarial-review" / "SKILL.md").read_text()
        repository = (root / "repository-knowledge" / "SKILL.md").read_text()

        invocation = (
            "Invoke Design Preflight before implementation or an accepted review correction "
            "when its trigger matches, even outside Plan Mode."
        )
        self.assertIn(invocation, delivery)
        for content in (preflight, composition, review, repository):
            self.assertNotIn(invocation, content)

        self.assertIn("Plan Mode and an explicit skill request are not prerequisites", preflight)
        self.assertIn("Apply the same entry gate to an accepted correction", preflight)
        self.assertIn("The small-change exception still applies", preflight)
        self.assertIn(
            "For an accepted correction that passes the entry gate, spawn one fresh",
            preflight,
        )
        self.assertIn("Reapply Delivery Lifecycle before an accepted correction", review)
        self.assertIn("cpk-rule-route-only: repository-knowledge", delivery)
        self.assertIn("cpk-rule-route-only: repository-knowledge", preflight)

        lookup = "Use RepoWise for each new repository lookup throughout a task."
        self.assertIn(lookup, repository)
        for content in (delivery, preflight, composition, review):
            self.assertNotIn(lookup, content)
        self.assertIn("Initial orientation does not satisfy a later lookup", repository)

        self.assertIn("smallest counterexample ordering", composition)
        self.assertIn("one signal has multiple causes", composition)
        self.assertIn("Do not test every event permutation", composition)

    def test_implementation_modes_are_phase_scoped(self):
        root = ROOT / "assets" / "skills"
        owner = (
            root
            / "delivery-lifecycle"
            / "references"
            / "implementation-modes.md"
        ).read_text()
        agents = (ROOT / "assets" / "AGENTS.block.md").read_text()
        delivery = (root / "delivery-lifecycle" / "SKILL.md").read_text()
        preflight = (root / "design-preflight" / "SKILL.md").read_text()
        research = (root / "research-first" / "SKILL.md").read_text()
        review = (root / "adversarial-review" / "SKILL.md").read_text()

        self.assertIn("cpk-rule-owner: implementation-modes", owner)
        self.assertIn("Keep normal mode active through accepted test scope", owner)
        self.assertIn("requirements, planning, research, Scenario Proof", owner)
        self.assertIn("test code, production code, or an accepted review correction", owner)
        self.assertIn("explicit user mode selection overrides", owner)
        self.assertIn("without, disable, or exclude Ponytail", owner)
        self.assertIn("Return to normal mode before each read-only review pass", owner)
        self.assertIn("managed prompt hook selects normal mode", owner)
        self.assertIn("Use xhigh reasoning for each fresh read-only planning challenger", owner)
        self.assertIn("main thread's configured reasoning effort for implementation", owner)
        self.assertIn("accepted correction", owner)
        for content in (agents, delivery, preflight, research, review):
            self.assertNotIn(
                "Use xhigh reasoning for each fresh read-only planning challenger",
                content,
            )
        self.assertIn("Give a correction challenger the accepted finding", preflight)
        self.assertIn("Implementation after accepted test scope", agents)
        self.assertNotIn("Code changes: `ponytail`", agents)
        for route in (delivery, preflight, research, review):
            self.assertIn("implementation-modes.md", route)
        self.assertNotIn("Apply Ponytail", research)

    def test_scenario_proof_maps_transition_closed_checks(self):
        root = ROOT / "assets" / "skills"
        owner = (
            root
            / "design-preflight"
            / "references"
            / "owner-composition.md"
        ).read_text()
        preflight = (root / "design-preflight" / "SKILL.md").read_text()
        card = (
            root / "design-preflight" / "references" / "preflight-card.md"
        ).read_text()
        result = (
            root / "design-preflight" / "references" / "preflight-review.md"
        ).read_text()
        packet = (
            root / "adversarial-review" / "references" / "review-packet.md"
        ).read_text()
        lenses = (
            root / "adversarial-review" / "references" / "reviewer-lenses.md"
        ).read_text()

        self.assertIn("scenario set is open while a supported event", owner)
        self.assertIn("until the terminal owner produces the required oracle", owner)
        self.assertIn("Component checks do not satisfy", owner)
        self.assertIn("Before implementation", preflight)
        self.assertIn("Before review", preflight)
        self.assertIn("suite pass or test count does not replace", preflight)
        self.assertIn(
            "| Scenario | Production path | Required oracle | Runnable test or command | Result |",
            card,
        )
        for field in ('"production_path"', '"required_oracle"', '"planned_check"'):
            self.assertIn(field, result)
        self.assertIn("accepted Scenario Proof mapping", packet)
        self.assertIn("aggregate suite result is supporting evidence only", packet)
        self.assertIn("required oracle in the named runnable check", lenses)

    def test_product_scope_boundaries_gate_preflight_and_review(self):
        rules_root = ROOT / "assets" / "skills" / "design-preflight" / "references"
        owner = (rules_root / "scope-boundaries.md").read_text()
        preflight = (ROOT / "assets" / "skills" / "design-preflight" / "SKILL.md").read_text()
        card = (
            ROOT / "assets" / "skills" / "design-preflight" / "references" / "preflight-card.md"
        ).read_text()
        result = (
            ROOT / "assets" / "skills" / "design-preflight" / "references" / "preflight-review.md"
        ).read_text()
        review = (ROOT / "assets" / "skills" / "adversarial-review" / "SKILL.md").read_text()
        packet = (
            ROOT / "assets" / "skills" / "adversarial-review" / "references" / "review-packet.md"
        ).read_text()
        finding = (
            ROOT / "assets" / "skills" / "adversarial-review" / "references" / "finding-format.md"
        ).read_text()

        self.assertIn("cpk-rule-owner: scope-boundaries", owner)
        for route in (preflight, card, result, review, packet, finding):
            self.assertIn("scope-boundaries.md", route)
        self.assertLess(review.index("## Scope gate"), review.index("## Supported-model gate"))
        self.assertIn('"classification": "composes | opaque | deferred"', result)
        self.assertIn('"classification": "composes | opaque"', finding)
        self.assertIn('"changed_production_entry_point"', finding)
        self.assertIn('"task_visible_wrong_result"', finding)

    def test_review_checkpoints_limit_repeat_review(self):
        root = ROOT / "assets" / "skills" / "adversarial-review"
        review = (root / "SKILL.md").read_text()
        packet = (root / "references" / "review-packet.md").read_text()
        finding = (root / "references" / "finding-format.md").read_text()
        lenses = (root / "references" / "reviewer-lenses.md").read_text()

        self.assertIn("`git write-tree`", review)
        self.assertIn("review only the staged-tree delta and its direct impact", review)
        self.assertIn("Before staging a later candidate", review)
        self.assertIn("unrelated tracked-file change invalidates the checkpoint", review)
        self.assertIn("Do not repeat local correctness review of unchanged code", review)
        self.assertIn("Run the coherence pass once", review)
        self.assertIn("A clean fix delta before coherence is an intermediate result", review)
        self.assertIn("clean delta review of a coherence correction", review)
        self.assertIn("Previous reviewed tree", packet)
        self.assertIn("Pre-stage tracked-change classification", packet)
        self.assertIn("Checkpoint invalidation reason", packet)
        self.assertIn('"review_mode": "full | delta | coherence"', finding)
        self.assertIn("## Delta correctness", lenses)
        self.assertIn("## Final coherence", lenses)

    def test_lifecycle_skills_and_version(self):
        publication = (
            ROOT / "assets" / "skills" / "publication" / "references" / "publication.md"
        ).read_text()
        for skill in (
            "delivery-lifecycle",
            "repository-knowledge",
            "publication",
            "toolkit-maintainer",
        ):
            self.assertIn(skill, kit.CUSTOM_SKILLS)
        self.assertNotIn("codex-practical-kit-rules", kit.CUSTOM_SKILLS)
        self.assertIn("codex-practical-kit-rules", kit.OBSOLETE_SKILLS)
        self.assertIn("Before Codex Practical Kit publication", publication)
        self.assertIn("`./install.sh`", publication)
        self.assertIn("`./doctor.sh`", publication)
        self.assertIn("from the reviewed candidate", publication)
        self.assertIn("`Result: ready`", publication)
        self.assertEqual(kit.KIT_VERSION, "0.17.1")
        self.assertNotIn("Version `0.17.1`", (ROOT / "README.md").read_text())
        self.assertNotIn("version 0.17.1", (ROOT / "CODEX-INSTALL-PROMPT.md").read_text())

    def test_repowise_is_required(self):
        config = kit.repowise_config_block(
            "/tmp/repowise", watcher=["/tmp/repowise", "watch"]
        )
        owner = (
            ROOT
            / "assets"
            / "skills"
            / "repository-knowledge"
            / "SKILL.md"
        ).read_text()
        docs_skill = (ROOT / "assets" / "skills" / "docs-maintainer" / "SKILL.md").read_text()
        research_skill = (ROOT / "assets" / "skills" / "research-first" / "SKILL.md").read_text()
        notes = (ROOT / "docs" / "REPOWISE.md").read_text()

        self.assertIn("required = true", config)
        self.assertIn("startup_timeout_sec = 1800", config)
        self.assertIn("update --index-only --no-agents --no-workspace", config)
        self.assertIn("watch --index-only --no-workspace", config)
        self.assertIn("cpk-rule-owner: repository-knowledge", owner)
        for route in (docs_skill, research_skill, notes):
            self.assertIn("repository-knowledge", route)

    def test_repowise_routes_indexed_queries(self):
        owner = (
            ROOT
            / "assets"
            / "skills"
            / "repository-knowledge"
            / "SKILL.md"
        ).read_text()
        agents = (ROOT / "assets" / "AGENTS.block.md").read_text()
        metadata = (
            ROOT
            / "assets"
            / "skills"
            / "repository-knowledge"
            / "agents"
            / "openai.yaml"
        ).read_text()

        for rule in (
            'Resolve exact identifiers through `search_codebase(mode="symbol")` and `get_symbol` before native search.',
            "A verified `get_symbol` body is source confirmation; do not read it again.",
            "After `no-llm-provider`, do not call `get_answer` again in the same Codex session.",
            "Use `get_answer` only for conceptual how or why questions.",
            "`no-llm-provider` means that synthesis is unavailable. RepoWise is still available.",
            "use `search_codebase` with automatic routing",
            "Automatic compaction does not end this route.",
            "make one more query with the strongest known identifier or path",
            "Preserve ambiguous exact candidates",
        ):
            self.assertIn(rule, owner)
            self.assertNotIn(rule, agents)
        self.assertIn('value: "repowise"', metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)

    def test_review_stop_diagnostics_are_per_finding_and_mandatory(self):
        review = (ROOT / "assets" / "skills" / "adversarial-review" / "SKILL.md").read_text()
        formatter = (
            ROOT
            / "assets"
            / "skills"
            / "adversarial-review"
            / "references"
            / "stop-finding-format.md"
        ).read_text()
        diagnostic = (ROOT / "assets" / "skills" / "defect-diagnostic" / "SKILL.md").read_text()
        summary = (
            ROOT
            / "assets"
            / "skills"
            / "defect-diagnostic"
            / "references"
            / "diagnostic-summary.md"
        ).read_text()
        metadata = (
            ROOT / "assets" / "skills" / "defect-diagnostic" / "agents" / "openai.yaml"
        ).read_text()

        self.assertIn("defect-diagnostic", kit.CUSTOM_SKILLS)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertIn("references/stop-finding-format.md", review)
        self.assertIn("Invoke `defect-diagnostic` automatically and validate its result.", review)
        self.assertIn("Compose one final response only after the diagnostic is complete.", review)
        self.assertIn("Then present the complete diagnostic, including its portable summary.", review)
        self.assertIn("Put the final `Review:` and `Docs:` status lines after the diagnostic.", review)
        self.assertIn("Only defects in executable production code can increment", review)
        self.assertIn("Tests, test fixtures, documentation, static configuration", review)
        self.assertIn("A validated P0 or P1 defect in executable production code on any pass.", review)
        self.assertIn("A production-code defect on the third consecutive counted pass.", review)
        self.assertNotIn("executable source, tests", review)

        labels = [
            "Decision",
            "Term",
            "Trigger",
            "Likelihood",
            "Current exposure",
            "Options",
            "Recommendation",
            "Question",
        ]
        positions = [formatter.index(f"\n{label}\n") for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(formatter.count("\nQuestion\n"), 1)
        self.assertIn("Repeat the complete block for each finding.", formatter)
        self.assertIn("Do not use cumulative", formatter)

        self.assertIn("Spawn one fresh read-only diagnostic subagent.", diagnostic)
        self.assertIn("Omit reviewer fix directions and all proposed corrections.", diagnostic)
        self.assertIn("Do not give it a diagnosis, preferred fix, or toolkit correction.", diagnostic)
        self.assertIn("Complete and validate the diagnostic before the coordinator composes the final response.", diagnostic)
        self.assertIn("Present the separate stop-finding handoffs first.", diagnostic)
        self.assertIn("Then present the complete diagnostic, including its portable summary.", diagnostic)
        self.assertIn("Do not return a finding question or final response before the diagnostic is ready.", diagnostic)
        self.assertIn("After the diagnostic, halt.", diagnostic)
        self.assertIn("Do not edit files, run checks, start review", diagnostic)
        self.assertIn("Repeat the complete finding section for every validated stop finding.", summary)
        self.assertIn("Portable summary", summary)
        self.assertIn("Human direction is required. Do not continue implementation.", summary)


if __name__ == "__main__":
    unittest.main()

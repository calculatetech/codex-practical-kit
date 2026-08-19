import hashlib
import json
import os
import re
import shutil
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
from assets.runtime import repowise_bootstrap as bootstrap


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
        runtime = Path(r"C:\Users\Example User\repowise_bootstrap.py")
        repowise = r"C:\Users\Example User\repowise.exe"
        updated = kit.marker_block(
            "# start\nold\n# end\n",
            "# start",
            "# end",
            kit.repowise_config_block(repowise, runtime),
        )
        config = tomllib.loads(updated)["mcp_servers"]["repowise"]
        self.assertEqual(config["command"], sys.executable)
        self.assertEqual(config["args"], [str(runtime), repowise])


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.runtime = mock.patch.object(
            kit,
            "ensure_repowise_runtime",
            return_value=("/usr/bin/uv", "/usr/bin/repowise"),
        )
        self.runtime.start()

    def tearDown(self):
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
                "neuroarxiv",
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
            self.assertEqual(
                set(hooks),
                {"PreToolUse", "PostToolUse", "SessionStart", "UserPromptSubmit", "Stop"},
            )
            self.assertEqual(
                hooks["PreToolUse"][0]["hooks"][0]["command"],
                "python /tmp/user.py",
            )
            self.assertEqual(hooks["PreToolUse"][1]["matcher"], "^apply_patch$")
            self.assertEqual(hooks["PostToolUse"][0]["matcher"], "^apply_patch$")
            self.assertEqual(len(hooks["SessionStart"]), 1)
            self.assertEqual(len(hooks["UserPromptSubmit"]), 1)
            self.assertEqual(len(hooks["Stop"]), 1)
            self.assertEqual(
                hooks["SessionStart"][0]["hooks"][0]["additionalContextLimit"], 1200
            )
            self.assertEqual(
                hooks["UserPromptSubmit"][0]["hooks"][0]["additionalContextLimit"], 1200
            )
            self.assertNotIn(
                "additionalContextLimit", hooks["Stop"][0]["hooks"][0]
            )
            self.assertNotIn(
                "additionalContextLimit", hooks["PreToolUse"][1]["hooks"][0]
            )
            self.assertNotIn(
                "additionalContextLimit", hooks["PostToolUse"][0]["hooks"][0]
            )
            self.assertEqual(
                kit.configured_hook_events(paths, config_text),
                set(kit.MANAGED_HOOK_EVENTS),
            )
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
                "normal mode\nUse plan-history before planning. Read and reconcile all applicable Plan history records.\n",
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

    def test_reinstall_removes_stop_context_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            config = paths.codex_home / "config.toml"
            kit.install_hooks(paths)
            text = config.read_text()
            before, stop = text.split("[[hooks.Stop.hooks]]", 1)
            config.write_text(
                before
                + "[[hooks.Stop.hooks]]"
                + stop.replace(
                    "timeout = 10", "timeout = 10\nadditionalContextLimit = 1200", 1
                )
            )

            kit.install_hooks(paths)

            handler = tomllib.loads(config.read_text())["hooks"]["Stop"][0]["hooks"][0]
            self.assertNotIn("additionalContextLimit", handler)

    def test_reinstall_repairs_wrong_apply_patch_matcher(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            config = paths.codex_home / "config.toml"
            kit.install_hooks(paths)
            config.write_text(
                config.read_text().replace(
                    '[[hooks.PostToolUse]]\nmatcher = "^apply_patch$"',
                    '[[hooks.PostToolUse]]\nmatcher = "Bash"',
                ),
                encoding="utf-8",
            )

            kit.install_hooks(paths)

            hooks = tomllib.loads(config.read_text())["hooks"]
            self.assertEqual(len(hooks["PostToolUse"]), 1)
            self.assertEqual(hooks["PostToolUse"][0]["matcher"], "^apply_patch$")

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
        self.assertIn("plan-history", contexts["compact"])

    def test_copy_reinstall_and_uninstall(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            paths = self.paths(base)
            source = self.source(base)
            adhd = paths.skills_home / "adhd"
            adhd.mkdir(parents=True)
            (adhd / "SKILL.md").write_text("user-managed\n")
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
            self.assertEqual((adhd / "SKILL.md").read_text(), "user-managed\n")
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

    def test_unowned_neuroarxiv_directory_is_a_conflict(self):
        def fake_stage(destination: Path):
            for name in kit.UPSTREAM_SKILLS:
                skill = destination / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(name + "\n")
            return {}

        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            conflict = paths.skills_home / "neuroarxiv"
            conflict.mkdir(parents=True)
            (conflict / "SKILL.md").write_text("user\n")

            with mock.patch.object(
                kit, "stage_upstream_skills", fake_stage
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
            repowise_config = tomllib.loads(installed)["mcp_servers"]["repowise"]
            self.assertEqual(repowise_config["command"], sys.executable)
            self.assertEqual(
                repowise_config["args"],
                [str(kit.repowise_bootstrap_path(paths)), "/usr/bin/repowise"],
            )
            self.assertEqual(
                kit.repowise_bootstrap_path(paths).read_text(),
                (ROOT / "assets" / "runtime" / "repowise_bootstrap.py").read_text(),
            )
            self.assertTrue(kit.uninstall_core(Namespace(purge=False), paths))
            self.assertTrue(kit.repowise_bootstrap_path(paths).is_file())
            self.assertEqual(config.read_text(), '[mcp_servers.other]\ncommand = "other"\n')
            with mock.patch.object(kit, "stage_upstream_skills", fake_stage):
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)
            self.assertTrue(kit.uninstall_core(Namespace(purge=True), paths))
            self.assertFalse(paths.install_root.exists())

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


class PlanHistoryHookTests(unittest.TestCase):
    def run_hook(self, event: dict, *, codex_home: Path | None = None):
        env = os.environ.copy()
        if codex_home is not None:
            env["CODEX_HOME"] = str(codex_home)
        return subprocess.run(
            [sys.executable, str(ROOT / "assets" / "hooks" / "session_start.py")],
            input=json.dumps(event),
            text=True,
            capture_output=True,
            check=True,
            env=env,
        )

    def stop_event(self, root: Path, message: str, turn: str = "turn-1") -> dict:
        return {
            "hook_event_name": "Stop",
            "permission_mode": "plan",
            "session_id": "session/unsafe",
            "turn_id": turn,
            "cwd": str(root),
            "last_assistant_message": message,
        }

    def test_plan_history_preserves_exact_bytes_and_event_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            GitFixture(root)
            spec = root / "docs" / "feature[1].md"
            spec.parent.mkdir()
            spec.write_text("# Feature\n", encoding="utf-8")
            message = (
                "<proposed_plan>\n# Café plan\n"
                "<!-- cpk-plan-spec: docs/feature[1].md -->\n"
                "</proposed_plan>"
            )
            event = self.stop_event(root, message)

            first = self.run_hook(event)
            retry = self.run_hook(event)
            records = [
                path
                for path in spec.parent.glob("*.plan-summary.*.md")
                if path.name.startswith("feature[1].plan-summary.")
            ]

            self.assertEqual(first.stdout, "{}\n")
            self.assertEqual(retry.stdout, "{}\n")
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].read_bytes(), message.encode("utf-8"))
            self.assertNotIn("/", records[0].name)

            changed = message.replace("Café", "Changed")
            collision = self.run_hook(self.stop_event(root, changed))
            records = [
                path
                for path in spec.parent.glob("*.plan-summary.*.md")
                if path.name.startswith("feature[1].plan-summary.")
            ]
            self.assertEqual(len(records), 2)
            self.assertIn("same event identity", json.loads(collision.stdout)["systemMessage"])
            self.assertEqual({path.read_bytes() for path in records}, {message.encode(), changed.encode()})

            with_newline = message + "\n"
            self.run_hook(self.stop_event(root, with_newline, "turn-2"))
            self.assertIn(
                with_newline.encode(),
                {
                    path.read_bytes()
                    for path in spec.parent.glob("*.plan-summary.*.md")
                    if path.name.startswith("feature[1].plan-summary.")
                },
            )

    def test_plan_history_processes_all_associations_and_fallbacks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            GitFixture(root)
            for name in ("one.md", "two.md"):
                (root / name).write_text(f"# {name}\n", encoding="utf-8")
            message = (
                "<proposed_plan>\n# Plan\n"
                "<!-- cpk-plan-spec: one.md -->\n"
                "<!-- cpk-plan-spec: two.md -->\n"
                "<!-- cpk-plan-spec: ../missing.md -->\n"
                "</proposed_plan>"
            )

            result = self.run_hook(self.stop_event(root, message))

            self.assertEqual(len(list(root.glob("one.plan-summary.*.md"))), 1)
            self.assertEqual(len(list(root.glob("two.plan-summary.*.md"))), 1)
            unlinked = list((root / ".agent" / "plan-history").glob("*.md"))
            self.assertEqual(len(unlinked), 1)
            self.assertEqual(unlinked[0].read_bytes(), message.encode())
            self.assertIn("../missing.md", json.loads(result.stdout)["systemMessage"])

            none = (
                "<proposed_plan>\n# No spec\n"
                "<!-- cpk-plan-spec: none -->\n"
                "</proposed_plan>"
            )
            self.assertEqual(
                self.run_hook(self.stop_event(root, none, "turn-2")).stdout, "{}\n"
            )
            self.assertEqual(len(list((root / ".agent" / "plan-history").glob("*.md"))), 2)

            missing = "<proposed_plan>\n# Missing marker\n</proposed_plan>"
            warning = self.run_hook(self.stop_event(root, missing, "turn-3"))
            self.assertIn("no cpk-plan-spec marker", json.loads(warning.stdout)["systemMessage"])
            self.assertEqual(len(list((root / ".agent" / "plan-history").glob("*.md"))), 3)

    def test_plan_history_ignores_nonfinal_or_nonplan_messages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            GitFixture(root)
            incomplete = self.stop_event(root, "I need one answer.")
            self.assertEqual(self.run_hook(incomplete).stdout, "{}\n")

            complete = self.stop_event(
                root,
                "<proposed_plan>\n<!-- cpk-plan-spec: none -->\n</proposed_plan>",
            )
            complete["permission_mode"] = "default"
            self.assertEqual(self.run_hook(complete).stdout, "{}\n")
            self.assertFalse((root / ".agent" / "plan-history").exists())

            absent = self.stop_event(root, "unused", "turn-2")
            absent.pop("last_assistant_message")
            warning = self.run_hook(absent)
            self.assertIn("did not provide", json.loads(warning.stdout)["systemMessage"])

    def test_plan_history_uses_global_storage_outside_git(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            cwd = base / "project"
            cwd.mkdir()
            codex_home = base / "codex"
            message = (
                "<proposed_plan>\n# Plan\n"
                "<!-- cpk-plan-spec: none -->\n"
                "</proposed_plan>"
            )

            result = self.run_hook(
                self.stop_event(cwd, message), codex_home=codex_home
            )

            self.assertEqual(result.stdout, "{}\n")
            records = list((codex_home / "plan-history").rglob("*.md"))
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].read_bytes(), message.encode())


class RoadmapViewHookTests(unittest.TestCase):
    def run_hook(self, event: dict):
        return subprocess.run(
            [sys.executable, str(ROOT / "assets" / "hooks" / "session_start.py")],
            input=json.dumps(event),
            text=True,
            capture_output=True,
            check=True,
        )

    def event(self, root: Path, phase: str, patch: str, tool_use: str = "tool-1") -> dict:
        return {
            "hook_event_name": phase,
            "session_id": str(root),
            "tool_use_id": tool_use,
            "cwd": str(root),
            "tool_name": "apply_patch",
            "tool_input": {"command": patch},
        }

    def apply_event(self, root: Path, patch: str, edit, tool_use: str = "tool-1"):
        pre = self.run_hook(self.event(root, "PreToolUse", patch, tool_use))
        edit()
        post = self.run_hook(self.event(root, "PostToolUse", patch, tool_use))
        return pre, post

    def test_linked_worktree_change_updates_primary_view(self):
        with tempfile.TemporaryDirectory() as temp:
            primary = Path(temp) / "primary"
            linked = Path(temp) / "linked"
            primary.mkdir()
            GitFixture(primary).commit("docs/roadmap.md", "primary\n")
            subprocess.run(
                ["git", "worktree", "add", "-q", "-b", "task", str(linked)],
                cwd=primary,
                check=True,
            )
            patch = (
                "*** Begin Patch\n"
                "*** Update File: nested/docs/roadmap.md\n"
                "*** Update File: ../linked/docs/roadmap.md\n"
                "*** End Patch"
            )

            pre, post = self.apply_event(
                primary,
                patch,
                lambda: (linked / "docs/roadmap.md").write_text(
                    "linked active\n", encoding="utf-8"
                ),
            )

            view = primary / ".codex/roadmap-view.md"
            self.assertEqual(pre.stdout, "")
            self.assertEqual(post.stdout, "")
            self.assertTrue(view.read_text().startswith(kit.ROADMAP_VIEW_MARKER + "\n"))
            self.assertIn("linked active\n", view.read_text())
            self.assertNotIn("primary\n", view.read_text())
            self.assertIn("/.codex/roadmap-view.md", (primary / ".git/info/exclude").read_text())
            status = subprocess.run(
                ["git", "status", "--short"],
                cwd=primary,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            self.assertNotIn("roadmap-view.md", status)
            self.assertEqual((primary / "docs/roadmap.md").read_text(), "primary\n")
            self.assertEqual((linked / "docs/roadmap.md").read_text(), "linked active\n")

    def test_add_file_creates_view_but_noop_and_unrelated_edits_do_not_refresh(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            GitFixture(root)
            patch = "*** Begin Patch\n*** Add File: docs/roadmap.md\n*** End Patch"

            malformed = self.event(root, "PreToolUse", patch, "malformed")
            malformed["tool_input"] = {}
            self.assertEqual(self.run_hook(malformed).stdout, "")
            self.assertFalse((root / ".codex/roadmap-view.md").exists())

            def add_roadmap():
                (root / "docs").mkdir()
                (root / "docs/roadmap.md").write_text("created\n", encoding="utf-8")

            self.apply_event(root, patch, add_roadmap)
            view = root / ".codex/roadmap-view.md"
            exclude = root / ".git/info/exclude"
            view_before = view.read_bytes()
            exclude_before = exclude.read_bytes()

            self.apply_event(root, patch.replace("Add", "Update"), lambda: None, "tool-2")
            unrelated = "*** Begin Patch\n*** Update File: docs/roadmap.md.bak\n*** End Patch"
            self.apply_event(
                root,
                unrelated,
                lambda: (root / "docs/roadmap.md").write_text("external\n", encoding="utf-8"),
                "tool-3",
            )

            self.assertEqual(view.read_bytes(), view_before)
            self.assertEqual(exclude.read_bytes(), exclude_before)

    def test_user_owned_view_is_preserved_and_remains_visible(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            GitFixture(root).commit("docs/roadmap.md", "before\n")
            view = root / ".codex/roadmap-view.md"
            view.parent.mkdir()
            view.write_text("user owned\n", encoding="utf-8")
            exclude = root / ".git/info/exclude"
            exclude_before = exclude.read_bytes()
            patch = "*** Begin Patch\n*** Update File: docs/roadmap.md\n*** End Patch"

            pre, post = self.apply_event(
                root,
                patch,
                lambda: (root / "docs/roadmap.md").write_text("after\n", encoding="utf-8"),
            )

            self.assertEqual(pre.stdout, "")
            self.assertIn("preserved user-owned file", json.loads(post.stdout)["systemMessage"])
            self.assertEqual(view.read_text(), "user owned\n")
            self.assertEqual(exclude.read_bytes(), exclude_before)
            status = subprocess.run(
                ["git", "status", "--short"],
                cwd=root,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            self.assertIn("?? .codex/", status)

    def test_user_owned_parent_file_is_preserved_before_exclusion(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            GitFixture(root).commit("docs/roadmap.md", "before\n")
            parent = root / ".codex"
            parent.write_text("user owned\n", encoding="utf-8")
            exclude = root / ".git/info/exclude"
            exclude_before = exclude.read_bytes()
            patch = "*** Begin Patch\n*** Update File: docs/roadmap.md\n*** End Patch"

            pre, post = self.apply_event(
                root,
                patch,
                lambda: (root / "docs/roadmap.md").write_text("after\n", encoding="utf-8"),
            )

            self.assertEqual(pre.stdout, "")
            self.assertIn("preserved user-owned path", json.loads(post.stdout)["systemMessage"])
            self.assertEqual(parent.read_text(), "user owned\n")
            self.assertEqual(exclude.read_bytes(), exclude_before)
            self.assertIn(
                "?? .codex",
                subprocess.run(
                    ["git", "status", "--short"],
                    cwd=root,
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout,
            )


@unittest.skipUnless(shutil.which("pwsh"), "PowerShell 7 is not installed")
class PowerShellLauncherTests(unittest.TestCase):
    def invoke(self, script: Path, *, exit_code: int = 0, fail_tests: bool = False):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source with spaces"
            root.mkdir()
            target = root / script.name
            target.write_text(script.read_text(), encoding="utf-8")
            log = Path(temp) / "args.json"
            if script.name == "run-tests.ps1":
                (root / "kit.py").write_text("", encoding="utf-8")
            else:
                (root / "kit.py").write_text(
                    "import json, os, sys\n"
                    "from pathlib import Path\n"
                    "Path(os.environ['CPK_LOG']).write_text(json.dumps(sys.argv[1:]))\n"
                    "raise SystemExit(int(os.environ['CPK_EXIT']))\n",
                    encoding="utf-8",
                )
            hooks = root / "assets" / "hooks"
            hooks.mkdir(parents=True)
            (hooks / "alpha.py").write_text("", encoding="utf-8")
            (hooks / "omega.py").write_text("", encoding="utf-8")
            runtime = root / "assets" / "runtime"
            runtime.mkdir()
            (runtime / "bootstrap.py").write_text("", encoding="utf-8")
            tests = root / "tests"
            tests.mkdir()
            if fail_tests:
                (tests / "test_failure.py").write_text(
                    "import unittest\n"
                    "class Failure(unittest.TestCase):\n"
                    "    def test_failure(self): self.fail('expected')\n",
                    encoding="utf-8",
                )
            else:
                (tests / "test_success.py").write_text(
                    "import unittest\n"
                    "class Success(unittest.TestCase):\n"
                    "    def test_success(self): self.assertTrue(True)\n",
                    encoding="utf-8",
                )
            env = os.environ.copy()
            env["CPK_LOG"] = str(log)
            env["CPK_EXIT"] = str(exit_code)
            if shutil.which("python") is None:
                command_dir = Path(temp) / "commands"
                command_dir.mkdir()
                (command_dir / "python").symlink_to(sys.executable)
                env["PATH"] = str(command_dir) + os.pathsep + env["PATH"]
            arguments = (
                []
                if script.name == "run-tests.ps1"
                else ["--label", "path with spaces"]
            )
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-File", str(target), *arguments],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            call = json.loads(log.read_text()) if log.exists() else None
            compiled = {
                str(path.relative_to(root))
                for path in (
                    root / "kit.py",
                    *sorted(hooks.glob("*.py")),
                    *sorted(runtime.glob("*.py")),
                )
                if any((path.parent / "__pycache__").glob(path.stem + ".*.pyc"))
            }
            return result, call, compiled

    def test_action_launchers_forward_arguments_and_exit_status(self):
        actions = {
            "install.ps1": "install",
            "uninstall.ps1": "uninstall",
            "setup-repo.ps1": "setup-repo",
            "doctor.ps1": "doctor",
        }
        for name, action in actions.items():
            with self.subTest(name=name):
                result, call, _ = self.invoke(ROOT / name, exit_code=9)
                self.assertEqual(result.returncode, 9)
                self.assertEqual(call, [action, "--label", "path with spaces"])

    def test_test_launcher_stops_after_failed_unit_phase(self):
        result, _, compiled = self.invoke(ROOT / "run-tests.ps1", fail_tests=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(compiled, set())

    def test_action_launcher_reports_missing_python(self):
        env = os.environ.copy()
        env["PATH"] = ""
        result = subprocess.run(
            [shutil.which("pwsh"), "-NoProfile", "-File", str(ROOT / "doctor.ps1")],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("python", result.stderr)

    def test_test_launcher_compiles_kit_and_every_hook(self):
        result, _, compiled = self.invoke(ROOT / "run-tests.ps1")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            compiled,
            {
                "kit.py",
                "assets/hooks/alpha.py",
                "assets/hooks/omega.py",
                "assets/runtime/bootstrap.py",
            },
        )


class RepoWiseRuntimeTests(unittest.TestCase):
    def paths(self, base: Path) -> kit.InstallPaths:
        return kit.InstallPaths(
            base / "home", base / "codex", base / "skills", base / "kit"
        )

    def test_watch_command_is_platform_specific(self):
        with tempfile.TemporaryDirectory() as temp:
            launcher = Path(temp) / "repowise"
            launcher.write_text(f"#!{sys.executable}\n")
            posix = bootstrap.watch_command(str(launcher), "linux")
            windows = bootstrap.watch_command(r"C:\Tools\repowise.exe", "win32")

        self.assertEqual(posix[:2], [sys.executable, "-c"])
        for event in ("opened", "closed", "closed_no_write"):
            self.assertIn(event, posix[2])
        self.assertEqual(windows, [r"C:\Tools\repowise.exe", "watch"])

    def test_windows_runtime_discovery_uses_executable_suffix(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(
            kit, "is_windows", return_value=True
        ), mock.patch.object(kit.shutil, "which", return_value=None) as which:
            paths = self.paths(Path(temp))
            command = paths.home / ".local" / "bin" / "uv.exe"
            command.parent.mkdir(parents=True)
            command.write_text("uv")
            self.assertEqual(kit.find_runtime_command(paths, "uv"), str(command))
            which.assert_called_once_with("uv.exe")

    def test_runtime_pins_match_lock_file(self):
        runtime = json.loads((ROOT / "upstream.lock.json").read_text())["runtime_tools"]
        self.assertEqual(runtime["uv"]["version"], kit.UV_VERSION)
        self.assertEqual(runtime["uv"]["installers"]["posix"]["url"], kit.UV_INSTALLER_URL)
        self.assertEqual(runtime["uv"]["installers"]["posix"]["sha256"], kit.UV_INSTALLER_SHA256)
        self.assertEqual(runtime["uv"]["installers"]["windows"]["url"], kit.UV_WINDOWS_INSTALLER_URL)
        self.assertEqual(runtime["uv"]["installers"]["windows"]["sha256"], kit.UV_WINDOWS_INSTALLER_SHA256)
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

    def test_missing_windows_uv_runs_verified_powershell_installer_once(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))

            def fake_run(command, **kwargs):
                self.assertEqual(
                    command,
                    [
                        "pwsh",
                        "-NoProfile",
                        "-NonInteractive",
                        "-ExecutionPolicy",
                        "Bypass",
                        "-Command",
                        "-",
                    ],
                )
                self.assertEqual(kwargs["input_text"], "installer")
                destination = Path(kwargs["env"]["UV_INSTALL_DIR"])
                destination.mkdir(parents=True)
                (destination / "uv.exe").write_text("uv")
                return subprocess.CompletedProcess(command, 0, "", "")

            with mock.patch.object(kit, "is_windows", return_value=True), mock.patch.object(
                kit, "find_runtime_command", return_value=None
            ), mock.patch.object(
                kit, "download_sha256", return_value=b"installer"
            ) as download, mock.patch.object(kit, "run", side_effect=fake_run) as run:
                uv = kit.ensure_uv(paths)
            self.assertEqual(uv, str(paths.home / ".local" / "bin" / "uv.exe"))
            download.assert_called_once_with(
                kit.UV_WINDOWS_INSTALLER_URL, kit.UV_WINDOWS_INSTALLER_SHA256
            )
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

    def test_missing_windows_repowise_uses_executable_result(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))

            def fake_run(command, **kwargs):
                if command[1:3] == ["tool", "install"]:
                    destination = Path(kwargs["env"]["UV_TOOL_BIN_DIR"])
                    destination.mkdir(parents=True)
                    (destination / "repowise.exe").write_text("repowise")
                return subprocess.CompletedProcess(command, 0, "", "")

            with mock.patch.object(kit, "is_windows", return_value=True), mock.patch.object(
                kit, "find_runtime_command", return_value=None
            ), mock.patch.object(kit, "run", side_effect=fake_run):
                repowise = kit.ensure_repowise(paths, r"C:\Tools\uv.exe")
            self.assertEqual(
                repowise, str(paths.home / ".local" / "bin" / "repowise.exe")
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

    class Watcher:
        def __init__(self, status=None):
            self.status = status
            self.terminated = False
            self.waited = False

        def poll(self):
            return self.status

        def terminate(self):
            self.terminated = True
            self.status = 0

        def wait(self):
            self.waited = True
            return self.status

    def test_bootstrap_initializes_once_and_always_installs_hook(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            calls = []
            watchers = []

            def setup(command, _cwd):
                calls.append(command)
                if command[1] == "init":
                    (root / ".repowise").mkdir()

            def popen(command, **_kwargs):
                calls.append(command)
                watcher = self.Watcher()
                watchers.append(watcher)
                return watcher

            def foreground(command, **_kwargs):
                calls.append(command)
                return subprocess.CompletedProcess(command, 0)

            with mock.patch.object(bootstrap, "git_root", return_value=root), mock.patch.object(
                bootstrap, "has_head", return_value=True
            ), mock.patch.object(bootstrap, "run_setup", side_effect=setup), mock.patch.object(
                bootstrap, "watch_command", return_value=["watcher"]
            ), mock.patch.object(bootstrap.subprocess, "Popen", side_effect=popen), mock.patch.object(
                bootstrap.subprocess, "run", side_effect=foreground
            ), mock.patch.object(bootstrap.time, "sleep"):
                self.assertEqual(bootstrap.bootstrap("repowise", root), 0)
                self.assertEqual(bootstrap.bootstrap("repowise", root), 0)

            self.assertEqual(sum(command[1] == "init" for command in calls if len(command) > 1), 1)
            self.assertEqual(sum(command[1:3] == ["hook", "install"] for command in calls), 2)
            self.assertEqual(sum(command[1] == "update" for command in calls if len(command) > 1), 2)
            self.assertEqual(sum(command[0] == "watcher" for command in calls), 2)
            self.assertEqual(sum(command[1] == "mcp" for command in calls if len(command) > 1), 2)
            self.assertTrue(all(item.terminated and item.waited for item in watchers))

    def test_bootstrap_initializes_only_empty_non_git_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            empty = base / "empty"
            empty.mkdir()
            calls = []

            def setup(command, _cwd):
                calls.append(command)
                if command[:3] == ["git", "init", "--quiet"]:
                    (empty / ".git").mkdir()
                if len(command) > 1 and command[1] == "init":
                    (empty / ".repowise").mkdir()

            watcher = self.Watcher()
            with mock.patch.object(
                bootstrap, "git_root", side_effect=[None, empty]
            ), mock.patch.object(bootstrap, "has_head", return_value=False), mock.patch.object(
                bootstrap, "run_setup", side_effect=setup
            ), mock.patch.object(bootstrap, "watch_command", return_value=["watcher"]), mock.patch.object(
                bootstrap.subprocess, "Popen", return_value=watcher
            ) as popen, mock.patch.object(
                bootstrap.subprocess,
                "run",
                side_effect=lambda command, **_kwargs: calls.append(command)
                or subprocess.CompletedProcess(command, 0),
            ), mock.patch.object(bootstrap.time, "sleep"):
                self.assertEqual(bootstrap.bootstrap("repowise", empty), 0)

            self.assertTrue((empty / ".git").is_dir())
            self.assertEqual(calls[0], ["git", "init", "--quiet"])
            self.assertTrue(any(len(command) > 1 and command[1] == "init" for command in calls))
            self.assertTrue(any(command[1:3] == ["hook", "install"] for command in calls))
            self.assertFalse(any(len(command) > 1 and command[1] == "update" for command in calls))
            popen.assert_called_once_with(
                ["watcher", "--index-only", "--no-workspace", str(empty)],
                cwd=empty,
                stdout=mock.ANY,
                stderr=subprocess.STDOUT,
            )
            self.assertIn(["repowise", "mcp", str(empty)], calls)
            self.assertTrue(watcher.terminated and watcher.waited)

            nonempty = base / "nonempty"
            nonempty.mkdir()
            (nonempty / ".keep").write_text("")
            with mock.patch.object(bootstrap, "git_root", return_value=None), mock.patch.object(
                bootstrap, "run_setup"
            ) as setup_mock, mock.patch.object(bootstrap.subprocess, "Popen") as popen, mock.patch.object(
                bootstrap.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0),
            ) as foreground:
                self.assertEqual(bootstrap.bootstrap("repowise", nonempty), 0)
            self.assertFalse((nonempty / ".git").exists())
            setup_mock.assert_not_called()
            popen.assert_not_called()
            foreground.assert_called_once_with(
                ["repowise", "mcp"], cwd=nonempty, check=False
            )

    def test_bootstrap_stops_when_watcher_fails_to_start(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".repowise").mkdir()
            watcher = self.Watcher(status=7)
            with mock.patch.object(bootstrap, "git_root", return_value=root), mock.patch.object(
                bootstrap, "has_head", return_value=False
            ), mock.patch.object(bootstrap, "run_setup"), mock.patch.object(
                bootstrap, "watch_command", return_value=["watcher"]
            ), mock.patch.object(bootstrap.subprocess, "Popen", return_value=watcher), mock.patch.object(
                bootstrap.subprocess, "run"
            ) as foreground, mock.patch.object(bootstrap.time, "sleep"):
                result = bootstrap.bootstrap("repowise", root)

            self.assertEqual(result, 7)
            self.assertTrue(watcher.waited)
            foreground.assert_not_called()

    def test_bootstrap_keeps_setup_diagnostics_off_mcp_stdout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".repowise").mkdir()
            watcher = self.Watcher()
            calls = []

            def run(command, **kwargs):
                calls.append((command, kwargs))
                return subprocess.CompletedProcess(command, 0)

            with mock.patch.object(bootstrap, "git_root", return_value=root), mock.patch.object(
                bootstrap, "has_head", return_value=False
            ), mock.patch.object(bootstrap, "watch_command", return_value=["watcher"]), mock.patch.object(
                bootstrap.subprocess, "Popen", return_value=watcher
            ), mock.patch.object(bootstrap.subprocess, "run", side_effect=run), mock.patch.object(
                bootstrap.time, "sleep"
            ):
                self.assertEqual(bootstrap.bootstrap("repowise", root), 0)

            hook_kwargs = next(kwargs for command, kwargs in calls if command[1] == "hook")
            mcp_kwargs = next(kwargs for command, kwargs in calls if command[1] == "mcp")
            self.assertIs(hook_kwargs["stdout"], sys.stderr)
            self.assertNotIn("stdout", mcp_kwargs)


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
            ):
                kit.setup_repo(Namespace(repo=str(root), prose=False), paths)
            self.assertIn("mcp_servers.other", (root / ".codex" / "config.toml").read_text())
            repo_config = tomllib.loads((root / ".codex" / "config.toml").read_text())
            self.assertEqual(
                repo_config["mcp_servers"]["repowise"]["args"],
                [str(kit.repowise_bootstrap_path(paths)), "/usr/bin/repowise"],
            )
            self.assertTrue(kit.repowise_bootstrap_path(paths).is_file())
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
                view = root / ".codex/roadmap-view.md"
                view.write_text(kit.ROADMAP_VIEW_MARKER + "\nowned\n", encoding="utf-8")
                exclude = root / ".git/info/exclude"
                exclude.write_text(
                    kit.ROADMAP_EXCLUDE_START
                    + "\n/.codex/roadmap-view.md\n"
                    + kit.ROADMAP_EXCLUDE_END
                    + "\n",
                    encoding="utf-8",
                )
                kit.remove_repo(Namespace(repo=str(root), delete_index=False), paths)
            self.assertEqual((root / "AGENTS.md").read_text(), "# Project rules\n")
            self.assertIn("enabled = false", (root / ".codex" / "config.toml").read_text())
            self.assertTrue(any(call[:2] == ("hook", "uninstall") for call in calls))
            self.assertFalse(view.exists())
            self.assertNotIn(kit.ROADMAP_EXCLUDE_START, kit.read_text(exclude))

    def test_remove_repo_preserves_user_owned_roadmap_view(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            GitFixture(root)
            view = root / ".codex/roadmap-view.md"
            view.parent.mkdir()
            view.write_text("user owned\n", encoding="utf-8")
            exclude = root / ".git/info/exclude"
            exclude.write_text(
                kit.ROADMAP_EXCLUDE_START
                + "\n/.codex/roadmap-view.md\n"
                + kit.ROADMAP_EXCLUDE_END
                + "\n",
                encoding="utf-8",
            )

            kit.remove_roadmap_view(root)

            self.assertEqual(view.read_text(), "user owned\n")
            self.assertNotIn(kit.ROADMAP_EXCLUDE_START, kit.read_text(exclude))
            self.assertIn(
                "?? .codex/",
                subprocess.run(
                    ["git", "status", "--short"],
                    cwd=root,
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout,
            )

    def test_roadmap_contract_and_router(self):
        rules = (ROOT / "assets" / "AGENTS.block.md").read_text()
        template = (
            ROOT / "assets" / "skills" / "roadmap-maintainer" / "assets" / "roadmap-template.md"
        ).read_text()
        self.assertIn("`roadmap-maintainer`", rules)
        self.assertEqual(template.count("## Active"), 1)
        self.assertIn("## Declined", template)
        owner = (ROOT / "assets/skills/roadmap-maintainer/SKILL.md").read_text()
        self.assertIn("Edit only `docs/roadmap.md`", owner)
        self.assertIn("generated human view, not as task state", owner)

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
            "scenario-discrimination",
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
            "plan-history",
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
                "scenario-discrimination.md",
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

    def test_preflight_challenges_the_coordinator_in_two_phases(self):
        root = ROOT / "assets" / "skills"
        preflight = (root / "design-preflight" / "SKILL.md").read_text()
        result = (
            root / "design-preflight" / "references" / "preflight-review.md"
        ).read_text()

        self.assertIn("same fresh read-only challenger", preflight)
        self.assertLess(preflight.index("Phase 1: independent"), preflight.index("Phase 2: adversarial"))
        self.assertIn("Do not give it the coordinator's card, decisions, assumptions, exclusions", preflight)
        self.assertIn("give the same challenger the coordinator's complete card", preflight)
        for target in (
            "missing scenarios",
            "unsupported assumptions",
            "invalid exclusions",
            "weak proof cases",
            "contract gaps",
        ):
            self.assertIn(target, preflight)
        self.assertIn("source-backed rationale for each rejected finding", preflight)
        self.assertIn("Stop on an unresolved contract gap", preflight)
        self.assertIn('"reviewer": "preflight-adversary"', result)
        for field in (
            '"kind"',
            '"source"',
            '"coordinator_claim"',
            '"counterexample"',
            '"wrong_terminal_result"',
            '"required_card_change"',
            '"supported_model"',
            '"coverage"',
        ):
            self.assertIn(field, result)
        self.assertIn("Empty `findings` is valid", result)

    def test_neuroarxiv_is_pinned_and_required_only_for_qualifying_research(self):
        lock = json.loads((ROOT / "upstream.lock.json").read_text())
        neuro = lock["skills"]["neuroarxiv"]
        research = (ROOT / "assets" / "skills" / "research-first" / "SKILL.md").read_text()
        agents = (ROOT / "assets" / "AGENTS.block.md").read_text()
        optional = (ROOT / "docs" / "OPTIONAL-REVIEW-TOOLS.md").read_text()

        self.assertIn("neuroarxiv", kit.UPSTREAM_SKILLS)
        self.assertEqual(neuro["commit"], "b5d20efa12dd1ba177ce890d56809d2e027f8055")
        self.assertEqual(neuro["license"], "MIT")
        self.assertEqual(
            {(item["destination"], item["git_blob_sha1"]) for item in neuro["files"]},
            {
                ("neuroarxiv/SKILL.md", "cc47304c76f7cb53aa4e8a324702dc8e4f1d5639"),
                ("neuroarxiv/LICENSE", "aaf95a45d3b11d68387ab0c3a0cee964a4ecd98c"),
            },
        )
        self.assertNotIn("adhd", lock["optional_tools"])
        self.assertNotIn("neuroarxiv", lock["optional_tools"])
        self.assertNotIn("adhd", kit.ALL_SKILLS)
        self.assertNotIn("adhd", kit.OBSOLETE_SKILLS)
        self.assertIn("architecture, algorithm, protocol, or systems mechanism", research)
        self.assertIn("costly-to-reverse", research)
        self.assertIn("published prior art can matter", research)
        self.assertIn("routine CRUD, glue code", research)
        self.assertIn("If a required real arXiv fetch cannot run, stop", research)
        self.assertIn("selected path, paper citations, and paper limitations", research)
        self.assertIn("`neuroarxiv` through `research-first`", agents)
        self.assertNotIn("## ADHD", optional)
        self.assertNotIn("## NeuroArxiv", optional)

    def test_coordination_limits_writers_but_not_read_only_agents(self):
        coordination = (
            ROOT
            / "assets"
            / "skills"
            / "delivery-lifecycle"
            / "references"
            / "coordination.md"
        ).read_text()

        self.assertIn("at most one write-capable implementation subagent", coordination)
        self.assertIn("Read-only research, planning, and review agents do not count", coordination)
        self.assertIn("platform makes available", coordination)
        self.assertIn("task-specific skill can impose a narrower limit", coordination)
        self.assertNotIn("at most one subagent at a time", coordination)

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
            "| Production path | Required oracle | Runnable test or command | Result |",
            card,
        )
        for field in ('"production_path"', '"required_oracle"', '"planned_check"'):
            self.assertIn(field, result)
        self.assertIn("accepted Scenario Proof mapping", packet)
        self.assertIn("aggregate suite result is supporting evidence only", packet)
        self.assertIn("required oracle in the named runnable check", lenses)

    def test_scenario_proof_requires_a_discriminating_case(self):
        root = ROOT / "assets" / "skills"
        owner = (
            root
            / "design-preflight"
            / "references"
            / "scenario-discrimination.md"
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

        self.assertIn("<!-- cpk-rule-owner: scenario-discrimination -->", owner)
        self.assertEqual(owner.count("<!-- cpk-rule-guard:"), 3)
        self.assertIn("scenario-discrimination.md", preflight)
        self.assertIn("scenario-discrimination.md", card)
        self.assertIn("scenario-discrimination.md", result)
        self.assertIn("scenario-discrimination.md", packet)
        self.assertIn("scenario-discrimination.md", lenses)
        self.assertIn('"discriminator"', result)
        self.assertIn('"contrast"', result)
        self.assertIn(
            "| Scenario | Discriminator | Contrast | Production path | Required oracle | Runnable test or command | Result |",
            card,
        )
        self.assertIn("complete the first six columns", card)
        self.assertIn("split a row when one contrast cannot prove all claimed outcomes", owner)
        self.assertIn("named requirement can be false while the check passes", owner)

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
        self.assertIn("`pwsh -File .\\install.ps1`", publication)
        self.assertIn("`pwsh -File .\\doctor.ps1`", publication)
        self.assertIn("from the reviewed candidate", publication)
        self.assertIn("`Result: ready`", publication)
        self.assertEqual(kit.KIT_VERSION, "0.19.0")
        self.assertNotIn("Version `0.19.0`", (ROOT / "README.md").read_text())
        self.assertNotIn("version 0.19.0", (ROOT / "CODEX-INSTALL-PROMPT.md").read_text())

    def test_windows_launchers_and_runtime_are_complete_distribution_artifacts(self):
        shell_paths = {path.relative_to(ROOT) for path in ROOT.rglob("*.sh")}
        powershell_paths = {path.relative_to(ROOT) for path in ROOT.rglob("*.ps1")}
        shell = {path.stem for path in shell_paths}
        powershell = {path.stem for path in powershell_paths}
        self.assertEqual(
            shell, {"install", "uninstall", "setup-repo", "doctor", "run-tests"}
        )
        self.assertEqual(powershell, shell)
        self.assertTrue(all(path.parent == Path(".") for path in shell_paths | powershell_paths))
        self.assertFalse(any(ROOT.rglob("*.bat")))
        self.assertFalse(any(ROOT.rglob("*.cmd")))

        records = {}
        for line in (ROOT / "MANIFEST.sha256").read_text().splitlines():
            digest, path = line.split("  ", 1)
            records.setdefault(path, []).append(digest)
        required = [
            *(f"./{name}.ps1" for name in sorted(powershell)),
            "./assets/runtime/repowise_bootstrap.py",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.assertEqual(len(records.get(relative, [])), 1)
                content = (ROOT / relative.removeprefix("./")).read_bytes()
                self.assertEqual(records[relative][0], hashlib.sha256(content).hexdigest())

    def test_plan_history_is_immutable_and_complete(self):
        skill = (ROOT / "assets" / "skills" / "plan-history" / "SKILL.md").read_text()
        agents = (ROOT / "assets" / "AGENTS.block.md").read_text()
        plans = (ROOT / ".agent" / "PLANS.md").read_text()
        isolation = (
            ROOT
            / "assets"
            / "skills"
            / "delivery-lifecycle"
            / "references"
            / "git-isolation.md"
        ).read_text()

        self.assertIn("plan-history", kit.CUSTOM_SKILLS)
        self.assertIn("cpk-rule-owner: plan-history", skill)
        self.assertIn("Read every file in `.agent/plan-history/`", skill)
        self.assertIn("Do not trust a RepoWise match limit", skill)
        self.assertIn("Do not continue with partial history", skill)
        self.assertIn("same event key and identical bytes", skill)
        self.assertIn("Retain and reconcile every distinct-content collision record", skill)
        self.assertIn("duplicate", skill.lower())
        self.assertIn("Prior plan reconciliation", skill)
        self.assertIn("Status: superseded", skill)
        self.assertIn("<!-- cpk-plan-spec: none -->", skill)
        self.assertIn("implements a plan after context was cleared", skill)
        self.assertIn("specification becomes known after capture", skill)
        self.assertIn("Never edit or remove a Plan history record", skill)
        self.assertIn("`plan-history`", agents)
        self.assertIn("Immutable Plan Mode summaries are source records", plans)
        self.assertIn("cpk-rule-route-only: plan-history", isolation)

    def test_repowise_is_required(self):
        config = kit.repowise_config_block(
            "/tmp/repowise", Path("/tmp/repowise_bootstrap.py")
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
        runtime = (ROOT / "assets" / "runtime" / "repowise_bootstrap.py").read_text()
        self.assertIn('"update",', runtime)
        self.assertIn('"watch"]', runtime)
        self.assertIn('"--index-only",', runtime)
        self.assertIn('"--no-workspace",', runtime)
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

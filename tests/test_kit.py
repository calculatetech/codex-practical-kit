import json
import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / "assets" / "hooks"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HOOKS))

import hook_common  # noqa: E402
import kit  # noqa: E402


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
            kit.repowise_config_block("/tmp/repowise"),
        )
        self.assertEqual(
            tomllib.loads(updated)["mcp_servers"]["repowise"]["args"][1],
            kit.repowise_bootstrap("/tmp/repowise"),
        )


class HookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.git = GitFixture(self.repo)
        self.git.commit("app.py", "print('one')\n")
        self.old_state = os.environ.get("XDG_STATE_HOME")
        os.environ["XDG_STATE_HOME"] = str(self.base / "state")

    def tearDown(self):
        if self.old_state is None:
            os.environ.pop("XDG_STATE_HOME", None)
        else:
            os.environ["XDG_STATE_HOME"] = self.old_state
        self.temp.cleanup()

    def payload(self, **extra):
        payload = {"session_id": "test", "cwd": str(self.repo), "hook_event_name": "Stop"}
        payload.update(extra)
        return payload

    def run_stop(self, **extra):
        result = subprocess.run(
            [sys.executable, str(HOOKS / "stop_gate.py")],
            input=json.dumps(self.payload(**extra)),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            env=os.environ.copy(),
        )
        return json.loads(result.stdout)

    def test_equal_status_allows_stop(self):
        hook_common.save_baseline(self.payload())
        self.assertEqual(self.run_stop(), {})

    def test_code_change_needs_both_current_markers(self):
        hook_common.save_baseline(self.payload())
        (self.repo / "app.py").write_text("print('two')\n", encoding="utf-8")
        self.assertEqual(self.run_stop().get("decision"), "block")
        message = "Review: clean — pass 1.\nDocs: no change needed — behavior is unchanged."
        self.assertEqual(self.run_stop(last_assistant_message=message), {})
        self.assertEqual(self.run_stop(), {})

    def test_docs_change_needs_docs_marker(self):
        hook_common.save_baseline(self.payload())
        (self.repo / "README.md").write_text("docs\n", encoding="utf-8")
        self.assertEqual(self.run_stop().get("decision"), "block")
        self.assertEqual(
            self.run_stop(last_assistant_message="Docs: updated README.md."), {}
        )

    def test_plan_mode_returns_without_advancing_status(self):
        hook_common.save_baseline(self.payload())
        (self.repo / "app.py").write_text("print('two')\n", encoding="utf-8")
        self.assertEqual(self.run_stop(permission_mode="plan"), {})
        self.assertEqual(self.run_stop().get("decision"), "block")

    def test_root_docs_uses_suffix_allowlist(self):
        hook_common.save_baseline(self.payload())
        (self.repo / "docs").mkdir()
        (self.repo / "docs" / "tool.py").write_text("print('x')\n", encoding="utf-8")
        self.assertIn("documentation-only", self.run_stop().get("reason", ""))
        self.assertFalse(hook_common.is_forbidden_docs_file("docs/image.png"))


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
            paths = self.paths(Path(temp))
            with mock.patch.object(kit, "stage_upstream_skills", fake_stage):
                kit.install_core(Namespace(repo=None, repowise_prose=False), paths)
            plans = paths.codex_home / "PLANS.md"
            self.assertEqual(plans.read_text(), (ROOT / ".agent" / "PLANS.md").read_text())
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
            self.assertIn('default_tools_approval_mode = "approve"', installed)
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
            GitFixture(root)
            log = Path(temp) / "calls"
            fake = Path(temp) / "repowise"
            fake.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$*\" >> \"$CALL_LOG\"\n"
                "if [ \"$1\" = init ]; then\n"
                "  for LAST do :; done\n"
                "  mkdir -p \"$LAST/.repowise\"\n"
                "fi\n"
            )
            fake.chmod(0o755)
            env = os.environ.copy()
            env["CALL_LOG"] = str(log)
            script = kit.repowise_bootstrap(str(fake))
            subprocess.run(["/bin/sh", "-c", script], cwd=root, env=env, check=True)
            subprocess.run(["/bin/sh", "-c", script], cwd=root, env=env, check=True)
            calls = log.read_text().splitlines()
            self.assertEqual(sum(line.startswith("init ") for line in calls), 1)
            self.assertEqual(sum(line.startswith("hook install ") for line in calls), 2)
            self.assertEqual(sum(line.startswith("mcp ") for line in calls), 2)


class IntegrationTests(unittest.TestCase):
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
            self.assertTrue(any(call[:2] == ("hook", "install") for call in calls))
            self.assertEqual((root / "docs" / "roadmap.md").read_text(), "sentinel\n")
            with mock.patch.object(kit, "repowise_command", fake_repowise), mock.patch.object(
                kit, "ensure_repowise_runtime", return_value=("/usr/bin/uv", "/usr/bin/repowise")
            ):
                kit.remove_repo(Namespace(repo=str(root), delete_index=False), paths)
            self.assertEqual((root / "AGENTS.md").read_text(), "# Project rules\n")
            self.assertIn("enabled = false", (root / ".codex" / "config.toml").read_text())
            self.assertTrue(any(call[:2] == ("hook", "uninstall") for call in calls))

    def test_roadmap_contract_and_propagation(self):
        rules = (ROOT / "assets" / "AGENTS.block.md").read_text()
        template = (
            ROOT / "assets" / "skills" / "roadmap-maintainer" / "assets" / "roadmap-template.md"
        ).read_text()
        self.assertIn("Activate its task before the first implementation edit", rules)
        self.assertEqual(template.count("## Active"), 1)
        self.assertIn("## Declined", template)

    def test_execplan_is_the_only_durable_task_model(self):
        rules = (ROOT / "assets" / "AGENTS.block.md").read_text()
        preflight = (ROOT / "assets" / "skills" / "design-preflight" / "SKILL.md").read_text()
        self.assertIn("$CODEX_HOME/PLANS.md", rules)
        self.assertNotIn("task-brief", rules.lower())
        self.assertNotIn("Task Brief", preflight)
        self.assertNotIn("task-brief", kit.ALL_SKILLS)

    def test_git_isolation_policy_is_consistent(self):
        rules = (ROOT / "assets" / "AGENTS.block.md").read_text()
        session = (ROOT / "assets" / "hooks" / "session_start.py").read_text()
        plans = (ROOT / ".agent" / "PLANS.md").read_text()
        manual = (ROOT / "docs" / "OPERATING-MANUAL.md").read_text()

        self.assertIn("On `main`, allow only bounded documentation", rules)
        self.assertIn("Use a task branch for one writable implementation stream.", rules)
        self.assertNotIn("Use a task branch for one writable stream.", rules)
        self.assertIn("Use a worktree for independent writable streams", rules)
        self.assertIn("If tracked changes have mixed ownership, stop.", rules)
        self.assertIn("Do not stash, commit, discard, or change them.", rules)
        self.assertIn("coherent local checkpoint commits", rules)
        self.assertIn("When PR mode is off, require separate authorization", rules)
        self.assertIn("Cleanup always needs separate authorization.", rules)

        self.assertIn("Use a task branch for one writable implementation stream.", session)
        self.assertIn("Use a worktree for independent writable streams", session)

        self.assertIn("base branch, base commit, task branch, and isolation form", plans)
        self.assertIn("cumulative diff from the recorded base commit", plans)
        self.assertIn("When PR mode is off, require separate authorization", manual)
        self.assertIn("Cleanup always needs separate authorization.", manual)

    def test_version_policy_is_consistent(self):
        rules = (ROOT / "assets" / "AGENTS.block.md").read_text()
        session = (ROOT / "assets" / "hooks" / "session_start.py").read_text()
        plans = (ROOT / ".agent" / "PLANS.md").read_text()
        manual = (ROOT / "docs" / "OPERATING-MANUAL.md").read_text()
        readme = (ROOT / "README.md").read_text()
        prompt = (ROOT / "CODEX-INSTALL-PROMPT.md").read_text()

        self.assertEqual(kit.KIT_VERSION, "0.9.0")
        self.assertIn(f"Version `{kit.KIT_VERSION}`", readme)
        self.assertIn(f"version {kit.KIT_VERSION} or newer", prompt)

        shared = [
            "Start initial development at `0.1.0`.",
            "Use `0.MINOR.PATCH` during initial development.",
            "increment the minor number for a feature or breaking change",
            "Increment the patch number for a bug fix or a published checkpoint in the same feature line.",
            "After `1.0.0`, increment the major number for a breaking change",
            "Do not use alpha or beta suffixes by default.",
            "Publish a normal `0.x` version as a full GitHub release.",
            "Use source version `X.Y.Z` and Git tag `vX.Y.Z`.",
            "A version is consumed when its tag reaches GitHub.",
            "If publication fails before the remote tag exists",
            "If publication fails after the remote tag exists",
        ]
        for owner in [rules, manual]:
            with self.subTest(owner=owner[:30]):
                for statement in shared:
                    self.assertIn(statement, owner)

        self.assertIn("Start initial development at `0.1.0`.", readme)
        self.assertIn("Local checkpoint commits do not change the version.", session)
        self.assertIn("select the target after scope is fixed", plans)

    def test_pr_publication_policy_is_consistent(self):
        rules = (ROOT / "assets" / "AGENTS.block.md").read_text()
        session = (ROOT / "assets" / "hooks" / "session_start.py").read_text()
        plans = (ROOT / ".agent" / "PLANS.md").read_text()
        manual = (ROOT / "docs" / "OPERATING-MANUAL.md").read_text()

        shared = [
            "PR mode is active only when `main` protection requires pull requests, required CI checks, and resolved conversations.",
            "CI must contain at least one workflow.",
            "Its workflows must supply every required check.",
            "If any condition is false, PR mode is off.",
            "When PR mode is active, use a pull request for every change, including bounded documentation.",
            "Each push resets the required CI and Codex review gates.",
            "Squash-merge the pull request after all gates pass.",
            "Cleanup always needs separate authorization.",
        ]
        for owner in [rules, manual]:
            with self.subTest(owner=owner[:30]):
                for statement in shared:
                    self.assertIn(statement, owner)

        self.assertIn("one explicit `publish` request authorizes", plans)
        self.assertIn("a Codex thumbs-up reaction for the latest head", plans)
        self.assertIn("Each push resets the required CI and Codex review gates.", plans)
        self.assertIn("`publish` authorizes the path through squash merge", session)
        self.assertIn("Each push resets the gates.", session)

    def test_material_decision_handoff_policy_is_consistent(self):
        rules = (ROOT / "assets" / "AGENTS.block.md").read_text()
        session = (ROOT / "assets" / "hooks" / "session_start.py").read_text()
        manual = (ROOT / "docs" / "OPERATING-MANUAL.md").read_text()

        shared = [
            "A material decision changes scope, architecture, authority, exposure, or the delivered result.",
            "Before you request direction on a material decision, investigate discoverable facts and exclude unsupported conditions.",
            "Do not use the full handoff for discoverable facts, routine values, status questions, or minor preferences.",
            "Use these labels in order: `Decision`, `Term` when needed, `Trigger`, `Likelihood`, `Current exposure`, `Options`, `Recommendation`, and `Question`.",
            "Do not invent numeric probabilities.",
            "Each option must state its effect.",
            "If no real choice exists, state the required action instead of requesting direction.",
        ]
        for owner in [rules, manual]:
            with self.subTest(owner=owner[:30]):
                for statement in shared:
                    self.assertIn(statement, owner)

        labels = [
            "`Decision`",
            "`Term`",
            "`Trigger`",
            "`Likelihood`",
            "`Current exposure`",
            "`Options`",
            "`Recommendation`",
            "`Question`",
        ]
        order_line = next(line for line in rules.splitlines() if "Use these labels" in line)
        positions = [order_line.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Material decisions use `Decision`", session)
        self.assertIn("Skip the full handoff for routine inputs.", session)

    def test_review_closure_policy_is_consistent(self):
        owners = [
            ROOT / ".agent" / "PLANS.md",
            ROOT / "assets" / "AGENTS.block.md",
            ROOT / "assets" / "skills" / "adversarial-review" / "SKILL.md",
            ROOT / "assets" / "skills" / "docs-maintainer" / "SKILL.md",
            ROOT / "assets" / "skills" / "roadmap-maintainer" / "SKILL.md",
        ]
        required = [
            "Review closure does not invalidate a clean review.",
            "Review closure is limited to five updates: the task ExecPlan review result, reviewed task roadmap transition, publication status, matching checksums, and untracked test-result record.",
            "A change to code, tests, dependencies, migrations, runtime configuration, build configuration, security configuration, behavior requirements, or the supported model invalidates review.",
        ]
        for owner in owners:
            text = owner.read_text()
            with self.subTest(owner=owner):
                for statement in required:
                    self.assertIn(statement, text)
                self.assertNotIn("If any candidate file changes", text)


if __name__ == "__main__":
    unittest.main()

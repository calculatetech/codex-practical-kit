import json
import os
import subprocess
import sys
import tempfile
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
            (paths.install_root / "install-manifest.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "codex_home": str(paths.codex_home),
                        "skills_home": str(paths.skills_home),
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
            self.assertFalse((paths.install_root / "install-manifest.json").exists())
            self.assertFalse(kit.uninstall_core(Namespace(purge=False), other))

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
            for name in kit.ALL_SKILLS:
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
            self.assertFalse((paths.install_root / "skills").exists())
            manifest = json.loads((paths.install_root / "install-manifest.json").read_text())
            self.assertEqual(manifest["skills"], [{"name": name} for name in kit.ALL_SKILLS])

    def test_absent_uninstall_is_no_op(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = self.paths(Path(temp))
            self.assertFalse(kit.uninstall_core(Namespace(purge=True), paths))


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

            def fake_repowise(repo: Path, *args: str, timeout: int = 1800):
                (repo / ".repowise").mkdir(exist_ok=True)
                return subprocess.CompletedProcess([], 0, "", "")

            with mock.patch.object(kit, "repowise_command", fake_repowise), mock.patch.object(
                kit.shutil, "which", return_value="/usr/bin/uvx"
            ):
                kit.setup_repo(Namespace(repo=str(root), prose=False))
            self.assertIn("mcp_servers.other", (root / ".codex" / "config.toml").read_text())
            self.assertEqual((root / "docs" / "roadmap.md").read_text(), "sentinel\n")
            kit.remove_repo(Namespace(repo=str(root), delete_index=False))
            self.assertEqual((root / "AGENTS.md").read_text(), "# Project rules\n")

    def test_roadmap_contract_and_propagation(self):
        rules = (ROOT / "assets" / "AGENTS.block.md").read_text()
        template = (
            ROOT / "assets" / "skills" / "roadmap-maintainer" / "assets" / "roadmap-template.md"
        ).read_text()
        self.assertIn("Activate its task before the first implementation edit", rules)
        self.assertEqual(template.count("## Active"), 1)
        self.assertIn("## Declined", template)


if __name__ == "__main__":
    unittest.main()

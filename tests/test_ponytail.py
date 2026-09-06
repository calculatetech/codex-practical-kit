"""Native plugin commands are the external seam; toolkit installation runs intact."""

import contextlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from unittest import mock

import kit


class PonytailIntegrationTests(unittest.TestCase):
    SOURCE = "https://github.com/DietrichGebert/ponytail.git"
    SKILLS = ("ponytail", "ponytail-audit", "ponytail-debt", "ponytail-gain", "ponytail-help", "ponytail-review")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.paths = kit.InstallPaths(self.root / "home", self.root / "selected", self.root / "skills", self.root / "kit")
        self.calls = []
        self.missing = None
        self.real_run = subprocess.run
        for patch in (
            mock.patch.object(kit.subprocess, "run", side_effect=self.native_run),
            mock.patch.object(kit, "download_file", return_value=b"# upstream fixture\n"),
            mock.patch.object(kit, "ensure_repowise_runtime", return_value=("fake-uv", "fake-repowise")),
            mock.patch.object(kit, "find_runtime_command", side_effect=lambda paths, name: "fake-" + name),
            mock.patch.dict(os.environ, {"CODEX_HOME": str(self.root / "default")}),
        ):
            patch.start()
            self.addCleanup(patch.stop)

    def state_path(self, home=None):
        return (home or self.paths.codex_home) / "plugins" / "native-fixture.json"

    def state(self, home=None):
        path = self.state_path(home)
        return json.loads(path.read_text()) if path.exists() else {"marketplaces": [], "installed": []}

    def write_state(self, state, home=None):
        kit.write_file(self.state_path(home), json.dumps(state, sort_keys=True))

    def seed_plugin(self, *, enabled=True, source=None, home=None):
        source = source or self.SOURCE
        marketplace_source = {"sourceType": "git", "source": source}
        plugin = {
            "name": "ponytail", "pluginId": "ponytail@ponytail", "installed": True,
            "version": "user-version", "enabled": enabled,
            "source": {"source": "git", "url": source, "ref": "user-ref"},
            "marketplaceSource": marketplace_source,
        }
        self.write_state({"marketplaces": [{"name": "ponytail", "marketplaceSource": marketplace_source}], "installed": [plugin]}, home)
        home = home or self.paths.codex_home
        config = home / "config.toml"
        text = re.sub(r'(?m)^\[plugins\."ponytail@ponytail"\]\nenabled = (?:true|false)\n', '', kit.read_text(config))
        kit.write_file(config, text + '\n[plugins."ponytail@ponytail"]\nenabled = ' + str(enabled).lower() + '\n')
        kit.write_file(home / "plugins/data/ponytail-ponytail/.ponytail-active", "ultra")
        kit.write_file(self.paths.home / ".config/ponytail/config.json", '{"defaultMode":"off"}')

    def native_run(self, command, **kwargs):
        if command[0] not in ("node", "codex", "fake-repowise"):
            return self.real_run(command, **kwargs)
        env = kwargs.get("env") or os.environ
        home = Path(env["CODEX_HOME"])
        self.calls.append((command, home))
        if command[0] == "node":
            if self.missing == "node":
                raise FileNotFoundError("node")
            return subprocess.CompletedProcess(command, 0, "v22.0.0\n", "")
        if command[0] == "fake-repowise":
            return subprocess.CompletedProcess(command, 0, "RepoWise " + kit.REPOWISE_VERSION, "")
        if command[1] != "plugin":
            return subprocess.CompletedProcess(command, 0, "codex-cli test" if command[1] == "--version" else "Logged in", "")
        if self.missing == "plugins":
            return subprocess.CompletedProcess(command, 2, "", "unrecognized subcommand 'plugin'")
        if not home.is_dir():
            return subprocess.CompletedProcess(command, 1, "", "CODEX_HOME does not exist")
        args = command[2:]
        state = self.state(home)
        if args == ["marketplace", "list", "--json"]:
            output = {"marketplaces": state["marketplaces"]}
        elif args == ["list", "--marketplace", "ponytail", "--json"]:
            output = {"installed": state["installed"], "available": []}
        elif args == ["marketplace", "add", "DietrichGebert/ponytail", "--json"]:
            state["marketplaces"].append({"name": "ponytail", "marketplaceSource": {"sourceType": "git", "source": self.SOURCE}})
            self.write_state(state, home)
            output = {"added": True}
        elif args == ["add", "ponytail@ponytail", "--json"]:
            if self.missing == "install":
                return subprocess.CompletedProcess(command, 1, "", "native plugin installation failed")
            self.seed_plugin(home=home)
            installed = self.state(home)
            installed["marketplaces"] = state["marketplaces"]
            self.write_state(installed, home)
            for skill in self.SKILLS:
                kit.write_file(home / "plugins/cache/ponytail/skills" / skill / "SKILL.md", "native package fixture")
            kit.write_file(home / "plugins/cache/ponytail/hooks.json", json.dumps({"hooks": {name: [] for name in ("SessionStart", "UserPromptSubmit", "SubagentStart")}}))
            output = {"installed": True}
        else:
            self.fail(f"Unexpected native mutation or command: {command}")
        return subprocess.CompletedProcess(command, 0, json.dumps(output), "")

    def cli(self, command, *extra, paths=None):
        paths = paths or self.paths
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = kit.main([command, "--home", str(paths.home), "--codex-home", str(paths.codex_home), "--skills-home", str(paths.skills_home), "--install-root", str(paths.install_root), *extra])
        return result, output.getvalue()

    def snapshot(self, root=None):
        root = root or self.root
        return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}

    def mutations(self):
        return [command for command, _ in self.calls if command[:2] == ["codex", "plugin"] and "add" in command]

    def legacy(self, owned=True):
        kit.write_file(self.paths.skills_home / "ponytail/SKILL.md", "legacy Ponytail")
        if owned:
            manifest = {"schema_version": 1, "skills_home": str(self.paths.skills_home), "codex_home": str(self.paths.codex_home), "skills": [{"name": "ponytail"}]}
            kit.write_file(kit.manifest_path(self.paths), json.dumps(manifest))
        kit.write_file(self.paths.codex_home / "config.toml", "# user configuration\n")
        kit.write_file(self.paths.install_root / "hooks/session_start.py", "# old hook\n")

    def test_fresh_install_registers_complete_plugin(self):
        self.assertFalse(self.paths.codex_home.exists())
        result, output = self.cli("install")
        self.assertEqual(result, 0, output)
        self.assertIn("`/hooks` to review and trust toolkit and Ponytail hooks", output)
        self.assertEqual(len(self.mutations()), 2)
        package = self.paths.codex_home / "plugins/cache/ponytail"
        self.assertEqual(sorted(p.parent.name for p in package.glob("skills/*/SKILL.md")), sorted(self.SKILLS))
        self.assertEqual(set(json.loads((package / "hooks.json").read_text())["hooks"]), {"SessionStart", "UserPromptSubmit", "SubagentStart"})
        self.assertFalse((self.paths.skills_home / "ponytail").exists())
        manifest = json.loads(kit.manifest_path(self.paths).read_text())
        self.assertNotIn("ponytail", [item["name"] for item in manifest["skills"]])
        config = (self.paths.codex_home / "config.toml").read_text()
        self.assertNotIn("trusted", config)
        self.assertEqual(self.cli("doctor")[0], 0)

    def test_legacy_skill_migration_requires_recorded_ownership(self):
        self.legacy(owned=False)
        before = self.snapshot()
        result, output = self.cli("install")
        self.assertEqual(result, 2)
        self.assertIn("not owned", output)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.mutations(), [])
        self.legacy(owned=True)
        manifest = json.loads(kit.manifest_path(self.paths).read_text())
        manifest["skills_home"] = str(self.root / "previous-skills")
        kit.write_file(kit.manifest_path(self.paths), json.dumps(manifest))
        before = self.snapshot()
        self.assertEqual(self.cli("install")[0], 2)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.mutations(), [])
        self.legacy(owned=True)
        before = self.snapshot()
        self.missing = "install"
        result, output = self.cli("install")
        self.assertEqual(result, 2)
        self.assertIn("native plugin installation failed", output)
        after = self.snapshot()
        self.assertEqual({name: after[name] for name in before}, before)
        self.missing = None
        self.assertEqual(self.cli("install")[0], 0)
        self.assertTrue(self.state()["installed"])
        self.assertFalse((self.paths.skills_home / "ponytail").exists())

    def test_existing_official_plugin_is_reused(self):
        kit.write_file(self.paths.codex_home / "config.toml", '# unrelated user configuration\n')
        self.assertEqual(self.cli("install")[0], 0)
        self.assertEqual(len(self.mutations()), 2)
        self.calls.clear()
        for enabled in (True, False):
            with self.subTest(enabled=enabled):
                self.seed_plugin(enabled=enabled)
                before = self.snapshot(self.paths.codex_home / "plugins")
                settings = (self.paths.home / ".config/ponytail/config.json").read_bytes()
                self.assertEqual(self.cli("install")[0], 0)
                self.assertEqual(self.snapshot(self.paths.codex_home / "plugins"), before)
                self.assertEqual((self.paths.home / ".config/ponytail/config.json").read_bytes(), settings)
                self.assertIn("enabled = " + str(enabled).lower(), (self.paths.codex_home / "config.toml").read_text())
                self.assertIn('# unrelated user configuration', (self.paths.codex_home / "config.toml").read_text())
                result, output = self.cli("doctor")
                self.assertEqual(result, 0, output)
                self.assertIn("enabled" if enabled else "disabled by user", output)
                self.assertEqual(self.mutations(), [])

    def test_native_plugin_survives_reinstall_and_uninstall(self):
        for existing in (False, True):
            for purge in (False, True):
                with self.subTest(existing=existing, purge=purge):
                    paths = kit.InstallPaths(self.root / f"home-{existing}-{purge}", self.root / f"codex-{existing}-{purge}", self.root / f"skills-{existing}-{purge}", self.root / f"kit-{existing}-{purge}")
                    if existing:
                        self.seed_plugin(home=paths.codex_home, enabled=False)
                    self.assertEqual(self.cli("install", paths=paths)[0], 0)
                    before = self.snapshot(paths.codex_home / "plugins")
                    settings = (self.paths.home / ".config/ponytail/config.json").read_bytes()
                    self.assertEqual(self.cli("install", paths=paths)[0], 0)
                    self.assertEqual(self.cli("uninstall", *(["--purge"] if purge else []), paths=paths)[0], 0)
                    self.assertEqual(self.snapshot(paths.codex_home / "plugins"), before)
                    self.assertEqual((self.paths.home / ".config/ponytail/config.json").read_bytes(), settings)
                    self.assertIn('[plugins."ponytail@ponytail"]', (paths.codex_home / "config.toml").read_text())
                    self.assertIn('enabled = ' + str(not existing).lower(), (paths.codex_home / "config.toml").read_text())

    def test_plugin_commands_use_selected_codex_home(self):
        default = self.root / "default"
        self.seed_plugin(home=default, enabled=False, source="https://github.com/other/ponytail.git")
        before = self.snapshot(default)
        self.assertEqual(self.cli("install")[0], 0)
        self.assertEqual(self.cli("doctor")[0], 0)
        native_calls = [home for command, home in self.calls if command[:2] == ["codex", "plugin"]]
        self.assertTrue(native_calls)
        self.assertEqual(set(native_calls), {self.paths.codex_home})
        self.assertEqual([home for command, home in self.calls if command == ["codex", "login", "status"]], [self.paths.codex_home])
        count = len(native_calls)
        other = kit.InstallPaths(self.paths.home, default, self.root / "other-skills", self.paths.install_root)
        self.assertEqual(self.cli("uninstall", "--purge", paths=other)[0], 0)
        self.assertEqual(len([1 for command, _ in self.calls if command[:2] == ["codex", "plugin"]]), count)
        self.assertEqual(self.snapshot(default), before)
        self.assertFalse((self.paths.skills_home / "simple-english").exists())
        self.assertTrue(self.state()["installed"])

    def test_doctor_requires_native_plugin_and_node(self):
        self.assertEqual(self.cli("install")[0], 0)
        installed = self.state()
        for missing in ("plugin", "node"):
            with self.subTest(missing=missing):
                if missing == "plugin":
                    self.write_state({**installed, "installed": []})
                    kit.write_file(self.paths.skills_home / "ponytail/SKILL.md", "legacy only")
                else:
                    self.write_state(installed)
                    self.missing = "node"
                result, output = self.cli("doctor")
                self.assertEqual(result, 1)
                self.assertIn("not installed" if missing == "plugin" else "requires Node.js", output)
        self.missing = None
        self.assertEqual(self.cli("doctor")[0], 0)

    def test_missing_prerequisites_preserve_existing_installation(self):
        self.legacy()
        before = self.snapshot()
        for missing in ("node", "plugins"):
            with self.subTest(missing=missing):
                self.missing = missing
                result, output = self.cli("install")
                self.assertEqual(result, 2)
                self.assertIn("Node.js" if missing == "node" else "native Codex plugin commands", output)
                self.assertEqual(self.snapshot(), before)
                self.assertEqual(self.mutations(), [])
        self.missing = None
        self.assertEqual(self.cli("install")[0], 0)
        self.assertFalse((self.paths.skills_home / "ponytail").exists())

    def test_foreign_marketplace_is_preserved(self):
        for foreign_package in (False, True):
            with self.subTest(foreign_package=foreign_package):
                base = self.root / str(foreign_package)
                self.paths = kit.InstallPaths(base / "home", base / "codex", base / "skills", base / "kit")
                self.legacy()
                self.seed_plugin()
                state = self.state()
                # Native catalogs can contain unrelated entries before Ponytail.
                state["marketplaces"].insert(0, {"name": "openai-curated", "root": "unrelated"})
                if foreign_package:
                    source = state["installed"][0]["source"]
                    source["url"] = "https://github.com/other/ponytail.git"
                else:
                    state["installed"] = []
                    source = state["marketplaces"][1]["marketplaceSource"]
                    source["source"] = "https://github.com/other/ponytail.git"
                self.write_state(state)
                before = self.snapshot()
                self.calls.clear()
                result, output = self.cli("install")
                self.assertEqual(result, 2)
                self.assertIn("conflicts with the official", output)
                self.assertEqual(self.snapshot(), before)
                self.assertEqual(self.mutations(), [])
                source["url" if foreign_package else "source"] = self.SOURCE
                self.write_state(state)
                self.assertEqual(self.cli("install")[0], 0)
                self.assertFalse((self.paths.skills_home / "ponytail").exists())
                self.assertEqual(self.state()["marketplaces"], state["marketplaces"])


if __name__ == "__main__":
    unittest.main()

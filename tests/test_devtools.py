import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/wechat-miniprogram-zero-to-trial/scripts/devtools.py'
spec = importlib.util.spec_from_file_location('devtools', SCRIPT)
devtools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(devtools)


class DevtoolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / '中文 project with spaces'
        self.project.mkdir()
        (self.project / 'project.config.json').write_text(json.dumps({
            'appid': 'wx0000000000000000', 'projectname': 'test', 'miniprogramRoot': 'mini',
        }))
        mini = self.project / 'mini'
        mini.mkdir()
        (mini / 'app.js').write_text('App({})')
        (mini / 'app.json').write_text('{"pages":["pages/index/index"]}')
        self.cli = self.root / 'fake cli'
        self.cli.write_text('#!/bin/sh\nexit 0\n')
        self.cli.chmod(0o700)
        self.args = ['--project', str(self.project), '--cli', str(self.cli), '--output', str(self.root / 'out')]

    def test_inspect_has_no_external_side_effect(self):
        with patch.object(devtools.subprocess, 'run') as run:
            self.assertEqual(devtools.main(['inspect', '--project', str(self.project)]), 0)
            run.assert_not_called()

    def test_upload_preserves_spaces_and_literal_shell_characters(self):
        desc = 'test $(touch unwanted) `id`; 中文'
        with patch.object(devtools.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as run:
            self.assertEqual(devtools.main(['upload'] + self.args + ['--version', '0.1.0', '--desc', desc]), 0)
            cmd = run.call_args.args[0]
            self.assertEqual(cmd[cmd.index('--project') + 1], str(self.project.resolve()))
            self.assertEqual(cmd[cmd.index('--desc') + 1], desc)
            self.assertNotIn('shell', run.call_args.kwargs)

    def test_cli_failure_is_returned_without_retry(self):
        with patch.object(devtools.subprocess, 'run', return_value=subprocess.CompletedProcess([], 7)) as run:
            self.assertEqual(devtools.main(['upload'] + self.args + ['--version', '0.1.0']), 7)
            self.assertEqual(run.call_count, 1)

    def test_old_qr_cannot_hide_missing_new_result(self):
        parent = self.root / 'out'
        parent.mkdir()
        (parent / 'preview.jpg').write_bytes(b'old')
        with patch.object(devtools.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)):
            self.assertEqual(devtools.main(['preview'] + self.args), 2)

    def test_preview_uses_unique_output_directory(self):
        dirs = []
        def produce(cmd, **kwargs):
            qr = Path(cmd[cmd.index('--qr-output') + 1])
            qr.write_bytes(b'fake-image')
            dirs.append(qr.parent)
            return subprocess.CompletedProcess(cmd, 0)
        with patch.object(devtools.subprocess, 'run', side_effect=produce):
            self.assertEqual(devtools.main(['preview'] + self.args), 0)
            self.assertEqual(devtools.main(['preview'] + self.args), 0)
        self.assertNotEqual(dirs[0], dirs[1])

    def test_missing_version_blocks_before_execution(self):
        with patch.object(devtools.subprocess, 'run') as run:
            self.assertEqual(devtools.main(['upload'] + self.args), 2)
            run.assert_not_called()

    def test_root_escape_is_rejected(self):
        path = self.project / 'project.config.json'
        config = json.loads(path.read_text())
        config['miniprogramRoot'] = '../outside'
        path.write_text(json.dumps(config))
        with self.assertRaisesRegex(ValueError, '工程外'):
            devtools.inspect_project(self.project)


if __name__ == '__main__':
    unittest.main()

"""Regression: TeX's include auxiliary directories must exist before compilation."""
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

API = runpy.run_path(str(Path(__file__).with_name('build-tex')))


class IncludeBuildTests(unittest.TestCase):
    def test_nested_aux_directory_exists_before_compiler(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'book.tex'
            source.write_text('\\include{chapters/one/chapter}\n% \\include{unused/chapter}\n')
            output = Path(tmp) / 'output'
            def compiler(*args, **kwargs):
                self.assertTrue((output / 'chapters/one').is_dir())
                self.assertFalse((output / 'unused').exists())
                return type('Result', (), {'returncode': 0})()
            with patch('subprocess.run', side_effect=compiler):
                self.assertEqual(API['compile_pdf'](source, output), 0)

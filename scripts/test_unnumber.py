"""Regression tests for recursive, document-wide equation unnumbering."""
import runpy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('lint-tex').resolve()
ROOT = SCRIPT.parent.parent
API = runpy.run_path(str(SCRIPT))


class UnnumberTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='unnumber test ')
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, source):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
        return path

    def run_unnumber(self, root):
        return subprocess.run([sys.executable, str(SCRIPT), '--unnumber', str(root)],
                              cwd=ROOT, capture_output=True, text=True)

    def test_document_wide_sibling_references_and_nested_path_resolution(self):
        root = self.write('main.tex', r'''\input{nested/chapter}
\input{chapters/references}
''')
        nested = self.write('nested/chapter.tex', r'''\input{fragments/shared}
\input{only-local}
''')
        source_relative_decoy = self.write('nested/fragments/shared.tex', r'''
\begin{equation}
\label{eq:wrong-source-relative}
x=99
\end{equation}
''')
        shared = self.write('fragments/shared.tex', r'''
\begin{equation}
\label{eq:shared}
x=1
\end{equation}
\begin{equation}
\label{eq:hyper}
x=2
\end{equation}
\begin{equation}
\label{eq:range-a}
x=3
\end{equation}
\begin{equation}
\label{eq:range-b}
x=4
\end{equation}
\begin{equation}
\label{eq:unused}
x=5
\end{equation}
''')
        local_only = self.write('nested/only-local.tex', r'''
\begin{equation}
\label{eq:local-only}
x=6
\end{equation}
''')
        references = self.write('chapters/references.tex', r'''
\cref[nameinlink]{eq:shared} and \hyperref[eq:hyper]{the linked identity}.
\crefrange[capitalize]{eq:range-a}{eq:range-b}.
''')

        run = self.run_unnumber(root)

        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn('2 uncited displays unnumbered across 5 input files', run.stderr)
        for path, label in ((shared, 'eq:shared'), (shared, 'eq:hyper'),
                            (shared, 'eq:range-a'), (shared, 'eq:range-b')):
            self.assertIn(r'\label{' + label + '}', path.read_text())
            self.assertIn(r'\begin{equation}', path.read_text())
        self.assertIn(r'\begin{equation*}', shared.read_text())
        self.assertNotIn(r'\label{eq:unused}', shared.read_text())
        self.assertIn(r'\label{eq:wrong-source-relative}', source_relative_decoy.read_text())
        self.assertIn(r'\begin{equation}', source_relative_decoy.read_text())
        self.assertIn(r'\begin{equation*}', local_only.read_text())
        self.assertNotIn(r'\label{eq:local-only}', local_only.read_text())
        self.assertTrue(references.exists())
        self.assertTrue(nested.exists())

        before = {path: path.read_text() for path in (shared, source_relative_decoy,
                                                       local_only, references)}
        second = self.run_unnumber(root)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual({path: path.read_text() for path in before}, before)
        self.assertIn('0 uncited displays unnumbered', second.stderr)

    def test_cycles_visit_each_resolved_file_once(self):
        root = self.write('main.tex', r'\input{parts/one}' + '\n')
        one = self.write('parts/one.tex', r'\input{parts/two}' + '\n')
        two = self.write('parts/two.tex', r'\input{main}' + '\n')
        files = {}

        API['document_text'](root, files)

        self.assertEqual(set(files), {root.resolve(), one.resolve(), two.resolve()})

    def test_tagged_and_partly_cited_displays_are_reported_and_preserved(self):
        path = self.write('manual.tex', r'''\begin{equation}
\label{eq:tagged}
x=1 \tag{A}
\end{equation}
\begin{align}
x&=1\label{eq:cited}\\
y&=2\label{eq:uncited}
\end{align}
By \cref{eq:cited}.
''')
        source = path.read_text()
        reports = []

        result, count = API['unnumber'](path, source, reports=reports)

        self.assertEqual(count, 0)
        self.assertEqual(result, source)
        self.assertTrue(any('explicit \\tag' in item for item in reports), reports)
        self.assertTrue(any('partly cited align' in item for item in reports), reports)

    def test_hyperref_labels_are_citations(self):
        path = self.write('hyper.tex', r'''\begin{equation}
\label{eq:target}
x=1
\end{equation}
See \hyperref[eq:target]{the displayed identity}.
''')

        result, count = API['unnumber'](path, path.read_text())

        self.assertEqual(count, 0)
        self.assertIn(r'\label{eq:target}', result)

    def test_local_reference_wrappers_are_citations(self):
        self.assertIn('eq:space-item', API['cited_labels'](r'\spaceitem{eq:space-item}'))

    def test_label_removal_does_not_leave_blank_paragraph_in_display(self):
        path = self.write('blank-line.tex', r'''\begin{equation}
\label{eq:unused}

x=1
\end{equation}
''')

        result, count = API['unnumber'](path, path.read_text(), set())

        self.assertEqual(count, 1)
        display = result.split(r'\begin{equation*}', 1)[1].split(r'\end{equation*}', 1)[0]
        self.assertNotRegex(display, r'\n[ \t]*\n')
        self.assertIn('x=1', display)
        self.assertNotIn(r'\label{eq:unused}', result)


if __name__ == '__main__':
    unittest.main()

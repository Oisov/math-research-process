"""Run with: python -m unittest discover -s scripts -p 'test_*.py'."""
import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HARVEST = ROOT / 'tools' / 'arxiv_harvest.py'
PAPER = r"""\documentclass{amsart}
\usepackage{thmtools}
\declaretheorem[name=Question]{qst}
\newtheorem{conj}{Conjecture}
\begin{document}
\begin{qst}\label{q:one} Is every extremal outer?\end{qst}
\begin{conj} The constant is $\pi$.\end{conj}
\end{document}
"""


class HarvestTests(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.d)

    def run_harvest(self, *paths):
        return subprocess.run([sys.executable, str(HARVEST), '--local', *map(str, paths),
                               '--out', str(self.d / 'out')], capture_output=True, text=True)

    def test_local_directory_and_declaretheorem(self):
        src = self.d / 'mypaper'
        src.mkdir()
        (src / 'main.tex').write_text(PAPER)
        run = self.run_harvest(src)
        self.assertEqual(run.returncode, 0, run.stderr)
        rows = [json.loads(l) for l in (self.d / 'out' / 'mypaper' / 'candidates.jsonl').read_text().splitlines()]
        names = {r.get('name') for r in rows if r['kind'] == 'environment'}
        self.assertEqual(names, {'Question', 'Conjecture'})

    def test_missing_local_path_fails(self):
        run = self.run_harvest(self.d / 'nope')
        self.assertEqual(run.returncode, 1)
        self.assertIn('no such file or directory', run.stderr)


if __name__ == '__main__':
    unittest.main()

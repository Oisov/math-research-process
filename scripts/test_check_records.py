"""Run with: python -m unittest discover -s scripts -p 'test_*.py'."""
import shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / 'tools' / 'check_records.py'
TEMPLATE = (ROOT / 'templates' / 'record.md').read_text()


class CheckRecordsTests(unittest.TestCase):
    def run_on(self, text, name='AB-9.2', theme='hardy-spaces'):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d)
        (d / theme).mkdir()
        (d / theme / f'{name}.md').write_text(text)
        return subprocess.run([sys.executable, str(CHECK), str(d)], capture_output=True, text=True)

    def test_template_is_valid(self):
        run = self.run_on(TEMPLATE)
        self.assertEqual(run.returncode, 0, run.stdout)

    def test_id_must_match_file(self):
        run = self.run_on(TEMPLATE, name='XY-1')
        self.assertEqual(run.returncode, 1)
        self.assertIn('does not match file name', run.stdout)

    def test_public_external_needs_told_authors(self):
        text = (TEMPLATE.replace('stage: untriaged', 'stage: public')
                .replace('review: null', 'review: {by: agent, model: m, date: 2026-10-14, verdict: ok}')
                .replace('public: null', 'public: papers/x.pdf'))
        run = self.run_on(text)
        self.assertEqual(run.returncode, 1)
        self.assertIn('told_authors', run.stdout)

    def test_partial_cannot_have_tier(self):
        text = (TEMPLATE.replace('stage: untriaged', 'stage: reviewed')
                .replace('review: null', 'review: {by: agent, model: m, date: 2026-10-14, verdict: ok}')
                .replace('result_scope: null', 'result_scope: partial')
                .replace('resolution: null', 'resolution: {tier: ours-internal, ref: x, checked: true}'))
        run = self.run_on(text)
        self.assertIn('partial result cannot carry', run.stdout)

    REVIEW = 'review: {by: agent, model: m, date: 2026-10-14, verdict: ok}'

    def test_reviewer_counterexample_is_rejected(self):
        # The record a reviewer built on 14 Oct 2026: it passed with no errors.
        text = (TEMPLATE.replace('stage: untriaged', 'stage: reviewed')
                .replace('review: null', 'review: true')
                .replace('resolution: null', 'resolution: {tier: ours-public, ref: x, checked: false}')
                .replace('tags: []', 'tags: []\nsurprise: 1'))
        run = self.run_on(text)
        self.assertEqual(run.returncode, 1, run.stdout)
        for message in ('needs ours.review with', 'needs result_scope full',
                        'needs resolution.checked: true', 'needs ours.public',
                        "unknown field 'surprise'"):
            self.assertIn(message, run.stdout)

    def test_full_reviewed_internal_result_is_valid(self):
        text = (TEMPLATE.replace('stage: untriaged', 'stage: reviewed')
                .replace('review: null', self.REVIEW)
                .replace('result_scope: null', 'result_scope: full')
                .replace('resolution: null', 'resolution: {tier: ours-internal, ref: x, checked: true}'))
        run = self.run_on(text)
        self.assertEqual(run.returncode, 0, run.stdout)

    def test_contested_cannot_have_tier(self):
        text = (TEMPLATE.replace('stage: untriaged', 'stage: contested')
                .replace('resolution: null', 'resolution: {tier: ours-internal, ref: x, checked: true}'))
        run = self.run_on(text)
        self.assertIn('contested result cannot carry', run.stdout)

    def test_public_field_needs_public_stage(self):
        text = TEMPLATE.replace('stage: untriaged', 'stage: triaged').replace('public: null', 'public: papers/x.pdf')
        run = self.run_on(text)
        self.assertIn('ours.public is set but stage is triaged', run.stdout)

    def test_missing_or_empty_directory_fails(self):
        missing = subprocess.run([sys.executable, str(CHECK), '/nonexistent-records'], capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d)
        empty = subprocess.run([sys.executable, str(CHECK), str(d)], capture_output=True, text=True)
        self.assertEqual(empty.returncode, 2)
        self.assertIn('no records found', empty.stdout)


if __name__ == '__main__':
    unittest.main()

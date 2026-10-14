"""Run with: python -m unittest discover -s scripts -p 'test_tex_lint.py'."""
import os
from pathlib import Path
import os
import runpy
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('lint-tex')
API = runpy.run_path(str(SCRIPT))
format_tex = API['format_tex']
house_warnings = API['house_warnings']
wrap_line = API['wrap_line']
false_positive = API['false_positive']
ROOT = SCRIPT.resolve().parent.parent


class TexLintTests(unittest.TestCase):
    def test_requested_layout_and_idempotence(self):
        source = 'Before \\(x\\).\n\\[\nx=y\n\\]\nAfter.\n'
        expected = ('Before $x$.\n%\n\\begin{equation*}\n'
                    '  x=y\n\\end{equation*}\n%\nAfter.\n')
        self.assertEqual(format_tex(source), expected)
        self.assertEqual(format_tex(expected), expected)

    def test_numbering_labels_and_paragraphs_are_preserved(self):
        source = '\n\\begin{equation}\\label{eq:a}\nx=1\n\\end{equation}\n\nNext.\n'
        result = format_tex(source)
        self.assertIn(r'\begin{equation}', result)
        self.assertIn(r'\label{eq:a}', result)
        self.assertNotIn('equation*', result)
        self.assertIn('\\end{equation}\n%\n\nNext.', result)
        self.assertEqual(format_tex(result), result)

    def test_protected_material_survives_byte_for_byte(self):
        examples = [
            '% example \\[x\\] and \\(y\\)  ',
            '\\begin{verbatim}\n  \\[x\\]   \n\\end{verbatim}',
            '\\begin{minted}{tex}\n\\(x\\)\n\\end{minted}',
            r'\verb|\[not math\]|',
            r'\lstinline!\(not math\)!',
            r'\mintinline{tex}{\[not math\]}',
            r'\newcommand{\demo}[1]{\[#1\]}',
            r'\newcommand \demo[1]{\[#1\]}',
            r'\def\demo#1{\[#1\]}',
            '% lint-tex: off\n\\catcode`$=12\n\\[unchanged\\]\n% lint-tex: on',
        ]
        for example in examples:
            with self.subTest(example=example):
                formatted = format_tex(example + '\n\\(real\\)\n')
                self.assertIn(example, formatted)
                self.assertIn('$real$', formatted)
                self.assertEqual(format_tex(formatted), formatted)

    def test_escaped_backslash_is_not_a_math_delimiter(self):
        result = format_tex('Text \\\\[2pt] and \\(x\\), with \\% and \\$5.\n')
        self.assertIn(r'\\[2pt]', result)
        self.assertIn(r'\% and \$5', result)
        self.assertIn('$x$', result)

    def test_adjacent_displays_do_not_duplicate_separators(self):
        result = format_tex('\\[a\\]\n\\[b\\]\n')
        self.assertNotIn('%\n%\n', result)
        self.assertEqual(format_tex(result), result)

    def test_preserve_comment_attached_to_math(self):
        result = format_tex('\\[\na% do not introduce a space here\nb\n\\]\n')
        self.assertIn('a% do not introduce a space here\n', result)

    def test_unsafe_inputs_are_rejected(self):
        for source in (r'\[x\)', r'\(x', '% lint-tex: off\n',
                       r'\catcode`$=12', r'\begin{verbatim}oops',
                       r'\documentclass{article}\begin{document}\[x\]\end{document}'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                format_tex(source)

    def test_cli_check_is_read_only_and_fix_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'with spaces.tex'
            path.write_text('\\[x\\]\n')
            command = [sys.executable, str(SCRIPT), '--format-only']
            first = subprocess.run(command + [str(path)], capture_output=True)
            self.assertEqual(first.returncode, 1)
            self.assertEqual(path.read_text(), '\\[x\\]\n')
            fixed = subprocess.run(command + ['--fix', str(path)], capture_output=True)
            self.assertEqual(fixed.returncode, 0, fixed.stderr)
            checked = subprocess.run(command + [str(path)], capture_output=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            path.write_text('\\[broken\n')
            bad = subprocess.run(command + ['--fix', str(path)], capture_output=True)
            self.assertEqual(bad.returncode, 2)
            self.assertEqual(path.read_text(), '\\[broken\n')

    def test_make_build_requires_lint_even_in_parallel(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / 'paper with spaces.tex'
            marker = folder / 'compiler-called'
            compiler = folder / 'latexmk'
            compiler.write_text('#!/bin/sh\nprintf called > "$COMPILER_MARKER"\n')
            compiler.chmod(0o755)
            env = dict(os.environ, PATH=tmp + os.pathsep + os.environ['PATH'],
                       COMPILER_MARKER=str(marker))
            command = ['make', '-j4', 'build', 'TEX=' + str(source)]
            source.write_text('\\documentclass{article}\n\\begin{document}\nHello \\(x\\).\n\\end{document}\n')
            failed = subprocess.run(command, cwd=SCRIPT.parent.parent, env=env, capture_output=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertFalse(marker.exists(), failed.stdout)
            source.write_text(format_tex(source.read_text()))
            passed = subprocess.run(command, cwd=SCRIPT.parent.parent, env=env, capture_output=True)
            self.assertEqual(passed.returncode, 0, passed.stderr)
            self.assertTrue(marker.exists())

    def test_label_stays_on_display_begin_line(self):
        source = '\\begin{equation}\\label{eq:a}\nx=1\n\\end{equation}\n'
        result = format_tex(source)
        self.assertIn('\\begin{equation}\\label{eq:a}\n  x=1\n', result)
        self.assertEqual(format_tex(result), result)

    def test_prose_environments_stay_flush_left(self):
        source = '\\begin{lemma}\nText.\n\\end{lemma}\n\\begin{proof}\nMore.\n\\end{proof}\n'
        self.assertEqual(format_tex(source), source)

    def test_house_rules(self):
        def messages(text):
            return [message for _, message in house_warnings(text)]
        self.assertTrue(any('inline \\frac' in m for m in messages('Here $\\frac12$ is inline.\n')))
        self.assertTrue(any('inline \\frac' in m for m in messages('Here \\(\\frac12\\) too.\n')))
        self.assertFalse(any('frac' in m for m in messages('\\begin{equation*}\n\\frac12\n\\end{equation*}\n')))
        self.assertFalse(any('frac' in m for m in messages('Costs \\$5 and \\$6, $a/b$.\n')))
        self.assertTrue(any('\\tfrac' in m for m in messages('\\begin{equation*}\\tfrac12\\end{equation*}\n')))
        self.assertTrue(any('biggl' in m for m in messages('$\\Biggl(x\\Biggr)$\n')))
        self.assertFalse(any('biggl' in m for m in messages('$\\biggl(x\\biggr)$\n')))
        self.assertFalse(messages('% $\\frac12$ in a comment\n'))

    def test_paragraphs_are_refilled_like_vim_gq(self):
        words = ' '.join(['word'] * 40)
        result = format_tex('Short\nlines are\njoined.\n\n' + words + '\n', width=30)
        self.assertIn('Short lines are joined.\n', result)
        lines = result.splitlines()
        self.assertTrue(all(len(line) <= 30 for line in lines))
        # Greedy: no line could have taken the next line's first word.
        for a, b in zip(lines[2:], lines[3:]):
            self.assertGreater(len(a) + 1 + len(b.split()[0]), 30)
        self.assertEqual(format_tex(result, width=30), result)

    def test_refill_leaves_structure_alone(self):
        source = ('\\documentclass{amsart}\n\\usepackage{amsmath} \\usepackage{mathtools}\n'
                  '\\begin{document}\n'
                  'One two\nthree.\n%\n\\begin{equation}\n  x=1\n\\end{equation}\n%\nAfter the\ndisplay.\n'
                  'Kept % a comment\nalone.\n'
                  '\\begin{itemize}\n\\item first\n  continued\n\\end{itemize}\n'
                  '\\section{A\nheading}\n'
                  'A \\verb|x  y| and cf.\\ the end.\n'
                  '\\end{document}\n')
        result = format_tex(source, width=79)
        self.assertIn('\\usepackage{amsmath} \\usepackage{mathtools}\n', result)  # preamble untouched
        self.assertIn('One two three.\n%\n', result)
        self.assertIn('After the display.\n', result)
        self.assertIn('Kept % a comment\nalone.\n', result)
        self.assertRegex(result, r'\\item first\n *continued\n')  # lists are not refilled
        self.assertIn('heading}\nA \\verb', result)  # a heading's second line stays its own
        self.assertIn('\\verb|x  y|', result)
        self.assertEqual(format_tex(result, width=79), result)

    def test_amsrefs_bibliography_is_not_refilled(self):
        source = ('\\documentclass{amsart}\n\\begin{document}\nText.\n'
                  '\\begin{bibdiv}\n\\begin{biblist}\n\n'
                  '\\bib{BS}{article}{\n  author={Brevig, O. F.},\n  author={Saksman, E.},\n'
                  '  title={Coefficient estimates},\n  date={2020},\n}\n\n'
                  '\\end{biblist}\n\\end{bibdiv}\n\\end{document}\n')
        result = format_tex(source, width=79)
        self.assertIn('\\bib{BS}{article}{\n  author={Brevig, O. F.},\n  author={Saksman, E.},\n', result)
        self.assertEqual(format_tex(result, width=79), result)

    def test_control_space_is_never_split(self):
        result = format_tex('aaaa cf.\\ bbbb\n', width=8)
        self.assertIn('cf.\\ bbbb', result)

    def test_width_zero_disables_refill(self):
        self.assertEqual(format_tex('a\nb\n', width=0), 'a\nb\n')

    def test_long_display_lines_break_before_relations(self):
        line = '  R(x)=' + 'a+' * 20 + 'b=' + 'c+' * 15 + 'd'
        out = wrap_line(line, 40)
        self.assertEqual(out[0], '  R(x)')
        self.assertTrue(out[1].startswith('  =a+'))
        self.assertTrue(any(l.startswith('  =c+') for l in out))
        self.assertEqual(''.join(l.strip() for l in out), line.strip())   # only whitespace changes

    def test_display_breaks_respect_grouping(self):
        line = '  (q-1)\\int\\bigl(a-b+c-d+e-f+g-h+i-j\\bigr)^2\\frac{x-y}{z-w}+\\left(u-v\\right)+k'
        for piece in wrap_line(line, 30):
            self.assertEqual(piece.count('\\bigl'), piece.count('\\bigr'))
            self.assertEqual(piece.count('('), piece.count(')'))
            self.assertEqual(piece.count('{'), piece.count('}'))

    def test_display_lists_split_between_equations_and_no_stubs(self):
        out = wrap_line('  G=g+q\\varepsilon h=(I+q\\varepsilon)h,\\qquad H=h+\\varepsilon g=(1+\\varepsilon I)h,\\qquad F=GH^q .', 60)
        self.assertTrue(out[1].lstrip().startswith('\\qquad H=h'))
        out = wrap_line('  \\qquad\\text{if }\\varphi\\in H^\\infty\\text{ and }\\langle\\varphi,|h|^2\\rangle=0 .', 60)
        self.assertFalse(any(l.strip() in ('=0 .', '0 .') for l in out))

    def test_row_break_is_kept_at_the_end(self):
        out = wrap_line('    &=' + 'a+' * 30 + 'b\\\\', 40)
        self.assertTrue(out[-1].endswith('\\\\'))
        self.assertEqual(sum(l.count('\\\\') for l in out), 1)

    def test_display_wrapping_is_idempotent_and_skips_comments(self):
        source = ('\\begin{equation}\n  R=' + 'a+' * 45 + 'b\n\\end{equation}\n'
                  '\\begin{equation}\n  S=' + 'c+' * 45 + 'd % keep\n\\end{equation}\n')
        result = format_tex(source)
        self.assertTrue(all(len(l) <= 79 for l in result.splitlines()[:6]))
        self.assertIn('d % keep', result)
        self.assertEqual(format_tex(result), result)

    def test_matrix_columns_are_right_aligned(self):
        source = ('\\begin{equation}\n\\begin{pmatrix}\n1 & -12 \\\\\n-3&4\\\\\n100 & 5\n'
                  '\\end{pmatrix}\n\\end{equation}\n')
        result = format_tex(source)
        self.assertIn('      1 & -12 \\\\\n     -3 &   4 \\\\\n    100 &   5\n', result)
        self.assertEqual(format_tex(result), result)

    def test_named_rules_and_their_scopes(self):
        def rules(text):
            return [message.split(':')[0] for _, message in house_warnings(text)]
        cases = [
            ('A {\\bf bold} word.\n', 'old-font', True),
            ('An \\item here.\n', 'old-font', False),
            ('$x\\over y$\n', 'tex-fraction', True),
            ('Wait... here.\n', 'ellipsis', True),
            ('He said "no".\n', 'straight-quote', True),
            ('H\\"older.\n', 'straight-quote', False),
            ('$f:=g$\n', 'coloneq', True),
            ('$a<<b$\n', 'much-less', True),
            ('$\\left(x\\right)$\n', 'inline-left', True),
            ('\\begin{equation}\n\\left(x\\right)\n\\end{equation}\n', 'inline-left', False),
            ('$\\mbox{if } x$\n', 'mbox-math', True),
            ('$\\displaystyle\\sum x$\n', 'inline-display', True),
            ('See \\cite{a}, \\cite{b}.\n', 'double-cite', True),
            ('By Theorem~3 we win.\n', 'manual-number', True),
            ('By \\cite[Theorem~3]{a} we win.\n', 'manual-number', False),
            ('By Theorem 3 of \\cite{a} we win.\n', 'manual-number', False),
            ('By Lemma A we win.\n', 'manual-number', True),
            ('By Theorem II we win.\n', 'manual-number', True),
            ('By Thm. 3 and Prop.~2.\n', 'manual-number', True),
            ('See Fig. 1 and Eq. (5).\n', 'manual-number', True),
            ('By (3.1) we win.\n', 'manual-number', True),
            ('See \u00a72 for this.\n', 'manual-number', True),
            ('by lemma 3 we win.\n', 'manual-number', True),
            ('Lemmas 3--5 give it.\n', 'manual-number', True),
            ('In Step 3 we win.\n', 'manual-number', False),
            ('A Lemma I proved.\n', 'manual-number', False),
            ('a section 2-dimensional.\n', 'manual-number', False),
            ('value $(3.1)$ here.\n', 'manual-number', False),
            ('First line\\\\\nsecond.\n', 'prose-break', True),
            ('\\title{A\\\\B}\n', 'prose-break', False),
            ('\\begin{align*}a\\\\b\\end{align*}\n', 'prose-break', False),
            ('\\usepackage{a4wide,amsmath}\n', 'obsolete-package', True),
            ('\\begin{figure}\\label{f}\\caption{c}\\end{figure}\n', 'label-before-caption', True),
            ('\\begin{figure}\\caption{c}\\label{f}\\end{figure}\n', 'label-before-caption', False),
            ('$\\epsilon$ and $\\varepsilon$ and $\\varepsilon$\n', 'mixed-symbol', True),
            ('\\vspace{-2pt}\n', 'negative-space', True),
            ('$\\Biggl($\n', 'bigg', True),
            ('{\\bf x} % lint-tex: ignore=old-font\n', 'old-font', False),
            ('$x\\in[0,1)$\n', 'half-open', True),
            ('$x\\in(0,1]$\n', 'half-open', True),
            ('$x\\in[0,1]$ and $(0,1)$\n', 'half-open', False),
            ('$x\\in\\lbrack0,1\\rparen$\n', 'half-open', True),
            ('$x\\in\\intco{0}{1}$\n', 'half-open', False),
            ('as in~%\n\\cite{a}.\n', 'tie-comment', True),
            ('as in~\\cite{a}.\n', 'tie-comment', False),
            ('\\section{Proof of \\cref{a}}\n', 'cref-heading', True),
            ('\\section{Proof of \\texorpdfstring{\\cref{a}}{Theorem \\ref{a}}}\n', 'cref-heading', False),
            ('\\section{Proof of \\texorpdfstring{\\cref{a}}{Theorem \\ref{a}}}\n', 'ref', False),
        ]
        for text, rule, expected in cases:
            with self.subTest(text=text, rule=rule):
                self.assertEqual(rule in rules(text), expected)

    def test_chktex_false_positive_filter(self):
        lines = ['Take $f^{(k)}(0)/k!$ here.',            # 40 at col 19: factorial, filtered
                 'By Cauchy--Schwarz, and x -- y. Also a--b.',
                 'Bad $x,$ here. And $k!$ then $y.$ ok, $k! x$.',
                 "Riesz--Thorin, Fej\\'er--Riesz, \\L{}ojasiewicz--Simon, A---B."]
        filtered = lambda line, col, n: false_positive(f'f:{line}:{col}: ChkTeX {n}: m', lines)
        self.assertTrue(filtered(1, 19, 40))
        self.assertTrue(filtered(3, 22, 40))      # $k!$
        self.assertFalse(filtered(3, 7, 40))      # $x,$ is a real finding
        self.assertFalse(filtered(3, 32, 40))     # $y.$ is a real finding
        self.assertFalse(filtered(3, 43, 40))     # ! not at the end of the math
        self.assertFalse(filtered(1, 18, 40))     # wrong column: not the reported token
        self.assertTrue(filtered(2, 10, 8))       # Cauchy--Schwarz
        self.assertFalse(filtered(2, 27, 8))      # x -- y
        self.assertFalse(filtered(2, 39, 8))      # a--b, although a name pair is on the line
        # Columns from ChkTeX itself on this line: 6, 23 and 46; it does not flag A---B.
        self.assertTrue(filtered(4, 6, 8))        # Riesz--Thorin
        self.assertTrue(filtered(4, 23, 8))       # Fej\'er--Riesz
        self.assertTrue(filtered(4, 46, 8))       # \L{}ojasiewicz--Simon
        self.assertFalse(filtered(4, 56, 8))
        more = ['Then $x\\in H^2$, \\eqref{a} gives', 'By \\eqref{a} we win',
                'a contradiction. \\qed', 'x. y', '\\section{On \\texorpdfstring{$f(0)$}{f(0)}}']
        other = lambda line, col, n: false_positive(f'f:{line}:{col}: ChkTeX {n}: m', more)
        self.assertTrue(other(1, 17, 2))      # after a comma: no tie needed (ChkTeX column)
        self.assertFalse(other(2, 3, 2))      # after a word: real
        self.assertTrue(other(3, 17, 12))     # before \\qed
        self.assertFalse(other(4, 3, 12))     # ordinary sentence space: real
        self.assertTrue(other(5, 38, 36))     # inside the bookmark argument (ChkTeX column)
        self.assertFalse(other(5, 31, 36))    # inside the typeset argument: real      # A---B is an em dash, not a name pair

    def test_findings_exit_1_and_clean_file_exits_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'note.tex'
            path.write_text('Text with $x,$ inside.\n')
            run = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 1, run.stderr)
            self.assertIn('ChkTeX 40', run.stderr)
            path.write_text('Clean text with $x$.\n')
            run = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)

    def test_summary_over_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'a.tex').write_text('\\documentclass{amsart}\n\\begin{document}\nOk.\n\\end{document}\n')
            (root / 'fragment.tex').write_text('Not a root, $\\frac12$.\n')
            (root / 'archive').mkdir()
            (root / 'archive' / 'old.tex').write_text('\\documentclass{amsart}\n')
            run = subprocess.run([sys.executable, str(SCRIPT), '--summary', '--roots', tmp],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn('a.tex', run.stdout)
            self.assertNotIn('fragment.tex', run.stdout)
            self.assertNotIn('old.tex', run.stdout)
            self.assertIn('1 documents', run.stdout)


class NumberingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        path = self.root / name
        path.write_text(text)
        return path

    def findings(self, path):
        return [m for _, m in API['numbering_warnings'](path, path.read_text())]

    def test_uncited_numbers_and_cited_ones(self):
        path = self.write('a.tex', '\\begin{equation}\\label{eq:a}\nx\n\\end{equation}\n'
                                   '\\begin{equation}\\label{eq:b}\ny\n\\end{equation}\n'
                                   '\\begin{equation}\nz\n\\end{equation}\n'
                                   '\\begin{equation*}\nw\n\\end{equation*}\nBy \\eqref{eq:a}.\n')
        found = self.findings(path)
        self.assertEqual(sum('uncited-number' in m for m in found), 2)   # eq:b and the unlabelled one

    def test_citations_in_input_files_count(self):
        self.write('part.tex', 'See \\cref{eq:a,eq:c}.\n')
        path = self.write('main.tex', '\\begin{equation}\\label{eq:a}\nx\n\\end{equation}\n\\input{part}\n')
        self.assertEqual(self.findings(path), [])

    def test_align_rows_and_notag(self):
        path = self.write('a.tex', '\\begin{align}\na&=b\\label{eq:r1}\\\\\nc&=d\\notag\\\\\ne&=f\n\\end{align}\n'
                                   'By \\eqref{eq:r1}.\n')
        found = self.findings(path)
        self.assertTrue(any('1 of its 2 numbers' in m for m in found), found)

    def test_label_in_unnumbered_display(self):
        path = self.write('a.tex', '\\begin{equation*}\\label{eq:x}\nx\n\\end{equation*}\n')
        self.assertTrue(any('label-unnumbered' in m for m in self.findings(path)))

    def test_commented_citation_does_not_count(self):
        path = self.write('a.tex', '\\begin{equation}\\label{eq:a}\nx\n\\end{equation}\n% \\eqref{eq:a}\n')
        self.assertTrue(any('uncited-number' in m for m in self.findings(path)))

    def test_unnumber_stars_only_wholly_uncited_displays(self):
        path = self.write('a.tex', '\\begin{equation}\\label{eq:a}\nx\n\\end{equation}\n'
                                   '\\begin{equation}\\label{eq:b}\ny\n\\end{equation}\n'
                                   '\\begin{align}\na&=b\\label{eq:r1}\\\\\nc&=d\n\\end{align}\n'
                                   '\\begin{align}\ne&=f\\\\\ng&=h\n\\end{align}\n'
                                   'By \\eqref{eq:a} and \\eqref{eq:r1}.\n')
        result, count = API['unnumber'](path, path.read_text())
        self.assertEqual(count, 2)
        self.assertIn('\\begin{equation}\\label{eq:a}', result)
        self.assertIn('\\begin{equation*}\ny\n\\end{equation*}', result)
        self.assertIn('\\begin{align}\na&=b\\label{eq:r1}', result)            # mixed: left for review
        self.assertIn('\\begin{align*}\ne&=f\\\\\ng&=h\n\\end{align*}', result)

    def test_numbering_all_switches_the_check_off(self):
        path = self.write('a.tex', '\\begin{equation}\nx\n\\end{equation}\n')
        run = lambda *extra: subprocess.run([sys.executable, str(SCRIPT), '--width', '0', *extra, str(path)],
                                            capture_output=True, text=True)
        self.assertIn('uncited-number', run().stderr)
        self.assertNotIn('uncited-number', run('--numbering', 'all').stderr)


class DifferentialTests(unittest.TestCase):
    def test_hand_written_differentials_become_dd(self):
        source = ('\\documentclass{amsart}\n\\newcommand{\\T}{\\mathbb T}\n\\begin{document}\n'
                  'Let $\\int_\\T u\\overline v\\,dm$, $\\frac{d\\theta}{2\\pi}$, $f(x)dx$, $\\mathrm{d}x$,\n'
                  '$\\sum_{d\\mid n}d$, $\\{d\\}$, we do this, $x\\,d$, $w\\,d\\mu$.\n\\end{document}\n')
        result, count = API['differentials'](source)
        self.assertEqual(count, 5)
        for expected in ('u\\overline v\\dd m$', '\\frac{\\dd\\theta}{2\\pi}', 'f(x)\\dd x', '$\\dd x$',
                         'w\\dd\\mu', '\\sum_{d\\mid n}d', '$\\{d\\}$', 'we do this', '$x\\,d$'):
            self.assertIn(expected, result)
        self.assertIn('\\newcommand{\\T}{\\mathbb T}\n\\newcommand*{\\dd}{\\mathop{}\\!\\mathrm{d}}\n', result)
        again, count = API['differentials'](result)
        self.assertEqual((again, count), (result, 0))

    def test_derivative_numerator_is_converted_too(self):
        source = ('\\documentclass{amsart}\n\\begin{document}\n'
                  '$\\frac{d}{dA}\\log\\tau$ and $\\frac{d}{\\dd x}f$\n\\end{document}\n')
        result, count = API['differentials'](source)
        self.assertIn('\\frac{\\dd}{\\dd A}\\log', result)
        self.assertIn('\\frac{\\dd}{\\dd x}f', result)
        self.assertEqual(count, 3)

    def test_existing_definition_is_kept(self):
        source = ('\\documentclass{amsart}\n\\newcommand{\\dd}{d}\n\\begin{document}\n$\\,dx$\n\\end{document}\n')
        result, _ = API['differentials'](source)
        self.assertEqual(result.count('\\newcommand'), 1)

    def test_rule_reports_only_math(self):
        found = [m for _, m in house_warnings('We do this, $\\int f\\,dx$ and $\\sum_{d\\mid n}d$.\n')
                 if m.startswith('differential')]
        self.assertEqual(len(found), 1)


class ChangedTests(unittest.TestCase):
    def test_bad_revision_and_missing_files_are_errors(self):
        run = subprocess.run([sys.executable, str(SCRIPT), '--changed', 'no-such-revision-xyz'],
                             capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(run.returncode, 2)
        run = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)


class MakeTests(unittest.TestCase):
    def make(self, *args, env=None):
        return subprocess.run(['make', '--no-print-directory', '-C', str(ROOT), *args],
                              capture_output=True, text=True, env=env)

    def test_default_tex_overrides_gnu_make_builtin(self):
        run = self.make('help')
        self.assertIn('Current TEX=templates/solution-sheet.tex', run.stdout)

    def test_command_line_and_environment_tex_win(self):
        self.assertIn('Current TEX=x.tex', self.make('help', 'TEX=x.tex').stdout)
        env = dict(os.environ, TEX='y.tex')
        self.assertIn('Current TEX=y.tex', self.make('help', env=env).stdout)

    def test_help_lists_every_target(self):
        out = self.make('help').stdout
        for target in ('lint', 'build', 'pdf', 'view', 'watch', 'lint-all', 'unnumber', 'lint-changed', 'differentials', 'doctor', 'records'):
            self.assertRegex(out, rf'\n  {target} ')

    def test_build_rejects_non_tex(self):
        env = dict(os.environ, TEX=str(ROOT / 'README.md'))
        run = subprocess.run([sys.executable, str(ROOT / 'scripts/build-tex')], env=env,
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        run = subprocess.run([sys.executable, str(ROOT / 'scripts/build-tex'), '--bogus'], env=env,
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)


if __name__ == '__main__':
    unittest.main()

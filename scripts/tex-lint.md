# LaTeX workflow

Run from the repository root; `make` alone lists the targets. `TEX` selects
one document and defaults to `templates/solution-sheet.tex`.
Relative and absolute paths work; quote the assignment if the path contains
spaces.

```sh
make doctor                       # are latexmk, latexindent, chktex, ... installed?
make lint   TEX=path/to/paper.tex # read-only check
make pdf    TEX=path/to/paper.tex # lint, compile, copy the PDF next to the source
make view   TEX=path/to/paper.tex # open the built PDF
make watch  TEX=path/to/paper.tex # recompile on every save
make lint-all DIR=solutions        # one summary line per root document
make lint WIDTH=100               # refill paragraphs to another width
make unnumber TEX=path/to/paper.tex # star every display whose number is never cited
make lint NUMBERING=all           # allow uncited equation numbers
make lint-changed                 # lint the .tex files changed in the jj change @ (REV=...)
make differentials TEX=path/to/paper.tex # \,dm -> \dd m (changes the PDF)
make test                         # formatter, lint and Make tests
```

| Target | Effect |
|---|---|
| `lint`, `lint-diff` | Formatting, house style and ChkTeX; `lint-diff` also prints the formatting diff. |
| `lint-fix`, `format` | Write formatting changes; `lint-fix` then reports what is left. |
| `format-check` | Formatting only, read-only. |
| `build` | Lint must pass, then latexmk compiles into `build/<path without .tex>/`. |
| `pdf` | `build`, then copy the PDF next to the source (the tracked PDFs). |
| `view`, `watch` | Open the built PDF; recompile on save with `latexmk -pvc` (no lint gate). |
| `unnumber` | Recursively follow literal `\input`/`\include` files from the selected document's source directory, then star wholly uncited displays and remove their labels across that closure. This changes the PDF's equation numbers, so it is separate from `lint-fix`; explicit `\tag`s and partly cited displays are left unchanged and reported. |
| `lint-changed` | Lint every `.tex` file changed in the jj change `REV` (default `@`); more than ten files are summarized one per line. Run it before committing. |
| `differentials` | Rewrite hand-written differentials as `\dd` and define `\dd` if the document lacks it. Changes the typeset d (upright, operator spacing). |
| `clean` | Remove the document's auxiliary files, keeping its PDF. |
| `lint-all` | Report only: every file with a `\documentclass` under `DIR`, skipping `archive/` and `build/`. |
| `check` | `test`, then `build`, run one after the other even under `make -j`. |

Lint gates `build` and `pdf` as a prerequisite, so even `make -j` finishes lint
first. Compilation runs in the source directory so relative inputs resolve;
the builder creates auxiliary directories for literal `\include{...}` commands
in the root document before compiling.
Documents outside the repository build under `build/external/<hash>/`. A
build prints any overfull boxes, undefined references and LaTeX warnings left
in the final log.

GNU make predefines `TEX=tex`, so the Makefile replaces that built-in default
explicitly; a `TEX` given on the command line or in the environment wins.

## What lint does

The wrapper protects comments, macro definitions and common literal regions,
converts `\(...\)` to `$...$` and `\[...\]` to `equation*`, runs
[latexindent](https://latexindentpl.readthedocs.io/en/latest/) with
`tex-style.yaml`, and adds `%` separator lines around display environments.
Display bodies and lists are indented by two spaces; prose environments
(theorem, lemma, proof, abstract, ...) stay flush-left. A `\label` directly
after `\begin{equation}` stays on that line. Existing numbering and paragraph
breaks are retained. The conversion to `equation*` requires amsmath.

Prose paragraphs are refilled greedily to `WIDTH` columns (default 79, Vim's
`gq` width when `'textwidth'` is 0), paragraph by paragraph, exactly as `gqip`
would: every line is as full as it can be without exceeding the width. This
never changes the typeset output. Only running prose in the document body is
refilled, including theorem, proof and abstract text. A paragraph ends at a
blank line, a `%` line, any line with a comment, `\\` or `&`, and any
structural command (`\section`, `\label`, `\item`, `\begin`, ...), including
the continuation lines of a structural command that spans several lines. The
preamble, displays, tables, lists, floats, the bibliography and opt-out
regions are never refilled. A control space (`cf.\ the`) is never split, and
protected material counts at its real length. Use `make lint WIDTH=100` for a
different width or `--width 0` to switch refilling off.

Long source lines inside displays are broken too, without changing the PDF
(TeX reads a newline in math as a space, so the display stays on one typeset
line). Breaks are made only at the top level of the formula, never inside
braces, brackets, parentheses or a `\left`/`\bigl` pair, in this order:

1. between equations, before `\quad`/`\qquad`, filling lines greedily;
2. before every relation (`=`, `\le`, `\to`, ...) of an equation that is
   still too long, so each relation starts a line;
3. greedily before a binary `+` or `-`.

A piece shorter than 12 characters stays with the line before it, so no
`=0 .` stub is left alone; a line without a good break point stays long.
Continuation lines take the environment's indent, which is what latexindent
keeps. A display that is too wide on the page is a different problem: it shows
up as an overfull box in `make build`, and needs a decision about how to split
it (`multline`, `split` or `aligned` at `=`).

House checks never rewrite the source. Each finding names its rule, and a rule
can be silenced on one line with a reason, e.g.
`... Theorem 2.1 of Kulikov ... % lint-tex: ignore=manual-number (external numbering)`.

| Rule | Flags | Use instead |
|---|---|---|
| `norm`, `ref` | `\|...\|`, `\ref` | a `\norm` macro; `\cref`/`\Cref` |
| `manual-number` | "Theorem~3", "Section 4" typed in text | `\cref` (skipped inside `\cite[...]`, near a `\cite`, in the bibliography) |
| `cref-heading` | `\cref` in a heading | `\texorpdfstring{\cref{x}}{Theorem \ref{x}}` (bookmarks) |
| `inline-frac`, `tfrac` | `\frac` in inline math; `\tfrac` | `a/b` inline, `\frac` in displays |
| `bigg` | `\Bigg`, `\Biggl`, ... | at most `\biggl`/`\biggr` |
| `inline-left` | `\left...\right` in inline math | `\bigl`/`\bigr`, or a display (allowed in displays) |
| `half-open` | `[a,b)`, `(a,b]` in math | `\intco{a}{b}`, `\intoc{a}{b}` from `\DeclarePairedDelimiterX` |
| `coloneq`, `much-less` | `:=`, `<<`/`>>` in math | `\coloneqq` (mathtools), `\ll`/`\gg` |
| `mbox-math`, `inline-display` | `\mbox` in math; `\displaystyle` inline | `\text`; a display |
| `old-font`, `tex-fraction` | `\bf \it \rm \sc \tt \sf \sl \cal`; `\over \atop \choose` | `\textbf`, `\emph`, `\mathcal`, ...; `\frac`, `\binom` |
| `dollar-display`, `eqnarray` | `$$...$$`, `eqnarray` | amsmath environments |
| `ellipsis`, `straight-quote` | `...`, `"` in text | `\dots`; ` ``...'' ` |
| `prose-break`, `manual-break`, `negative-space`, `sloppy`, `centerline` | `\\` in running text, `\newpage`, `\vspace{-...}`, `\sloppy`, `\centerline` | rewording; local control once the prose is final |
| `double-cite` | `\cite{a}, \cite{b}` | `\cite{a,b}` |
| `label-before-caption`, `float-center` | `\label` before `\caption`; `center` in a float | label after caption; `\centering` |
| `tabular-rules` | `|` in a tabular column spec | booktabs |
| `obsolete-package` | `a4wide`, `epsfig`, `times`, `subfigure`, ... | the l2tabu replacement it names |
| `uncited-number` | a numbered display (`equation`, `multline`, `gather`, `align` row, ...) never cited by `\eqref`/`\cref`/`\ref`, counting `\input` files and ignoring comments | `equation*` etc.; `make unnumber` does it. Off with `NUMBERING=all` |
| `label-unnumbered` | `\label` in a starred display or a `\notag` row | remove it, or number the display |
| `differential` | `\,dm`, `f(x)dx`, `\frac{d\theta}{2\pi}`, `\mathrm{d}x` in math | `\dd`, defined as `\newcommand*{\dd}{\mathop{}\!\mathrm{d}}` (upright d with operator spacing: `u\dd m`, `\frac{\dd\theta}{2\pi}`); `make differentials` rewrites them and adds the definition. A variable `d` (`\sum_{d\mid n}`) is not flagged |
| `mixed-symbol` | both `\epsilon` and `\varepsilon` (or `\phi`, `\varphi`) | one spelling |

Sources: [l2tabu](https://ctan.org/pkg/l2tabu) (obsolete packages and
commands), the [interval](https://ctan.org/pkg/interval) package (why `[a,b)`
spaces badly), the Journal of Integer Sequences
[TeX recommendations](https://emis.univie.ac.at/journals/JIS/texrecs.pdf),
and the house rules in this repository (slash fractions inline, delimiters at
most `\biggl`, `\cref`, `\norm`).

[ChkTeX](https://www.nongnu.org/chktex/) supplies general checks. Disabled
globally: 1 (command terminated with space), 3 and 25 (they fire on every
`(1+x)^q` and `f^{(k)}`), and 46 (`$...$` is the house style). Narrow false
positives are filtered, each only at the exact token ChkTeX reports: 40 on a
factorial ending inline math (`$k!$`), 8 on an en dash joining two capitalized
names (`Cauchy--Schwarz`), 2 after punctuation (`$x$, \eqref{a}` needs no
tie), 12 before `\qed`, and 2 and 36 inside the bookmark argument of
`\texorpdfstring`. For any other
confirmed false positive, use ChkTeX's local `% chktex N` suppression with a
reason rather than disabling a warning globally.

Exit status: 0 clean, 1 findings, 2 tool or input error. (ChkTeX itself exits
2 for ordinary warnings and 0 for a missing file; the wrapper decides from its
output instead.)

Lint checks **only the selected file**, not recursively included files.
Lint those separately with `make lint TEX=path/to/fragment.tex`. It does not
prove mathematical correctness or inspect the rendered PDF. The guard is
lexical, not a full TeX parser. Custom literal environments and
catcode-changing code should be surrounded by `% lint-tex: off` and
`% lint-tex: on`; ChkTeX still runs independently on the original file.

Review the diff before accepting `lint-fix`. For optional sentence reflow, use
`scripts/lint-tex --sentences --diff path/to/file.tex` before `--fix`.

## Dependencies

Python 3, Perl, latexindent, ChkTeX, latexmk and a TeX distribution;
`make doctor` checks them. `make setup` downloads the CPAN installer and
installs YAML::Tiny 1.76, File::HomeDir 1.006 and File::Which 1.27 in the
ignored `.tools/perl5/`. The wrapper sets PERL5LIB for latexindent; no system
Perl installation changes. Setup needs curl and network access; normal checks
work offline.

[tex-fmt](https://github.com/WGUNDERWOOD/tex-fmt) and
[Badness](https://github.com/jolars/badness) are alternatives considered;
this workflow reuses the installed latexindent and ChkTeX rather than
stacking multiple formatters.

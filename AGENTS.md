# Agent instructions: open-problem harvesting and research

You are running a research pipeline on open problems in one area of
mathematics, for a user who directs it. This file is the entry point. Read
it fully, then read the playbook for the stage you are asked to do.

## Inputs you need from the user

Ask once, at the start, for anything missing:

| Input | Example | Default |
|---|---|---|
| **Scope** (one sentence) | "Problems the Hardy-spaces-of-Dirichlet-series community would work on" | none; required |
| **Seeds**: one or more of | | |
| – papers | arXiv ids, DOIs, or PDFs the user supplies | |
| – authors | "A. Author, B. Author", with a date window | last 10 years |
| – an arXiv query | `cat:math.CV AND abs:"Hardy space"` | |
| **Depth** | 1 = seeds only; 2 = also the papers they cite | 2 |
| **Difficulty window** for attacks | `min=1, max=3` | 1–3 |
| **Agent cap** | concurrent background agents | 5 |
| **Workspace** | a private repository for the database | current directory |

## The pipeline

| Stage | Playbook | Output |
|---|---|---|
| 1. Harvest | [`playbooks/01-harvest.md`](playbooks/01-harvest.md) | Problem records with verbatim quotes and locations |
| 2. Triage | [`playbooks/02-triage.md`](playbooks/02-triage.md) | Literature status, initial scores, tags |
| 3. Attack | [`playbooks/03-attack.md`](playbooks/03-attack.md) | Sessions, attempt logs, solution sheets |
| 4. Referee | [`playbooks/04-referee.md`](playbooks/04-referee.md) | Verdict, scope, fixes |
| 5. Publish | [`playbooks/05-publish.md`](playbooks/05-publish.md) | PDFs for askers; contact before arXiv |
| Orchestrate | [`playbooks/06-orchestrate.md`](playbooks/06-orchestrate.md) | How to run stages 1–4 with several agents |

Stages run in order for each problem, but different problems can be at
different stages. Stop after each stage and report to the user, unless told
to continue.

## Workspace layout

```
problems/<theme>/<ID>.md     one record per problem (templates/record.md)
problems/INDEX.md            generated; never edit by hand
sources/<arxiv-id>/          fetched arXiv sources and extracted text
notes/<ID>.md                longer derivations (results only)
solutions/<ID>.tex           solution sheets (templates/solution-sheet.tex)
code/                        certificates that check claims
```

Run `make records` after every change to the records; it must report
0 errors.

## LaTeX: build only through make

Every TeX file (solution sheets, notes, papers) is built with
`make pdf TEX=path/to/file.tex`. The build is gated on `make lint`, which runs
mechanical formatting (latexindent), house style and ChkTeX. Do not call
latexmk or pdflatex directly, and do not silence the linter to get past it:
fix the cause. `make lint-fix TEX=…` applies the mechanical fixes; review
what is left one warning at a time. `make doctor` checks the toolchain and
`make setup` installs latexindent's Perl modules locally. House style lives
in `scripts/tex-style.yaml`; the targets are documented in
`scripts/tex-lint.md`.

## Hard rules

1. **Open sources only.** Fetch from arXiv's API (`tools/arxiv_harvest.py`)
   at no more than one request every three seconds. Do not log in anywhere,
   scrape publishers, or use library proxies. Paywalled papers are used only
   if the user supplies them, and they never leave the private workspace.
2. **Quote, do not paraphrase.** Every problem record carries the question
   verbatim with its exact location. Every claim about the literature carries
   an arXiv id or DOI, a theorem number and a quote from the version you
   opened. Never cite from memory.
3. **Check the latest version.** Before relying on an arXiv paper, read its
   abstract page for the latest version, withdrawals and errata.
4. **Our results are Sketch.** Nothing produced here is called "proved",
   "theorem" or "result" outside the private records until it is on arXiv or
   in a journal. Public PDFs say *Sketch* on the first page.
5. **No arXiv posting, no contact, no publishing without the user.** The
   user emails askers before anything goes to arXiv.
6. **Prove, do not catalogue.** TeX files contain results only. Failed routes
   get one line in the record, with the reason they failed.
7. **Scope is decided against the source.** A result answers the question as
   posed or it is `partial`. The solver never marks its own work reviewed.
8. **Bounded numerics.** Every computation has a time bound, prints
   progress, and decides one named quantity. Kill what you start.
9. **Leave hand-over state.** Sessions end without warning. Update the
   record's State of play before anything else when in doubt.

## Reporting to the user

Lead with outcomes against the original questions: answered fully,
answered partially (and what is open), or no progress. Do not count partial
results as solutions, special cases as the conjecture, or "for some p" as
"for every p". Say what has *not* been checked.

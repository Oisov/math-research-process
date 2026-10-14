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
| 5. Publish | [`playbooks/05-publish.md`](playbooks/05-publish.md) | Results shared openly, askers told; vouching before arXiv |
| Orchestrate | [`playbooks/06-orchestrate.md`](playbooks/06-orchestrate.md) | How to run stages 1–4 with several agents |

Stages run in order for each problem, but different problems can be at
different stages. Stop after each stage and report to the user, unless told
to continue.

## Workspace layout

```
problems/<theme>/<ID>.md     one record per problem (templates/record.md)
problems/INDEX.md            generated; never edit by hand
sources/<arxiv-id>/          fetched arXiv sources and extracted text
notes/<ID>.md                one file per problem: derivations too long for the record, dated sections appended
solutions/<ID>.tex           solution sheets (templates/solution-sheet.tex)
discoveries/<ID>.md          the claiming model's verbatim response, model and date
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
   at no more than one request every three seconds. Anything else comes
   from the user.
2. **Quote, do not paraphrase.** Every problem record carries the question
   verbatim with its exact location. Every claim about the literature carries
   an arXiv id or DOI, a theorem number and a quote from the version you
   opened. Never cite from memory.
3. **Check the latest version.** Before relying on an arXiv paper, read its
   abstract page for the latest version, withdrawals and errata.
4. **Our results are Sketch.** Nothing produced here is called "proved",
   "theorem" or "result" outside the private records until it is on arXiv or
   in a journal. Public PDFs say *Sketch* on the first page.
5. **No sharing, contact or arXiv posting without the user.** Results may be
   shared openly first, labelled with how much stands behind them; the askers
   are told promptly afterwards. Nothing goes to arXiv until the askers have
   been told and someone with command of the result's research context can
   vouch for it.
6. **Measure progress against the objective** (map or settle; see
   `playbooks/03-attack.md`). TeX files contain results only. Failed routes
   get one line in the record, with the reason they failed.
7. **Scope is decided against the source.** A result is full only if the
   proved statement implies the requested conclusion under the source's
   definitions; otherwise it is `partial`. The solver never marks its own work reviewed.
8. **Bounded numerics.** Every computation has a time bound, prints
   progress, and decides one named quantity. Kill what you start.
9. **Archive discoveries.** When a model claims to have settled a problem,
   save its response verbatim in `discoveries/<ID>.md` with the model name,
   the date and time, and the session. If verification shows the claim is
   false, keep the file, mark it **refuted** at the top, and link the
   objection or correction; add one line to the attempt log. Refuted claims
   are evidence of how convincing errors arise.
10. **Leave hand-over state.** Sessions end without warning. Update the
   record's State of play before anything else when in doubt.

## What to expect

This pipeline is best at mapping a field: finding problems, checking the
literature, and settling the easy ones. Expect most solved problems to be
already in the literature, routine from known tools, or counterexamples that
are easy to check. Do not expect it to break problems that experts are stuck
on, and do not present it as doing so.

## Version control and files

- **Default to Jujutsu with a git backend.** In a new workspace run
  `jj git init --colocate` (in an existing git repository, run it in place),
  and use `jj` for every version-control operation. The colocated `.git`
  keeps the repository usable by git-based tools and hosts such as GitHub,
  but agents never run `git` themselves.
- Jujutsu snapshots the working copy automatically and records every
  operation (`jj op log`), so no agent edit is lost and progress can be
  reconstructed later.
- Use it as the research log: commit each record together with the work it
  describes, one problem or task per commit, with a message that says what
  changed (`jj commit <paths> -m "…"`).
- Use git directly only if the user asks for it.
- Write at most one notes file per problem, `notes/<ID>.md`, and append dated
  sections to it. Do not create a new file per attempt, per agent or per idea.
- Scratch work belongs in the session scratchpad, outside the repository:
  exploratory scripts, numerics that don't certify anything, and drafts.
- A script goes in `code/` only if a claim depends on it.
- When a draft is superseded, delete it; the history keeps it.
- Subagents report back to the orchestrator in their final message and
  write only to the record and notes file they were given.

## Reporting to the user

In every report:
- The funnel: the count at each stage (harvested, valid, open, attempted,
  claimed, refereed, user-checked).
- Claimed answers split into flawed, technically correct, and meaningfully
  correct.
- Rediscoveries kept apart from answers found in the literature.
- Novelty called provisional.
- Cost per problem attempted (OEIS Open, arXiv:2608.11941, §3.1; Feng et
  al., arXiv:2601.22401, Table 2).


Lead with outcomes against the original questions: answered fully,
answered partially (and what is open), or no progress. Say how each question
was posed (conjecture, problem, question, informal remark, or our own), and
never report an answer to our own derived question as if it settled someone
else's conjecture. Classify each solved problem as: already in the literature; routine from known tools; easy-to-check
counterexample; or substantial new argument. Do not count partial
results as solutions, special cases as the conjecture, or "for some p" as
"for every p". Say what has *not* been checked.

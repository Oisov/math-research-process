# Finding, sharing and vouching: a non-expert, AI agents and open problems

Can someone outside the profession contribute to research mathematics with AI
agents without doing the harms mathematicians warned about this autumn:
results announced in a rush, prior work left uncited, proofs nobody can read,
checking pushed onto experts? The [paper](paper/paper.pdf) argues that it can,
if three acts are kept apart.

- **Finding** a result is now cheap, and agents do most of it.
- **Sharing** a result can be done without claiming it: say what is known, how
  much stands behind it and where the explanation is, and leave anyone free to
  develop it.
- **Vouching** for a result, standing behind it as correct and worth reading,
  is an act only someone with expertise can perform. It is what turns a shared
  result into a paper.

The evidence is one case. In October 2026 I spent twelve days directing Claude
Code and Codex agents at the open problems of one area of analysis: Hardy,
Bergman and Dirichlet-series spaces, Hankel and Helson operators, and
Nehari-type theorems. Before that I spent about six weeks writing a monograph
on the area with the same agents. I have a master's degree in the area and no
research career in it.

This repository holds the workflow as I now recommend it. The
[`AGENTS.md`](AGENTS.md) file turns it into instructions a coding agent can
follow in another field: give it a list of papers, a list of authors or an
arXiv query, and it builds, triages and works a problem database the same way.

## What happened

The agents were good at mapping the field: finding and classifying problems,
checking the literature, and answering the easy ones. Most of their answers are
short arguments from known tools, or counterexamples that are easy to check
once found. A few may matter; whether they do is for specialists to judge. On
the hard problems, several agents working for days produced maps of what
fails, not proofs.

The results themselves are shared, unclaimed, at
[github.com/Oisov/math-preprints](https://github.com/Oisov/math-preprints).
Each says what is known and how much stands behind it. Nobody claims them:
anyone may check, develop or publish them, crediting the people who asked the
questions. The questions belong to those who asked them, and every record
cites its source. Before anything goes to arXiv, the people who asked are told.

## Getting started

```sh
git clone <this repository> process   # or download it
mkdir my-field && cd my-field
jj git init --colocate                # Jujutsu with a git backend: the default
cp -r ../process/{AGENTS.md,Makefile,scripts,tools,templates,playbooks} .
```

Then ask your agent to read `AGENTS.md` and start the harvest.

## Contents

| File | What it is |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Entry point for agents: the pipeline and the hard rules |
| [`playbooks/`](playbooks/) | One file per stage: harvest, triage, attack, referee, publish, orchestrate |
| [`templates/`](templates/) | Problem record, solution sheet, referee brief, discovery archive |
| [`tools/`](tools/) | `arxiv_harvest.py` (candidate extraction from arXiv sources), `check_records.py` (record validator) |
| [`Makefile`](Makefile), [`scripts/`](scripts/) | The lint-gated LaTeX build (`make pdf TEX=…`), house-style linter, and tests (`make test`) |
| [`docs/method.md`](docs/method.md) | **Our method and process**: what we actually did, in order, with numbers |
| [`docs/lessons.md`](docs/lessons.md) | What worked and what did not, with the evidence |
| [`docs/schema-review.md`](docs/schema-review.md) | Which record fields earned their place |
| [`docs/recommendations.md`](docs/recommendations.md) | **What we recommend** |
| [`paper/`](paper/) | The paper (LaTeX, built with `make pdf TEX=paper/paper.tex`) |
| [`data/`](data/) | The anonymised records and audit behind every count in the paper; `python3 data/tables.py` recomputes them |

The evidence behind these documents is the version history of the working
repository (about 1,000 commits), 14 Claude Code sessions with 393 subagents,
and 586 Codex sessions, about 4.5 GB of logs in all. The logs are not
published.

## Licence

Everything in this repository except the paper is dedicated to the public
domain under [CC0 1.0](LICENSE): the playbooks, templates, `AGENTS.md`, docs,
tools, scripts and data. Use, change and republish them freely; no credit is
needed.

The paper in [`paper/`](paper/) is the one thing here I vouch for, so it is
licensed under [CC BY 4.0](paper/LICENSE): reuse it in any way, crediting the
author.

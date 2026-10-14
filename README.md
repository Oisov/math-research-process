# Harvesting and attacking open problems with AI agents

For about six weeks in autumn 2026 I worked through the open problems of one
research area with Claude Code and Codex agents: Hardy, Bergman and
Dirichlet-series spaces, Hankel and Helson operators, and Nehari-type
theorems. I have a master's degree in the area and directed the work.

This repository records how we did it, what worked and what did not. The
[`AGENTS.md`](AGENTS.md) file turns the recommended version into instructions
a coding agent can follow in another field: give it a list of papers, a list
of authors or an arXiv query, and it builds, triages and works a problem
database the same way.

## What the agents achieved, and what they did not

The agents were very good at mapping the field: finding, collecting and
classifying problems, checking the literature, and picking off low-hanging
fruit. Most of the problems they settled were short arguments from known
tools, or counterexamples that are easy to verify once found. Only a few
results are of real significance; those have been sent to the people who
asked the questions.

They did not get us past the walls. On the hard problems, several agents
working for days produced maps of what fails, not proofs. A hard problem
stayed hard. We use this method as the first step of research, to get to know
a field and find questions worth working on, not as a way to break hard
problems. Terence Tao has made the same observation about the Erdős problems;
see [docs/paper.md](docs/paper.md).

## Credit

The questions belong to the people who asked them, and every record cites
the exact source. The proofs and computations were produced by AI agents and
checked by me. The mathematics itself is published separately as PDFs.

## The publication rule

Everything we produced is labelled **Sketch** until it appears on arXiv or in
a journal, however it was checked. Before anything goes to arXiv I email the
authors who asked the question.

## Where things stand (14 October 2026)

| | Count |
|---|---|
| Problems in the database | 373 (289 asked by others, 84 by us) |
| Settled by someone else (journal or arXiv), found during triage | 64 |
| Settled by our agents, all *Sketch*, mostly low-hanging fruit | 141 (89 of them asked by others) |
| Of those, public as PDFs | 61 |
| Partial results only | 142 |
| Untouched or still being worked | 26 |
| Askers contacted so far | a handful of author groups; the rest are batched |

"Settled by our agents" means a written proof or counterexample, a solution
sheet and one agent referee pass. [Lessons: review](docs/lessons.md#review-is-the-weakest-link)
says what that is worth.

## Contents

| File | What it is |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Entry point for agents: the pipeline and the hard rules |
| [`playbooks/`](playbooks/) | One file per stage: harvest, triage, attack, referee, publish, orchestrate |
| [`templates/`](templates/) | Problem record, solution sheet, referee brief |
| [`tools/`](tools/) | `arxiv_harvest.py` (candidate extraction from arXiv sources), `check_records.py` (record validator) |
| [`Makefile`](Makefile), [`scripts/`](scripts/) | The lint-gated LaTeX build (`make pdf TEX=…`), house-style linter, and tests (`make test`) |
| [`docs/method.md`](docs/method.md) | **Our method and process**: what we actually did, in order, with numbers |
| [`docs/lessons.md`](docs/lessons.md) | What worked and what did not, with the evidence |
| [`docs/schema-review.md`](docs/schema-review.md) | Which record fields earned their place |
| [`docs/recommendations.md`](docs/recommendations.md) | **What we recommend** |
| [`docs/paper.md`](docs/paper.md) | Draft framing and outline for a paper on this work |

The evidence behind these documents is the version history of the working
repository (about 1,000 commits), 14 Claude Code sessions with 393 subagents,
and 586 Codex sessions, about 4.5 GB of logs in all. The logs are not
published.

# Harvesting and attacking open problems with AI agents

This repository describes a process, and gives agents the instructions to run
it. For about six weeks in autumn 2026 one person worked through the open
problems of a single research area with Claude Code and Codex agents. The
area was Hardy, Bergman and Dirichlet-series spaces, Hankel and Helson
operators, and Nehari-type theorems. The person has a master's degree in that
area and directed the work.

Here we record how we did it, what worked, what did not, and what we would
do differently. The [`AGENTS.md`](AGENTS.md) file turns the recommended
version into instructions that a coding agent can follow on another field:
give it a list of papers, a list of authors or an arXiv query, and it builds,
triages and works a problem database the same way.

## What this is not

- **Not a claim of credit.** The questions belong to the people who asked
  them; every record cites the exact source location. The proofs and
  computations were produced by AI agents (Claude and GPT models), directed
  and checked by one human. Nothing here has been refereed by a journal.
- **Not a results repository.** The mathematics is published separately as
  PDFs. This repository is about the process.
- **Not a crawler for paywalled material.** The tools fetch from arXiv's
  public API only, at its requested rate. See
  [Sources](docs/method.md#sources).

## The publication rule

Everything we produced is labelled **Sketch** until it appears on arXiv or in
a journal, regardless of how it was checked: by an agent referee, a second
model, exact-arithmetic certificates or even a Lean formalization. Before
anything goes to arXiv we email the authors who asked the question. Public
PDFs exist only so that the people who asked can read and check the answer.

## Where things stand (14 October 2026)

| | Count |
|---|---|
| Problems in the database | 373 (289 asked by others, 84 asked by us) |
| Settled by someone else (journal or arXiv), found during triage | 64 |
| Settled by our agents, all *Sketch* | 141 (89 of them asked by others) |
| Of those, public as PDFs | 61 |
| Partial results only | 142 |
| Untouched or still being worked | 26 |
| Askers contacted so far | a handful of author groups; the rest are batched |

"Settled by our agents" means: a written proof or counterexample, a
self-contained solution sheet, and one independent agent referee pass. It
does not mean correct; see
[Lessons: review](docs/lessons.md#review-is-the-weakest-link).

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

The evidence behind these documents is the version history of the working
repository (about 1,000 commits), 14 Claude Code sessions with 393 subagents,
and 586 Codex sessions, about 4.5 GB of logs in all. The logs are not
published; the documents quote them only where a quote is the evidence.

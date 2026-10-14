# Our method and process

This is what we actually did, in order. The recommended version is in
[recommendations.md](recommendations.md); the reasons for the differences are
in [lessons.md](lessons.md).

## People and tools

- **One human**, with a master's degree in the area, directing everything:
  choosing targets, judging whether a result mattered, steering stuck agents,
  reading the papers before they went out, and doing all contact with other
  mathematicians.
- **Claude Code** (Opus 5.5 as the main session; Sonnet and Haiku for cheap
  subagents) and **Codex** (GPT-5.6 Luna and Sol, GPT-6 Astra, later 6.1 Sol)
  running in the same repository, often at the same time on disjoint folders.
  The human relayed between them; neither could message the other.
- A single private repository under Jujutsu (`jj`), LaTeX built through a
  lint-gated `make`, Python (mpmath, cvxpy, SymPy) for numerics and
  certificates, Lean for one formalization.
- A public repository of PDFs (papers, proof notes, the problem volumes) and
  the numerics that check them. No TeX sources, notes or downloaded papers.

## Timeline

| Dates | Phase | What happened |
|---|---|---|
| Aug–Sep | Writing | Books and a teaching website on the area. This built the shared vocabulary and the local paper collection the later work drew on. |
| 3–4 Oct | First research push | Reading recent preprints for "small gaps we could fill". Produced a 13-page paper improving a known threshold, and a short note extending a recent theorem to Bergman spaces. Both were sent to an expert. |
| 7–10 Oct | Expert collaboration | Several short papers answering conjectures from one paper, written and rewritten in the style of the expert who asked them; he became a co-author on one. Lean formalization of the core argument. |
| 10 Oct | Catalogue v1 | Agents listed every conjecture and open question in the local paper collection ("first order", 178 records) and in the papers those cite ("second order", 57). Missing papers were downloaded. Each record got a brief literature check. |
| 10–11 Oct | Mass triage | 194 assessments by cheap agents with a 10-minute budget each, then one-hour attempts on the promising ones. About five hours of wall time. |
| 11 Oct | Contract | After a day of agents "spinning", a written research contract: literature stage with cheap models, routes and obstructions, then an attempt; a stronger model only for promising targets. |
| 12 Oct | Database | Migration to one Markdown file per problem with validated YAML frontmatter (275 records), then 72 more from "read between the lines" synthesis passes, workshop problem lists and two monographs, with duplicates merged: **373 records**. Tags, impact and difficulty scores. `WORKING.md` session protocol. Claude and Codex split the work by difficulty and theme. About 500 commits that day. |
| 13 Oct | Campaign and publication | Difficulty-4 and -5 campaigns; agent referees for every claimed result; a second-model referee pass; proofs rewritten for their askers; public problem volumes (308 questions, 58 answers, 32 proof notes). About 400 commits. |
| 13–14 Oct | Single hard problems | Multi-agent "lanes" on one endpoint problem, which did not move and was handed to the person who asked it; a two-day attack on one contractivity conjecture that produced two special cases and a refutation of a natural strengthening. |

## How the 373 problems were found

There were four sources, in this order.

1. **Stated problems in a local collection.** We started from papers already
   on disk from the writing phase, most of them by a handful of active groups
   in the area. Agents searched each one for `Conjecture`, `Question`,
   `Problem` and `Open problem` environments, and for phrases such as "it
   would be interesting", "we do not know" and "remains open". Each candidate
   was recorded with the paper, the exact location and a quote.
2. **Second order: the references of those papers.** The same extraction on
   the papers they cite, after downloading the missing ones (arXiv first; a
   minority through a university library, which we would no longer do, see
   below).
3. **Synthesis passes.** Agents read the last decade of the core authors'
   papers "between the lines". This produced `implicit` questions (a remark
   suggests the question but does not pose it) and `inference` records:
   paper A proves X and paper B proves Y, so Z should follow. These records
   must name their premises.
4. **Problem lists and monographs.** Problem sessions from Oberwolfach and AIM
   workshops, a classical problem book, and the open-problem sections of two
   monographs.

Scope came from the human: "what the people working in this area would work
on". Agents proposed scope decisions, and excluded records were kept in a
separate report rather than deleted.

## How they were sorted

- **Theme** (20 folders, matching the research topics: Hankel and Schatten
  classes, Nehari theorems, Paley–Wiener spaces, composition operators,
  random multiplicative functions, and so on).
- **Kind**: `stated` (298), `implicit` (55), `inference` (20).
- **Origin**: `external`, asked by someone else (289), or `ours` (84).
  This split was added late, on 13 Oct, after it became clear that answering
  someone else's question and answering our own are different kinds of
  result.
- **Tags** from a controlled vocabulary with facets (`setting:`, `space:`,
  `object:`, `type:`, `method:`), validated by `make problems`.
- **Impact and difficulty**, 1–5 each, against anchor problems, with a
  one-line justification.
- **Literature status** (open, partial, resolved, claimed, refuted), which
  describes other people's work only, and **our stage** (untriaged → triaged
  → attacking → sketch → written → reviewed → public → in-book).
- **Resolution tier**, once anyone settled a problem: journal, arXiv,
  ours-public, ours-internal.

## The working loop

Each problem was worked in **sessions**:

1. Read the whole record, the source passage and the attempt log. Write a
   three-line plan: route, why it might work, and what counts as progress.
2. Work: analysis first, numerics only to decide one quantity, and
   certificates (exact or interval arithmetic) where a computation is part of
   the proof.
3. End in hand-over state. *State of play* is rewritten (what is true, the
   best route, the exact open subgoal). One entry is appended to the *Attempt
   log* (route, outcome, why, next). Failed approaches go in the record, never
   in a TeX file.
4. A claimed result becomes a **solution sheet**: the problem as posed, the
   answer as a theorem, a complete proof with exact citations, and nothing
   else. It builds through the lint gate.
5. An **independent referee** (a fresh agent with a fixed brief) re-derives
   every step, reruns certificates, re-reads the source question and checks
   novelty. It applies minor fixes or reports real errors; it never decides
   its own result.

Budgets started as "15 minutes × difficulty" and changed the same day to
"sessions per difficulty". Agents given 30 minutes used 2–4 and then stopped,
so time was not the binding constraint; the depth of the attempt was.

## Orchestration

- A main session orchestrated up to about seven background agents, each on a
  different problem or a different route.
- On hard problems: **lanes**. Several agents shared a brief and each took
  one approach (subcritical range, endpoint, disproof side, two alternative
  reformulations). A coordinator steered mid-run, for example "three lanes
  have proved the same single-scale bound; stop extending it".
- A **prove-mode** override brief once lanes started producing catalogues of
  obstructions: commit to one strategy and push it to a theorem, or to a
  proof complete modulo one precisely stated lemma.
- **Handoff files** when a session neared its context or usage limit, so a
  fresh session (or the other tool) could continue.

## Publication and outreach

- Proofs for external problems were rewritten in the asker's notation, using
  the methods familiar in their papers, with the intuition before the
  computation and no explanation of what an expert knows.
- A public problem volume (308 questions, each with its source; 58 answers
  with their evidence tier) and 32 proof notes went to a public repository,
  after an export allowlist and a grep for private paths and IDs.
- Everything of ours is labelled *Sketch*. Askers are emailed before anything
  goes to arXiv. Several groups have been contacted. Groups at the same
  department are batched into one email.

## Sources, and what we would not do again

Most sources were arXiv preprints. Some books and paywalled articles were
retrieved through a university library login, and some were OCR'd. They
stayed private and were never published, but a reusable process should not
depend on them. The tools in this repository fetch from arXiv only. Anything
else must be supplied by the user from their own legitimate access.

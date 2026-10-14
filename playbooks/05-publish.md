# Stage 5: Publish and contact

Nothing in this stage happens without the user's explicit approval for that
item.

## The labels

| Label | Meaning |
|---|---|
| Published | Proof in a refereed journal (someone else's or ours) |
| arXiv | Proof in a public preprint, not yet refereed |
| **Sketch** | Everything of ours not on arXiv or in a journal, however it was checked |

Our results are *Sketch* however they were checked, until they appear on
arXiv or in a journal.

## Writing for the asker

Before a result leaves the private workspace, rewrite it for the people who
asked the question:

- their notation and normalizations, taken from their papers;
- methods familiar to them where a choice exists;
- the idea before the computation;
- nothing an expert already knows; outline routine steps rather than spell
  them out;
- self-contained, except for results cited with exact numbers;
- no telltale signs of machine writing:
  - one-off variables;
  - defensive asides;
  - the same point explained twice;
  - headings that narrate;
  - bullet lists where prose would do;
  - negative parallelism, that is, a claim followed by a stack of "No X." fragments and a closing "Just Y.". State the point once, in full sentences;
  - colons used for drama;
  - "quietly" and "silently".

Then ask a second-model referee to read it as the asker would.

## Before anything leaves the workspace

- **The user signs off** that the statement proved matches the question
  asked. This is separate from refereeing the proof (Kallel and El Louadi,
  arXiv:2608.28997, §9).
- **The explain-it test:** the user confirms they could give a clear,
  expert-level talk on the result (Tao, arXiv:2608.16753, §8).
- **The exposition** sent to askers is one the user has read, understood and
  approved, not an unread agent-generated PDF (Bloom, *Changes to the Erdős
  problems web site*, 2026).
- **State the check level next to *Sketch*:** agent-reviewed, user-checked,
  or asker-checked.
- **Disclosure section.** Every PDF has a "Tool and computational resource
  disclosure" section. It names the models and their roles, and says what
  the user checked (Leiden Declaration).
- **Language.** Avoid "first", "we solved" and other ownership language.
  Novelty is at best an upper bound (Feng et al., §1.4).
- **Lean, where feasible.** Attach a Lean proof, and have a referee check
  that the formal statement matches the source.

## Exporting

- Publish **PDFs and certificate code only**. No TeX sources, notes, records
  or downloaded papers.
- Export through an allowlist script, never by copying a folder.
- Grep every PDF's text for private paths, record ids and file extensions
  (`.md`, `.tex`) before pushing.
- Put *Sketch* on page one, in the title block or the first line.

## Contacting authors

- The user writes the email; draft it if asked.
- One email per research group, not one per result. Colleagues in the same
  department get one batched message.
- Say plainly how the work was done (with AI agents, checked by the user)
  and what has *not* been checked.
- Nothing goes to arXiv before the askers have been told.
- Record the date in `told_authors`. Mark held items with a reason.

## Public language

When writing for the public, state what is known and how much stands behind
it, and link to the explanation: "x > y. A proof sketch, not checked by a
specialist, is at [link]." Once an expert stands behind it: "x > y; see
[paper]." No credit or scoreboard language: no "we solved", no "answered by
us", no counts of solved problems. Say plainly that nobody claims the results
and that anyone may develop them, crediting the people who asked the
questions. (After Bloom's change to the Erdős problems site, 6 October 2026.)

## Three routes to the literature

Which route fits depends on the user's standing in the field, and the user
decides. Do not push for one.

1. **Publish it yourself.** For a user with command of the result's
   research context who has checked it with colleagues. Add a disclosure of how it was found.
2. **Write it up with an expert.** For a user who has not yet acquired
   command of the result's research context, with a specialist who has checked the
   result and wants to develop it. Each supplies what the paper needs: the
   result and its proof, and the judgement of whether it is correct, new and
   worth reading.
3. **Show it to the askers and claim nothing.** Send the solution sheet,
   leave them free to use it, and expect at most an acknowledgement.

Having found or understood a proof is not the same as understanding its
research context: its claims, dependencies, relevant prior work, scope and
implications. Before route 1, the user takes the time to understand the result's
importance, formulation and framing, and what it means to the people who work
nearby; a fast result is not readiness to publish. Without that, use route 2
or 3.

All three are reasonable. Prepare every external result so that any of them
is easy: a self-contained sheet in the asker's notation, an honest account of
how it was checked, and no expectation attached.

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
- no telltale signs of machine writing: one-off variables, defensive asides,
  the same point explained twice, or headings that narrate.

Then ask a second-model referee to read it as the asker would.

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

# Stage 2: Triage

Goal: for each untriaged record, find out whether it is already settled,
score it once, and tag it. Use a cheap model; budget about 20 minutes per
record.

## 1. Literature check (the most valuable step)

- Search arXiv (listings and full text) for the last few years, and follow
  citations forward from the source paper, for example through Semantic
  Scholar or OpenAlex, both of which have open APIs.
- A verdict of "settled" or "partly settled" needs an arXiv id or DOI, the
  theorem number, and the statement quoted verbatim from the paper you
  opened. **No quote, no claim.**
- Read the latest version's abstract page. Check for withdrawals and errata.
  A withdrawn paper is never evidence of a resolution.
- Record what the paper does not cover (normalization, dimension, range of
  exponents) in one line.

Set `literature.status` (open, partial, resolved, claimed, refuted),
`literature.checked` (today's date) and `literature.evidence`. "Open" only
means that a bounded search on that date found nothing.

If it is resolved, set `resolution.tier` (`journal` or `arxiv`) and
`resolution.ref`, and stop. Mark `resolution.checked: true` only after
someone has read the proof.

## 2. Score once

Score against anchors you write down in `problems/SCORES.md`, with one
example problem per level.

- `impact` 1–5: how much the field would care.
- `difficulty` 1–5: expected effort with current tools, where 1 is a short
  argument from known tools and 5 is a major open problem.

Write both into `difficulty_initial` and `difficulty`, and give one line of
justification. **Never change `difficulty_initial` afterwards.** It is the
prediction that the outcomes will be measured against.

## 3. Tag

Use 3–6 tags from a controlled vocabulary in `problems/TAGS.md`, with facets
such as `setting:`, `space:`, `object:`, `type:` and `method:`. Add a
`method:` tag only for a credible route. If a tag is missing, add it to the
vocabulary first.

## 4. Finishability

For open records, write one line under *State of play*: the most plausible
route, and what would count as progress. Then set `stage: triaged`.

## Output

Report:

- counts by literature status;
- the records resolved by others, with references;
- a table of open records by `difficulty_initial` and impact;
- the records inside the human's difficulty window, which the human selects
  for attack.

# Schema review: why the database exists, and which fields earned their place

## Why we built a database at all

Until 12 October the problem list was a set of JSON catalogues, a ranking
file and a handoff note. Several Codex workers appended to the ranking at
the same time, and the next session could not tell what had been tried. Two
failures forced the change:

- **No memory between sessions.** Agents repeated routes that had already
  failed, because the failures lived only in chat transcripts.
- **No safe concurrency.** Claude and Codex, and several subagents of each,
  needed to edit the list at once.

The fix was one Markdown file per problem, with YAML frontmatter validated
by `make problems` and generated index pages. Most fields were then added
one at a time over the next 24 hours, each in response to a concrete need
(table below).

## Evidence

We measured each field in two ways.

- **Edits:** the number of commits that changed the field. This comes from a
  walk over all 772 commits touching the database, 12–14 October.
- **Fill:** how many of the 373 records have the field filled in on
  14 October.

A field changed in hundreds of separate commits was part of the daily work.
A field changed in one or two commits was filled in bulk and then left
alone.

| Field | Why it was added (date) | Commits changing it | Filled | Verdict |
|---|---|---|---|---|
| Body: State of play | Session protocol (12 Oct): "the next agent should not start blank" | 615 | ~300 | **Essential.** The memory between sessions. |
| Body: Attempt log | Same | 566 | ~300 | **Essential**, if the "why" is precise. |
| `ours.stage` | Migration (12 Oct) | 532 | 373 | **Essential.** Drives the next action. |
| `effort.sessions`, `effort.last` | Session protocol (12 Oct) | ~400 | 296 | **Useful.** Budgets and escalation run on it. |
| Body: Failed approaches | Rule that TeX holds results only (12 Oct) | 322 | 207 | **Essential.** Stops repeated dead routes. |
| `references` | Request to record papers that bear on a problem (12 Oct) | 319 | 260 | **Useful.** Overlaps `literature.evidence`. |
| `ours.artifacts` | Migration | 304 | 318 | **Useful.** Shows the referee what to open. |
| `literature.evidence` | Migration | 275 | 361 | **Essential.** Caught already-solved and withdrawn cases. |
| `ours.review` | Migration; required for `reviewed` | 273 | 271 | **Essential**, but it should name the model. |
| `ours.result_scope` | After overclaiming: "distinguish partial results" (12 Oct) | 230 | 221 | **Essential.** Only the referee should set it. |
| `ours.sign` | Migration | 198 | 372 | **Useful.** Powers the proof/counterexample analysis. |
| `literature.checked` | Migration | 158 | 373 | **Useful.** "Open" means nothing without a date. |
| `effort.parked` | Session protocol | 123 | 132 | **Useful.** Keeps dead problems off the queue. |
| `resolution.*` (tier, ref, checked, conditional_on) | Request for "levels of solved: journal, arXiv, ours" (12 Oct) | 66–82 | 205 | **Essential.** The public labels come from it. |
| `related` | Migration | 66 | 198 | Moderate. |
| `difficulty` | Request for "a difficulty… some starting points" (12 Oct) | 34 | 373 | **Useful**, but it was re-scored after attempts. Keep a frozen initial copy. |
| `scores_note` | Same | 426 (943 edits) | 373 | **Harmful as designed.** Escalations were appended to it, so it churned and went stale. Use it for the initial reason only, and log escalations in the attempt log. |
| `tags` | Request to classify (12 Oct) | 12 | 373 | Useful for the index; filled in bulk, almost never revised. |
| `impact` | Same | 2 | 373 | Filled once; used for ordering and picking. |
| `origin` | Request to split "did we ask this or did someone else" (13 Oct) | 1 | 373 | **Essential**, and it should have existed from day one. |
| `book_target`, `ours.book` | Request to link solved problems to the book (12 Oct) | 2 / 29 | 373 / 45 | Specific to this project. |
| `relevance` | Migration default | 41 | 93 | **Drop.** It duplicated impact and scores_note. |
| `effort.minutes` | Session protocol | 36 | 25 | **Drop.** Never recorded consistently. |
| `premises` | Migration, for inferences | 18 | 20 | Needed for inferences only. |
| `aliases` | Migration from the old catalogue | 4 | 310 | Needed only for migrations. |
| `ours.told_authors` | Outreach policy (12–13 Oct) | 3 | 6 | **Important but unused.** Nothing forced it. The publish step must check it. |
| `literature.claim_basis` | Announcements without a proof (12 Oct) | 4 | 5 | **Drop.** Fold into `evidence`. |
| `ours.abandoned_reason` | Migration | 4 | 4 | Only used together with `abandoned`. |

## Missing fields we wished we had

- **`source.form`**: whether the source poses the question as a conjecture,
  a numbered problem or question, an informal remark, or as our own derived
  question. We had to recover it from the location strings afterwards. It
  turned out to predict which answers mattered: all seven significant results
  answer a formally posed question.
- **`source.quote`**: the question verbatim. The rework of the public volume
  found altered quotations; a quote is cheaper to check than a page number.
- **`review.model`**: which model refereed. Same-model review is weaker, and
  this should be visible.
- **`difficulty_initial`**: frozen at triage, so that outcomes can be
  compared with a real prediction.

The lean schema in [`templates/record.md`](../templates/record.md) follows
these verdicts.

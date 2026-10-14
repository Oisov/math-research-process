# Schema review: which fields earned their place

Fill rates are over the 373 records on 14 October 2026. Usefulness is our
judgement after six weeks of agents, and me, reading these records.

## Most useful

| Field | Filled | Why |
|---|---|---|
| `source.paper` + `source.location` | 353 | Lets a referee re-read the question as posed. Overclaimed scope was our most common error, and this is the field that catches it. |
| `literature.status`, `.checked`, `.evidence` | 373 | A dated search with quoted evidence. It caught already-solved problems (most of difficulty 1) and a resolution resting on a withdrawn paper. "Open" without a date is meaningless. |
| `ours.stage` | 373 | The pipeline position; drives the index and the next action. |
| `ours.artifacts` | 318 | Where the notes, sheets and certificates live; what a referee opens. |
| `ours.review` | 271 | Who checked what, and the verdict. Required for `reviewed`. |
| `resolution.tier` + `.ref` + `.conditional_on` | 205 | Separates journal, arXiv and our own *Sketch* results, and tracks dependence on unrefereed preprints. The public volume labels come from it directly. |
| `origin` (external / ours) | 373 | Added late, should have been first. Our own questions are cheap to "answer"; external ones are what matter. |
| `kind` (stated / implicit / inference) | 373 | Honesty about how strongly the source poses the question. |
| Body: *State of play*, *Attempt log*, *Failed approaches* | ~300 | The memory between sessions. The most valuable text in the database. |

## Useful, but needs a change

| Field | Filled | Problem | Change |
|---|---|---|---|
| `difficulty` | 373 | Re-scored after attempts (73 records 4→5), so it ends up recording failure | Add a frozen `difficulty_initial`; keep `difficulty` as current |
| `impact` | 373 | Subjective, rarely used to choose work, though useful for the public volume's ordering | Keep, with anchors |
| `scores_note` | 373 | Goes stale: still says "agent inference, not verified" after a review | Shorten to a reason for the initial scores, and never touch it after |
| `told_authors` | 6 | Important but almost never filled, because nothing forced it | Make the publish step refuse without it, or without an explicit "held" note |
| `result_scope` | 221 | Essential, but it was set by the solver | Only the referee sets it |
| `tags` | 373 | Good for the index; the facet vocabulary grew to dozens of values | Cap the vocabulary; 3–6 tags per record |
| `references` | 260 | Useful for linking related work, but overlaps `literature.evidence` | Keep `evidence` for "settles it" and `references` for "bears on it" |
| `effort.sessions`, `.last`, `.parked` | 296 | Sessions and parked status were used. | Keep these |
| `effort.minutes` | 25 | Almost never recorded | Drop |

## Least useful

| Field | Filled | Verdict |
|---|---|---|
| `relevance` | 93 | Duplicated `impact` and `scores_note`. Drop. |
| `literature.claim_basis` | 5 | Too fine a distinction (announcement versus manuscript). Fold into `evidence`. |
| `premises` | 20 | Needed, but only for `kind: inference`. Keep it conditional. |
| `abandoned_reason` | 4 | Rare; fine as conditional on `stage: abandoned`. |
| `book_target`, `ours.book` | 45 | Specific to our book project. Project-specific, not generic. |
| `aliases` | 310 | Needed only because of the migration from an older catalogue. Keep it for migrations; a fresh project barely needs it. |
| `sign` (proof / counterexample / determination / unclear) | 372 | Cheap and used for public labels, but 87 are "unclear". Optional. |

## Missing fields we wished we had

- **`source.quote`**: the question verbatim. The public volume rework found
  altered quotations, and a quote is cheaper to check than a page number.
- **`review.model`**: which model refereed. Same-model review is weaker, and
  this should be visible.
- **`difficulty_initial`**: see above.
- **`next`**: the concrete next step, as a field. It lives in the attempt
  log's last entry, and agents often did not find it.

The recommended lean schema is in
[`templates/record.md`](../templates/record.md).

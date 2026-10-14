# Stage 3: Attack

Goal: a proof, a counterexample, or a precise obstruction, for one problem at
a time. Breadth is cheap and worthless here. What counts is depth: several
genuinely different routes, each pushed until it either works or fails for a
reason you can state.

## Starting a session

1. Read the whole record, the source passage it quotes, every artifact it
   lists, and the full attempt log. Do not repeat a route the log marks as
   dead unless you say how you get past the recorded obstruction.
2. Read the papers the source relies on. Results in an active area are often
   two known theorems combined in a new way.
3. Write a three-line plan into the attempt log: the route, why this one, and
   what would count as progress.

## During the session

- **Analysis before search.** Check claims by hand. Use numerics only to
  decide one named quantity, or to test a conjecture on small cases before
  trying to prove it. Every computation is time-bounded and prints progress.
- **At least three different routes** before you park a problem. Different
  means a different idea, not a different parameter.
- **Prove, do not catalogue.** A map of what fails is not progress. If you
  find yourself proving more and more special classes of the claim, stop and
  ask whether the approach can ever reach the full statement.
- **Prove-mode** (when the user asks for a proof): commit to the single
  strategy most likely to give a proof. Push it to a theorem, or to a proof
  that is complete except for one precisely stated lemma. Report only that.
- **Certificates.** If a computation is part of the proof, use exact or
  outward-rounded arithmetic, cover the whole parameter range, handle tails
  analytically, and make it run in seconds. Put it in `code/`.
- **A counterexample counts.** If evidence turns against the conjecture,
  look for a disproof as seriously as for a proof.

## Before claiming a result

- Re-read the question in its source, not in the record's paraphrase. Check
  the quantifiers: every p versus some p, a given object versus some object.
- Decide honestly whether your result is full or partial. Name the open part.
- Search once more for prior work on exactly your statement.

## Archiving the claim

The moment a model claims a result, before any rewriting, save its response
verbatim to `discoveries/<ID>.md` using
[`templates/discovery.md`](../templates/discovery.md): model, date and time,
session, the prompt it answered, and the response. If the result is later
published, this records who found what and when. If verification shows the
claim is false, the file is deleted.

## Writing it up

A claimed result becomes a **solution sheet**
([`templates/solution-sheet.tex`](../templates/solution-sheet.tex)): the
problem as posed, the answer as a theorem, a complete proof with exact
citations, and nothing else. Write it in the asker's notation. Build it with
`make pdf TEX=solutions/<ID>.tex`; it must pass the lint gate without
warnings. Set `stage: written` and list it in `artifacts`. Then
request a referee (stage 4); never review your own work.

## Keeping the files few

- Append to `notes/<ID>.md`; never start `notes/<ID>-attempt3.md` or
  `<ID>-agentB.md`.
- Run exploratory numerics from the scratchpad, and record the one number
  that matters in the record.
- If you rewrite a solution sheet, overwrite it; the history keeps the old
  version.

## Ending a session

- Rewrite *State of play* (5–10 lines): what is known, the reductions proved,
  the best route, the exact open subgoal. A cold reader must be able to start
  from this alone.
- Append one entry to the *Attempt log*:
  `- <date> · route: … · outcome: dead end | partial | promising | solved | counterexample · why: … · next: …`
  The **why** is the valuable part. "Schur test fails" is useless. "Schur
  test with weight x^-1/2 loses a log because the row sums diverge at the
  diagonal; any weight must vanish to order 1/2 there" saves the next agent
  the whole attempt.
- Add failed routes to *Failed approaches*, one line each, with a repair if
  you see one.
- Update `effort.sessions` and `effort.last`, and run the record check.

## Parking

The session budget is the difficulty: 1 to 4 sessions for difficulty 1 to 4.
A problem that uses its budget without a full answer moves to difficulty 5.
Difficulty 5 problems are worked only with a specific new idea; park them
(`effort.parked: true`) after that, or after six sessions without even a
partial result, or when the user decides. Write in State of play what would justify reopening
it: a specific new idea, a new paper, or a specific lemma.

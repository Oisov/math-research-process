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
   what would count as progress against the brief's objective (map or
   settle; see below).

4. Search the literature again before attacking, even though triage
   already did. Then check your restatement of the question against the
   source's examples and its known special cases (FAR, arXiv:2608.16977,
   §3.2; AlphaProof Nexus, arXiv:2605.22763, §3).
5. Briefs say "prove or disprove", unless the user has switched the problem
   to prove-mode. An agent told to prove a false statement will paper over
   the gap (arXiv:2602.03837, §9.2).

## During the session

- **Analysis before search.** Check claims by hand. Use numerics only to
  decide one named quantity, or to test a conjecture on small cases before
  trying to prove it. Every computation is time-bounded and prints progress.
- **At least three different routes** before you park a problem. Different
  means a different idea, not a different parameter.
- **Measure progress against the current objective.** The brief states one
  of two objectives. When the objective is to *map* the problem (triage, or
  a first session on a problem nobody has looked at), a reduction, a special
  case or a precise obstruction is progress: the goal is to know where the
  problem stands. When the objective is to *settle* it, none of these is
  progress; only a theorem, or a proof complete except for one precisely
  stated lemma, counts. If the brief does not say, ask. If you find yourself
  proving more and more special classes of the claim under a settle
  objective, stop and ask whether the approach can ever reach the full
  statement.
- **Prove-mode** (when the user asks for a proof): commit to the single
  strategy most likely to give a proof. Push it to a theorem, or to a proof
  that is complete except for one precisely stated lemma. Report only that.
- **Certificates.** If a computation is part of the proof, use exact or
  outward-rounded arithmetic, cover the whole parameter range, handle tails
  analytically, and make it run in seconds. Put it in `code/`.
- **A counterexample counts.** If evidence turns against the conjecture,
  look for a disproof as seriously as for a proof.

- **Classify a failure before switching route.** Is it an execution error
  (the plan is sound), a structural gap in the plan, or a sign that the
  approach is fundamentally flawed? Write the class in the attempt log
  (QED, arXiv:2604.24021, §4.2).
- **A dead end names a concrete defect.** "Too long" or "too hard" does not
  count (LeanMarathon, arXiv:2606.05400, §4.7).
- **Narrowing is not progress.** If the outcome is "reduced to a narrower
  question" twice in a row with no new idea, count it as no progress. Park
  the problem, or ask the user (Gowers, *What sort of maths are LLMs good
  at?*, 2026).
- **Disproof methods.** On the disproof side, work through:
  - off-the-shelf examples;
  - examples with free parameters (metavariables);
  - trying to prove the opposite;
  - successive approximation;
  - random examples;
  - generic examples (Gowers, same post).
- **No placeholders.** If a prerequisite is missing, park the problem. Never
  substitute a dummy object that only looks like the real one.

## Before claiming a result

- Re-read the question in its source, not in the record's paraphrase. Check
  the quantifiers: every p versus some p, a given object versus some object.
- Decide honestly whether your result is full or partial. Name the open part.
- Search once more for prior work on exactly your statement.
- **An easy proof is a warning.** First look for a misreading: a
  convention, a quantifier, a domain. If the statement is ambiguous, the
  user asks the asker before anything is claimed (AlphaProof Nexus,
  arXiv:2605.22763, §3–4).
- **Asymptotic results.** An asymptotic answer is partial when the original
  question requires all parameter values or an explicit effective threshold
  and those requirements remain unresolved. A bound "for all sufficiently
  large N" fully answers a question that asks for an order of growth. A
  counterexample at a case the asker would exclude does not
  settle the question (Le Duc and Liberti, arXiv:2510.12829, §5.2).
- **End with one outcome label**, recorded in the attempt log:
  - KNOWN: the answer is already in the literature;
  - NEW: a new answer;
  - FIX: the statement as written is defective; record the counterexample
    and the minimal repair as a new record with `form: ours`;
  - NONE: no answer.

  (FAR, arXiv:2608.16977, §3.2.)

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

## Writing standards for the sheet

- Put the verbatim source quote directly above the theorem.
- For every citation, quote the cited statement and check each of its
  hypotheses. Hallucinated "standard" lemmas are a known failure (QED,
  arXiv:2604.24021, §4.3; AlphaProof Nexus, §3).
- Name the key step. Inside it, do not use "clearly", "obviously" or
  "straightforward" (QED, §4.4).

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

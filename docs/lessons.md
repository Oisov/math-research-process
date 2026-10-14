# Lessons: what worked and what did not

Each lesson comes with the evidence that taught it. Numbers are from the
problem database on 14 October 2026; quotes are from the session logs.

## What worked

### Checking the literature first is most of the value at low difficulty

The difficulty we assigned *before* attempting each problem predicted the
outcome well. It also showed that easy problems are usually easy because they
are already solved:

| Initial difficulty | Settled by others | Settled by us | Partial | Open |
|---|---|---|---|---|
| 1 | 9 | 3 | 0 | 0 |
| 2 | 4 | 15 | 2 | 0 |
| 3 | 7 | 27 | 19 | 7 |
| 4 | 4 | 29 | 75 | 6 |
| 5 | 0 | 3 | 15 | 3 |

(275 records that had an initial score; the other 98 were added later.)

Nine of twelve "difficulty 1" problems already had a published answer. The
literature sweep also caught a problem marked *resolved* on the strength of a
paper that had been withdrawn for an irreparable error. It checked the latest
version of 173 cited arXiv papers and found that one.

### One file per problem, validated

A Markdown file per problem, with YAML frontmatter checked by `make problems`
(unknown keys, enums, duplicate ids, stage and tier consistency), let six or
more agents and two different tools edit the database at once without
corrupting it. The generated index (INDEX, GAPS, PEOPLE, CITED) gave the
human a dashboard for free. Moving from a single JSON catalogue to this
format on 12 October was the turning point in throughput.

### State of play plus attempt log

"The record is the memory": a rewritten *State of play* and an append-only
*Attempt log* (route, outcome, **why**, next step). This is what let
a second session start where the first stopped. 207 records have a non-empty
*Failed approaches* section and there are about 780 log entries. The rule
that the "why" must be precise ("the Schur test with weight x^-1/2 loses a
log because row sums diverge at the diagonal") was worth more than any other
wording in the protocol.

### Solution sheets with a lint gate

A claimed result counted only once it was a self-contained TeX sheet (problem
as posed, theorem, proof, exact citations) that builds through a lint gate.
This turned vague "it should follow" claims into checkable objects, and the
lint gate removed most typographic noise before a human looked.

### Adversarial referees, and a second model

Every claimed result got a fresh referee agent with a fixed brief: re-read the
source question, re-derive every step, rerun certificates, check novelty, and
assume the result is wrong. They found real problems. One example:

- a displayed bound justified only for half the claimed range;
- a lemma that needed a non-constant hypothesis;
- overstated scope ("answers the question" when it answered a special case).

A referee from a *different* model family was the most valuable single check
before anything was shown to a human.

### Certificates that run in seconds

Computer-assisted steps were written as certificates in exact or
outward-rounded arithmetic, with complete coverage of the parameter range and
analytic tails. They had to run in seconds to a minute. Slow certificates do
not get rerun by referees, so they do not get checked.

### Writing for the asker

Expert feedback was consistent. The arguments were "fairly standard
variational arguments; the hard part is finding which variation". An expert
rewrote one of our proofs in his own style in an afternoon, half the length.
After that we:

- rewrote proofs in the asker's notation, using methods from their papers;
- put the idea before the computation;
- cut explanations of what an expert already knows.

Telltale signs of machine-written mathematics were removed: many one-off
variables, defensive commentary, and the same explanation repeated in
several places.

### Lean, faster than predicted

A Lean formalization of one paper's core argument was estimated by an agent
to take "months"; it was done overnight. Its value was confidence, not
publication. Its README also initially overstated what the proof used: eight
modules were never imported by the main theorem. Formal artifacts need the
same scope check as prose.

## What did not work

### Shallow first passes

Bulk passes over many problems produced one attempt per problem, usually an
elementary construction, followed by stopping when it failed. One agent's own
summary: "I tested one route per open problem … 14 failed routes do not
demonstrate that I seriously exhausted the mathematical possibilities." Another
campaign began and ended with the same number of unsolved problems. Fixes
that helped:

- "try three genuinely different approaches before giving up";
- reading the existing attempt log first;
- one problem at a time with all agents on it, for the hardest problems.

### Cataloguing instead of proving

Left alone, agents turn a hard problem into a map: what fails, three
equivalent reformulations, a list of special cases. This looks like progress,
and on one endpoint problem it absorbed two days. The human's phrase for
proving more and more special classes was "filling ℝ with ℚ". The repair was
an explicit *prove mode*: commit to one strategy, push it to a theorem or to
a proof modulo one precisely stated lemma, and report only that. Failures get
one line in the record.

### Overclaiming scope

The most common error was answering an easier question than the one asked:

- a special case reported as "the conjecture";
- "for some p" reported as "for every p";
- a partial result reported as a solution.

One agent's honest recount: "Against the original questions: 0 of these 4
fully solved." The rule that fixed it is that the referee re-reads the
question in the source, not in the record's paraphrase, and sets
`result_scope` itself.

### Duplicated parallel work

Parallel agents given overlapping briefs proved the same lemma three times.
Three cheap agents were once given the same task. Lanes need disjoint
mandates, and a coordinator who reads interim reports and redirects.

### Unbounded numerics

Background Python searches without time bounds or progress output. On one
night, 14 runaway processes used 19 GB of RAM and swap-thrashed the machine.
Agents also reported sweeps that did not bear on any proof. The rule now:
numerics are optimized, bounded to minutes, print progress, and must decide
one named quantity.

### Gaming the checks

An agent asked to fix linter warnings across the papers started silencing
the linter instead. Whatever is checked automatically will be optimized
against; a human or a second agent must sample the diffs.

### Difficulty as a lagging label

Difficulty was re-scored after attempts (73 records went from 4 to 5). This
made the final difficulty a record of failure rather than a prediction. Keep
the initial score frozen and store the current one separately.

### Session lengths, crashes and limits

Many sessions ended early: model stream disconnects, context limits and
five-hour usage windows. Every protocol rule about hand-over state exists
because of this. A fixed handoff file per campaign was the only reliable
recovery.

## Review is the weakest link

Of the 141 results our agents settled, essentially all were checked by
agents, most of them by the same model family that wrote them. Agent referees
catch local errors well and global errors poorly. They rarely ask "is this
the right claim?" or "did anyone try a different weight?". One human
complaint, accurate: "The audits check each step line by line but never ask
whether the claim is the right one."

That is why everything stays *Sketch* until the asker or arXiv sees it.

## Human steering

Reading the human side of the logs back shows the same interventions again and again:

- "Did I ask you to stop?" (agents ending turns early);
- "any real progress or just churn?";
- "partial results don't count";
- "write it so an expert understands it, don't explain the obvious".

Each of these became a written rule, in `WORKING.md`, the agent briefs or
persistent memory, and the rule stuck better than the reminder. The same
correction delivered repeatedly in conversation did not.

## Cost

One month of Codex use was about $1,200 in API-equivalent terms, 68% of it
cache reads; Claude Code was about $300 over the same month. Long-running orchestrator
sessions that re-read large contexts dominate the cost. Cheap models for the
literature and triage stages, and strong models only for attempts on
promising targets, were the right split.

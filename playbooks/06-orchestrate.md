# Orchestrating several agents

The orchestrator runs stages 1–4 across many problems with background agents.
It does not do the mathematics itself. It assigns work, reads interim
reports, redirects, and keeps the database consistent.

## Allocation

- **Cap concurrent agents** at a number the user sets (we used about 7).
  Do not stop an agent that is working productively just to meet a schedule.
- **Model by stage.** Use cheap models for harvest, triage and literature
  checks, and strong models for attempts on problems that survived triage.
  Use a different model family for referees.
- **Disjoint mandates.** Each agent works on a different problem, or on one
  problem in a different lane: say the subcritical case, the endpoint, the
  disproof side, or an alternative reformulation. Two agents must never be
  given the same task.
- **Disjoint files.** Each agent edits only its own records and folders. Tell
  it which.

## Briefs

A brief is self-contained: the record path, the files to read first, the
lane, what counts as success, what not to touch, and the hard rules from
`AGENTS.md`. Do not tell agents about time limits; manage time yourself.

## Steering

- Read every interim report. Redirect when:
  - lanes duplicate each other: "Lane C owns this lemma; cite it";
  - an agent is cataloguing rather than proving: switch it to prove-mode;
  - numerics are running without a question they answer.
- When an agent reports success, send the claim to a referee before you
  report it to the user.
- Report to the user against the original questions: full, partial or no
  progress. Partial results are not solutions.

## Hand-over

Keep `problems/HANDOFF.md` current: which agents are running on what, what
is waiting for review, and the next queue. Sessions end without warning.

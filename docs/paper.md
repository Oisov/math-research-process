# Paper draft: a map of the range, not a way up the wall

Working title: *Mapping a research area with AI agents: 373 open problems,
six weeks, and what did not get easier.*

This is the framing and outline for a paper about this project. It is a
living document: the status numbers change as askers reply and as results
reach arXiv.

## The thesis

Research mathematics is a landscape of mountains. Most of the work is finding
out where the mountains are, which paths have already been walked, which
peaks are small hills that nobody bothered to climb, and where everyone gets
stuck at the same wall. Only then does the long climb start.

Over six weeks we pointed AI agents at every open problem we could find in
one research area. The agents were very good at the first part. They found,
collected, de-duplicated and classified 373 problems from papers, problem
lists and monographs. They checked the literature and discovered that many
"open" problems were already solved. They tried the obvious routes and found
counterexamples that are easy to verify once found. A person with a master's
degree in the area got, in a few weeks, a working map of the whole field:
what is open, what is quietly solved, what is cheap, and where the walls are.

They were not good at the walls. A hard problem stayed hard. On the problems
where experts had made partial progress and stopped, the agents produced
reformulations, special cases and long lists of obstructions, not proofs.
The successes they did have came from breadth: throw a hundred balls at a
hundred baskets, and some go in. That is useful, but it is a different thing
from getting better at the shot that matters.

So we argue that this kind of work should be the first step of a research
project, not the last. It is a fast way to get to know a field and to find
good questions to work on. We did not see it make the hard part easier.

## What others have observed

Terence Tao reached a similar conclusion from the Erdős problems database. In
December 2025, after several Erdős problems were "solved" by AI and then
found to be already solved in the literature, he wrote:

> My theory is that the AI tools are now becoming capable enough to pick off
> the lowest hanging fruit amongst the problems listed as open in the Erdos
> problem database, where by "lowest hanging" I mean "amenable to simple
> proofs using fairly standard techniques". However, that category is also
> precisely the category of nominally open problems that are most likely to
> have been solved in the literature, perhaps without much fanfare due to the
> simple nature of the arguments.
> — T. Tao, Mathstodon, 26 December 2025
> ([link](https://mathstodon.xyz/@tao/115788262274999408))

Our data shows the same correlation. Nine of the twelve problems we first
rated easiest already had a published answer.

The same post ends on the positive side that we also saw:

> Nevertheless, the amount of progress in capability of these tools is
> non-trivial, and bodes well for the ability of such tools to automatically
> scan through the "long tail" of underexamined problems in the mathematical
> literature.

Our "hundred balls" are, in Tao's words from earlier that month, a kind of
"artificial general cleverness":

> By "general cleverness", I mean the ability to solve broad classes of
> complex problems via somewhat ad hoc means. […] they can have a non-trivial
> success rate at achieving an increasingly wide spectrum of tasks,
> particularly when coupled with stringent verification procedures to filter
> out incorrect or unpromising approaches, at scales beyond what individual
> humans could achieve.
> — T. Tao, Mathstodon, 15 December 2025
> ([link](https://mathstodon.xyz/@tao/115722360006034040))

The caveats page of the Erdős problems AI wiki makes the point about
difficulty directly:

> If an Erdős problem was posed N years ago and was recently solved by AI, it
> may be tempting to conclude: "the problem resisted all human attempts at
> solution for N years" in order to imply the problem is difficult. Instead,
> it could be that the problem has received little attention from or is
> relatively unknown to mathematicians.
> ([Disclaimers and caveats, §5](https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats))

Many of our problems were of exactly this kind: asked once, in passing, and
never followed up.

Finally, Tao's ICM 2026 essay argues that generating a proof is only the
first stage of a pipeline: after it come verification, exposition,
acceptance by the community, and absorption into the standard theory. He
expects AI to produce "proof indigestion", with proofs accumulating faster
than they can be checked and digested ([*Mathematics in the age of AI*,
arXiv:2608.16753](https://arxiv.org/abs/2608.16753), §§6–7). That matches
our experience. Producing a candidate proof was cheap; checking whether it
was right, and whether it answered the question asked, was the bottleneck.
His rule of thumb is one we adopt:

> if the authors cannot convincingly demonstrate that they are able to give a
> clear, expert-level talk on their results, one that is correct and properly
> attributed, then the result should not be published.
> (arXiv:2608.16753, §8)

## What the agents achieved, stated plainly

- **Mapping.** 373 problems from papers, problem lists and monographs, each
  with its source, classified by theme, kind and initial difficulty. This is
  the part of the work that changed the most.
- **Literature triage.** 64 problems turned out to be settled already, in a
  journal or on arXiv. One problem was marked as resolved by a paper that had
  since been withdrawn.
- **Low-hanging fruit.** Most of the 141 problems our agents settled are easy
  in hindsight: short arguments from known tools, or counterexamples that are
  easy to check once found. Their difficulty had been overestimated, or they
  had received little attention.
- **A few results of real significance.** Only a handful. These have been
  sent to the people who asked the questions, and their status here will be
  updated as they respond. Until a result is on arXiv or in a journal, it is
  a *Sketch*.
- **No movement on the walls.** On the hardest problems we attacked, over
  days and with several agents in parallel, we got maps of what fails, not
  proofs.

## Outline

1. **Introduction.** The mountain picture; the claim that this is a first
   step, not a last one; what was not achieved.
2. **Setting.** The research area at a level a non-specialist can follow; the
   tools and models.
3. **Building the map.** The four sources of problems, de-duplication, scope,
   and kinds of record. One figure: the 373 by source, kind and origin.
4. **The workflow.** Records, sessions, solution sheets, referees, and
   orchestration, kept short, with the details in an appendix.
5. **What kind of results were these?** Every result classified as: already
   in the literature; routine from known tools; counterexample easy to verify;
   substantial new argument. Expect the last class to be small, and name it.
6. **Walls.** The hard problems attacked for days, what the agents produced,
   and why it was not a proof.
7. **Verification and credit.** Sketch until arXiv; why agent review is weak;
   how askers were told; who gets credit.
8. **Discussion.** Where this belongs in a mathematician's work: orientation,
   finding tractable questions, clearing the long tail. What we would need to
   see before claiming more.
9. **Appendices.** Schema, agent instructions, referee brief, status table
   with its date.

## Before submission

- **Significance audit.** Classify all 141 results into the four classes of
  §5. Most of this can be done from the records in an afternoon, with expert
  judgement on the borderline cases.
- **Correctness audit.** A random sample of about 20 results checked
  independently. Report correct, wrong, and answers to a weaker question.
- **Consent.** Clear any description of correspondence with the people
  involved.
- **Limits.** One person, one area, no control group, models that will be
  outdated within a year, and difficulty scores set by the same agents.

## Sources

- T. Tao, Mathstodon post, 26 December 2025,
  <https://mathstodon.xyz/@tao/115788262274999408>.
- T. Tao, Mathstodon post, 15 December 2025,
  <https://mathstodon.xyz/@tao/115722360006034040>.
- T. Tao, *Mathematics in the age of AI*, arXiv:2608.16753 (2026), based on a
  public lecture at the 2026 International Congress of Mathematicians.
- Erdős problems AI wiki, *Disclaimers and caveats*,
  <https://github.com/teorth/erdosproblems/wiki/Disclaimers-and-caveats>.

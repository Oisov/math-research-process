# Deep significance assessment of four settled problems

You assess how significant our answer to each of four open problems is, as a
specialist in the field would judge it. A quick blind grading has already been
done from the records alone. This pass must use the literature.

Repository: /home/oisov/git/github.com/nehari-thesis (read-only for you).
Each record is at research/problems/<theme>/<ID>.md; find it with
`ls research/problems/*/<ID>.md`. Its `ours.artifacts` lists the solution
sheets (.tex). Its `source` names the paper that posed the question.

Rules:
- Do not edit, create or delete any file in the repository. Do not run git
  or jj. Do not open research/significance-audit/ or any earlier grading.
- Web searches and fetching public pages (arXiv, Semantic Scholar API,
  journal pages, MathOverflow, Google Scholar results) are allowed. Send
  nothing else outside: no emails, no uploads, no posting.
- Budget: about 15–25 minutes per record. Stop searching when more searching
  stops changing the grade.

For each record, work through:
1. **The question as posed.** Read the source passage (the PDF or .txt under
   reference/ if present, otherwise arXiv). Quote it. Is it a numbered
   conjecture or problem, a question in the introduction, or an aside? Did the
   authors call it important, central or difficult?
2. **Standing.** Venue and age of the source. Citation count of the source
   (Semantic Scholar API: https://api.semanticscholar.org/graph/v1/paper/arXiv:<id>?fields=citationCount,venue,year).
   Is the question restated in surveys, problem lists, later papers or talks?
   Who has attempted it, with what partial results? Search for the
   question's key phrases.
3. **Is it really open, and is our answer new?** Search for later work that
   answers it or contains our key idea. Note anything close.
4. **What our answer takes.** Read the theorem statement and the proof
   outline in the solution sheet. Is it a new idea, a clever use of known
   tools, a routine argument, or a computer certificate? Is it full or
   partial, conditional on unrefereed work?
5. **Consequences.** Does the answer settle other questions, change a
   programme, or close a gap in a published theorem?

Grade on mathematical content and standing only, never on how it was found:
- **H**: a specialist would call it a genuine contribution: a standing,
  formally posed question with real attempts or prominence, answered fully
  with a non-routine argument. Paper-worthy on its own in a good journal.
- **M**: a real answer to a real question, but the question is niche or
  recent, or the argument is short or routine. Note-sized.
- **L**: a minor, literal, degenerate or conditional answer, or one with
  little standing.

Reply with, for each record, a dossier of 120–200 words: the quoted
question with its location, the standing evidence with numbers and links,
any close prior or later work, what the argument takes, then the grade, a
confidence (high / medium / low) and the one fact that would change the
grade. End with a four-row table: ID | grade | confidence | one-line reason.

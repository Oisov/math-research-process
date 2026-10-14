# What we recommend

The short version, in priority order. Each point comes from
[lessons.md](lessons.md).

## Before you start

1. **Decide scope as a sentence you sign off**, for example "what the
   people working on Hardy spaces of Dirichlet series would work on". Keep
   excluded candidates in a report instead of deleting them.
2. **Open sources only.** Harvest from arXiv through its API, at its rate
   limit. Anything else comes from the user's own legitimate access and never
   leaves the private repository.
3. **Set the publication rule on day one.** All your results are *Sketch*
   until they are on arXiv or in a journal. Askers are contacted before
   anything goes to arXiv. Write it into the agents' instructions, because
   agents will otherwise call things "proved".

## The database

4. **One Markdown file per problem**, with validated frontmatter and
   generated indexes. Use the lean schema in
   [`templates/record.md`](../templates/record.md).
5. **Record the question verbatim with its location.** Every later step is
   checked against it.
6. **Freeze the initial difficulty.** It predicts outcomes. The re-scored one
   records history.
7. **Separate `origin: external` from `ours` from the start.**

## The pipeline

8. **Harvest everything, filter later.** Extraction is cheap; difficulty
   guessed before a literature check is noise. Apply your difficulty window
   (`min`–`max`) when choosing what to *attack*.
9. **Literature check before any attempt**, against the latest arXiv
   version, with forward citations. At difficulty 1–2 this check is most of
   the work: most easy problems are already solved.
10. **Attack with depth, not breadth.** At least three genuinely different
    routes before parking. All agents on one problem for the hardest ones,
    each in a disjoint lane. Read the attempt log first.
11. **Prove, do not catalogue.** Failures get one line and a reason in the
    record. Only results get TeX.
12. **Analysis before numerics.** Numerics decide one named quantity,
    bounded to minutes, with progress output. Certificates use exact or
    outward-rounded arithmetic and run in seconds.
13. **Solution sheet before "solved".** Problem as posed, theorem, complete
    proof, exact citations, nothing else.

## Review

14. **An adversarial referee re-reads the source and sets the scope.** The
    solver never marks its own result reviewed.
15. **Cross-model review** for anything a person will read. Record the model
    in the review field.
16. **A human expert is the only real check.** Budget for it: the asker, a
    supervisor or a colleague.

## Writing and outreach

17. **Write for the asker**: their notation, their methods, intuition first,
    nothing an expert does not need. Remove model tells: one-off variables,
    defensive asides, repeated explanations.
18. **Contact askers early and briefly.** Results in an active area are found
    in parallel; in our case one was found independently, also with AI, in
    the same week. One email per research group, not one per result.
19. **Publish PDFs, not sources**, through an allowlist export with a leak
    grep for private paths and IDs.

## Orchestration

20. **Cap concurrent agents** (about seven for us) and give each a disjoint
    mandate. A coordinator reads interim reports and redirects.
21. **Cheap models for harvest and triage; strong models for attempts** on
    targets that survived triage.
22. **Write rules into files, not chat.** Repeated corrections in
    conversation did not stick; the same correction in `AGENTS.md` or the
    protocol did.
23. **Hand-over state at all times.** Sessions die from limits and
    disconnects; the record must let a fresh agent continue.

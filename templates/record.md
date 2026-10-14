---
id: AB-9.2                    # <source initials>-<number>, or a short slug for inferences
title: One line
kind: stated                  # stated | implicit | inference
origin: external              # external (asked by others) | ours
theme: hardy-spaces           # one folder per theme
source:                       # for stated and implicit
  paper: "arXiv:2303.12345v2" # the version you read
  location: "Conjecture 9.2, p. 31"
  posed_by: [Author, Author]
  form: conjecture             # conjecture | problem | question | remark (stated informally) | ours
  quote: >-
    The question verbatim, copied from the PDF.
premises: []                  # inference only: [{paper, location, result}]
references: []                # papers that bear on it: [{paper, location, relevance}]
literature:
  status: open                # open | partial | resolved | claimed | refuted (other people's work only)
  checked: 2026-10-14         # date of the bounded search
  evidence: []                # "arXiv:… Thm 1.3 proves the case p>1", with a quote in the body
ours:
  stage: untriaged            # untriaged | triaged | attacking | written | contested | reviewed | public | abandoned
  sign: null                  # proof | counterexample | determination (set when settled)
  result_scope: null          # full | partial (set by the referee)
  artifacts: []               # notes, sheets, certificates
  review: null                # {by, model, date, verdict}
  public: null                # path of the public PDF
  told_authors: null          # date and how; or "held: <reason>"
resolution: null              # {tier: journal|arxiv|ours-public|ours-internal, ref, checked, conditional_on: []}
impact: null                  # 1-5
difficulty_initial: null      # 1-5, set once at triage, never changed
difficulty: null              # 1-5, current
scores_note: null             # one line at triage, never edited; log escalations in the Attempt log
tags: []                      # 3-6 from TAGS.md
effort: {sessions: 0, last: null, parked: false}
related: []
---

## Statement

The problem exactly as posed, with the notation defined.

## State of play

Rewritten each session: what is known, reductions proved, the best route,
the exact open subgoal. A cold reader starts from this alone.

## Failed approaches

- One line per dead route, with the reason it failed and a repair if one is visible.

## Attempt log

- 2026-10-14 · route: … · outcome: dead end | partial | promising | solved | counterexample · why: … · next: …

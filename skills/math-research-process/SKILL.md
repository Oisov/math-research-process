---
name: math-research-process
description: Map the open problems of a research area in mathematics and work on them with AI agents, then share the results honestly. Use when the user wants to harvest open problems from papers, authors or an arXiv query, build a problem database, triage it, attack problems with agents, referee claimed answers, or decide how to share or publish them.
---

# Finding, sharing and vouching for results in mathematics

You help one person, the user, map the open problems of an area of
mathematics and work on them with AI agents. The user directs; you and your
subagents do the reading, the attempts and the bookkeeping. The full method,
with playbooks, templates and tools, is in the process repository
(github.com/Oisov/math-research-process). If it is in the workspace, read its
`AGENTS.md` first and the playbook for the stage you are asked to do. This
file is the short version.

## The position behind the method

Keep three acts apart.

- **Finding** a result is cheap now, and agents do most of it.
- **Sharing** a result means saying what is known, how much stands behind it
  and where the explanation is, and leaving anyone free to develop it.
  Sharing claims no priority. It still carries responsibility for describing
  the statement, its source and its checks accurately.
- **Vouching** for a result, standing behind it as correct, new and worth
  reading, needs command of its research context: its claims, dependencies,
  prior work, scope and implications. It is what an arXiv post or a paper
  says. Understanding a proof, or even finding it, is not the same.

Agents bring results within reach before the user has that command. Do not
treat a fast result as readiness to publish. The user decides between three
routes: publish it themselves once they have the command; develop it with a
specialist who has it, until both can stand behind the paper; or share it
openly and claim nothing.

## Inputs to ask for once

A one-sentence scope; seeds (papers, authors with a date window, or an arXiv
query); depth (seeds only, or also the papers they cite); the difficulty
window to attack; the cap on concurrent agents; and the workspace.

## Pipeline

1. **Harvest.** Extract conjectures, questions and problems with the exact
   quote and location (`tools/arxiv_harvest.py`, or the user's files). Record
   how the source poses each one: conjecture, problem, question, remark, or
   our own.
2. **Triage.** A dated, bounded literature search; impact and difficulty from
   1 to 5 against anchor problems. Freeze the initial difficulty. Expect many
   easy problems to be solved already.
3. **Attack.** One problem per session. Read the record, the source and the
   attempt log first; write a three-line plan; end by rewriting the State of
   play and adding one line to the attempt log: route, outcome, why, next.
4. **Referee.** A fresh agent, from a different model family where possible,
   re-reads the question in the source, re-derives every step, reruns every
   certificate and alone sets `result_scope`. The solver never reviews its own
   work.
5. **Share.** Only with the user's approval: see "Sharing and telling".

One file per problem (`problems/<theme>/<ID>.md`), validated after every
change. The record is the memory between sessions.

## Rules that matter most

- **State the objective in every brief: map or settle.** Under *map*,
  reductions, special cases and precise obstructions are progress. Under
  *settle*, only a theorem, or a proof missing one precisely stated lemma,
  counts. Agents keep mapping after the objective has changed; switch them.
- **Scope against the source.** A result is full only if the proved statement
  implies the requested conclusion under the source's definitions. An
  equivalent or stronger theorem can be full if the implication is proved. An
  order of growth needs matching bounds. Answering an easier question is the
  most common error.
- **Read the question before answering it.** An easy answer is a sign of a
  misreading until shown otherwise.
- **Certificates establish the exact claim**, in exact or outward-rounded
  arithmetic, covering the whole range where the claim has one. Anything
  published must rerun in seconds to a minute.
- **Bounded numerics.** Every computation has a time limit, prints progress
  and decides one named quantity.
- **Parallel lanes need distinct mandates** and a coordinator who reads their
  reports; otherwise they reproduce the same bounds.
- **Archive claims.** Save the model's response verbatim when it claims a
  result; if the claim is refuted, keep the file and mark it refuted.
- **Hand-over state.** Sessions end without warning; keep the State of play
  current.

## Sharing and telling

- Share openly first, then tell the people who asked the question promptly.
  Telling them first implies a head start and leaves the result in limbo.
- Public language says what is known and how much stands behind it, with no
  credit or scoreboard language: "x > y. A proof sketch, not checked by a
  specialist, is at [link]." No "we solved", no solved counts.
- Before sharing, the user has read and understood what is sent and confirms
  the statement matches the question. Disclose how agents were used.
- Before vouching (arXiv or a journal), someone can give a clear,
  expert-level talk on the result and say what it extends and whether it is
  new, and the askers have been told.
- Batch messages per research group, and send the few results that matter
  most; expert attention is the scarce resource.
- Write for people: the asker's notation, the idea before the computation,
  nothing an expert does not need. Published work should be the work of
  people who understand it and stand behind every sentence.

## What to expect

The method is best at mapping a field, checking its literature and answering
its easy problems. Most answers will be routine, rediscovered or easy to check
once found. Hard problems usually end as precise records of what fails. Report
results against the original questions, split full from partial, and call
novelty provisional.

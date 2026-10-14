# Stage 4: Referee

You are an independent referee for one record and its solution sheet. You did
not write the result. Assume it is wrong until you have checked every step
yourself. Prefer a different model family from the one that wrote it, and
record which model you are.

## How to referee

- **Blind first.** Read only the source quote and the solution sheet, and
  reach a verdict. Only then read the State of play, the notes and
  `discoveries/` (QED, arXiv:2604.24021, §4.1).
- **Model family.** You must be from a different model family than the
  solver. Same-family referees overrate the answers (UQ, arXiv:2508.17580,
  §3.3; QED, §3.1).
- **Check your own objections** before reporting them. Re-verify each one,
  and drop those that do not survive (arXiv:2602.03837, §2.1).
- **At most two rounds** of referee and fix. After that, mark the record
  `contested` and send it to the user. A sheet revised after a rejection
  goes to a fresh referee, because revisions converge on errors the old
  referee can no longer see (AI co-mathematician, arXiv:2605.06651, §3.4,
  §7).

## What to check

1. **The question.** Open the source and read the exact wording. Does the
   sheet answer the question as posed, with its quantifiers? You set
   `result_scope`: `full` only if the posed question is answered; otherwise
   `partial`, and name the open part. Ask whether the claim is the *right*
   one, not only whether each line is correct.
1b. **Statement match.** Compare the proved statement with the source
   quote, word by word. Check each kind of mismatch:
   - quantifier scope;
   - a surrogate reformulation;
   - the asker's own definitions and normalizations;
   - a restricted domain or range of parameters;
   - a hypothesis that holds by construction rather than by content.

   Any difference makes the result `partial` (QED, §4.3; Kallel and
   El Louadi, arXiv:2608.28997, §4).

   Then the **vacuity check**: if the answer is easy, assume the problem
   was misread until shown otherwise (Feng et al., arXiv:2601.22401, §1.1).
2. **Every step.** Re-derive the proof. Rerun every certificate and audit it:
   - exact or outward-rounded arithmetic;
   - complete coverage of the parameter range, with no gaps between cells;
   - analytic tails;
   - monotonicity claims going the direction the argument needs.

   Check small cases numerically yourself, time-bounded.
2b. **Lemmas.**
   - Every lemma must feed the main theorem; an orphan lemma is a sign of
     drift.
   - Name the lemma that carries the difficulty, and check it is not a
     restatement of the target.
   - Treat every lemma called "standard" as uncited until you have checked
     it (LeanMarathon, arXiv:2606.05400, §3.3; AlphaProof Nexus, §3).
3. **Citations.** Check the exact theorem numbers against the source. For
   every arXiv paper, read the latest version's abstract page for withdrawals
   and errata. A step that rests on an unrefereed preprint makes the result
   conditional on it; list it in `resolution.conditional_on`.
4. **Novelty.** Is any part already in the source, the literature or our own
   earlier work? Do a bounded search and fix overclaimed novelty.
4b. **Novelty grade.** Search problem sites, MathOverflow and forums, not
   only arXiv. Grade the result as known / minor / short paper / strong
   paper, and round down when unsure. Record where the key ideas came from,
   and state it when no attribution could be found (FAR, App. A.3; Leiden
   Declaration).
5. **Presentation.** The asker's notation, no undefined symbols, and a build
   with no warnings.

## What to do

- **Correct, or correct after minor fixes:**
  - apply the fixes, rebuild and set `stage: reviewed`;
  - write `review` as `{by: agent, model: <model>, date: <date>, verdict: "<verdict and what you checked>"}`;
  - for a full result, set `resolution` (tier `ours-internal`, ref, `checked: true`).
- **Real errors:** do not repair the proof yourself. Leave the stage at
  `written`, describe the error and any repair you see under State of play,
  and report it. If the error sinks the claim, delete `discoveries/<ID>.md`.
- Add a review entry to the attempt log, and run the record check.

## Report

Give the verdict (correct / correct with fixable gaps / wrong), the scope,
and a numbered list of issues. For each issue give its severity (fatal,
major, minor or typo), its location and a fix. Then say what you verified,
and how.

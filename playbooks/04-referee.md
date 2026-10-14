# Stage 4: Referee

You are an independent referee for one record and its solution sheet. You did
not write the result. Assume it is wrong until you have checked every step
yourself. Prefer a different model family from the one that wrote it, and
record which model you are.

## What to check

1. **The question.** Open the source and read the exact wording. Does the
   sheet answer the question as posed, with its quantifiers? You set
   `result_scope`: `full` only if the posed question is answered; otherwise
   `partial`, and name the open part. Ask whether the claim is the *right*
   one, not only whether each line is correct.
2. **Every step.** Re-derive the proof. Rerun every certificate and audit it:
   - exact or outward-rounded arithmetic;
   - complete coverage of the parameter range, with no gaps between cells;
   - analytic tails;
   - monotonicity claims going the direction the argument needs.

   Check small cases numerically yourself, time-bounded.
3. **Citations.** Check the exact theorem numbers against the source. For
   every arXiv paper, read the latest version's abstract page for withdrawals
   and errata. A step that rests on an unrefereed preprint makes the result
   conditional on it; list it in `resolution.conditional_on`.
4. **Novelty.** Is any part already in the source, the literature or our own
   earlier work? Do a bounded search and fix overclaimed novelty.
5. **Presentation.** The asker's notation, no undefined symbols, and a build
   with no warnings.

## What to do

- **Correct, or correct after minor fixes:**
  - apply the fixes, rebuild and set `stage: reviewed`;
  - write `review` as `{by: agent, model: <model>, date: <date>, verdict: "<verdict and what you checked>"}`;
  - for a full result, set `resolution` (tier `ours-internal`, ref, `checked: true`).
- **Real errors:** do not repair the proof yourself. Leave the stage at
  `written`, describe the error and any repair you see under State of play,
  and report it.
- Add a review entry to the attempt log, and run the record check.

## Report

Give the verdict (correct / correct with fixable gaps / wrong), the scope,
and a numbered list of issues. For each issue give its severity (fatal,
major, minor or typo), its location and a fix. Then say what you verified,
and how.

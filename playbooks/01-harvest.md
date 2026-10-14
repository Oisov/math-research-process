# Stage 1: Harvest

Goal: from the seeds, produce one record per open question, with the question
verbatim and its exact location. Do not judge difficulty here; extraction is
cheap and filtering comes later.

## 1. Collect the papers

```sh
# by id
python3 tools/arxiv_harvest.py --ids 2504.05986 1601.01616 --out sources/
# by author, last ten years
python3 tools/arxiv_harvest.py --authors "A. Author" "B. Author" --since 2016 --out sources/
# by query
python3 tools/arxiv_harvest.py --query 'cat:math.CV AND abs:"Hardy space"' --max 200 --out sources/
```

The tool queries the arXiv API, downloads each paper's source archive
(falling back to PDF-only when the source is not available), extracts it
safely, and writes `sources/<id>/candidates.jsonl`. It waits three seconds
between requests; do not lower this. For papers the user supplies as files,
use `--local <archive-or-dir>`.

**Depth 2.** Read each seed's bibliography, keep the references that fall in
scope, look them up on arXiv, and harvest those too. Record which seed led to
each paper.

## 2. Extract candidates

`candidates.jsonl` lists:

- theorem-like environments whose printed name is Conjecture, Question,
  Problem or Open problem (the tool reads the `\newtheorem` declarations, so
  `\begin{conj}` is found if `conj` prints as "Conjecture");
- sentences containing phrases such as "it would be interesting", "we do not
  know", "remains open", "it is natural to ask", "we conjecture" and "open
  question".

Each candidate has the file, the line, the environment or phrase, and the
text. Candidates are not records. Read each one in context and decide:

| Decision | When |
|---|---|
| `stated` record | An explicit Conjecture/Question/Problem. |
| `implicit` record | A remark or phrase poses a question without labelling it. Say in the body what suggests it. |
| `form` | How strongly the source poses it: `conjecture` (the author predicts the answer), `problem` or `question` (asked in a numbered environment or a problem list), `remark` ("it would be interesting", "we do not know"), or `ours` (our own derived question). Record it; it predicts how much an answer matters. |
| Discard | Rhetorical, answered later in the same paper, or out of scope. Keep a one-line note in `problems/EXCLUDED.md`. |

## 3. Locate exactly

Source line numbers are not citations. Open the PDF of the **same version**
and record the printed location: "Conjecture 9.2, p. 31", "Question after
Theorem 22". Copy the statement verbatim from the PDF into `source.quote`,
with the notation defined in the record body if the quote depends on it.

Also copy the source's conventions into the record body: normalizations,
the definition of every term, and the range of every parameter. Misreading a
convention is the commonest way to "solve" the wrong problem; one large
study found most technically correct AI solutions were vacuous for this
reason (Feng et al., arXiv:2601.22401, §1.1).

## 4. Inferences (optional, after stated problems)

Read the core authors' papers "between the lines". When paper A proves X and
paper B proves Y, and Z would follow, or Z is the obvious next case, create
an `inference` record with `premises` naming both, and the derivation in the
body. These are our questions: `origin: ours`.

## 5. De-duplicate

The same question is often posed in several papers. Before creating a record,
search existing records by content, not only by source. Merge into the richer
record and list the other sources in `literature.evidence` or `references`.

## 6. Write the record

Use [`templates/record.md`](../templates/record.md). At this stage fill in:

- `id`, `title`, `kind`, `origin`, `theme`, `source` (paper, location,
  posed_by, quote);
- `stage: untriaged`;
- the *Statement* section.

Leave scores and literature status to triage.

## Output

Report the counts: papers fetched, candidates, records created, duplicates
merged, and excluded with reasons. Also list the papers you could not fetch;
the user decides whether to supply them.

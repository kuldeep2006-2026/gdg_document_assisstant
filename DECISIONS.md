# DECISIONS

## 1. Chunking: two word-window sizes and section-based
Same 11 questions, top-3 retrieval, evidence = the phrase that answers the question.

| Setting | Chunks | Evidence hit | Observation |
|---|---|---|---|
| A: 100 words, 20 overlap | 11 | 8/8 | Precise, but chunks cut sections mid-way |
| B: 300 words, 60 overlap | 4 | 8/8 | Scores low and bunched (0.14-0.22): each chunk mixes many topics, so top-3 returns most of the document |
| C: by section | 8 | 8/8 | Clean, readable sources; each chunk is one topic |

Chosen: **C (by section)** because the handbook has clear numbered headings, sources are easy
to read and cite. Alternative considered: fixed windows (A/B), which work on any document but
split topics arbitrarily. Trade-off: C depends on the heading format.
Note: B "refused" the date question only because dilution pushed its score to the threshold,
not because it understood anything. I do not count that as a win.

## 2. Failed approach: threshold alone to reject unanswerable questions
Plan: if the best similarity is low, answer "not found". Result: "What is the capital of France?"
scored 0.00 and was refused, but "Who is the current community lead?" scored 0.16-0.26 and
"What is the date of the next event?" up to 0.12, because section 7 of the handbook literally
mentions both topics (saying they are not specified). A threshold cannot tell "mentioned" from
"answered". Change: the prompt now tells the LLM to reply "I could not find this in the
document." when the context says information is not specified. 
## 3. Evaluation fix
Question 7 first showed a miss in setting A. The cause was my test, not the retriever: the
evidence phrase came from section 1, but the FAQ chunk answers the question more directly.
Changed the evidence to the FAQ wording. Lesson: check whether a "miss" is a test problem.

## 4. Per-page chunking
Chunks never cross page boundaries so every source has an exact page. Cost: a fact split
across a page break is split in two. The handbook has only 2 pages, so page-level hit rate
is meaningless; that is why I score retrieval by evidence phrase.

## 5. Two retrievers
`embed` (meaning-based) is the default; `tfidf` (keywords) is an offline fallback and the
way I tested without downloading a model. 

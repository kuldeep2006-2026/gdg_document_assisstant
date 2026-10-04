# AI-Powered Document Assistant (GDG-USAR AI/ML Task 3)

Ask questions about the GDG-USAR handbook (`data/handbook.pdf`). The assistant finds the
relevant passages, answers using only those passages, and shows the source page.
If the document doesn't contain the answer, it says so.

## How it works
1. **Extract** text page by page (`pypdf`), keeping page numbers.
2. **Chunk** the text. Two strategies: sliding word window (size/overlap configurable) or one chunk per numbered section.
3. **Retrieve**: score every chunk against the question, take the top-k (default 3).
   - `embed` (default): sentence embeddings (`all-MiniLM-L6-v2`), cosine similarity.
   - `tfidf`: keyword matching, runs offline with no model download.
4. **Threshold gate**: if the best score is too low, answer "not found" without calling the LLM.
5. **Generate**: an LLM gets only the retrieved passages and a strict prompt (context only, say "not found" otherwise, cite pages).
6. **Show sources**: page, similarity score and passage for every answer.

## Setup
```bash
git clone <your-repo-url> && cd <repo>
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # then put ONE API key inside (never commit .env)
```
First run with `embed` downloads a small model once (needs internet), then it is cached.

## Run
```bash
python rag.py                                   # interactive, uses data/handbook.pdf
python rag.py --ask "When is the support desk open?"
python rag.py --chunking section                # section-based chunks
python rag.py --retriever tfidf                 # no model download
LLM_PROVIDER=none python rag.py --retriever tfidf   # retrieval only, no API key
```
Windows PowerShell: set the variable with `$env:LLM_PROVIDER="none"` before the command.

## Evaluate
```bash
python evaluate.py --retriever embed            # compares 3 chunk settings -> results.md
```
`questions.json` holds 11 test questions (8 answerable, 3 not answerable from the handbook).
`results.md` currently contains a retrieval-only run with `tfidf`; re-run it with your own setup.

## Limitations
- Scanned PDFs need OCR (not included). Tables are extracted poorly.
- Section chunking relies on headings like `4. Title`; other documents need a different rule.
- Similarity thresholds were tuned only on this handbook.
- Retrieval-only mode cannot refuse questions whose topic IS mentioned in the document
  (for example the "not specified" section); the LLM prompt handles those.

"""
Run the same test questions under different chunking settings and save results.md.
Usage: python evaluate.py [--retriever embed|tfidf] [doc]
Set LLM_PROVIDER=none to test retrieval only (no API key needed).

Metrics
- evidence hit: does any retrieved passage contain the phrase that answers the question?
  (Page-level hits are meaningless here: the handbook only has 2 pages.)
- unanswerable questions: did the system say "not found"?
"""
import argparse
import json

from rag import NOT_FOUND, DocAssistant

CONFIGS = {
    "A: words 100/20": dict(chunking="words", size=100, overlap=20),
    "B: words 300/60": dict(chunking="words", size=300, overlap=60),
    "C: by section":   dict(chunking="section"),
}

ap = argparse.ArgumentParser()
ap.add_argument("doc", nargs="?", default="data/handbook.pdf")
ap.add_argument("--retriever", default="embed", choices=["embed", "tfidf"])
ap.add_argument("--k", type=int, default=3)
a = ap.parse_args()

questions = json.load(open("questions.json"))
norm = lambda s: " ".join(s.lower().split())
out = [f"# Evaluation results (retriever: {a.retriever}, top-k: {a.k})\n"]

for name, cfg in CONFIGS.items():
    bot = DocAssistant(a.doc, retriever=a.retriever, k=a.k, **cfg)
    hits = answerable = refused_ok = unanswerable = 0
    out.append(f"\n## Config {name} ({len(bot.chunks)} chunks, threshold {bot.threshold})\n")
    out.append("| # | Question | Best score | Evidence retrieved? | Answer (start) |")
    out.append("|---|---|---|---|---|")
    for i, item in enumerate(questions, 1):
        r = bot.ask(item["q"])
        answer = r["answer"].replace("\n", " ")[:70]
        if item["evidence"]:
            answerable += 1
            found = any(norm(item["evidence"]) in norm(s["text"]) for s in r["sources"])
            hits += found
            flag = "yes" if found else "NO"
        else:
            unanswerable += 1
            said_no = r["answer"].strip() == NOT_FOUND
            refused_ok += said_no
            flag = "n/a (should refuse): " + ("refused" if said_no else "ANSWERED")
        out.append(f"| {i} | {item['q'][:55]} | {r['best_score']:.2f} | {flag} | {answer} |")
    out.append(f"\nEvidence hit rate: {hits}/{answerable} | "
               f"Unanswerable refused: {refused_ok}/{unanswerable}")

open("results.md", "w").write("\n".join(out) + "\n")
print("\n".join(out))

"""
Document Assistant (RAG)
Pipeline: PDF -> pages -> chunks -> retriever -> top-k passages -> LLM (context only) -> answer + sources
"""
import argparse
import os
import re
from dataclasses import dataclass

from pypdf import PdfReader

try:  # optional: loads API keys from a local .env file
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

NOT_FOUND = "I could not find this in the document."

SYSTEM_PROMPT = f"""You are a document assistant. Answer the question using ONLY the context passages provided.
Rules:
1. Never use outside knowledge.
2. If the context does not contain the answer, or says the information is not specified, reply exactly: {NOT_FOUND}
3. Keep the answer short and cite pages like [Page 2].
4. If the context answers only part of the question, answer that part and say the rest is not in the document."""

# Minimum similarity needed before we even ask the LLM. Scales differ per retriever.
# Tune these on your own test questions (see evaluate.py output).
DEFAULT_THRESHOLD = {"embed": 0.20, "tfidf": 0.10}


@dataclass
class Chunk:
    id: int
    page: int
    text: str


# ---------- 1. Read the PDF (keep page numbers) ----------
def load_pages(path):
    if path.lower().endswith(".pdf"):
        reader = PdfReader(path)
        return [(i + 1, p.extract_text() or "") for i, p in enumerate(reader.pages)]
    with open(path, encoding="utf-8") as f:
        return [(1, f.read())]


# ---------- 2. Split into chunks ----------
def chunk_by_words(pages, size=200, overlap=40):
    """Sliding window of `size` words; consecutive chunks share `overlap` words."""
    step = size - overlap
    chunks = []
    for page, text in pages:
        words = text.split()
        for start in range(0, len(words), step):
            chunks.append(Chunk(len(chunks), page, " ".join(words[start:start + size])))
            if start + size >= len(words):
                break
    return chunks


HEADING = re.compile(r"(?m)^(?=\d+\.\s+[A-Z])")  # a line starting like "4. Project Submissions"


def chunk_by_section(pages):
    """One chunk per numbered section heading (keeps each topic together)."""
    chunks = []
    for page, text in pages:
        for part in HEADING.split(text):
            part = " ".join(part.split())
            if part:
                chunks.append(Chunk(len(chunks), page, part))
    return chunks


# ---------- 3. Retrievers: score every chunk against the question ----------
class TfidfRetriever:
    """Keyword-style matching. Light, offline, no model download."""
    def __init__(self, chunks):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
        self.matrix = self.vec.fit_transform([c.text for c in chunks])

    def scores(self, question):
        from sklearn.metrics.pairwise import linear_kernel
        return linear_kernel(self.vec.transform([question]), self.matrix).ravel()


class EmbedRetriever:
    """Meaning-based matching using sentence embeddings (downloads a small model once)."""
    def __init__(self, chunks, model_name="all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        self.emb = self.model.encode([c.text for c in chunks], normalize_embeddings=True)

    def scores(self, question):
        q = self.model.encode([question], normalize_embeddings=True)[0]
        return self.emb @ q  # cosine similarity because vectors are normalized


# ---------- 4. LLM answer ----------
def generate(prompt):
    provider = os.getenv("LLM_PROVIDER", "gemini")
    model = os.getenv("LLM_MODEL")
    if provider == "none":
        return None
    try:
        if provider == "gemini":  # needs GEMINI_API_KEY
            from google import genai
            client = genai.Client()  # keep a reference, or it gets closed mid-request
            r = client.models.generate_content(
                model=model or "gemini-3.8-flash", contents=prompt,
                config={"system_instruction": SYSTEM_PROMPT, "temperature": 0})
            return r.text.strip()
        if provider == "anthropic":  # needs ANTHROPIC_API_KEY
            import anthropic
            r = anthropic.Anthropic().messages.create(
                model=model or "claude-haiku-4-5-20251001", max_tokens=400, temperature=0,
                system=SYSTEM_PROMPT, messages=[{"role": "user", "content": prompt}])
            return r.content[0].text.strip()
        if provider == "openai":  # needs OPENAI_API_KEY
            from openai import OpenAI
            client = OpenAI()
            r = client.chat.completions.create(
                model=model or "gpt-4o-mini",
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": prompt}])
            return r.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(
            f"LLM call failed ({provider}): {e}\n"
            "Check your API key / LLM_MODEL, or run with LLM_PROVIDER=none for retrieval-only.")
    raise ValueError(f"Unknown LLM_PROVIDER '{provider}' (use gemini, anthropic, openai or none)")


# ---------- The assistant ----------
class DocAssistant:
    def __init__(self, path, chunking="words", size=200, overlap=40,
                 retriever="embed", k=3, threshold=None):
        pages = load_pages(path)
        self.chunks = chunk_by_section(pages) if chunking == "section" \
            else chunk_by_words(pages, size, overlap)
        if not self.chunks:
            raise ValueError("No text extracted. Is the PDF scanned? It would need OCR.")
        self.k = k
        self.threshold = DEFAULT_THRESHOLD[retriever] if threshold is None else threshold
        self.retriever = EmbedRetriever(self.chunks) if retriever == "embed" \
            else TfidfRetriever(self.chunks)

    def retrieve(self, question):
        scores = self.retriever.scores(question)
        top = scores.argsort()[::-1][: self.k]
        return [(self.chunks[i], float(scores[i])) for i in top]

    def ask(self, question):
        hits = self.retrieve(question)
        best = hits[0][1]
        sources = [{"page": c.page, "score": round(s, 3), "text": c.text} for c, s in hits]
        if best < self.threshold:  # nothing similar enough: don't bother the LLM
            return {"answer": NOT_FOUND, "refused_by_threshold": True,
                    "best_score": best, "sources": sources}
        context = "\n\n".join(f"[Page {c.page}] {c.text}" for c, _ in hits)
        answer = generate(f"Context:\n{context}\n\nQuestion: {question}\nAnswer:")
        if answer is None:  # LLM_PROVIDER=none
            answer = f"(retrieval-only mode, best passage) {hits[0][0].text}"
        return {"answer": answer, "refused_by_threshold": False,
                "best_score": best, "sources": sources}


def show(result):
    print(f"\nAnswer: {result['answer']}")
    print(f"(best similarity: {result['best_score']:.2f})")
    for s in result["sources"]:
        print(f"  - Page {s['page']} | score {s['score']} | {s['text'][:110]}...")


def main():
    ap = argparse.ArgumentParser(description="Ask questions about a document.")
    ap.add_argument("doc", nargs="?", default="data/handbook.pdf")
    ap.add_argument("--chunking", choices=["words", "section"], default="words")
    ap.add_argument("--size", type=int, default=200, help="words per chunk (words mode)")
    ap.add_argument("--overlap", type=int, default=40, help="shared words between chunks")
    ap.add_argument("--retriever", choices=["embed", "tfidf"], default="embed")
    ap.add_argument("--k", type=int, default=3, help="passages sent to the LLM")
    ap.add_argument("--threshold", type=float, default=None)
    ap.add_argument("--ask", help="ask one question and exit")
    a = ap.parse_args()

    bot = DocAssistant(a.doc, a.chunking, a.size, a.overlap, a.retriever, a.k, a.threshold)
    print(f"Loaded {len(bot.chunks)} chunks ({a.chunking}, {a.retriever}, threshold {bot.threshold}).")
    if a.ask:
        show(bot.ask(a.ask))
        return
    print("Type a question, or 'exit' to quit.")
    while (q := input("\nQuestion: ").strip()) not in ("exit", "quit"):
        if q:
            show(bot.ask(q))


if __name__ == "__main__":
    main()

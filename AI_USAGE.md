# AI_USAGE

> DRAFT: edit so it matches what you actually did.

- **Tools used:** Claude (Anthropic) for planning the pipeline, generating the first version of the code, and drafting documentation.
- **What AI helped with:** project structure, `rag.py` (chunking, retrieval, prompt, CLI), `evaluate.py`, test questions, first drafts of README/DECISIONS.
- **What I reviewed or changed myself:** (fill in: e.g. read every function, ran the evaluation, tuned the threshold, edited the prompt, wrote the final DECISIONS conclusions)
- **Runtime AI:** the assistant calls an LLM (Gemini or Claude, set in `.env`) only to write the final answer from retrieved passages.
- **Understanding:** I can explain each pipeline step and why I chose section-based chunking.

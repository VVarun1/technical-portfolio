from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    repo_url: str
    question: str

@app.post("/ask")
async def ask_codebase(q: Query):
    # 1. Clone Repo -> 2. Chunk via AST -> 3. Vector Search (pgvector) -> 4. LLM Answer
    return {"answer": "Based on auth.py:42, the authentication is handled via JWT...", "sources": ["auth.py:42"]}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

app = FastAPI(
    title="ResearchMind API",
    description="Multi-agent research pipeline powered by LangChain + GPT-4o-mini",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response schemas ────────────────────────────────────────────────

class ResearchRequest(BaseModel):
    topic: str


class StepResult(BaseModel):
    search_output: str
    reader_output: str
    report: str
    critique: str


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "message": "ResearchMind API is running."}


@app.get("/health")
def health():
    return {"status": "healthy"}


# ── Main pipeline endpoint ────────────────────────────────────────────────────

@app.post("/research", response_model=StepResult)
def run_research(req: ResearchRequest):
    topic = req.topic.strip()
    if not topic:
        raise HTTPException(status_code=422, detail="Topic must not be empty.")

    # Step 1 — Search Agent
    try:
        search_agent = build_search_agent()
        search_result = search_agent.invoke(
            {"messages": [("human", f"Search for information about: {topic}")]}
        )
        search_output = search_result["messages"][-1].content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search Agent failed: {e}")

    # Step 2 — Reader Agent
    try:
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke(
            {"messages": [("human", f"Read and extract content from these search results:\n{search_output}")]}
        )
        reader_output = reader_result["messages"][-1].content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reader Agent failed: {e}")

    # Step 3 — Writer Chain
    try:
        report = writer_chain.invoke({"topic": topic, "research": reader_output})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Writer Chain failed: {e}")

    # Step 4 — Critic Chain
    try:
        critique = critic_chain.invoke({"report": report})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Critic Chain failed: {e}")

    return StepResult(
        search_output=search_output,
        reader_output=reader_output,
        report=report,
        critique=critique,
    )

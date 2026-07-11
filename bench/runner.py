"""Run a candidate model against the question set and capture metrics."""

import logging
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import UsageLimits

from core.agent import ResearchAgent, create_research_agent
from core.models import check_if_model_is_available

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "nomic-embed-text"
DEFAULT_FOLDER = "Research"

# Disable qwen3-family "thinking" mode for candidate runs. Thinking inflates
# latency and can produce runaway generation (e.g. qwen3.5:9b emitted 8.5K
# tokens on a numeric question), which is unsuitable for an interactive RAG
# app. Routed to Ollama via the OpenAI-compatible extra_body.
NO_THINK_SETTINGS: ModelSettings = {
    "extra_body": {"chat_template_kwargs": {"enable_thinking": False}}
}

# Cap tool calls per question so a model cannot get stuck in a search loop
# (observed: qwen3.5:9b issued 21+ searches on one comparison question).
# 4 allows the multi-search strategy the prompt encourages (2-3 searches).
MAX_TOOL_CALLS = 4
RUN_USAGE_LIMITS = UsageLimits(tool_calls_limit=MAX_TOOL_CALLS)


@dataclass
class QuestionResult:
    """Captured output for a single (model, question) run."""

    question_id: str
    question: str
    category: str
    answer: str
    searches: list[str] = field(default_factory=list)
    num_searches: int = 0
    total_time_s: float = 0.0
    time_to_first_text_s: float | None = None
    error: str | None = None


def _run_single(agent: ResearchAgent, question: str) -> QuestionResult:
    """Run one question through the agent's streaming handler with tool events."""
    handler = agent.get_streaming_chat_handler(
        include_tool_calls=True,
        model_settings=NO_THINK_SETTINGS,
        usage_limits=RUN_USAGE_LIMITS,
    )
    start = time.perf_counter()
    first_text_at: float | None = None
    searches: list[str] = []
    parts: list[str] = []

    for event_type, content in handler(question, message_history=None):
        if event_type == "tool_call" and isinstance(content, dict):
            args = content.get("args", {})
            if isinstance(args, dict):
                searches.append(args.get("query", ""))
        elif event_type == "text" and isinstance(content, str):
            if first_text_at is None and content.strip():
                first_text_at = time.perf_counter()
            parts.append(content)

    total = time.perf_counter() - start
    return QuestionResult(
        question_id="",
        question=question,
        category="",
        answer="".join(parts).strip(),
        searches=searches,
        num_searches=len(searches),
        total_time_s=round(total, 2),
        time_to_first_text_s=(
            round(first_text_at - start, 2) if first_text_at is not None else None
        ),
    )


def run_model(
    model: str,
    questions: list[dict],
    documents_path: str = DEFAULT_FOLDER,
    reload_store: bool = False,
    out_path: Path | None = None,
) -> list[QuestionResult]:
    """
    Run a model against all questions.

    Args:
        model: Ollama model name (e.g. "qwen3:8b").
        questions: Loaded question dicts from questions.jsonl.
        documents_path: Folder passed to the agent.
        reload_store: Whether to rebuild the LanceDB store for this run.
        out_path: If given, write results to this JSONL after every question so
            a runaway or error on one question cannot lose the others.

    Returns:
        One QuestionResult per question, in input order.
    """
    logger.info("Ensuring model %s is available...", model)
    check_if_model_is_available(model)

    agent = create_research_agent(
        llm_model=model,
        embedding_model=EMBEDDING_MODEL,
        documents_path=documents_path,
        reload=reload_store,
    )

    results: list[QuestionResult] = []
    for i, q in enumerate(questions, 1):
        logger.info("[%s] (%d/%d) %s", model, i, len(questions), q["question"])
        try:
            res = _run_single(agent, q["question"])
            res.question_id = q["id"]
            res.category = q.get("category", "")
            logger.info(
                "  -> %d searches, %.1fs, %d chars",
                res.num_searches,
                res.total_time_s,
                len(res.answer),
            )
        except Exception as e:  # noqa: BLE001
            logger.error("  -> FAILED: %s", e)
            res = QuestionResult(
                question_id=q["id"],
                question=q["question"],
                category=q.get("category", ""),
                answer="",
                error=str(e),
            )
        results.append(res)
        if out_path is not None:
            save_raw(results, out_path)
    return results


def save_raw(results: list[QuestionResult], path: Path) -> None:
    """Write results as JSONL (one line per question)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in results:
            f.write(_to_json_line(asdict(r)) + "\n")


def _to_json_line(d: dict) -> str:
    import json

    return json.dumps(d, ensure_ascii=False)

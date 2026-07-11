"""CLI: run candidate models against the question set, judge, and report.

Usage:
    uv run python -m bench --models qwen3:8b qwen3:14b lfm2.5:8b-a1b --judge qwen3:30b
"""

import argparse
import csv
import json
import logging
import sys
from pathlib import Path

from bench.judge import judge_answer
from bench.runner import run_model

DEFAULT_MODELS = ["qwen3.5:9b"]
DEFAULT_JUDGE = "qwen3-coder:480b-cloud"
HERE = Path(__file__).resolve().parent
DEFAULT_QUESTIONS = HERE / "questions.jsonl"
DEFAULT_OUT = HERE / "results"

logger = logging.getLogger("bench")


def load_questions(path: Path, limit: int | None = None) -> list[dict]:
    """Read questions.jsonl into a list of dicts."""
    questions: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))
    if limit:
        questions = questions[:limit]
    return questions


def _safe_name(model: str) -> str:
    """Filesystem-safe version of a model name (e.g. qwen3:8b -> qwen3_8b)."""
    return model.replace(":", "_").replace("/", "_")


def _avg(rows: list[dict], key: str) -> float:
    """Mean of a numeric column across rows, rounded to 2 decimals."""
    return round(sum(r[key] for r in rows) / len(rows), 2)


def _run_phase(
    models: list[str],
    questions: list[dict],
    out_dir: Path,
    documents_path: str,
    reload_store: bool,
) -> dict[str, list[dict]]:
    """Run each candidate model; return {model: [raw result dict, ...]}."""
    raw_dir = out_dir / "raw"
    raw_by_model: dict[str, list[dict]] = {}
    for i, model in enumerate(models):
        reload_this = reload_store and i == 0
        logger.info("=== Running model %s ===", model)
        raw_path = raw_dir / f"{_safe_name(model)}.jsonl"
        results = run_model(
            model,
            questions,
            documents_path=documents_path,
            reload_store=reload_this,
            out_path=raw_path,
        )
        rows = [r.__dict__ for r in results]
        raw_by_model[model] = rows
    return raw_by_model


def _judge_phase(
    raw_by_model: dict[str, list[dict]],
    questions: list[dict],
    judge_model: str,
) -> list[dict]:
    """Score every (model, question) pair; return score rows."""
    q_by_id = {q["id"]: q for q in questions}
    rows: list[dict] = []
    for model, results in raw_by_model.items():
        logger.info("=== Judging model %s with %s ===", model, judge_model)
        for r in results:
            q = q_by_id[r["question_id"]]
            verdict = judge_answer(
                question=r["question"],
                reference_answer=q["reference_answer"],
                key_facts=q["key_facts"],
                candidate_answer=r["answer"],
                judge_model=judge_model,
            )
            row = {
                "question_id": r["question_id"],
                "category": r["category"],
                "model": model,
                "score": verdict.score,
                "num_searches": r["num_searches"],
                "total_time_s": r["total_time_s"],
                "time_to_first_text_s": r["time_to_first_text_s"],
                "answer_chars": len(r["answer"]),
                "error": r.get("error") or "",
                "covered_facts": "; ".join(verdict.covered_facts),
                "reasoning": verdict.reasoning,
            }
            logger.info(
                "  [%s] %s -> score %d (%d searches, %.1fs)",
                r["question_id"],
                model,
                verdict.score,
                r["num_searches"],
                r["total_time_s"],
            )
            rows.append(row)
    return rows


def _write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_summary(
    rows: list[dict], models: list[str], questions: list[dict], path: Path
) -> None:
    """Markdown report: per-model averages + per-question breakdown."""
    lines: list[str] = []
    lines.append("# Model Benchmark Results\n")

    # Per-model averages
    lines.append("## Per-Model Summary\n")
    lines.append(
        "| Model | Avg Score | Avg Searches | Avg Total Time (s) "
        "| Avg Time to First Text (s) | Errors |"
    )
    lines.append("|---|---|---|---|---|---|")
    for model in models:
        mr = [r for r in rows if r["model"] == model]
        if not mr:
            continue
        ttft_vals = [r["time_to_first_text_s"] for r in mr if r["time_to_first_text_s"]]
        avg_ttft = round(sum(ttft_vals) / len(ttft_vals), 2) if ttft_vals else 0.0
        errors = sum(1 for r in mr if r["error"])
        lines.append(
            f"| {model} | {_avg(mr, 'score')} | {_avg(mr, 'num_searches')} "
            f"| {_avg(mr, 'total_time_s')} | {avg_ttft} | {errors} |"
        )
    lines.append("")

    # Per-question breakdown
    lines.append("## Per-Question Breakdown\n")
    lines.append("| Question | " + " | ".join(models) + " |")
    lines.append("|---" * (len(models) + 1) + "|")
    for q in questions:
        scores = []
        for model in models:
            match = next(
                (
                    r
                    for r in rows
                    if r["question_id"] == q["id"] and r["model"] == model
                ),
                None,
            )
            s = f"{match['score']}" if match else "-"
            ns = f" ({match['num_searches']}s)" if match else ""
            scores.append(s + ns)
        lines.append(f"| {q['id']} | " + " | ".join(scores) + " |")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bench",
        description="Benchmark LLM models on the agentic RAG pipeline.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=DEFAULT_MODELS,
        help=f"Candidate models to compare (default: {DEFAULT_MODELS}).",
    )
    parser.add_argument(
        "--judge",
        default=DEFAULT_JUDGE,
        help=f"Ollama model used as the LLM judge (default: {DEFAULT_JUDGE}).",
    )
    parser.add_argument(
        "--questions",
        type=Path,
        default=DEFAULT_QUESTIONS,
        help="questions.jsonl path.",
    )
    parser.add_argument(
        "--out", type=Path, default=DEFAULT_OUT, help="Output directory."
    )
    parser.add_argument(
        "--folder", default="Research", help="Documents folder for the agent."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only run first N questions (quick test).",
    )
    parser.add_argument(
        "--reload-store",
        action="store_true",
        help="Rebuild the LanceDB vector store before running.",
    )
    parser.add_argument(
        "--no-judge", action="store_true", help="Run candidates but skip judging."
    )
    parser.add_argument(
        "--skip-run",
        action="store_true",
        help="Skip running candidates; re-judge existing raw/ outputs.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose (INFO) logging."
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    questions = load_questions(args.questions, limit=args.limit)
    logger.info("Loaded %d questions from %s", len(questions), args.questions)

    if args.skip_run:
        # Load raw outputs from disk
        raw_by_model: dict[str, list[dict]] = {}
        for model in args.models:
            p = args.out / "raw" / f"{_safe_name(model)}.jsonl"
            if not p.exists():
                logger.error("Missing raw output for %s at %s; run first.", model, p)
                return 1
            with p.open(encoding="utf-8") as f:
                raw_by_model[model] = [json.loads(line) for line in f if line.strip()]
    else:
        raw_by_model = _run_phase(
            args.models,
            questions,
            args.out,
            documents_path=args.folder,
            reload_store=args.reload_store,
        )

    if args.no_judge:
        logger.info("Skipping judge phase (--no-judge).")
        return 0

    rows = _judge_phase(raw_by_model, questions, args.judge)

    csv_path = args.out / "scores.csv"
    md_path = args.out / "summary.md"
    _write_csv(rows, csv_path)
    _write_summary(rows, args.models, questions, md_path)
    logger.info("Wrote %s and %s", csv_path, md_path)
    print(f"\nDone. Results in {args.out}/")
    print(f"  - {csv_path}")
    print(f"  - {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

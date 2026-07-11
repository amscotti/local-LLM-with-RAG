"""LLM-as-judge: score candidate answers against golden answers via Ollama."""

import json
import logging
import re

import ollama

logger = logging.getLogger(__name__)

JUDGE_PROMPT = """
You are an evaluator for a RAG (Retrieval-Augmented Generation) system.
You will be given a question, a reference ground-truth answer, the key facts a
correct answer should contain, and a candidate answer produced by a model.

Score the candidate answer on a 1-5 integer scale:
- 5: Excellent. Covers all key facts accurately, no hallucination, cites sources.
- 4: Good. Covers most key facts, only minor gaps, no major errors.
- 3: Partial. Covers some key facts but misses important ones, or minor errors.
- 2: Weak. Misses most key facts, or contains significant errors / hallucination.
- 1: Wrong. Fundamentally incorrect, empty, or unrelated to the question.

Penalize hallucinations (facts not supported by the reference) heavily.
Empty or error outputs must receive score 1.

QUESTION:
{question}

REFERENCE ANSWER (ground truth):
{reference}

KEY FACTS a correct answer should contain:
{key_facts}

CANDIDATE ANSWER to evaluate:
{candidate}

Respond with ONLY a JSON object (no markdown fences, no prose) of this shape:
{{"score": <int 1-5>,
 "covered_facts": ["<key facts the candidate covered>"],
 "reasoning": "<one short sentence>"}}
"""


class JudgeResult:
    """Parsed judge verdict for one candidate answer."""

    __slots__ = ("score", "covered_facts", "reasoning")

    def __init__(self, score: int, covered_facts: list[str], reasoning: str) -> None:
        self.score = score
        self.covered_facts = covered_facts
        self.reasoning = reasoning


def _extract_json(text: str) -> dict:
    """Tolerantly pull the first {...} JSON object out of a model response."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {}
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}


def judge_answer(
    question: str,
    reference_answer: str,
    key_facts: list[str],
    candidate_answer: str,
    judge_model: str,
) -> JudgeResult:
    """
    Ask the judge model to score one candidate answer.

    Args:
        question: The question that was asked.
        reference_answer: Ground-truth golden answer.
        key_facts: Facts the judge should look for.
        candidate_answer: The candidate model's answer to score.
        judge_model: Ollama model name to use as the judge.

    Returns:
        A JudgeResult with score, covered facts, and reasoning.
    """
    if not candidate_answer.strip():
        return JudgeResult(1, [], "Empty candidate answer.")

    prompt = JUDGE_PROMPT.format(
        question=question,
        reference=reference_answer,
        key_facts="\n".join(f"- {f}" for f in key_facts),
        candidate=candidate_answer,
    )

    response = ollama.chat(
        model=judge_model,
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"temperature": 0.0},
        think=False,
    )
    raw = response.message.content or ""
    parsed = _extract_json(raw)

    try:
        score = int(parsed.get("score", 1))
    except (TypeError, ValueError):
        score = 1
    score = max(1, min(5, score))

    covered = parsed.get("covered_facts", [])
    if not isinstance(covered, list):
        covered = [str(covered)]
    reasoning = str(parsed.get("reasoning", "")).strip()

    return JudgeResult(score, [str(c) for c in covered], reasoning)

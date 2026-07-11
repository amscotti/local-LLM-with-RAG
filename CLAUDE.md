# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an experimental sandbox for **agentic RAG** (Retrieval-Augmented Generation) using local LLMs via Ollama and Pydantic AI. Unlike fixed RAG pipelines, the AI agent decides when and how to search documents.

**Key constraint:** Requires Ollama running locally at `http://localhost:11434`.

## Commands

```bash
# Install dependencies
uv sync

# Run the app
uv run streamlit run interfaces/streamlit_app.py

# Code quality
uv run ruff check .           # Lint
uv run ruff check . --fix     # Auto-fix
uv run ruff format .          # Format
uv run pyrefly check          # Type check

# Benchmark models (requires Ollama running)
uv run python -m bench --models qwen3:8b qwen3:14b qwen3.5:9b --judge qwen3-coder:480b-cloud
uv run python -m bench --limit 2 -v          # quick smoke test (2 questions)
uv run python -m bench --skip-run             # re-judge existing raw outputs
uv run python -m bench --max-tool-calls 3     # tighten search loop protection
```

## Architecture

```
interfaces/streamlit_app.py ──▶ core/agent.py (ResearchAgent) ──▶ Ollama LLM
                                        │
                                        │ @agent.tool
                                        ▼
                                 core/document_loader.py ──▶ LanceDB (storage/)
                                        │
                                        ▼
                                 Ollama Embeddings (nomic-embed-text)
```

**Core flow:**
1. Documents loaded from folder into LanceDB vector store (supports PDF, Word, PowerPoint, Excel, Markdown, HTML, CSV, JSON via MarkItDown)
2. ResearchAgent uses Pydantic AI with a `search_documents` tool
3. Agent autonomously decides whether to search documents or answer directly
4. Streaming responses via `agent.run_stream_sync()`

## Project Structure

```
├── core/
│   ├── __init__.py
│   ├── agent.py                  # Pydantic AI agent with RAG tool
│   ├── document_loader.py        # Document loading, LanceDB integration
│   └── models.py                 # Ollama model management
├── interfaces/
│   ├── __init__.py
│   └── streamlit_app.py          # Streamlit web interface (main entry point)
├── bench/                        # Model benchmarking harness
│   ├── questions.jsonl           # Eval questions w/ golden answers + key facts
│   ├── runner.py                 # Runs a model via ResearchAgent, captures metrics
│   ├── judge.py                  # LLM-as-judge (Ollama) scoring vs golden answers
│   └── cli.py                    # CLI orchestrator -> results/scores.csv + summary.md
├── Research/                     # Sample documents
└── storage/                      # LanceDB vector store (gitignored)
```

## Benchmarking

The `bench/` package compares LLM models on the agentic RAG pipeline. It runs each
candidate model against `bench/questions.jsonl` (10 questions spanning factual,
methodology, numeric, and comparison categories) and uses a larger **judge** model
via Ollama to score answers 1-5 against hand-written golden answers + key facts.

**Captured per (model, question):** answer text, number of `search_documents` calls,
total time, time-to-first-text, judge score, covered facts.

**Outputs** (in `bench/results/`, gitignored):
- `raw/<model>.jsonl` — full raw outputs per model
- `scores.csv` — one row per (model, question)
- `summary.md` — per-model averages + per-question score table

Edit `bench/questions.jsonl` to add questions; each line needs `id`, `category`,
`question`, `reference_answer`, and `key_facts` (a list the judge checks for).

## Tech Stack

- **Pydantic AI**: Agent orchestration, tool calling, streaming
- **LanceDB**: Vector store with native Ollama embeddings
- **MarkItDown**: Document loading (PDF, Word, PowerPoint, Excel, etc.)
- **Ollama**: Local LLM and embeddings
- **Streamlit**: Web interface

## Model Notes

- Default LLM: `qwen3.5:9b`
- Default embeddings: `nomic-embed-text` (768 dimensions)
- Recommended models: `qwen3.5:9b` (best overall), `qwen3:8b` (strong alternative)
- Judge model for benchmarks: `qwen3-coder:480b-cloud` (free-tier Ollama cloud)
- Some models don't support tool calling in Ollama - test before using for this project
- Hybrid/MoE models with few active parameters (e.g. `lfm2.5:8b-a1b`) are unreliable for agentic RAG
- Vector store only reloads when folder path changes (not on model switch)

## Code Style Guidelines

### Naming Conventions
- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private functions: `_single_leading_underscore`

### Import Organization
Group imports in this order (separated by blank lines):
1. Standard library imports
2. Third-party imports
3. Local application imports

```python
import logging
import os
from pathlib import Path
from typing import Annotated

import lancedb
from pydantic_ai import Agent, RunContext

from core.document_loader import load_documents_into_database
```

### Type Hints
- Always include type hints for function parameters and return values
- Use `-> None` for functions that don't return a value
- Use `Annotated` for complex type metadata (see LanceDB vector fields)

### Docstrings
Use Google-style docstrings:

```python
def create_research_agent(
    llm_model: str = "mistral",
    embedding_model: str = "nomic-embed-text",
) -> ResearchAgent:
    """
    Factory function to create a configured research agent.

    Args:
        llm_model: Name of the LLM model to use.
        embedding_model: Name of the embedding model to use.

    Returns:
        A configured research agent instance.
    """
```

### Formatting
- 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters
- No trailing whitespace

## Pydantic AI Patterns

### Agent Setup
```python
model = OpenAIChatModel(
    model_name=self.llm_model,
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

agent = Agent(
    model,
    deps_type=AgentDeps,
    system_prompt="You are a helpful research assistant...",
)
```

### Tool Definition
- Tools are async functions decorated with `@agent.tool`
- First parameter is `RunContext[DepsType]` for accessing dependencies
- Return types must be JSON-serializable (str, int, list, etc.)

```python
@self.agent.tool
async def search_documents(
    ctx: RunContext[AgentDeps],
    query: str,
) -> str:
    # Generate embedding for the query
    query_embedding = embedding_func.compute_query_embeddings(query)[0]

    # Search LanceDB
    results = ctx.deps.vector_store.search(query_embedding).limit(10).to_list()

    # Format results with numbered sections
    result_parts = []
    for i, doc in enumerate(results, 1):
        result_parts.append(f"--- Result {i} ---")
        result_parts.append(f"Source: {doc['source']}, Page: {doc['page']}")
        result_parts.append(doc["text"].strip())
    result_parts.append("--- End of results ---")
    return "\n\n".join(result_parts)
```

### Streaming
```python
response = self.agent.run_stream_sync(
    question,
    deps=deps,
    message_history=history,
    model_settings=model_settings,
    usage_limits=usage_limits,
)
last_text = ""
for text in response.stream_text():
    # Yield only the new part (delta) of the text
    new_text = text[len(last_text):]
    yield new_text
    last_text = text
```

## Streamlit Best Practices

- Use `st.session_state` for persistent state
- Check for state existence: `if "key" not in st.session_state:`
- Use `st.spinner` for long-running operations
- Use `st.chat_message` for conversational interfaces
- Use `st.status` to show tool call activity

## Before Committing

1. `uv run ruff check . --fix`
2. `uv run ruff format .`
3. `uv run pyrefly check`
4. Test Streamlit UI if changes affect user interaction
5. Verify agent tool calling works correctly

import logging
from dataclasses import dataclass, field

import lancedb
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import UsageLimits

from core.document_loader import (
    get_db_connection,
    get_embedding_function,
    load_documents_into_database,
)

logger = logging.getLogger(__name__)


@dataclass
class AgentDeps:
    """Dependencies for RAG agent."""

    embedding_model: str
    vector_store: lancedb.table.Table


def _create_vector_store(
    embedding_model: str, documents_path: str = "Research", reload: bool = True
) -> lancedb.table.Table:
    """
    Create or load a LanceDB vector store.

    Args:
        embedding_model: Name of the embedding model to use.
        documents_path: Path to the documents directory.
        reload: Whether to reload from documents or load existing store.

    Returns:
        LanceDB table instance.
    """
    if reload:
        logger.info("Loading documents into vector store...")
        return load_documents_into_database(embedding_model, documents_path)
    else:
        logger.info("Loading existing vector store...")
        db = get_db_connection()
        table_name = "documents"

        if table_name in db.table_names():
            return db.open_table(table_name)
        else:
            # Need to reload if no existing table
            logger.info("No existing table found, loading documents...")
            return load_documents_into_database(embedding_model, documents_path)


@dataclass
class ResearchAgent:
    """Agentic RAG system for research document queries."""

    llm_model: str
    embedding_model: str
    vector_store: lancedb.table.Table = field(
        default_factory=lambda: _create_vector_store("nomic-embed-text", reload=False)
    )
    agent: Agent[AgentDeps, str] = field(init=False)

    def __post_init__(self) -> None:
        """Initialize agent after creation."""
        model = OpenAIChatModel(
            model_name=self.llm_model,
            provider=OllamaProvider(base_url="http://localhost:11434/v1"),
        )

        self.agent = Agent(
            model,
            deps_type=AgentDeps,
            system_prompt=(
                "You are a helpful research assistant. "
                "ALWAYS use the search_documents tool for any question that could be "
                "answered from the documents (facts, numbers, methodologies, systems, "
                "techniques). Never rely on your own knowledge.\n\n"
                "Search guidelines:\n"
                "- Use complete, self-contained queries (no pronouns).\n"
                "- For compound questions, run multiple focused searches rather than "
                "one broad query.\n"
                "- After 2–3 searches you should usually have enough information to "
                "answer. Do not keep searching indefinitely.\n\n"
                "When you have sufficient information, give a clear final answer and "
                "stop. If the documents do not contain the answer, say so explicitly. "
                "Always cite sources using the exact format "
                "[Source: ..., Page: ...].\n\n"
                "Example of a good final answer:\n"
                '"The paper describes three main components: memory stream, '
                "reflection, and planning "
                '[Source: Research/2304.03442v1.pdf, Page: 3]."'
            ),
        )

        # Get the embedding function for search queries
        embedding_func = get_embedding_function(self.embedding_model)

        @self.agent.tool
        async def search_documents(
            ctx: RunContext[AgentDeps],
            query: str,
        ) -> str:
            """
            Search for relevant document sections in the research database.

            Args:
                ctx: The agent run context.
                query: Natural language search query with full topic context.

            Returns:
                The retrieved document sections formatted as text.
            """
            # Generate embedding for the query
            query_embedding = embedding_func.compute_query_embeddings(query)[0]

            # Search LanceDB
            results = ctx.deps.vector_store.search(query_embedding).limit(10).to_list()

            if not results:
                return "No relevant documents found for this query."

            result_parts = []
            for i, doc in enumerate(results, 1):
                source = doc.get("source", "Unknown")
                page = doc.get("page", "N/A")
                text = doc.get("text", "")
                result_parts.append(f"--- Result {i} ---")
                result_parts.append(f"Source: {source}, Page: {page}")
                result_parts.append(text.strip())
            result_parts.append("--- End of results ---")

            return "\n\n".join(result_parts)

    def get_chat_handler(
        self,
        model_settings: ModelSettings | None = None,
        usage_limits: UsageLimits | None = None,
    ):
        """
        Get a callable that handles chat interactions.

        Args:
            model_settings: Optional pydantic-ai model settings.
            usage_limits: Optional tool-call / token limits.

        Returns:
            A function that takes a question and returns a response.
        """

        def chat(question: str) -> str:
            """Process a user question and return an answer."""
            deps = AgentDeps(
                embedding_model=self.embedding_model, vector_store=self.vector_store
            )
            result = self.agent.run_sync(
                question,
                deps=deps,
                model_settings=model_settings,
                usage_limits=usage_limits,
            )
            return result.output

        return chat

    def get_streaming_chat_handler(
        self,
        include_tool_calls: bool = False,
        model_settings: ModelSettings | None = None,
        usage_limits: UsageLimits | None = None,
    ):
        """
        Get a generator that handles streaming chat interactions.

        Args:
            include_tool_calls: If True, yields tool call info as well as text.
            model_settings: Optional pydantic-ai model settings forwarded to
                ``run_stream_sync`` (e.g. ``{"extra_body": ...}`` to toggle a
                provider-specific option like qwen3 thinking mode). ``None``
                keeps the model's default behaviour.
            usage_limits: Optional ``UsageLimits`` forwarded to
                ``run_stream_sync``. Use ``UsageLimits(tool_calls_limit=N)`` to
                bound the number of tool calls per run and prevent search loops.

        Returns:
            A function that takes a question, optional message_history,
            and yields text chunks or tuples of (type, content).
        """

        def chat_stream(
            question: str,
            message_history: list[ModelMessage] | None = None,
        ):
            """Process a user question and stream an answer."""
            deps = AgentDeps(
                embedding_model=self.embedding_model, vector_store=self.vector_store
            )

            response = self.agent.run_stream_sync(
                question,
                deps=deps,
                message_history=message_history,
                model_settings=model_settings,
                usage_limits=usage_limits,
            )
            last_text = ""
            for text in response.stream_text():
                # Yield only the new part of the text
                new_text = text[len(last_text) :]
                yield new_text
                last_text = text

        def chat_stream_with_tools(
            question: str,
            message_history: list[ModelMessage] | None = None,
        ):
            """Process a user question and stream answer with tool call info."""
            from pydantic_ai.messages import (
                ModelResponse,
                ToolCallPart,
            )

            deps = AgentDeps(
                embedding_model=self.embedding_model, vector_store=self.vector_store
            )

            response = self.agent.run_stream_sync(
                question,
                deps=deps,
                message_history=message_history,
                model_settings=model_settings,
                usage_limits=usage_limits,
            )

            # Get only tool calls from current run (not previous history)
            for message in response.new_messages():
                if isinstance(message, ModelResponse):
                    for part in message.parts:
                        if isinstance(part, ToolCallPart):
                            yield (
                                "tool_call",
                                {
                                    "tool_name": part.tool_name,
                                    "args": part.args_as_dict(),
                                },
                            )

            # Now stream the text output
            last_text = ""
            for text in response.stream_text():
                new_text = text[len(last_text) :]
                if new_text:
                    yield ("text", new_text)
                last_text = text

        return chat_stream_with_tools if include_tool_calls else chat_stream


def create_research_agent(
    llm_model: str = "mistral",
    embedding_model: str = "nomic-embed-text",
    documents_path: str = "Research",
    reload: bool = False,
) -> ResearchAgent:
    """
    Factory function to create a configured research agent.

    Args:
        llm_model: Name of the LLM model to use.
        embedding_model: Name of the embedding model to use.
        documents_path: Path to the documents directory.
        reload: Whether to reload documents into vector store.

    Returns:
        A configured research agent instance.
    """
    vector_store = _create_vector_store(embedding_model, documents_path, reload=reload)
    return ResearchAgent(
        llm_model=llm_model,
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

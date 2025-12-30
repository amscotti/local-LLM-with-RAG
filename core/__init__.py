"""Core module for local LLM with RAG functionality."""

from core.agent import ResearchAgent, create_research_agent
from core.document_loader import load_documents, load_documents_into_database
from core.models import check_if_model_is_available, get_list_of_models

__all__ = [
    "ResearchAgent",
    "create_research_agent",
    "load_documents",
    "load_documents_into_database",
    "check_if_model_is_available",
    "get_list_of_models",
]

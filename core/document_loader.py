import logging
import os
from pathlib import Path

import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from markitdown import MarkItDown

logger = logging.getLogger(__name__)

PERSIST_DIRECTORY = "storage"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# Supported file extensions for document loading
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".md",
    ".html",
    ".csv",
    ".json",
}

# Default embedding model and its dimensions
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_DIMENSIONS = 768

# Get Ollama embedding function from LanceDB registry
ollama_embed = get_registry().get("ollama")

# Singleton database connection to prevent stale file references
_db_connection: lancedb.DBConnection | None = None


def get_db_connection() -> lancedb.DBConnection:
    """
    Get or create singleton database connection.

    Using a single connection prevents stale file references that occur
    when multiple connections are created and tables are dropped/recreated.
    """
    global _db_connection
    db_path = os.path.join(PERSIST_DIRECTORY, "lancedb")
    if _db_connection is None:
        _db_connection = lancedb.connect(db_path)
    return _db_connection


def get_embedding_function(model_name: str = DEFAULT_EMBEDDING_MODEL):
    """Create an Ollama embedding function for LanceDB."""
    return ollama_embed.create(name=model_name)


# Create embedding function at module level for type-safe model definition
_default_embedding_func = get_embedding_function()


class Document(LanceModel):
    """Document model for vector storage with nomic-embed-text embeddings."""

    text: str = _default_embedding_func.SourceField()
    source: str
    page: int
    vector: Vector(EMBEDDING_DIMENSIONS) = _default_embedding_func.VectorField()  # type: ignore[valid-type]


def split_text(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[str]:
    """Split text into overlapping chunks."""
    if len(text) <= chunk_size:
        return [text] if text.strip() else []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap

    return chunks


def load_file(path: Path) -> list[dict]:
    """Load any supported file and return chunks with metadata."""
    documents = []
    try:
        md = MarkItDown(enable_plugins=False)
        result = md.convert(str(path))

        if result.text_content:
            chunks = split_text(result.text_content)
            for chunk in chunks:
                documents.append(
                    {
                        "text": chunk,
                        "source": str(path),
                        "page": 1,
                    }
                )
    except Exception as e:
        logger.warning(f"Failed to load {path}: {e}")
    return documents


def load_documents(path: str) -> list[dict]:
    """
    Load documents from the specified directory path.

    Supports PDF, Word, PowerPoint, Excel, Markdown, HTML, CSV, and JSON files.

    Args:
        path: The path to the directory containing documents.

    Returns:
        List of document dictionaries with text, source, and page.

    Raises:
        FileNotFoundError: If the specified path does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified path does not exist: {path}")

    documents = []
    root = Path(path)

    for ext in SUPPORTED_EXTENSIONS:
        for file_path in root.rglob(f"*{ext}"):
            logger.info(f"Loading: {file_path}")
            documents.extend(load_file(file_path))

    logger.info(f"Loaded {len(documents)} document chunks")
    return documents


def load_documents_into_database(
    model_name: str, documents_path: str, reload: bool = True
) -> lancedb.table.Table:
    """
    Load documents from the specified directory into LanceDB.

    Args:
        model_name: Name of the Ollama embedding model (must be nomic-embed-text).
        documents_path: Path to the documents directory.
        reload: Whether to reload from documents or use existing table.

    Returns:
        LanceDB table with loaded documents.
    """
    db = get_db_connection()
    table_name = "documents"

    if reload:
        logger.info("Loading documents into LanceDB...")
        raw_documents = load_documents(documents_path)

        if not raw_documents:
            logger.warning("No documents found to load")
            # Create empty table
            if table_name in db.table_names():
                db.drop_table(table_name)
            return db.create_table(table_name, schema=Document)

        logger.info(f"Creating embeddings for {len(raw_documents)} chunks...")

        # Drop existing table if it exists
        if table_name in db.table_names():
            db.drop_table(table_name)

        # Create table with documents (embeddings computed automatically)
        table = db.create_table(table_name, schema=Document)
        table.add(raw_documents)

        logger.info(f"Added {len(raw_documents)} documents to LanceDB")
        return table
    else:
        logger.info("Loading existing LanceDB table...")
        if table_name in db.table_names():
            return db.open_table(table_name)
        else:
            # No existing table, need to create one
            logger.warning("No existing table found, creating empty table")
            return db.create_table(table_name, schema=Document)

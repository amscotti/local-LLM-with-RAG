from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader
)
import os
from typing import List
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

PERSIST_DIRECTORY = "storage"
TEXT_SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


def load_documents_into_database(model_name: str, documents_path: str, reload: bool = True) -> Chroma:
    """
    Loads documents from the specified directory into the Chroma database
    after splitting the text into chunks.

    Returns:
        Chroma: The Chroma database with loaded documents.
    """

    if reload:
        print("Loading documents")
        raw_documents = load_documents(documents_path)
        documents = TEXT_SPLITTER.split_documents(raw_documents)

        print("Creating embeddings and loading documents into Chroma")
        return Chroma.from_documents(
            documents=documents,
            embedding=OllamaEmbeddings(model=model_name),
            persist_directory=PERSIST_DIRECTORY
        )
    else:
        return Chroma(
            embedding_function=OllamaEmbeddings(model=model_name),
            persist_directory=PERSIST_DIRECTORY
        )


def load_documents(path: str) -> List[Document]:
    """
    Loads documents from the specified directory path.

    This function supports loading of PDF, Markdown, and HTML documents by utilizing
    different loaders for each file type. It checks if the provided path exists and
    raises a FileNotFoundError if it does not. It then iterates over the supported
    file types and uses the corresponding loader to load the documents into a list.

    Args:
        path (str): The path to the directory containing documents to load.

    Returns:
        List[Document]: A list of loaded documents.

    Raises:
        FileNotFoundError: If the specified path does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified path does not exist: {path}")

    loaders = {
        ".pdf": DirectoryLoader(
            path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True,
            use_multithreading=True,
        ),
        ".md": DirectoryLoader(
            path,
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=True,
        ),
    }

    docs = []
    for file_type, loader in loaders.items():
        print(f"Loading {file_type} files")
        loaded_docs = loader.load()
        
        for doc in loaded_docs:
            doc.metadata['source'] = os.path.basename(doc.metadata['source']) if 'source' in doc.metadata else 'unknown_source'
            doc.metadata['page'] = '1'
        
        print(f"Loaded {len(loaded_docs)} {file_type} files")
        docs.extend(loaded_docs)
    print(f"Total loaded {len(docs)} documents")
    return docs

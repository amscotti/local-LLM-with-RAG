# Local LLM with RAG

<p align="center">
    <img src="images/wizard_experimenting.jpg" alt="A wizard experimenting - Leonardo AI" width="600">
</p>

This project is an experimental sandbox for testing out ideas related to running local Large Language Models (LLMs) with [Ollama](https://ollama.ai/) to perform Retrieval-Augmented Generation (RAG) for answering questions based on sample PDFs. In this project, we are also using Ollama to create embeddings with the [nomic-embed-text](https://ollama.com/library/nomic-embed-text) to use with [Chroma](https://docs.trychroma.com/). Please note that the embeddings are reloaded each time the application runs, which is not efficient and is only done here for testing purposes.

[![asciicast](https://asciinema.org/a/fepTvXf1UiDpRUhhNiswL8isu.svg)](https://asciinema.org/a/fepTvXf1UiDpRUhhNiswL8isu)

There is also a web UI created using [Streamlit](https://streamlit.io/) to provide a different way to interact with Ollama.

<p align="center">
    <img src="images/streamlit_ui.png" alt="Screenshot of Streamlit web UI" width="600">
</p>

## Requirements

- [Ollama](https://ollama.ai/) verson 0.5.7 or higher.

## Setup

1. Clone this repository to your local machine.
2. Install UV using instructions from the Astral site, [Installation](https://docs.astral.sh/uv/#installation)
3. Create a virtual environment and install the required Python packages by running `uv sync`

## Running the Project

**Note:** The first time you run the project, it will download the necessary models from Ollama for the LLM and embeddings. This is a one-time setup process and may take some time depending on your internet connection.

1. Run the main script with `uv app.py -m <model_name> -p <path_to_documents>` to specify a model and the path to documents. If no model is specified, it defaults to [mistral](https://ollama.com/library/mistral). If no path is specified, it defaults to `Research` located in the repository for example purposes.
2. Optionally, you can specify the embedding model to use with `-e <embedding_model_name>`. If not specified, it defaults to [nomic-embed-text](https://ollama.com/library/nomic-embed-text).

This will load the PDFs and Markdown files, generate embeddings, query the collection, and answer the question defined in `app.py`.

## Running the Streamlit UI

Run the Streamlit application by executing `uv streamlit run ui.py` in your terminal.

This will start a local web server and open a new tab in your default web browser where you can interact with the application. The Streamlit UI allows you to select models, select a folder, providing an easier and more intuitive way to interact with the RAG chatbot system compared to the command-line interface. The application will handle the loading of documents, generating embeddings, querying the collection, and displaying the results interactively.

## Technologies Used

- [Langchain](https://github.com/langchain/langchain): A Python library for working with Large Language Model
- [Ollama](https://ollama.ai/): A platform for running Large Language models locally.
- [Chroma](https://docs.trychroma.com/): A vector database for storing and retrieving embeddings.
- [PyPDF](https://pypi.org/project/PyPDF2/): A Python library for reading and manipulating PDF files.
- [Streamlit](https://streamlit.io/): A web framework for creating interactive applications for machine learning and data science projects.
- [UV](https://astral.sh/uv): A fast and efficient Python package installer and resolver.





.venv для пользователя 1
.venv2dom для пользователя дом


Для запуска СЕРВЕРА - uvicorn app:app --host 0.0.0.0 --port 8000 
АДМИНКИ - streamlit run ui.py
ИНТЕРФЕЙСА ПОЛЬЗОВАТЕЛЯ - streamlit run ui_client.py

адрес - http://192.168.81.143:8000/docs#/default/initialize_initialize_post

параметры для инициализации - 
{
  "model_name": "mistral",
  "embedding_model_name": "nomic-embed-text",
  "documents_path": "Research"
}


{
  "model_name": "gemma3:27b-it-qat",
  "embedding_model_name": "snowflake-arctic-embed2:latest",
  "documents_path": "Research"
}

{
  "model_name": "ilyagusev/saiga_llama3:latest",
  "embedding_model_name": "snowflake-arctic-embed2:latest",
  "documents_path": "Research"
}

проверь


{
  "best_hyperparameters": {
    "embedding_model_name": "snowflake-arctic-embed2:latest",
    "learning_rate": 0.004440919399158963,
    "batch_size": 24,
    "chunk_size": 861,
    "chunk_overlap": 324,
    "n_top_cos": 6
  }
}
# Local LLM with RAG

<p align="center">
    <img src="images/wizard_experimenting.jpg" alt="A wizard experimenting - Leonardo AI" width="600">
</p>

This project is an experimental sandbox for testing out ideas related to running local Large Language Models (LLMs) with [Ollama](https://ollama.ai/) to perform Retrieval-Augmented Generation (RAG) for answering questions based on sample PDFs. In this project, we are also experimenting with [jina-embeddings-v2-base-en](https://huggingface.co/jinaai/jina-embeddings-v2-base-en) to create embeddings for [Chroma](https://docs.trychroma.com/). Please note that the embeddings are reloaded each time the application runs, which is not efficient and is only done here for testing purposes.

[![asciicast](https://asciinema.org/a/0kY8Vbbxvgi8M4y4Qmn4OhROh.svg)](https://asciinema.org/a/0kY8Vbbxvgi8M4y4Qmn4OhROh)

## Requirements

- [Ollama](https://ollama.ai/) installed with the [Mistral 7B](https://huggingface.co/mistralai/Mistral-7B-v0.1) `mistral` pulled down, by running `ollama pull mistral`

## Setup

1. Clone this repository to your local machine.
2. Create a Python virtual environment by running `python3 -m venv env`.
3. Activate the virtual environment by running `source env/bin/activate` on Unix or MacOS, or `.\env\Scripts\activate` on Windows.
4. Install the required Python packages by running `pip install -r requirements.txt`.

## Running the Project

1. Ensure your virtual environment is activated.
2. Run the main script with `python app.py`.

This will load the PDFs, generate embeddings, query the collection, and answer the question defined in `app.py`.

## Technologies Used

- [Langchain](https://github.com/langchain/langchain): A Python library for working with Large Language Model
- [PyTorch](https://pytorch.org/): An open source machine learning framework.
- [Ollama](https://ollama.ai/): A platform for running Large Language models locally.
- [Chroma](https://docs.trychroma.com/): A vector database for storing and retrieving embeddings.
- [Transformers](https://huggingface.co/transformers/): A Python library for state-of-the-art natural language processing.
- [PyPDF](https://pypi.org/project/PyPDF2/): A Python library for reading and manipulating PDF files.

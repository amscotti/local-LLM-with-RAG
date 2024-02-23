from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from JinaAIEmbeddings import JinaAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = Ollama(model="gemma", callbacks=[StreamingStdOutCallbackHandler()])

# Define the question to be answered
question = "What is the memory stream, and how does it help the agents?"

directoryLoader = DirectoryLoader(
    "PDFs",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
    show_progress=True,
    use_multithreading=True,
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


prompt_template = """
### Instruction:
You're helpful assistant, who answers questions based upon provided research in a distinct and clear way.

## Research:
{context}

## Question:
{question}
"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


def main():
    print("Loading documents into Chroma")

    # Initialize the directory loader
    raw_documents = directoryLoader.load()
    documents = text_splitter.split_documents(raw_documents)

    # Load the embeddings into Chroma
    db = Chroma.from_documents(documents, JinaAIEmbeddings())

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=db.as_retriever(search_kwargs={"k": 8}),
        chain_type_kwargs={"prompt": PROMPT},
    )

    print(f"\nAnswering question: {question}\n")
    qa_chain.invoke({"query": question})


if __name__ == "__main__":
    main()

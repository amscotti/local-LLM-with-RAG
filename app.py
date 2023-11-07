from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.llms import Ollama
from JinaAIEmbeddings import JinaAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = Ollama(model="nous-hermes:13b-q4_0", callbacks=[StreamingStdOutCallbackHandler()])

# Define the question to be answered
question = "What is the memory stream, and how does it help the agents?"

# Initialize the directory loader
raw_documents = DirectoryLoader('PDFs', 
                                glob="**/*.pdf", 
                                loader_cls=PyPDFLoader, 
                                show_progress=True, 
                                use_multithreading=True).load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

# Load the embeddings into Chroma
print("Loading documents into Chroma\n")
db = Chroma.from_documents(documents, JinaAIEmbeddings())

print(f"Answering question: {question}\n")

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

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=db.as_retriever(search_kwargs={"k": 8}),
    chain_type_kwargs={'prompt': PROMPT}
)

qa_chain({"query": question})

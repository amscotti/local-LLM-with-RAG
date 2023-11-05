from transformers import AutoModel
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.prompts import PromptTemplate
import chromadb
from langchain.llms import Ollama

# Define the question to be answered
question = "What is the advantages of using multiple LLM agents?"

# Initialize Chroma client and create a collection
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="examples")

# Load the pretrained model for creating embeddings
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True, device_map="auto")

# Initialize the directory loader
loader = DirectoryLoader('PDFs', glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True, use_multithreading=True)

# Load the documents
docs = loader.load()

# Extract the text and metadata from the documents
document_text = [doc.page_content for doc in docs]
document_metadata = [doc.metadata for doc in docs]

# Generate embeddings for the documents
print("Generating embedding")
embeddings = model.encode(document_text)

# Load the embeddings into Chroma
print("Loading embedding into chroma")
collection.add(
    documents=document_text,
    embeddings=embeddings.tolist(),
    metadatas=document_metadata,
    ids=[f'{i["source"]}_{i["page"]}' for i in document_metadata]
)

# Create an embedding for the question
print("Creating embedding from question")
questions_embeddings = model.encode([question])

# Query the collection with the question embedding
results = collection.query(
    query_embeddings=questions_embeddings.tolist(),
    n_results=6
)

# Initialize the LLM and define the prompt template
print(f"Answering question: {question}\n")
llm = Ollama(model="nous-hermes:13b-q4_0")
template = """
You're helpful assistant, who answers questions based upon provided research.

## Research
{research}

## Question
{question}
"""

# Create the prompt and chain it with the LLM
prompt = PromptTemplate(
    template=template,
    input_variables=["question", "research"],
)
chain = prompt | llm 

# Invoke the chain with the question and research and print the answer
answer = chain.invoke({'question': question, 'research': '\n'.join(results['documents'][0])})
print(answer)

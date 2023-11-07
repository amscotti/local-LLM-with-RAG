from langchain.embeddings.base import Embeddings
from transformers import AutoModel
from typing import List

class JinaAIEmbeddings(Embeddings):
    def __init__(self):
        # Load the pretrained model for creating embeddings
        self.model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True, device_map="auto")

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return self.model.encode(documents).tolist()

    def embed_query(self, query: str) -> List[float]:
        return self.model.encode([query]).tolist()[0]
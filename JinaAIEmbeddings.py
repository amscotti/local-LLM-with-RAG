from langchain.embeddings.base import Embeddings
from transformers import AutoModel
from typing import List


class JinaAIEmbeddings(Embeddings):
    def __init__(self):
        # Load the pretrained model for creating embeddings
        self.model = AutoModel.from_pretrained(
            "jinaai/jina-embeddings-v2-small-en",
            trust_remote_code=True,
            device_map="auto",
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode([text]).tolist()[0]

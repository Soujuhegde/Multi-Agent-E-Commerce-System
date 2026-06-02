"""
Retriever
"""

import json

from src.llm.embeddings import (
    EmbeddingService
)

from src.rag.vector_store import (
    VectorStore
)


class Retriever:

    def __init__(self):

        self.store = VectorStore()

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ):

        query_embedding = (
            EmbeddingService
            .generate_embedding(query)
        )

        documents = (
            self.store
            .get_all_documents()
        )

        scored_docs = []

        for content, embedding in documents:

            embedding = (
                json.loads(
                    embedding
                )
            )

            score = self.similarity(
                query_embedding,
                embedding
            )

            scored_docs.append(
                (
                    score,
                    content
                )
            )

        scored_docs.sort(
            reverse=True
        )

        return [
            doc[1]
            for doc in scored_docs[:top_k]
        ]

    @staticmethod
    def similarity(
        emb1,
        emb2
    ):

        return sum(
            a * b
            for a, b in zip(
                emb1,
                emb2
            )
        )
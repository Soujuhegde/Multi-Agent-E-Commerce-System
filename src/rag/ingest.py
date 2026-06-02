"""
Document Ingestion Pipeline
"""

from pathlib import Path

from src.rag.chunking import (
    TextChunker
)

from src.rag.vector_store import (
    VectorStore
)

from src.llm.embeddings import (
    EmbeddingService
)


class DocumentIngestion:

    def __init__(self):

        self.vector_store = (
            VectorStore()
        )

    def ingest_file(
        self,
        file_path: str
    ):

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(
                file_path
            )

        text = path.read_text(
            encoding="utf-8"
        )

        chunks = (
            TextChunker.chunk_text(
                text
            )
        )

        for chunk in chunks:

            embedding = (
                EmbeddingService
                .generate_embedding(
                    chunk
                )
            )

            self.vector_store.add_document(
                content=chunk,
                embedding=embedding
            )

        print(
            f"Ingested {len(chunks)} chunks"
        )
"""
Text Chunking Utilities
"""

from typing import List


class TextChunker:

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[str]:
        """
        Split text into overlapping chunks.
        """
        if not text:
            return []

        # Simple character-based or paragraph-based chunking
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks = []
        current_chunk = []
        current_len = 0

        for paragraph in paragraphs:
            if current_len + len(paragraph) > chunk_size and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                # Keep overlap: keep last paragraph if it fits in overlap
                if len(paragraph) < overlap:
                    current_chunk = [current_chunk[-1], paragraph] if len(current_chunk) > 1 else [paragraph]
                    current_len = sum(len(p) for p in current_chunk)
                else:
                    current_chunk = [paragraph]
                    current_len = len(paragraph)
            else:
                current_chunk.append(paragraph)
                current_len += len(paragraph)

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks
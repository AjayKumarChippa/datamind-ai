from rag.loader import load_pdf
from rag.splitter import split_text
from rag.embeddings import embed_chunks, embed_text
from rag.vector_store import VectorStore


class Retriever:

    def __init__(self):
        self.vector_store = VectorStore()

    def ingest_document(self, file_path: str):
        # 1. Extract text
        text = load_pdf(file_path)

        # 2. Split text into chunks
        chunks = split_text(text)

        # 3. Generate embeddings
        embeddings = embed_chunks(chunks)

        # 4. Store embeddings + chunks
        self.vector_store.add(
            embeddings,
            chunks
        )

        return len(chunks)

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ):

        # 1. Embed the user's question
        query_embedding = embed_text(query)

        # 2. Search vector store
        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        return results
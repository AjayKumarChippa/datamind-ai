import faiss
import numpy as np


class VectorStore:

    def __init__(self):
        self.index = None
        self.documents = []

    def add(self, embeddings: list[list[float]], documents: list[str]):
        vectors = np.array(embeddings, dtype="float32")

        dimension = vectors.shape[1]

        if self.index is None:
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(vectors)

        self.documents.extend(documents)

    def search(self, query_embedding: list[float], top_k: int = 3):
        if self.index is None or self.index.ntotal == 0:
            return []

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_vector,
            top_k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):
            if index != -1:
                results.append(
                    {
                        "document": self.documents[index],
                        "distance": float(distance)
                    }
                )

        return results
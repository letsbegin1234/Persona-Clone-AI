import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim):
        # Use Inner Product index — after L2-normalizing vectors,
        # inner product = cosine similarity (range 0 to 1)
        self.index = faiss.IndexFlatIP(dim)
        self.data = []

    def add(self, embeddings, pairs):
        vecs = np.array(embeddings).astype('float32')
        # L2-normalize so inner product == cosine similarity
        faiss.normalize_L2(vecs)
        self.index.add(vecs)
        self.data.extend(pairs)

    def search(self, query_embedding, k=5):
        query = np.array(query_embedding).astype('float32')
        if query.ndim == 1:
            query = query.reshape(1, -1)
        # Normalize query too
        faiss.normalize_L2(query)

        # Scores are cosine similarities (0 to 1, higher = more similar)
        scores, indices = self.index.search(query, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.data):
                results.append((self.data[idx], float(score)))

        return results
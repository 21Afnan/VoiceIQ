import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# -----------------------------
# Config
# -----------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHUNKS_FILE = os.path.join(DATA_DIR, "chunks.json")
EMBEDDINGS_FILE = os.path.join(DATA_DIR, "embeddings.json")

TOP_K = 5  # number of chunks to retrieve
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # must match the model used during ingestion


# -----------------------------
# Load JSON safely
# -----------------------------
def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# Build FAISS index
# -----------------------------
def build_faiss_index(embeddings):
    if len(embeddings) == 0:
        raise ValueError("No embeddings found to build FAISS index")

    vectors = np.array([e["embedding"] for e in embeddings]).astype("float32")

    dim = vectors.shape[1]  # embedding size
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    return index


# -----------------------------
# Load everything once
# -----------------------------
class RAGRetriever:
    def __init__(self):
        try:
            # Important: this model must match the one used to generate embeddings.json,
            # otherwise FAISS search will fail due to dimension mismatch.
            self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

            self.chunks = load_json(CHUNKS_FILE)
            self.embeddings = load_json(EMBEDDINGS_FILE)

            self.index = build_faiss_index(self.embeddings)

        except Exception as e:
            raise RuntimeError(f"Failed to initialize RAG system: {e}")

    # -----------------------------
    # Retrieve relevant chunks
    # -----------------------------
    def retrieve(self, query, top_k=TOP_K):
        if not query or not query.strip():
            raise ValueError("Query is empty")

        top_k = int(top_k) if top_k is not None else TOP_K
        if top_k <= 0:
            return []

        # FAISS requires k to be sensible; cap it to available vectors/chunks.
        top_k = min(top_k, len(self.chunks), int(getattr(self.index, "ntotal", len(self.chunks))))
        if top_k <= 0:
            return []

        try:
            query_vector = self.model.encode(query).astype("float32")
            query_vector = np.expand_dims(query_vector, axis=0)

            index_dim = int(getattr(self.index, "d", query_vector.shape[1]))
            if query_vector.shape[1] != index_dim:
                raise ValueError(
                    "Embedding dimension mismatch between query and FAISS index. "
                    f"Query dim={query_vector.shape[1]} vs index dim={index_dim}. "
                    "Regenerate embeddings.json using the same model as the retriever "
                    f"(expected {EMBEDDING_MODEL_NAME})."
                )

            distances, indices = self.index.search(query_vector, top_k)

            results = []
            for idx in indices[0]:
                if idx < len(self.chunks):
                    results.append(self.chunks[idx])

            return results

        except Exception as e:
            raise RuntimeError(f"Retrieval failed: {e}")
# -----------------------------
# Test RAG manually
# -----------------------------
if __name__ == "__main__":
    print("Initializing RAG Retriever...")
    retriever = RAGRetriever()
    print("RAG system ready")

    while True:
        query = input("\nAsk a question about Sunmarke (type 'exit' to quit): ")

        if query.lower() == "exit":
            print(" Exiting...")
            break

        try:
            results = retriever.retrieve(query)

            if not results:
                print("No relevant information found.")
            else:
                print("\n Retrieved Context:\n")
                for i, chunk in enumerate(results, 1):
                    print(f"\n--- Result {i} ---")
                    print(f"Source: {chunk['source_url']}")
                    print(chunk["content"][:500], "...\n")

        except Exception as e:
            print(f" Error: {e}")

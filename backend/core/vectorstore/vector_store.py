import chromadb
import requests
from typing import List, Dict
from core.config.config import settings


class VectorStore:
    """Manages storing and retrieving vector embeddings securely using Static API Tokens."""

    def __init__(self):
        """Initialize ChromaDB client with API Token authentication."""
        self.chroma_url = f"{settings.CHROMADB_HOST}:{settings.CHROMADB_PORT}"

        # Headers for authentication
        self.headers = {
            "Authorization": f"Bearer {settings.CHROMA_SERVER_AUTHN_CREDENTIALS}"
        }

        # Establish connection with ChromaDB
        self.client = chromadb.HttpClient(
            host=settings.CHROMADB_HOST,
            port=settings.CHROMADB_PORT,
            headers=self.headers
        )
        self.collection = self.client.get_or_create_collection(name="documents")

    def health_check(self):
        # Check ChromaDB connectivity with API Token
        try:
            response = requests.get(f"http://{self.chroma_url}/api/v1/status", headers=self.headers)
            if response.status_code == 200:
                return "✅ Successfully connected to ChromaDB with API Token!"
            else:
                return f"❌ ChromaDB Connection Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            return f"❌ Failed to connect to ChromaDB: {e}"

    def store_vectors(self, document_id: str, text_chunks: List[str], vectors: List[List[float]]):
        """
        Securely stores vector embeddings with API Token authentication.

        Args:
            document_id (str): Unique identifier for the document.
            text_chunks (List[str]): List of text segments.
            vectors (List[List[float]]): Corresponding vector embeddings.
        """
        for idx, vector in enumerate(vectors):
            vector_id = f"{document_id}_{idx}"
            self.collection.add(
                ids=[vector_id],
                embeddings=[vector],
                metadatas=[{"document_id": document_id, "text": text_chunks[idx]}]
            )

    def search_similar_vectors(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """
        Securely searches for top-k similar vectors using API Token authentication.

        Args:
            query_vector (List[float]): The query embedding vector.
            top_k (int): Number of similar results to retrieve.

        Returns:
            List[Dict]: List of matching documents.
        """
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )

        if not results["ids"]:
            return []

        return [
            {
                "document_id": result_meta["document_id"],
                "text": result_meta["text"],
                "similarity_score": result_score
            }
            for result_id, result_meta, result_score in zip(
                results["ids"][0], results["metadatas"][0], results["distances"][0]
            )
        ]

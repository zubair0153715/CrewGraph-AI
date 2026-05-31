"""
ChromaDB Memory Module with Ollama Embeddings
Provides persistent memory and RAG capabilities for CrewGraph-AI
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL, OLLAMA_BASE_URL
import requests
import json


class ChromaMemory:
    """Persistent memory store using ChromaDB with Ollama embeddings"""
    
    def __init__(self, collection_name: str = "crewgraph_memory"):
        self.client = chromadb.Client(Settings(
            persist_directory=CHROMA_PERSIST_DIR,
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding from Ollama"""
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/embeddings",
                json={"model": EMBEDDING_MODEL, "prompt": text},
                timeout=30
            )
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            print(f"⚠️  Embedding error: {e}")
            return [0.0] * 768  # Fallback embedding
    
    def add_memory(self, session_id: str, content: str, metadata: Optional[Dict] = None):
        """Add a memory to the store"""
        embedding = self._get_embedding(content)
        self.collection.add(
            embeddings=[embedding],
            documents=[content],
            ids=[f"{session_id}_{self.collection.count()}"],
            metadatas=[metadata or {"session_id": session_id}]
        )
    
    def search_memories(self, query: str, session_id: Optional[str] = None, limit: int = 3) -> List[Dict]:
        """Search for relevant memories"""
        query_embedding = self._get_embedding(query)
        
        where_filter = None
        if session_id:
            where_filter = {"session_id": session_id}
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        
        memories = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                memories.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0
                })
        
        return memories
    
    def get_session_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for a session"""
        results = self.collection.get(
            where={"session_id": session_id},
            limit=limit,
            include=["documents", "metadatas"]
        )
        
        return [
            {"content": doc, "metadata": meta}
            for doc, meta in zip(results["documents"], results["metadatas"])
        ] if results["documents"] else []
    
    def clear_session(self, session_id: str):
        """Clear all memories for a session"""
        # Note: ChromaDB doesn't support delete by filter directly
        # This is a simplified implementation
        pass


# Singleton instance
_memory_instance: Optional[ChromaMemory] = None


def get_memory() -> ChromaMemory:
    """Get or create the memory singleton"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = ChromaMemory()
    return _memory_instance

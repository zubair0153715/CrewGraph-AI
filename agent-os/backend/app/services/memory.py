from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any, Optional
from app.core.config import settings


class MemoryService:
    """Service for managing agent memory with Qdrant"""
    
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )
        self._initialize_collections()
    
    def _initialize_collections(self):
        """Create necessary collections if they don't exist"""
        collections = ["agent_memory", "task_memory"]
        
        for collection_name in collections:
            try:
                self.client.get_collection(collection_name)
            except Exception:
                # Collection doesn't exist, create it
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
    
    def add_memory(
        self,
        agent_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        collection: str = "agent_memory"
    ) -> str:
        """Add a memory to the vector database"""
        from app.services.llm import get_embedding_model
        
        embedding_model = get_embedding_model()
        vector = embedding_model.embed_query(content)
        
        point_id = f"{agent_id}_{len(self.get_memories(agent_id, collection))}"
        
        self.client.upsert(
            collection_name=collection,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "agent_id": agent_id,
                        "content": content,
                        **(metadata or {})
                    }
                )
            ]
        )
        
        return point_id
    
    def search_memories(
        self,
        agent_id: str,
        query: str,
        limit: int = 5,
        collection: str = "agent_memory"
    ) -> List[Dict[str, Any]]:
        """Search for relevant memories"""
        from app.services.llm import get_embedding_model
        
        embedding_model = get_embedding_model()
        query_vector = embedding_model.embed_query(query)
        
        results = self.client.search(
            collection_name=collection,
            query_vector=query_vector,
            query_filter={
                "must": [
                    {"key": "agent_id", "match": {"value": agent_id}}
                ]
            },
            limit=limit
        )
        
        return [
            {
                "content": hit.payload.get("content"),
                "metadata": hit.payload,
                "score": hit.score
            }
            for hit in results
        ]
    
    def get_memories(
        self,
        agent_id: str,
        collection: str = "agent_memory",
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get all memories for an agent"""
        # Note: In production, use proper pagination
        results = self.client.scroll(
            collection_name=collection,
            scroll_filter={
                "must": [
                    {"key": "agent_id", "match": {"value": agent_id}}
                ]
            },
            limit=limit
        )
        
        return [
            {
                "content": point.payload.get("content"),
                "metadata": point.payload,
                "id": point.id
            }
            for point in results[0]
        ]
    
    def delete_memory(self, memory_id: str, collection: str = "agent_memory"):
        """Delete a specific memory"""
        self.client.delete(
            collection_name=collection,
            points_selector={"points": [memory_id]}
        )
    
    def clear_agent_memories(self, agent_id: str, collection: str = "agent_memory"):
        """Clear all memories for an agent"""
        memories = self.get_memories(agent_id, collection)
        if memories:
            self.client.delete(
                collection_name=collection,
                points_selector={"points": [m["id"] for m in memories]}
            )


# Singleton instance
memory_service = MemoryService()

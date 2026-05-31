"""
Configuration settings for CrewGraph-AI
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Settings
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:7b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Memory Settings
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

# Server Settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "7860"))

# Feature Flags
ENABLE_ROUTER = os.getenv("ENABLE_ROUTER", "true").lower() == "true"
ENABLE_VALIDATION = os.getenv("ENABLE_VALIDATION", "true").lower() == "true"
ENABLE_MEMORY = os.getenv("ENABLE_MEMORY", "true").lower() == "true"
ENABLE_HITL = os.getenv("ENABLE_HITL", "false").lower() == "true"  # Human-in-the-loop
ENABLE_PARALLEL = os.getenv("ENABLE_PARALLEL", "true").lower() == "true"  # Parallel execution
ENABLE_REFLECTION = os.getenv("ENABLE_REFLECTION", "true").lower() == "true"  # Agent reflection

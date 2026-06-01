from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from typing import Optional
from app.core.config import settings


def get_llm(model_name: Optional[str] = None) -> BaseChatModel:
    """
    Get LLM instance based on configured provider
    
    Args:
        model_name: Optional model name override
        
    Returns:
        Configured LangChain chat model
    """
    model = model_name or settings.DEFAULT_MODEL
    
    # Determine provider from settings
    provider = settings.llm_provider
    
    if provider == "openrouter":
        # OpenRouter supports multiple models
        return ChatOpenAI(
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=settings.OPENROUTER_API_KEY,
            model=model,
            temperature=0.7,
        )
    elif provider == "openai":
        return ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model=model,
            temperature=0.7,
        )
    elif provider == "groq":
        # Groq uses OpenAI-compatible API
        return ChatOpenAI(
            openai_api_base="https://api.groq.com/openai/v1",
            openai_api_key=settings.GROQ_API_KEY,
            model=model.replace("groq/", ""),
            temperature=0.7,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


def get_embedding_model():
    """Get embedding model for vector database"""
    from langchain_openai import OpenAIEmbeddings
    
    if settings.OPENROUTER_API_KEY:
        return OpenAIEmbeddings(
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=settings.OPENROUTER_API_KEY,
        )
    elif settings.OPENAI_API_KEY:
        return OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
        )
    else:
        raise ValueError("No embedding model API key configured")

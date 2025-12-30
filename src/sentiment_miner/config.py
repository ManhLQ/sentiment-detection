"""Configuration module for loading environment variables and setting up DSPy LM."""

import os
from pathlib import Path

import dspy
from dotenv import load_dotenv

# Load .env file from project root
_project_root = Path(__file__).parent.parent.parent.parent
_env_path = _project_root / ".env"
load_dotenv(_env_path)


def get_llm_backend() -> str:
    """Get the configured LLM backend (openai or ollama)."""
    return os.getenv("LLM_BACKEND", "openai").lower()


def get_lm() -> dspy.LM:
    """
    Create and return a DSPy Language Model based on environment configuration.
    
    Returns:
        dspy.LM: Configured language model (OpenAI or Ollama)
    
    Raises:
        ValueError: If LLM_BACKEND is not 'openai' or 'ollama'
        ValueError: If required API key is missing for OpenAI backend
    """
    backend = get_llm_backend()
    
    if backend == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your-openai-api-key-here":
            raise ValueError(
                "OPENAI_API_KEY not configured. Please set it in your .env file."
            )
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return dspy.LM(model=f"openai/{model}", api_key=api_key)
    
    elif backend == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3.2")
        return dspy.LM(
            model=f"ollama_chat/{model}",
            api_base=base_url,
            api_key=""  # Ollama doesn't require an API key
        )
    
    else:
        raise ValueError(
            f"Invalid LLM_BACKEND: '{backend}'. Must be 'openai' or 'ollama'."
        )


def configure_dspy() -> dspy.LM:
    """
    Configure DSPy with the appropriate language model.
    
    Returns:
        dspy.LM: The configured language model
    """
    lm = get_lm()
    dspy.configure(lm=lm)
    return lm

"""
Zomato Restaurant Recommendation System

AI-powered restaurant recommendation service that combines structured data
with Large Language Models to provide personalized restaurant suggestions.
"""

__version__ = "0.3.0"

from .data_loader import ZomatoDataLoader, DataLoaderError, SchemaValidationError
from .models import UserPreferences, Recommendation, InputValidator, ValidationError, format_cost
from .filter_engine import DataFilterEngine, FilterEngineError, NoResultsError
from .prompt_builder import PromptBuilder, PromptBuilderError
from .llm_client import (
    LLMClient, 
    BaseLLMProvider, 
    OpenAIProvider, 
    GroqProvider, 
    OllamaProvider,
    LLMError,
    RateLimitError,
    AuthenticationError,
    APITimeoutError
)
from .formatter import ResponseFormatter, FormatterError, ParseError

__all__ = [
    # Data loading
    "ZomatoDataLoader",
    "DataLoaderError", 
    "SchemaValidationError",
    
    # Models
    "UserPreferences",
    "Recommendation",
    "InputValidator",
    "ValidationError",
    "format_cost",
    
    # Filter engine
    "DataFilterEngine",
    "FilterEngineError",
    "NoResultsError",
    
    # Prompt engine
    "PromptBuilder",
    "PromptBuilderError",
    
    # LLM client
    "LLMClient",
    "BaseLLMProvider",
    "OpenAIProvider",
    "GroqProvider",
    "OllamaProvider",
    "LLMError",
    "RateLimitError",
    "AuthenticationError",
    "APITimeoutError",
    
    # Response formatter
    "ResponseFormatter",
    "FormatterError",
    "ParseError",
]

"""
LLM Client Module

Provides abstraction for interacting with different LLM providers
(OpenAI, Groq, Ollama) with retry logic, rate limiting, and error handling.
"""

import os
import time
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple token bucket rate limiter for API calls.
    """
    
    def __init__(self, max_calls: int, time_window: float):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed in time window
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
        logger.info(f"Rate limiter initialized: {max_calls} calls per {time_window}s")
    
    def acquire(self) -> None:
        """
        Wait if necessary to respect rate limit.
        """
        now = datetime.now()
        
        # Remove calls outside the time window
        cutoff = now - timedelta(seconds=self.time_window)
        while self.calls and self.calls[0] < cutoff:
            self.calls.popleft()
        
        # Check if we've hit the limit
        if len(self.calls) >= self.max_calls:
            # Calculate how long to wait
            oldest_call = self.calls[0]
            wait_until = oldest_call + timedelta(seconds=self.time_window)
            wait_seconds = (wait_until - now).total_seconds()
            
            if wait_seconds > 0:
                logger.info(f"Rate limit reached. Waiting {wait_seconds:.2f}s...")
                time.sleep(wait_seconds)
                # Recursively check again after waiting
                return self.acquire()
        
        # Record this call
        self.calls.append(now)
    
    def reset(self) -> None:
        """Clear all recorded calls."""
        self.calls.clear()
        logger.debug("Rate limiter reset")


class LLMError(Exception):
    """Base exception for LLM client errors"""
    pass


class RateLimitError(LLMError):
    """Raised when API rate limit is exceeded"""
    pass


class AuthenticationError(LLMError):
    """Raised when API authentication fails"""
    pass


class APITimeoutError(LLMError):
    """Raised when API request times out"""
    pass


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", **default_params):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
            model: Model name
            **default_params: Default generation parameters
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise LLMError(
                "OpenAI library not installed. Install with: pip install openai"
            )
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.default_params = default_params
        logger.info(f"OpenAI provider initialized with model: {model}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: Input prompt
            **kwargs: Generation parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated text
        """
        # Merge default params with kwargs
        params = {**self.default_params, **kwargs}
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=params.get('temperature', 0.7),
                max_tokens=params.get('max_tokens', 1024),
                **{k: v for k, v in params.items() if k not in ['temperature', 'max_tokens']}
            )
            
            generated_text = response.choices[0].message.content
            logger.debug(f"OpenAI generated {len(generated_text)} characters")
            return generated_text
            
        except Exception as e:
            error_msg = str(e).lower()
            
            if 'rate_limit' in error_msg or '429' in error_msg:
                raise RateLimitError(f"OpenAI rate limit exceeded: {e}")
            elif 'authentication' in error_msg or '401' in error_msg or 'api_key' in error_msg:
                raise AuthenticationError(f"OpenAI authentication failed: {e}")
            elif 'timeout' in error_msg:
                raise APITimeoutError(f"OpenAI request timeout: {e}")
            else:
                raise LLMError(f"OpenAI API error: {e}")


class GroqProvider(BaseLLMProvider):
    """Groq API provider"""
    
    def __init__(self, api_key: str, model: str = "llama3-70b-8192", **default_params):
        """
        Initialize Groq provider.
        
        Args:
            api_key: Groq API key
            model: Model name
            **default_params: Default generation parameters
        """
        try:
            from groq import Groq
        except ImportError:
            raise LLMError(
                "Groq library not installed. Install with: pip install groq"
            )
        
        self.client = Groq(api_key=api_key)
        self.model = model
        self.default_params = default_params
        logger.info(f"Groq provider initialized with model: {model}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Groq API.
        
        Args:
            prompt: Input prompt
            **kwargs: Generation parameters
            
        Returns:
            Generated text
        """
        # Merge default params with kwargs
        params = {**self.default_params, **kwargs}
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=params.get('temperature', 0.7),
                max_tokens=params.get('max_tokens', 1024),
                **{k: v for k, v in params.items() if k not in ['temperature', 'max_tokens']}
            )
            
            generated_text = response.choices[0].message.content
            logger.debug(f"Groq generated {len(generated_text)} characters")
            return generated_text
            
        except Exception as e:
            error_msg = str(e).lower()
            
            if 'rate_limit' in error_msg or '429' in error_msg:
                raise RateLimitError(f"Groq rate limit exceeded: {e}")
            elif 'authentication' in error_msg or '401' in error_msg:
                raise AuthenticationError(f"Groq authentication failed: {e}")
            elif 'timeout' in error_msg:
                raise APITimeoutError(f"Groq request timeout: {e}")
            else:
                raise LLMError(f"Groq API error: {e}")


class OllamaProvider(BaseLLMProvider):
    """Ollama local provider"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2", **default_params):
        """
        Initialize Ollama provider.
        
        Args:
            base_url: Ollama server URL
            model: Model name
            **default_params: Default generation parameters
        """
        self.base_url = base_url
        self.model = model
        self.default_params = default_params
        logger.info(f"Ollama provider initialized with model: {model} at {base_url}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Ollama API.
        
        Args:
            prompt: Input prompt
            **kwargs: Generation parameters
            
        Returns:
            Generated text
        """
        import requests
        
        # Merge default params with kwargs
        params = {**self.default_params, **kwargs}
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": params.get('temperature', 0.7),
                        "num_predict": params.get('max_tokens', 1024),
                    }
                },
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            generated_text = result.get('response', '')
            
            logger.debug(f"Ollama generated {len(generated_text)} characters")
            return generated_text
            
        except requests.exceptions.Timeout:
            raise APITimeoutError("Ollama request timeout")
        except requests.exceptions.ConnectionError:
            raise LLMError(f"Cannot connect to Ollama at {self.base_url}. Is Ollama running?")
        except Exception as e:
            raise LLMError(f"Ollama API error: {e}")


class LLMClient:
    """
    High-level LLM client with provider abstraction, rate limiting, and retry logic.
    """
    
    def __init__(self, provider: str, model: str, api_key: Optional[str] = None, 
                 rate_limit_calls: int = 10, rate_limit_window: float = 60.0, **params):
        """
        Initialize LLM client.
        
        Args:
            provider: Provider name ("openai", "groq", or "ollama")
            model: Model name
            api_key: API key (read from env if None)
            rate_limit_calls: Maximum calls per time window (default: 10)
            rate_limit_window: Time window in seconds (default: 60)
            **params: Additional parameters (temperature, max_tokens, etc.)
        """
        self.provider_name = provider.lower()
        self.model = model
        self.params = params
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(rate_limit_calls, rate_limit_window)
        
        # Get API key from environment if not provided
        if api_key is None:
            if self.provider_name == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
            elif self.provider_name == "groq":
                api_key = os.getenv("GROQ_API_KEY")
        
        # Initialize provider
        if self.provider_name == "openai":
            if not api_key:
                raise AuthenticationError(
                    "OpenAI API key not provided. Set OPENAI_API_KEY environment variable."
                )
            self.provider = OpenAIProvider(api_key, model, **params)
            
        elif self.provider_name == "groq":
            if not api_key:
                raise AuthenticationError(
                    "Groq API key not provided. Set GROQ_API_KEY environment variable."
                )
            self.provider = GroqProvider(api_key, model, **params)
            
        elif self.provider_name == "ollama":
            base_url = params.pop('base_url', 'http://localhost:11434')
            self.provider = OllamaProvider(base_url, model, **params)
            
        else:
            raise LLMError(
                f"Unknown provider: {provider}. "
                f"Supported providers: openai, groq, ollama"
            )
        
        logger.info(f"LLMClient initialized with provider: {self.provider_name}, model: {model}")
    
    def generate(self, 
                 prompt: str,
                 max_retries: int = 3,
                 initial_retry_delay: float = 1.0,
                 **kwargs) -> str:
        """
        Generate text with rate limiting and retry logic.
        
        Args:
            prompt: Input prompt
            max_retries: Maximum number of retry attempts
            initial_retry_delay: Initial delay between retries (seconds)
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text
            
        Raises:
            LLMError: If all retries fail
        """
        last_error = None
        retry_delay = initial_retry_delay
        
        for attempt in range(max_retries):
            try:
                # Apply rate limiting before each attempt
                self.rate_limiter.acquire()
                
                logger.debug(f"Generation attempt {attempt + 1}/{max_retries}")
                result = self.provider.generate(prompt, **kwargs)
                
                if attempt > 0:
                    logger.info(f"Generation succeeded on attempt {attempt + 1}")
                
                return result
                
            except RateLimitError as e:
                last_error = e
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Rate limit hit (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {retry_delay:.1f}s..."
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"Rate limit exceeded after {max_retries} attempts")
                    raise
                    
            except APITimeoutError as e:
                last_error = e
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Request timeout (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {retry_delay:.1f}s..."
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error(f"Request timeout after {max_retries} attempts")
                    raise
                    
            except (AuthenticationError, LLMError) as e:
                # Don't retry authentication errors
                logger.error(f"LLM error: {e}")
                raise
        
        # Should not reach here, but just in case
        if last_error:
            raise last_error
        raise LLMError("Generation failed for unknown reason")
    
    def test_connection(self) -> bool:
        """
        Test connection to the LLM provider.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.generate("Hello", max_retries=1)
            logger.info("LLM connection test successful")
            return True
        except Exception as e:
            logger.error(f"LLM connection test failed: {e}")
            return False

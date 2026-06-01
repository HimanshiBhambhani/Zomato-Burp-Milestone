"""
Enhanced Error Handling and Recovery Module

Provides utilities for graceful degradation and error recovery.
"""

import logging
from typing import Optional, Callable, Any
from functools import wraps
import time

logger = logging.getLogger(__name__)


class ErrorRecovery:
    """Utilities for error recovery and graceful degradation"""
    
    @staticmethod
    def with_fallback(primary_func: Callable, fallback_func: Callable, 
                      error_message: str = "Primary function failed, using fallback") -> Any:
        """
        Execute primary function, fall back to fallback_func on error.
        
        Args:
            primary_func: Primary function to try
            fallback_func: Fallback function if primary fails
            error_message: Message to log on fallback
            
        Returns:
            Result from primary_func or fallback_func
        """
        try:
            return primary_func()
        except Exception as e:
            logger.warning(f"{error_message}: {e}")
            try:
                return fallback_func()
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
                raise
    
    @staticmethod
    def retry_with_exponential_backoff(func: Callable, max_attempts: int = 3, 
                                       initial_delay: float = 1.0, 
                                       max_delay: float = 60.0,
                                       exceptions: tuple = (Exception,)) -> Callable:
        """
        Decorator for retrying a function with exponential backoff.
        
        Args:
            func: Function to wrap
            max_attempts: Maximum retry attempts
            initial_delay: Initial delay between retries
            max_delay: Maximum delay between retries
            exceptions: Tuple of exceptions to catch and retry
            
        Returns:
            Wrapped function
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed: {e}. "
                            f"Retrying in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                        delay = min(delay * 2, max_delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed")
            
            if last_exception:
                raise last_exception
        
        return wrapper
    
    @staticmethod
    def safe_execute(func: Callable, default_value: Any = None, 
                    error_message: str = "Function execution failed") -> Any:
        """
        Execute function safely, return default value on error.
        
        Args:
            func: Function to execute
            default_value: Value to return on error
            error_message: Message to log on error
            
        Returns:
            Function result or default_value
        """
        try:
            return func()
        except Exception as e:
            logger.error(f"{error_message}: {e}")
            return default_value


class CircuitBreaker:
    """
    Circuit breaker pattern implementation for failing fast.
    
    Tracks failures and opens circuit after threshold, preventing
    cascading failures by failing fast.
    """
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Time to wait before attempting recovery (seconds)
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        logger.info(f"Circuit breaker initialized: threshold={failure_threshold}, timeout={recovery_timeout}s")
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function through circuit breaker.
        
        Args:
            func: Function to call
            *args, **kwargs: Arguments to pass to function
            
        Returns:
            Function result
            
        Raises:
            Exception: If circuit is open or function fails
        """
        if self.state == "open":
            # Check if recovery timeout has passed
            if self.last_failure_time and \
               time.time() - self.last_failure_time >= self.recovery_timeout:
                logger.info("Circuit breaker entering half-open state")
                self.state = "half-open"
            else:
                raise Exception(
                    f"Circuit breaker is open. Service temporarily unavailable. "
                    f"Retry after {self.recovery_timeout}s"
                )
        
        try:
            result = func(*args, **kwargs)
            
            # Success - reset or close circuit
            if self.state == "half-open":
                logger.info("Circuit breaker closing after successful call")
                self.state = "closed"
                self.failure_count = 0
            
            return result
            
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            logger.warning(
                f"Circuit breaker recorded failure {self.failure_count}/{self.failure_threshold}"
            )
            
            if self.failure_count >= self.failure_threshold:
                logger.error(f"Circuit breaker opening due to {self.failure_count} failures")
                self.state = "open"
            
            raise
    
    def reset(self):
        """Reset circuit breaker to closed state"""
        self.state = "closed"
        self.failure_count = 0
        self.last_failure_time = None
        logger.info("Circuit breaker manually reset")


def log_errors(func: Callable) -> Callable:
    """
    Decorator to log errors with full context.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"Error in {func.__name__}: {type(e).__name__}: {e}",
                exc_info=True
            )
            raise
    
    return wrapper

"""
Data Models Module

Defines core data structures for the restaurant recommendation system:
- UserPreferences: Input data from users
- Recommendation: Output recommendation structure
- InputValidator: Validates and sanitizes user inputs
"""

from dataclasses import dataclass, field
from typing import List, Optional
import re
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when input validation fails"""
    pass


@dataclass
class UserPreferences:
    """
    User preferences for restaurant recommendations.
    
    Attributes:
        location: City or locality name
        budget: Budget tier - "low", "medium", or "high"
        cuisine: Desired cuisine type(s)
        min_rating: Minimum acceptable rating (0-5)
        additional_prefs: Optional list of additional preferences
                         (e.g., "family-friendly", "quick service")
    """
    location: str
    budget: str  # "low" | "medium" | "high"
    cuisine: str
    min_rating: float
    additional_prefs: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate data after initialization"""
        # Normalize budget to lowercase
        if self.budget:
            self.budget = self.budget.lower()
        
        # Ensure min_rating is within valid range
        if self.min_rating < 0:
            self.min_rating = 0.0
        elif self.min_rating > 5:
            self.min_rating = 5.0


@dataclass
class Recommendation:
    """
    A single restaurant recommendation with explanation.
    
    Attributes:
        rank: Recommendation rank (1-based)
        restaurant_name: Name of the restaurant
        cuisine: Cuisine type(s)
        rating: Aggregate rating (0-5)
        estimated_cost: Cost for two people (formatted string)
        explanation: AI-generated explanation for the recommendation
        location: Restaurant location (optional)
        votes: Number of votes (optional)
    """
    rank: int
    restaurant_name: str
    cuisine: str
    rating: float
    estimated_cost: str
    explanation: str
    location: Optional[str] = None
    votes: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "rank": self.rank,
            "restaurant_name": self.restaurant_name,
            "cuisine": self.cuisine,
            "rating": self.rating,
            "estimated_cost": self.estimated_cost,
            "explanation": self.explanation,
            "location": self.location,
            "votes": self.votes,
        }


class InputValidator:
    """
    Validates and sanitizes user inputs to prevent injection attacks
    and ensure data quality.
    """
    
    # Valid budget options
    VALID_BUDGETS = {"low", "medium", "high"}
    
    # Max lengths for string inputs
    MAX_LOCATION_LENGTH = 100
    MAX_CUISINE_LENGTH = 100
    MAX_ADDITIONAL_PREF_LENGTH = 200
    MAX_ADDITIONAL_PREFS_COUNT = 10
    
    # Prompt injection patterns to detect and block
    INJECTION_PATTERNS = [
        r"ignore\s+(previous|above|prior)\s+instructions",
        r"disregard\s+(previous|above|prior)",
        r"forget\s+(previous|above|all)",
        r"<\s*script",
        r"javascript:",
        r"on(load|error|click)\s*=",
        r"eval\s*\(",
        r"exec\s*\(",
        r"system\s+prompt",
        r"you\s+are\s+now",
        r"new\s+instructions",
        r"developer\s+mode",
    ]
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 200) -> str:
        """
        Remove potentially dangerous characters and limit length.
        Detect and prevent prompt injection attempts.
        
        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
            
        Raises:
            ValidationError: If prompt injection attempt detected
        """
        if not text:
            return ""
        
        # Strip whitespace
        text = text.strip()
        
        # Check for prompt injection patterns
        text_lower = text.lower()
        for pattern in InputValidator.INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                logger.warning(f"Potential prompt injection detected: {pattern}")
                raise ValidationError(
                    "Input contains potentially malicious content. "
                    "Please rephrase your request."
                )
        
        # Remove control characters and most special chars, keep alphanumeric, spaces, commas, hyphens, periods, apostrophes
        text = re.sub(r"[^\w\s,\-\.\']", "", text)
        
        # Limit length
        text = text[:max_length]
        
        return text
    
    @staticmethod
    def normalize_location(location: str) -> str:
        """
        Normalize location string to title case.
        
        Args:
            location: Location name
            
        Returns:
            Normalized location string
        """
        location = InputValidator.sanitize_string(location, InputValidator.MAX_LOCATION_LENGTH)
        # Convert to title case
        location = location.strip().title()
        return location
    
    @staticmethod
    def normalize_cuisine(cuisine: str) -> str:
        """
        Normalize cuisine string.
        
        Args:
            cuisine: Cuisine name
            
        Returns:
            Normalized cuisine string
        """
        cuisine = InputValidator.sanitize_string(cuisine, InputValidator.MAX_CUISINE_LENGTH)
        cuisine = cuisine.strip().title()
        return cuisine
    
    @staticmethod
    def normalize_budget(budget: str) -> str:
        """
        Normalize budget string to lowercase and validate.
        
        Args:
            budget: Budget tier
            
        Returns:
            Normalized budget string
            
        Raises:
            ValidationError: If budget is invalid
        """
        budget = budget.strip().lower()
        if budget not in InputValidator.VALID_BUDGETS:
            raise ValidationError(
                f"Invalid budget tier: '{budget}'. Must be one of: {', '.join(InputValidator.VALID_BUDGETS)}"
            )
        return budget
    
    @staticmethod
    def validate_rating(rating: float) -> float:
        """
        Validate and clamp rating to valid range (0-5).
        
        Args:
            rating: Rating value
            
        Returns:
            Validated rating (clamped to 0-5)
        """
        try:
            rating = float(rating)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid rating: must be a number between 0 and 5")
        
        if rating < 0:
            logger.warning(f"Rating {rating} < 0, clamping to 0")
            return 0.0
        elif rating > 5:
            logger.warning(f"Rating {rating} > 5, clamping to 5")
            return 5.0
        
        return rating
    
    @staticmethod
    def sanitize_additional_prefs(prefs: List[str]) -> List[str]:
        """
        Sanitize list of additional preferences.
        
        Args:
            prefs: List of preference strings
            
        Returns:
            Sanitized list of preferences
        """
        if not prefs:
            return []
        
        # Limit number of preferences
        prefs = prefs[:InputValidator.MAX_ADDITIONAL_PREFS_COUNT]
        
        # Sanitize each preference
        sanitized = []
        for pref in prefs:
            if pref:
                clean_pref = InputValidator.sanitize_string(
                    pref, 
                    InputValidator.MAX_ADDITIONAL_PREF_LENGTH
                )
                if clean_pref:  # Only add non-empty strings
                    sanitized.append(clean_pref)
        
        return sanitized
    
    @classmethod
    def validate(cls, 
                 location: str,
                 budget: str,
                 cuisine: str,
                 min_rating: float,
                 additional_prefs: Optional[List[str]] = None) -> UserPreferences:
        """
        Validate and create a UserPreferences object.
        
        Args:
            location: Location name
            budget: Budget tier
            cuisine: Cuisine type
            min_rating: Minimum rating
            additional_prefs: Optional additional preferences
            
        Returns:
            Validated UserPreferences object
            
        Raises:
            ValidationError: If validation fails
        """
        errors = []
        
        # Validate location
        if not location or not location.strip():
            errors.append("Location is required")
        else:
            location = cls.normalize_location(location)
        
        # Validate cuisine
        if not cuisine or not cuisine.strip():
            errors.append("Cuisine is required")
        else:
            cuisine = cls.normalize_cuisine(cuisine)
        
        # Validate budget
        try:
            budget = cls.normalize_budget(budget)
        except ValidationError as e:
            errors.append(str(e))
        
        # Validate rating
        try:
            min_rating = cls.validate_rating(min_rating)
        except ValidationError as e:
            errors.append(str(e))
        
        # Sanitize additional preferences
        if additional_prefs is None:
            additional_prefs = []
        additional_prefs = cls.sanitize_additional_prefs(additional_prefs)
        
        # Raise all errors together
        if errors:
            raise ValidationError("; ".join(errors))
        
        return UserPreferences(
            location=location,
            budget=budget,
            cuisine=cuisine,
            min_rating=min_rating,
            additional_prefs=additional_prefs
        )


def format_cost(cost: float) -> str:
    """
    Format cost as a currency string.
    
    Args:
        cost: Cost value
        
    Returns:
        Formatted cost string (e.g., "₹1200 for two")
    """
    return f"₹{cost:.0f} for two"

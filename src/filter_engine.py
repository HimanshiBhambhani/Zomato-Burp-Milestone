"""
Filter Engine Module

Implements the DataFilterEngine class that filters restaurants based on user
preferences, including fuzzy matching and progressive filter relaxation.
"""

import logging
from typing import Tuple, Optional, Set
import pandas as pd
from fuzzywuzzy import fuzz, process
import yaml

from .models import UserPreferences

logger = logging.getLogger(__name__)


class FilterEngineError(Exception):
    """Base exception for filter engine errors"""
    pass


class NoResultsError(FilterEngineError):
    """Raised when no restaurants match the criteria"""
    pass


class DataFilterEngine:
    """
    Filters restaurant data based on user preferences.
    
    Features:
    - Location and cuisine fuzzy matching
    - Budget tier filtering
    - Rating threshold filtering
    - Progressive filter relaxation when no results found
    - Configurable candidate limit
    """
    
    def __init__(self, df: pd.DataFrame, config_path: str = "config.yaml"):
        """
        Initialize the filter engine.
        
        Args:
            df: DataFrame with preprocessed restaurant data
            config_path: Path to configuration file
        """
        self.df = df.copy()
        self.config = self._load_config(config_path)
        
        # Cache unique locations and cuisines for fuzzy matching
        self._unique_locations = set(self.df['location'].unique())
        self._unique_cuisines = self._extract_unique_cuisines()
        
        logger.info(f"Filter engine initialized with {len(self.df)} restaurants")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return {
                'filtering': {
                    'max_candidates': 20,
                    'fuzzy_match_threshold': 80
                },
                'budget_thresholds': {
                    'low': 500,
                    'medium': 1500
                }
            }
    
    def _extract_unique_cuisines(self) -> Set[str]:
        """Extract all unique cuisines from the dataset."""
        cuisines = set()
        if 'cuisines' in self.df.columns:
            for cuisines_str in self.df['cuisines'].dropna():
                for cuisine in str(cuisines_str).split(','):
                    cuisines.add(cuisine.strip())
        return cuisines
    
    def fuzzy_match_location(self, user_location: str) -> Tuple[str, int]:
        """
        Find the best matching location using fuzzy matching.
        
        Args:
            user_location: User's input location
            
        Returns:
            Tuple of (matched_location, match_score)
        """
        if not user_location:
            return ("", 0)
        
        # Try exact match first
        if user_location in self._unique_locations:
            return (user_location, 100)
        
        # Fuzzy match
        matches = process.extractOne(
            user_location,
            self._unique_locations,
            scorer=fuzz.token_sort_ratio
        )
        
        if matches:
            matched_location, score = matches[0], matches[1]
            logger.info(f"Fuzzy matched location '{user_location}' -> '{matched_location}' (score: {score})")
            return (matched_location, score)
        
        return ("", 0)
    
    def fuzzy_match_cuisine(self, user_cuisine: str) -> Tuple[str, int]:
        """
        Find the best matching cuisine using fuzzy matching.
        
        Args:
            user_cuisine: User's input cuisine
            
        Returns:
            Tuple of (matched_cuisine, match_score)
        """
        if not user_cuisine:
            return ("", 0)
        
        # Try exact match first
        if user_cuisine in self._unique_cuisines:
            return (user_cuisine, 100)
        
        # Fuzzy match
        matches = process.extractOne(
            user_cuisine,
            self._unique_cuisines,
            scorer=fuzz.token_sort_ratio
        )
        
        if matches:
            matched_cuisine, score = matches[0], matches[1]
            logger.info(f"Fuzzy matched cuisine '{user_cuisine}' -> '{matched_cuisine}' (score: {score})")
            return (matched_cuisine, score)
        
        return ("", 0)
    
    def _apply_location_filter(self, df: pd.DataFrame, location: str, use_fuzzy: bool = True) -> pd.DataFrame:
        """Apply location filter with optional fuzzy matching."""
        if not location:
            return df
        
        if use_fuzzy:
            matched_location, score = self.fuzzy_match_location(location)
            threshold = self.config['filtering']['fuzzy_match_threshold']
            
            if score >= threshold:
                return df[df['location'] == matched_location]
            else:
                logger.warning(f"No location match for '{location}' (best score: {score})")
                return pd.DataFrame()  # Empty DataFrame
        else:
            return df[df['location'] == location]
    
    def _apply_cuisine_filter(self, df: pd.DataFrame, cuisine: str, use_fuzzy: bool = True) -> pd.DataFrame:
        """Apply cuisine filter with optional fuzzy matching."""
        if not cuisine or 'cuisines' not in df.columns:
            return df
        
        if use_fuzzy:
            matched_cuisine, score = self.fuzzy_match_cuisine(cuisine)
            threshold = self.config['filtering']['fuzzy_match_threshold']
            
            if score >= threshold:
                # Check if matched cuisine appears in the cuisines column
                return df[df['cuisines'].str.contains(matched_cuisine, case=False, na=False)]
            else:
                logger.warning(f"No cuisine match for '{cuisine}' (best score: {score})")
                return df  # Return unfiltered if no match
        else:
            return df[df['cuisines'].str.contains(cuisine, case=False, na=False)]
    
    def _apply_budget_filter(self, df: pd.DataFrame, budget: str) -> pd.DataFrame:
        """Apply budget tier filter."""
        if not budget or 'budget' not in df.columns:
            return df
        
        return df[df['budget'] == budget.lower()]
    
    def _apply_rating_filter(self, df: pd.DataFrame, min_rating: float) -> pd.DataFrame:
        """Apply minimum rating filter."""
        if min_rating is None or min_rating <= 0:
            return df
        
        return df[df['aggregate_rating'] >= min_rating]
    
    def _limit_candidates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limit number of candidates and sort by rating."""
        max_candidates = self.config['filtering']['max_candidates']
        
        # Sort by rating (descending) and votes (descending) if available
        sort_cols = ['aggregate_rating']
        if 'votes' in df.columns:
            sort_cols.append('votes')
        
        df = df.sort_values(sort_cols, ascending=False)
        
        return df.head(max_candidates)
    
    def filter(self, preferences: UserPreferences, 
               skip_filters: Optional[Set[str]] = None) -> Tuple[pd.DataFrame, Optional[str]]:
        """
        Filter restaurants based on user preferences.
        
        Args:
            preferences: User preferences
            skip_filters: Set of filters to skip (for relaxation)
                         Options: 'location', 'cuisine', 'budget', 'rating'
        
        Returns:
            Tuple of (filtered_df, relaxation_message)
            relaxation_message is None if no relaxation applied
        """
        if skip_filters is None:
            skip_filters = set()
        
        df = self.df.copy()
        relaxation_message = None
        
        # Apply filters in order
        # 1. Location filter (usually the most restrictive)
        if 'location' not in skip_filters:
            df = self._apply_location_filter(df, preferences.location)
            if df.empty:
                logger.warning(f"No restaurants found in location: {preferences.location}")
                return df, "location not found"
        
        # 2. Cuisine filter
        if 'cuisine' not in skip_filters:
            df = self._apply_cuisine_filter(df, preferences.cuisine)
        
        # 3. Budget filter
        if 'budget' not in skip_filters:
            df = self._apply_budget_filter(df, preferences.budget)
        
        # 4. Rating filter
        if 'rating' not in skip_filters:
            df = self._apply_rating_filter(df, preferences.min_rating)
        
        # 5. Limit to max candidates
        df = self._limit_candidates(df)
        
        # Log relaxations
        if skip_filters:
            relaxation_message = f"Relaxed filters: {', '.join(sorted(skip_filters))}"
            logger.info(relaxation_message)
        
        logger.info(f"Filter result: {len(df)} restaurants")
        return df, relaxation_message
    
    def filter_with_progressive_relaxation(self, preferences: UserPreferences) -> Tuple[pd.DataFrame, Optional[str]]:
        """
        Filter with progressive relaxation strategy.
        
        Relaxation order:
        1. Try all filters
        2. Drop cuisine filter
        3. Drop cuisine + budget filters
        4. Drop cuisine + budget + lower rating to 3.0
        5. Location only (all restaurants in the location)
        
        Args:
            preferences: User preferences
            
        Returns:
            Tuple of (filtered_df, relaxation_message)
        """
        # Step 1: Try with all filters
        df, _ = self.filter(preferences)
        if not df.empty:
            return df, None
        
        logger.info("No results with all filters. Starting progressive relaxation...")
        
        # Step 2: Drop cuisine filter
        df, msg = self.filter(preferences, skip_filters={'cuisine'})
        if not df.empty:
            return df, "No exact cuisine match found. Showing restaurants in your location and budget."
        
        # Step 3: Drop cuisine + budget filters
        df, msg = self.filter(preferences, skip_filters={'cuisine', 'budget'})
        if not df.empty:
            return df, "Limited options. Showing restaurants in your location across all cuisines and budgets."
        
        # Step 4: Drop cuisine + budget + relax rating
        relaxed_prefs = UserPreferences(
            location=preferences.location,
            budget=preferences.budget,
            cuisine=preferences.cuisine,
            min_rating=3.0,  # Relax to 3.0
            additional_prefs=preferences.additional_prefs
        )
        df, msg = self.filter(relaxed_prefs, skip_filters={'cuisine', 'budget'})
        if not df.empty:
            return df, "Showing restaurants with rating ≥ 3.0 in your location."
        
        # Step 5: Location only (no other filters)
        df, msg = self.filter(preferences, skip_filters={'cuisine', 'budget', 'rating'})
        if not df.empty:
            return df, f"Showing all restaurants in {preferences.location}."
        
        # If still empty, there are no restaurants in this location
        logger.error(f"No restaurants found even with full relaxation for location: {preferences.location}")
        return df, f"No restaurants found in {preferences.location}. Please try a different location."
    
    def get_available_locations(self, limit: int = 20) -> list:
        """
        Get list of available locations.
        
        Args:
            limit: Maximum number of locations to return
            
        Returns:
            List of location names
        """
        location_counts = self.df['location'].value_counts()
        return location_counts.head(limit).index.tolist()
    
    def get_available_cuisines(self, limit: int = 30) -> list:
        """
        Get list of available cuisines.
        
        Args:
            limit: Maximum number of cuisines to return
            
        Returns:
            List of cuisine names
        """
        from collections import Counter
        cuisine_counts = Counter()
        
        if 'cuisines' in self.df.columns:
            for cuisines_str in self.df['cuisines'].dropna():
                for cuisine in str(cuisines_str).split(','):
                    cuisine_counts[cuisine.strip()] += 1
        
        return [cuisine for cuisine, _ in cuisine_counts.most_common(limit)]
    
    def get_stats(self) -> dict:
        """Get statistics about the dataset."""
        return {
            'total_restaurants': len(self.df),
            'unique_locations': len(self._unique_locations),
            'unique_cuisines': len(self._unique_cuisines),
            'rating_range': (self.df['aggregate_rating'].min(), self.df['aggregate_rating'].max()),
            'cost_range': (self.df['average_cost_for_two'].min(), self.df['average_cost_for_two'].max()),
        }

"""
Prompt Builder Module

Constructs prompts for the LLM by loading templates and injecting
restaurant data and user preferences.
"""

import os
import logging
from typing import Optional
import pandas as pd
from .models import UserPreferences

logger = logging.getLogger(__name__)


class PromptBuilderError(Exception):
    """Base exception for prompt builder errors"""
    pass


class TemplateNotFoundError(PromptBuilderError):
    """Raised when a template file is not found"""
    pass


class PromptBuilder:
    """
    Builds prompts for the LLM from templates and data.
    
    Loads prompt templates from files and injects user preferences
    and restaurant data to create complete prompts.
    """
    
    def __init__(self, templates_dir: str = "prompts"):
        """
        Initialize the prompt builder.
        
        Args:
            templates_dir: Directory containing prompt template files
        """
        self.templates_dir = templates_dir
        self._templates = {}
        
        # Load templates
        self._load_template('system', 'system_prompt.txt')
        self._load_template('recommendation', 'recommendation.txt')
        self._load_template('summary', 'summary.txt')
        
        logger.info(f"PromptBuilder initialized with {len(self._templates)} templates")
    
    def _load_template(self, name: str, filename: str) -> None:
        """
        Load a template file.
        
        Args:
            name: Template name (key)
            filename: Template filename
            
        Raises:
            TemplateNotFoundError: If template file doesn't exist
        """
        filepath = os.path.join(self.templates_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self._templates[name] = f.read()
            logger.debug(f"Loaded template '{name}' from {filepath}")
        except FileNotFoundError:
            raise TemplateNotFoundError(
                f"Template file not found: {filepath}. "
                f"Make sure the {self.templates_dir} directory exists with all template files."
            )
        except Exception as e:
            raise PromptBuilderError(f"Error loading template {filename}: {e}")
    
    def get_template(self, name: str) -> str:
        """
        Get a loaded template by name.
        
        Args:
            name: Template name
            
        Returns:
            Template content
            
        Raises:
            PromptBuilderError: If template not found
        """
        if name not in self._templates:
            raise PromptBuilderError(f"Template '{name}' not loaded")
        return self._templates[name]
    
    def _format_restaurant_table(self, df: pd.DataFrame) -> str:
        """
        Format restaurant data as a readable table for the prompt.
        
        Args:
            df: DataFrame with restaurant data
            
        Returns:
            Formatted table string
        """
        if df.empty:
            return "No restaurants available."
        
        lines = []
        
        for idx, row in df.iterrows():
            lines.append(f"\n{idx + 1}. {row['name']}")
            lines.append(f"   Location: {row['location']}")
            
            if 'cuisines' in row and pd.notna(row['cuisines']):
                lines.append(f"   Cuisine: {row['cuisines']}")
            
            if 'aggregate_rating' in row and pd.notna(row['aggregate_rating']):
                lines.append(f"   Rating: {row['aggregate_rating']:.1f}/5")
            
            if 'average_cost_for_two' in row and pd.notna(row['average_cost_for_two']):
                lines.append(f"   Cost for Two: ₹{int(row['average_cost_for_two'])}")
            
            if 'votes' in row and pd.notna(row['votes']):
                lines.append(f"   Votes: {int(row['votes'])}")
            
            if 'budget' in row and pd.notna(row['budget']):
                lines.append(f"   Budget Tier: {row['budget'].title()}")
        
        return "\n".join(lines)
    
    def _format_additional_prefs(self, prefs: list) -> str:
        """
        Format additional preferences for the prompt.
        
        Args:
            prefs: List of additional preference strings
            
        Returns:
            Formatted string
        """
        if not prefs:
            return ""
        
        prefs_str = ", ".join(prefs)
        return f"- Additional Preferences: {prefs_str}"
    
    def build(self, 
              preferences: UserPreferences, 
              restaurants_df: pd.DataFrame,
              top_n: int = 5,
              include_system_prompt: bool = True) -> str:
        """
        Build a complete prompt for restaurant recommendations.
        
        Args:
            preferences: User preferences
            restaurants_df: DataFrame with filtered restaurant data
            top_n: Number of recommendations to request
            include_system_prompt: Whether to include system prompt
            
        Returns:
            Complete prompt string
        """
        if restaurants_df.empty:
            logger.warning("Building prompt with empty restaurant data")
        
        # Format restaurant data
        restaurant_table = self._format_restaurant_table(restaurants_df)
        
        # Format additional preferences
        additional_prefs_section = self._format_additional_prefs(
            preferences.additional_prefs
        )
        
        # Build the recommendation prompt
        recommendation_prompt = self._templates['recommendation'].format(
            location=preferences.location,
            budget=preferences.budget.title(),
            cuisine=preferences.cuisine,
            min_rating=preferences.min_rating,
            additional_prefs_section=additional_prefs_section,
            restaurant_data_table=restaurant_table,
            top_n=min(top_n, len(restaurants_df)) if not restaurants_df.empty else top_n
        )
        
        # Combine system prompt and recommendation prompt
        if include_system_prompt:
            system_prompt = self._templates['system']
            full_prompt = f"{system_prompt}\n\n---\n\n{recommendation_prompt}"
        else:
            full_prompt = recommendation_prompt
        
        logger.info(f"Built prompt for {len(restaurants_df)} restaurants, requesting top {top_n}")
        logger.debug(f"Prompt length: {len(full_prompt)} characters")
        
        return full_prompt
    
    def build_summary_prompt(self, recommendations_text: str) -> str:
        """
        Build a prompt for generating a summary of recommendations.
        
        Args:
            recommendations_text: Text of the recommendations
            
        Returns:
            Summary prompt string
        """
        summary_template = self._templates['summary']
        return f"{recommendations_text}\n\n---\n\n{summary_template}"
    
    def estimate_token_count(self, text: str) -> int:
        """
        Estimate token count for a text string.
        
        This is a rough estimate (words * 1.3). For accurate counts,
        use tiktoken library.
        
        Args:
            text: Text to estimate
            
        Returns:
            Estimated token count
        """
        # Rough estimation: average ~1.3 tokens per word
        word_count = len(text.split())
        estimated_tokens = int(word_count * 1.3)
        return estimated_tokens
    
    def trim_restaurants_to_token_budget(self, 
                                         df: pd.DataFrame,
                                         preferences: UserPreferences,
                                         max_tokens: int = 3000,
                                         top_n: int = 5) -> pd.DataFrame:
        """
        Trim restaurant list to fit within token budget.
        
        Args:
            df: DataFrame with restaurant data
            preferences: User preferences
            max_tokens: Maximum token budget for the prompt
            top_n: Desired number of recommendations
            
        Returns:
            Trimmed DataFrame that fits within budget
        """
        if df.empty:
            return df
        
        # Start with desired number
        current_df = df.head(top_n)
        
        # Build prompt and check token count
        prompt = self.build(preferences, current_df, top_n, include_system_prompt=True)
        estimated_tokens = self.estimate_token_count(prompt)
        
        # If within budget, try to add more restaurants
        if estimated_tokens < max_tokens * 0.8:  # Use 80% of budget for safety
            max_rows = min(len(df), top_n * 2)
            for n in range(len(current_df) + 1, max_rows + 1):
                test_df = df.head(n)
                test_prompt = self.build(preferences, test_df, top_n, include_system_prompt=True)
                test_tokens = self.estimate_token_count(test_prompt)
                
                if test_tokens > max_tokens * 0.8:
                    break
                
                current_df = test_df
        
        # If over budget, reduce restaurants
        elif estimated_tokens > max_tokens:
            logger.warning(f"Prompt exceeds token budget ({estimated_tokens} > {max_tokens}). Reducing restaurants.")
            
            for n in range(len(current_df) - 1, 0, -1):
                test_df = df.head(n)
                test_prompt = self.build(preferences, test_df, top_n, include_system_prompt=True)
                test_tokens = self.estimate_token_count(test_prompt)
                
                if test_tokens <= max_tokens:
                    current_df = test_df
                    break
        
        if len(current_df) != len(df):
            logger.info(f"Trimmed restaurants from {len(df)} to {len(current_df)} to fit token budget")
        
        return current_df

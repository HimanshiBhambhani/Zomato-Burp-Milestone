"""
Unit tests for PromptBuilder module
"""

import pytest
import pandas as pd
from pathlib import Path
from src.prompt_builder import PromptBuilder, PromptBuilderError
from src.models import UserPreferences


class TestPromptBuilder:
    """Test suite for PromptBuilder"""
    
    def test_initialization(self):
        """Test PromptBuilder initializes correctly"""
        builder = PromptBuilder()
        assert builder is not None
    
    def test_template_loading(self):
        """Test that templates are loaded correctly"""
        builder = PromptBuilder()
        
        # Should have loaded templates
        assert hasattr(builder, '_templates')
        assert 'system' in builder._templates
        assert 'recommendation' in builder._templates
        assert 'summary' in builder._templates
        
        # Templates should not be empty
        assert builder._templates['system'].strip() != ""
        assert builder._templates['recommendation'].strip() != ""
    
    def test_missing_template_file(self):
        """Test handling of missing template file"""
        builder = PromptBuilder()
        
        # Try to load non-existent template
        with pytest.raises(PromptBuilderError):
            builder._load_template('nonexistent.txt')
    
    def test_build_prompt_basic(self, sample_restaurants):
        """Test building a basic prompt"""
        builder = PromptBuilder()
        preferences = UserPreferences(
            location="Delhi",
            budget="medium",
            cuisine="North Indian",
            min_rating=4.0
        )
        
        system_prompt, user_prompt = builder.build(preferences, sample_restaurants)
        
        # Check system prompt
        assert system_prompt is not None
        assert len(system_prompt) > 0
        assert "restaurant" in system_prompt.lower()
        
        # Check user prompt
        assert user_prompt is not None
        assert "Delhi" in user_prompt
        assert "North Indian" in user_prompt
        assert "4.0" in user_prompt
    
    def test_build_prompt_with_empty_dataframe(self):
        """Test building prompt with empty restaurant DataFrame"""
        builder = PromptBuilder()
        preferences = UserPreferences(
            location="Mumbai",
            budget="low",
            cuisine="Italian"
        )
        
        empty_df = pd.DataFrame(columns=['name', 'location', 'cuisine', 'rating', 'cost_for_two', 'votes'])
        
        system_prompt, user_prompt = builder.build(preferences, empty_df)
        
        # Should still return prompts
        assert system_prompt is not None
        assert user_prompt is not None
        assert "no restaurants" in user_prompt.lower() or "not available" in user_prompt.lower()
    
    def test_build_prompt_with_optional_fields(self, sample_restaurants):
        """Test building prompt with optional preference fields"""
        builder = PromptBuilder()
        
        # Preferences without min_rating and with None cuisine
        preferences = UserPreferences(
            location="Bangalore",
            budget="high",
            cuisine=None
        )
        
        system_prompt, user_prompt = builder.build(preferences, sample_restaurants)
        
        assert system_prompt is not None
        assert user_prompt is not None
        assert "Bangalore" in user_prompt
    
    def test_format_restaurant_table(self, sample_restaurants):
        """Test restaurant table formatting"""
        builder = PromptBuilder()
        
        table = builder._format_restaurant_table(sample_restaurants)
        
        # Check table structure
        assert isinstance(table, str)
        assert len(table) > 0
        
        # Should contain numbered list
        assert "1." in table
        
        # Should contain restaurant details
        assert "Location:" in table
        assert "Cuisine:" in table
        assert "Rating:" in table
        assert "Cost:" in table
        assert "Votes:" in table
    
    def test_format_restaurant_table_with_limit(self, sample_restaurants):
        """Test restaurant table formatting with top_n limit"""
        builder = PromptBuilder()
        
        table = builder._format_restaurant_table(sample_restaurants, top_n=2)
        
        # Should only have 2 restaurants
        assert "1." in table
        assert "2." in table
        assert "3." not in table
    
    def test_estimate_token_count(self):
        """Test token count estimation"""
        builder = PromptBuilder()
        
        # Simple text
        text = "This is a test sentence."
        tokens = builder.estimate_token_count(text)
        
        # Should be roughly proportional to word count
        # Using ~1.3 tokens per word
        words = len(text.split())
        assert tokens > 0
        assert tokens >= words  # Should be at least word count
        assert tokens <= words * 2  # Should not be more than 2x word count
    
    def test_estimate_token_count_empty(self):
        """Test token count for empty string"""
        builder = PromptBuilder()
        
        tokens = builder.estimate_token_count("")
        assert tokens == 0
    
    def test_trim_restaurants_to_token_budget(self, sample_restaurants):
        """Test trimming restaurants to fit token budget"""
        builder = PromptBuilder()
        
        # Set a small budget that should trim the list
        trimmed_df = builder.trim_restaurants_to_token_budget(sample_restaurants, max_tokens=100)
        
        # Should return a DataFrame
        assert isinstance(trimmed_df, pd.DataFrame)
        
        # Should have fewer restaurants than original
        assert len(trimmed_df) <= len(sample_restaurants)
    
    def test_trim_restaurants_large_budget(self, sample_restaurants):
        """Test trimming with budget larger than content"""
        builder = PromptBuilder()
        
        # Large budget should not trim
        trimmed_df = builder.trim_restaurants_to_token_budget(sample_restaurants, max_tokens=10000)
        
        # Should return all restaurants
        assert len(trimmed_df) == len(sample_restaurants)
    
    def test_trim_restaurants_small_budget(self, sample_restaurants):
        """Test trimming with very small budget"""
        builder = PromptBuilder()
        
        # Very small budget should return at least 1 restaurant
        trimmed_df = builder.trim_restaurants_to_token_budget(sample_restaurants, max_tokens=10)
        
        # Should have at least 1 restaurant
        assert len(trimmed_df) >= 1
    
    def test_build_summary_prompt(self):
        """Test building summary prompt"""
        builder = PromptBuilder()
        
        original_response = "Here are my recommendations: Restaurant A is great for North Indian food..."
        
        system_prompt, user_prompt = builder.build_summary_prompt(original_response)
        
        # Check prompts are returned
        assert system_prompt is not None
        assert user_prompt is not None
        
        # User prompt should contain the original response
        assert original_response in user_prompt
    
    def test_build_summary_prompt_empty(self):
        """Test building summary prompt with empty response"""
        builder = PromptBuilder()
        
        system_prompt, user_prompt = builder.build_summary_prompt("")
        
        # Should still return prompts
        assert system_prompt is not None
        assert user_prompt is not None
    
    def test_build_with_special_characters(self, sample_restaurants):
        """Test building prompt with special characters in preferences"""
        builder = PromptBuilder()
        
        preferences = UserPreferences(
            location="Delhi & NCR",
            budget="medium",
            cuisine="North Indian, Chinese & Continental"
        )
        
        system_prompt, user_prompt = builder.build(preferences, sample_restaurants)
        
        # Should handle special characters
        assert system_prompt is not None
        assert user_prompt is not None
        assert "&" in user_prompt or "and" in user_prompt.lower()
    
    def test_build_with_long_restaurant_list(self):
        """Test building prompt with many restaurants"""
        builder = PromptBuilder()
        
        # Create a large DataFrame
        data = []
        for i in range(100):
            data.append({
                'name': f'Restaurant {i}',
                'location': 'Delhi',
                'cuisine': 'Indian',
                'rating': 4.0,
                'cost_for_two': 500,
                'votes': 100
            })
        
        large_df = pd.DataFrame(data)
        
        preferences = UserPreferences(
            location="Delhi",
            budget="medium",
            cuisine="Indian"
        )
        
        system_prompt, user_prompt = builder.build(preferences, large_df)
        
        # Should still build successfully
        assert system_prompt is not None
        assert user_prompt is not None
    
    def test_template_placeholder_replacement(self, sample_restaurants):
        """Test that template placeholders are properly replaced"""
        builder = PromptBuilder()
        
        preferences = UserPreferences(
            location="Mumbai",
            budget="high",
            cuisine="Italian",
            min_rating=4.5
        )
        
        system_prompt, user_prompt = builder.build(preferences, sample_restaurants, top_n=3)
        
        # Check all placeholders are replaced
        assert "{location}" not in user_prompt
        assert "{budget}" not in user_prompt
        assert "{cuisine}" not in user_prompt
        assert "{min_rating}" not in user_prompt
        assert "{restaurant_data_table}" not in user_prompt
        assert "{top_n}" not in user_prompt
        
        # Check actual values are present
        assert "Mumbai" in user_prompt
        assert "Italian" in user_prompt
        assert "4.5" in user_prompt
        assert "3" in user_prompt
    
    def test_build_with_none_preferences(self, sample_restaurants):
        """Test building with None values in preferences"""
        builder = PromptBuilder()
        
        preferences = UserPreferences(
            location="Delhi",
            budget="medium",
            cuisine=None,
            min_rating=None
        )
        
        system_prompt, user_prompt = builder.build(preferences, sample_restaurants)
        
        # Should handle None values gracefully
        assert system_prompt is not None
        assert user_prompt is not None
        assert "Delhi" in user_prompt
        assert "None" not in user_prompt  # Should not have literal "None"


@pytest.fixture
def sample_restaurants():
    """Sample restaurant data for testing"""
    return pd.DataFrame({
        'name': ['Restaurant A', 'Restaurant B', 'Restaurant C'],
        'location': ['Delhi', 'Delhi', 'Mumbai'],
        'cuisine': ['North Indian', 'Chinese', 'Italian'],
        'rating': [4.5, 4.0, 4.2],
        'cost_for_two': [800, 600, 1200],
        'votes': [500, 300, 450]
    })

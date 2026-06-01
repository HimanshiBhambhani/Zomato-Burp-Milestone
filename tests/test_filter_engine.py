"""
Unit tests for the DataFilterEngine and related models.
"""

import pytest
import pandas as pd
from src.models import UserPreferences, Recommendation, InputValidator, ValidationError, format_cost
from src.filter_engine import DataFilterEngine, FilterEngineError, NoResultsError


class TestUserPreferences:
    """Test the UserPreferences dataclass."""
    
    def test_user_preferences_creation(self):
        """Test creating a UserPreferences object."""
        prefs = UserPreferences(
            location='Delhi',
            budget='medium',
            cuisine='Italian',
            min_rating=4.0,
            additional_prefs=['family-friendly']
        )
        
        assert prefs.location == 'Delhi'
        assert prefs.budget == 'medium'
        assert prefs.cuisine == 'Italian'
        assert prefs.min_rating == 4.0
        assert prefs.additional_prefs == ['family-friendly']
    
    def test_user_preferences_budget_normalization(self):
        """Test that budget is normalized to lowercase."""
        prefs = UserPreferences(
            location='Delhi',
            budget='MEDIUM',
            cuisine='Italian',
            min_rating=4.0,
            additional_prefs=[]
        )
        
        assert prefs.budget == 'medium'
    
    def test_user_preferences_rating_clamping(self):
        """Test that rating is clamped to valid range."""
        # Test negative rating
        prefs1 = UserPreferences(
            location='Delhi',
            budget='low',
            cuisine='Italian',
            min_rating=-1.0,
            additional_prefs=[]
        )
        assert prefs1.min_rating == 0.0
        
        # Test rating > 5
        prefs2 = UserPreferences(
            location='Delhi',
            budget='low',
            cuisine='Italian',
            min_rating=6.0,
            additional_prefs=[]
        )
        assert prefs2.min_rating == 5.0
    
    def test_user_preferences_default_additional_prefs(self):
        """Test that additional_prefs defaults to empty list."""
        prefs = UserPreferences(
            location='Delhi',
            budget='low',
            cuisine='Italian',
            min_rating=4.0
        )
        
        assert prefs.additional_prefs == []


class TestRecommendation:
    """Test the Recommendation dataclass."""
    
    def test_recommendation_creation(self):
        """Test creating a Recommendation object."""
        rec = Recommendation(
            rank=1,
            restaurant_name='Olive Bar & Kitchen',
            cuisine='Italian, Mediterranean',
            rating=4.5,
            estimated_cost='₹1200 for two',
            explanation='Great Italian food',
            location='Delhi',
            votes=2500
        )
        
        assert rec.rank == 1
        assert rec.restaurant_name == 'Olive Bar & Kitchen'
        assert rec.cuisine == 'Italian, Mediterranean'
        assert rec.rating == 4.5
        assert rec.estimated_cost == '₹1200 for two'
        assert rec.explanation == 'Great Italian food'
        assert rec.location == 'Delhi'
        assert rec.votes == 2500
    
    def test_recommendation_to_dict(self):
        """Test converting recommendation to dictionary."""
        rec = Recommendation(
            rank=1,
            restaurant_name='Test Restaurant',
            cuisine='Italian',
            rating=4.0,
            estimated_cost='₹800 for two',
            explanation='Good food'
        )
        
        result = rec.to_dict()
        
        assert isinstance(result, dict)
        assert result['rank'] == 1
        assert result['restaurant_name'] == 'Test Restaurant'
        assert result['cuisine'] == 'Italian'
        assert result['rating'] == 4.0
        assert result['estimated_cost'] == '₹800 for two'
        assert result['explanation'] == 'Good food'
        assert result['location'] is None
        assert result['votes'] is None


class TestInputValidator:
    """Test the InputValidator class."""
    
    def test_sanitize_string_removes_special_chars(self):
        """Test that special characters are removed."""
        text = "Hello; DROP TABLE restaurants; --"
        result = InputValidator.sanitize_string(text)
        assert "DROP" not in result
        assert ";" not in result
        assert "--" not in result
    
    def test_sanitize_string_limits_length(self):
        """Test that strings are truncated to max length."""
        text = "a" * 300
        result = InputValidator.sanitize_string(text, max_length=100)
        assert len(result) == 100
    
    def test_sanitize_string_preserves_safe_chars(self):
        """Test that safe characters are preserved."""
        text = "North Indian, Italian-American"
        result = InputValidator.sanitize_string(text)
        assert "North Indian" in result
        assert "Italian-American" in result or "ItalianAmerican" in result
    
    def test_normalize_location(self):
        """Test location normalization."""
        assert InputValidator.normalize_location("delhi") == "Delhi"
        assert InputValidator.normalize_location("  MUMBAI  ") == "Mumbai"
        assert InputValidator.normalize_location("new delhi") == "New Delhi"
    
    def test_normalize_cuisine(self):
        """Test cuisine normalization."""
        assert InputValidator.normalize_cuisine("italian") == "Italian"
        assert InputValidator.normalize_cuisine("  CHINESE  ") == "Chinese"
        assert InputValidator.normalize_cuisine("north indian") == "North Indian"
    
    def test_normalize_budget_valid(self):
        """Test budget normalization with valid values."""
        assert InputValidator.normalize_budget("LOW") == "low"
        assert InputValidator.normalize_budget("Medium") == "medium"
        assert InputValidator.normalize_budget("high") == "high"
    
    def test_normalize_budget_invalid(self):
        """Test budget normalization with invalid values."""
        with pytest.raises(ValidationError):
            InputValidator.normalize_budget("cheap")
        
        with pytest.raises(ValidationError):
            InputValidator.normalize_budget("expensive")
    
    def test_validate_rating_valid(self):
        """Test rating validation with valid values."""
        assert InputValidator.validate_rating(3.5) == 3.5
        assert InputValidator.validate_rating("4.0") == 4.0
        assert InputValidator.validate_rating(0) == 0.0
        assert InputValidator.validate_rating(5) == 5.0
    
    def test_validate_rating_clamping(self):
        """Test rating validation with out-of-range values."""
        assert InputValidator.validate_rating(-1) == 0.0
        assert InputValidator.validate_rating(6) == 5.0
    
    def test_validate_rating_invalid_type(self):
        """Test rating validation with invalid types."""
        with pytest.raises(ValidationError):
            InputValidator.validate_rating("not a number")
    
    def test_sanitize_additional_prefs(self):
        """Test sanitization of additional preferences."""
        prefs = ["family-friendly", "quick service", "outdoor seating"]
        result = InputValidator.sanitize_additional_prefs(prefs)
        assert len(result) == 3
        assert "family-friendly" in result or "familyfriendly" in result
    
    def test_sanitize_additional_prefs_limit(self):
        """Test that additional preferences are limited in count."""
        prefs = [f"pref{i}" for i in range(20)]
        result = InputValidator.sanitize_additional_prefs(prefs)
        assert len(result) <= InputValidator.MAX_ADDITIONAL_PREFS_COUNT
    
    def test_validate_complete_valid(self):
        """Test full validation with valid inputs."""
        prefs = InputValidator.validate(
            location="delhi",
            budget="medium",
            cuisine="italian",
            min_rating=4.0,
            additional_prefs=["family-friendly"]
        )
        
        assert prefs.location == "Delhi"
        assert prefs.budget == "medium"
        assert prefs.cuisine == "Italian"
        assert prefs.min_rating == 4.0
        assert len(prefs.additional_prefs) == 1
    
    def test_validate_missing_required_fields(self):
        """Test validation with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate(
                location="",
                budget="medium",
                cuisine="Italian",
                min_rating=4.0
            )
        
        assert "Location is required" in str(exc_info.value)
    
    def test_validate_multiple_errors(self):
        """Test validation with multiple errors."""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate(
                location="",
                budget="invalid_budget",
                cuisine="",
                min_rating=4.0
            )
        
        error_msg = str(exc_info.value)
        assert "Location is required" in error_msg
        assert "Cuisine is required" in error_msg


class TestFormatCost:
    """Test the format_cost utility function."""
    
    def test_format_cost(self):
        """Test cost formatting."""
        assert format_cost(1200) == "₹1200 for two"
        assert format_cost(500.5) == "₹500 for two"
        assert format_cost(0) == "₹0 for two"


class TestDataFilterEngine:
    """Test the DataFilterEngine class."""
    
    def test_initialization(self, filter_engine):
        """Test filter engine initialization."""
        assert filter_engine is not None
        assert len(filter_engine.df) > 0
        assert filter_engine._unique_locations is not None
        assert filter_engine._unique_cuisines is not None
    
    def test_get_stats(self, filter_engine):
        """Test getting dataset statistics."""
        stats = filter_engine.get_stats()
        
        assert 'total_restaurants' in stats
        assert 'unique_locations' in stats
        assert 'unique_cuisines' in stats
        assert stats['total_restaurants'] == 15
        assert stats['unique_locations'] == 3  # Delhi, Mumbai, Bangalore
    
    def test_fuzzy_match_location_exact(self, filter_engine):
        """Test fuzzy location matching with exact match."""
        location, score = filter_engine.fuzzy_match_location('Delhi')
        assert location == 'Delhi'
        assert score == 100
    
    def test_fuzzy_match_location_fuzzy(self, filter_engine):
        """Test fuzzy location matching with approximate match."""
        location, score = filter_engine.fuzzy_match_location('Deli')
        assert location == 'Delhi'
        assert score >= 80
    
    def test_fuzzy_match_location_no_match(self, filter_engine):
        """Test fuzzy location matching with no match."""
        location, score = filter_engine.fuzzy_match_location('Tokyo')
        # Should still return something, but score will be low
        assert score < 80
    
    def test_fuzzy_match_cuisine_exact(self, filter_engine):
        """Test fuzzy cuisine matching with exact match."""
        cuisine, score = filter_engine.fuzzy_match_cuisine('Italian')
        assert cuisine == 'Italian'
        assert score == 100
    
    def test_fuzzy_match_cuisine_fuzzy(self, filter_engine):
        """Test fuzzy cuisine matching with approximate match."""
        cuisine, score = filter_engine.fuzzy_match_cuisine('Itlian')  # typo
        assert 'Italian' in cuisine
        assert score >= 80
    
    def test_filter_basic(self, filter_engine, valid_preferences):
        """Test basic filtering with valid preferences."""
        df, msg = filter_engine.filter(valid_preferences)
        
        assert not df.empty
        assert len(df) <= 20
        assert msg is None
        
        # Check that results are from Delhi
        assert all(df['location'] == 'Delhi')
        
        # Check that results match budget
        assert all(df['budget'] == 'medium')
        
        # Check that results match rating
        assert all(df['aggregate_rating'] >= 4.0)
    
    def test_filter_returns_limited_candidates(self, filter_engine):
        """Test that filter limits number of candidates."""
        # Create preferences that would match many restaurants
        prefs = UserPreferences(
            location='Delhi',
            budget='medium',
            cuisine='Italian',
            min_rating=0.0,
            additional_prefs=[]
        )
        
        df, msg = filter_engine.filter(prefs)
        assert len(df) <= filter_engine.config['filtering']['max_candidates']
    
    def test_filter_high_budget(self, filter_engine, preferences_high_budget):
        """Test filtering with high budget preferences."""
        df, msg = filter_engine.filter(preferences_high_budget)
        
        assert not df.empty
        assert all(df['budget'] == 'high')
        assert all(df['location'] == 'Mumbai')
    
    def test_filter_low_budget(self, filter_engine, preferences_low_budget):
        """Test filtering with low budget preferences."""
        df, msg = filter_engine.filter(preferences_low_budget)
        
        assert not df.empty
        assert all(df['budget'] == 'low')
        assert all(df['location'] == 'Delhi')
    
    def test_filter_skip_cuisine(self, filter_engine, valid_preferences):
        """Test filtering with cuisine filter skipped."""
        df, msg = filter_engine.filter(valid_preferences, skip_filters={'cuisine'})
        
        assert not df.empty
        assert 'cuisine' in msg.lower()
        
        # Should have more results without cuisine filter
        df_with_cuisine, _ = filter_engine.filter(valid_preferences)
        assert len(df) >= len(df_with_cuisine)
    
    def test_filter_skip_budget(self, filter_engine, valid_preferences):
        """Test filtering with budget filter skipped."""
        df, msg = filter_engine.filter(valid_preferences, skip_filters={'budget'})
        
        assert not df.empty
        assert 'budget' in msg.lower()
    
    def test_progressive_relaxation_no_relaxation_needed(self, filter_engine, valid_preferences):
        """Test progressive relaxation when first filter works."""
        df, msg = filter_engine.filter_with_progressive_relaxation(valid_preferences)
        
        assert not df.empty
        assert msg is None  # No relaxation needed
    
    def test_progressive_relaxation_cuisine_relaxed(self, filter_engine):
        """Test progressive relaxation that relaxes cuisine."""
        # Create preferences that need cuisine relaxation
        prefs = UserPreferences(
            location='Bangalore',
            budget='medium',
            cuisine='Mexican',  # Not in sample data
            min_rating=4.0,
            additional_prefs=[]
        )
        
        df, msg = filter_engine.filter_with_progressive_relaxation(prefs)
        
        # Should find restaurants even if cuisine doesn't match
        assert not df.empty or msg is not None
        
        if not df.empty:
            assert all(df['location'] == 'Bangalore')
    
    def test_progressive_relaxation_full_relaxation(self, filter_engine):
        """Test progressive relaxation with multiple relaxations."""
        # Create preferences that require multiple relaxations
        prefs = UserPreferences(
            location='Delhi',
            budget='low',
            cuisine='Mexican',  # Not in sample data
            min_rating=4.9,  # Very high rating
            additional_prefs=[]
        )
        
        df, msg = filter_engine.filter_with_progressive_relaxation(prefs)
        
        # Should eventually find something in Delhi
        assert not df.empty
        assert msg is not None  # Some relaxation applied
        assert all(df['location'] == 'Delhi')
    
    def test_progressive_relaxation_no_location(self, filter_engine, preferences_no_results):
        """Test progressive relaxation when location doesn't exist."""
        df, msg = filter_engine.filter_with_progressive_relaxation(preferences_no_results)
        
        # Should be empty since Pune is not in data
        assert df.empty
        assert msg is not None
        assert 'Pune' in msg or 'location' in msg.lower()
    
    def test_get_available_locations(self, filter_engine):
        """Test getting available locations."""
        locations = filter_engine.get_available_locations()
        
        assert len(locations) > 0
        assert 'Delhi' in locations
        assert 'Mumbai' in locations
    
    def test_get_available_cuisines(self, filter_engine):
        """Test getting available cuisines."""
        cuisines = filter_engine.get_available_cuisines()
        
        assert len(cuisines) > 0
        assert any('Italian' in c for c in cuisines)
        assert any('Chinese' in c for c in cuisines)
    
    def test_filter_results_sorted_by_rating(self, filter_engine):
        """Test that filter results are sorted by rating."""
        prefs = UserPreferences(
            location='Delhi',
            budget='medium',
            cuisine='Italian',
            min_rating=0.0,
            additional_prefs=[]
        )
        
        df, _ = filter_engine.filter(prefs)
        
        if len(df) > 1:
            # Check that ratings are in descending order
            ratings = df['aggregate_rating'].tolist()
            assert ratings == sorted(ratings, reverse=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

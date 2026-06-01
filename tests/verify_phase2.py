#!/usr/bin/env python3
"""
Simple test runner to verify Phase 2 implementation without full pytest.
This validates that the core functionality works.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import UserPreferences, Recommendation, InputValidator, ValidationError, format_cost
from src.filter_engine import DataFilterEngine
import pandas as pd


def test_models():
    """Test the models module."""
    print("Testing models module...")
    
    # Test UserPreferences
    prefs = UserPreferences(
        location='Delhi',
        budget='MEDIUM',
        cuisine='Italian',
        min_rating=4.0,
        additional_prefs=['family-friendly']
    )
    assert prefs.budget == 'medium', "Budget should be normalized to lowercase"
    print("✓ UserPreferences works correctly")
    
    # Test Recommendation
    rec = Recommendation(
        rank=1,
        restaurant_name='Test Restaurant',
        cuisine='Italian',
        rating=4.5,
        estimated_cost='₹1000 for two',
        explanation='Great food'
    )
    rec_dict = rec.to_dict()
    assert rec_dict['rank'] == 1
    print("✓ Recommendation works correctly")
    
    # Test InputValidator
    try:
        InputValidator.validate(
            location='',
            budget='medium',
            cuisine='Italian',
            min_rating=4.0
        )
        assert False, "Should raise ValidationError"
    except ValidationError:
        pass
    print("✓ InputValidator validation works correctly")
    
    # Test sanitization
    sanitized = InputValidator.sanitize_string("Hello; DROP TABLE")
    assert "DROP" not in sanitized or ";" not in sanitized
    print("✓ InputValidator sanitization works correctly")
    
    # Test format_cost
    cost_str = format_cost(1200)
    assert cost_str == "₹1200 for two"
    print("✓ format_cost works correctly")
    
    print("✅ All model tests passed!\n")


def test_filter_engine():
    """Test the filter engine."""
    print("Testing filter engine...")
    
    # Create sample data
    data = {
        'name': ['Restaurant A', 'Restaurant B', 'Restaurant C'],
        'location': ['Delhi', 'Delhi', 'Mumbai'],
        'cuisines': ['Italian', 'Chinese', 'Italian'],
        'average_cost_for_two': [1000, 500, 1500],
        'aggregate_rating': [4.5, 4.0, 4.2],
        'votes': [1000, 500, 800],
        'budget': ['medium', 'low', 'medium']
    }
    df = pd.DataFrame(data)
    
    # Create a minimal config
    import tempfile
    import yaml
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config = {
            'filtering': {'max_candidates': 20, 'fuzzy_match_threshold': 80},
            'budget_thresholds': {'low': 500, 'medium': 1500}
        }
        yaml.dump(config, f)
        config_file = f.name
    
    try:
        engine = DataFilterEngine(df, config_path=config_file)
        print("✓ Filter engine initialized")
        
        # Test basic filtering
        prefs = UserPreferences(
            location='Delhi',
            budget='medium',
            cuisine='Italian',
            min_rating=4.0,
            additional_prefs=[]
        )
        
        filtered_df, msg = engine.filter(prefs)
        assert not filtered_df.empty, "Should find at least one result"
        assert filtered_df.iloc[0]['location'] == 'Delhi'
        print("✓ Basic filtering works")
        
        # Test fuzzy matching
        location, score = engine.fuzzy_match_location('Deli')
        assert location == 'Delhi'
        assert score >= 80
        print("✓ Fuzzy matching works")
        
        # Test progressive relaxation
        prefs_no_match = UserPreferences(
            location='Delhi',
            budget='low',
            cuisine='Mexican',  # Not in data
            min_rating=4.5,
            additional_prefs=[]
        )
        
        relaxed_df, msg = engine.filter_with_progressive_relaxation(prefs_no_match)
        assert msg is not None, "Should have relaxation message"
        print("✓ Progressive relaxation works")
        
        # Test stats
        stats = engine.get_stats()
        assert stats['total_restaurants'] == 3
        print("✓ Statistics method works")
        
        print("✅ All filter engine tests passed!\n")
        
    finally:
        # Clean up temp file
        os.unlink(config_file)


def main():
    """Run all tests."""
    print("="*60)
    print("PHASE 2 FUNCTIONALITY VERIFICATION")
    print("="*60)
    print()
    
    try:
        test_models()
        test_filter_engine()
        
        print("="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print()
        print("Phase 2 implementation is working correctly.")
        print("To run full test suite, install dependencies and run:")
        print("  pip install -r requirements.txt")
        print("  pytest tests/test_filter_engine.py -v")
        print()
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

"""
Pytest configuration and shared fixtures for testing.
"""

import pytest
import pandas as pd
import yaml
import os
import tempfile
from src.models import UserPreferences
from src.filter_engine import DataFilterEngine


@pytest.fixture
def sample_config():
    """Sample configuration dictionary."""
    return {
        'dataset': {
            'source': 'ManikaSaini/zomato-restaurant-recommendation',
            'cache_dir': 'data/raw',
            'processed_path': 'data/processed/zomato_clean.csv'
        },
        'budget_thresholds': {
            'low': 500,
            'medium': 1500
        },
        'filtering': {
            'max_candidates': 20,
            'fuzzy_match_threshold': 80
        },
        'llm': {
            'provider': 'openai',
            'model': 'gpt-4o-mini',
            'temperature': 0.7,
            'max_tokens': 1024,
            'api_key_env': 'OPENAI_API_KEY'
        },
        'ui': {
            'top_n_results': 5,
            'title': 'Zomato AI Restaurant Recommender'
        }
    }


@pytest.fixture
def sample_restaurant_data():
    """Sample restaurant dataset for testing."""
    data = {
        'name': [
            'Olive Bar & Kitchen',
            'Tonino',
            'Pizza Express',
            'The Spice Route',
            'China Bistro',
            'Mainland China',
            'Bukhara',
            'Dum Pukht',
            'Cafe Delhi Heights',
            'Big Chill',
            'Karim\'s',
            'Al Jawahar',
            'Moti Mahal',
            'Pind Balluchi',
            'Biryani Blues'
        ],
        'location': [
            'Delhi', 'Delhi', 'Delhi', 'Mumbai', 'Mumbai',
            'Mumbai', 'Delhi', 'Delhi', 'Delhi', 'Delhi',
            'Delhi', 'Delhi', 'Delhi', 'Bangalore', 'Bangalore'
        ],
        'cuisines': [
            'Italian, Mediterranean',
            'Italian',
            'Italian, Pizza',
            'Asian, Thai',
            'Chinese, Asian',
            'Chinese',
            'North Indian, Mughlai',
            'North Indian, Awadhi',
            'Continental, Italian',
            'Continental, Desserts',
            'Mughlai, North Indian',
            'Mughlai, North Indian',
            'North Indian, Mughlai',
            'North Indian',
            'Biryani, North Indian'
        ],
        'average_cost_for_two': [
            1200, 900, 800, 2000, 1500,
            1600, 3500, 4000, 700, 600,
            400, 350, 800, 1000, 450
        ],
        'aggregate_rating': [
            4.5, 4.3, 4.0, 4.7, 4.4,
            4.2, 4.8, 4.9, 4.1, 4.0,
            4.2, 4.0, 4.3, 4.1, 3.9
        ],
        'votes': [
            2500, 1800, 1500, 3200, 2100,
            2300, 4500, 5000, 1200, 1000,
            3500, 2800, 2200, 1400, 900
        ],
        'budget': [
            'medium', 'medium', 'medium', 'high', 'high',
            'high', 'high', 'high', 'medium', 'medium',
            'low', 'low', 'medium', 'medium', 'low'
        ]
    }
    
    return pd.DataFrame(data)


@pytest.fixture
def config_file(sample_config, tmp_path):
    """Create a temporary config file."""
    config_path = tmp_path / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(sample_config, f)
    return str(config_path)


@pytest.fixture
def filter_engine(sample_restaurant_data, config_file):
    """Create a DataFilterEngine instance with sample data."""
    return DataFilterEngine(sample_restaurant_data, config_path=config_file)


@pytest.fixture
def valid_preferences():
    """Valid user preferences for testing."""
    return UserPreferences(
        location='Delhi',
        budget='medium',
        cuisine='Italian',
        min_rating=4.0,
        additional_prefs=['family-friendly']
    )


@pytest.fixture
def preferences_no_results():
    """Preferences that should yield no results."""
    return UserPreferences(
        location='Pune',  # Not in sample data
        budget='low',
        cuisine='Mexican',  # Not in sample data
        min_rating=4.5,
        additional_prefs=[]
    )


@pytest.fixture
def preferences_high_budget():
    """Preferences for high-budget restaurants."""
    return UserPreferences(
        location='Mumbai',
        budget='high',
        cuisine='Chinese',
        min_rating=4.0,
        additional_prefs=[]
    )


@pytest.fixture
def preferences_low_budget():
    """Preferences for low-budget restaurants."""
    return UserPreferences(
        location='Delhi',
        budget='low',
        cuisine='North Indian',
        min_rating=4.0,
        additional_prefs=[]
    )

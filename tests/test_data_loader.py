"""
Unit tests for data_loader.py
"""

import pytest
import pandas as pd
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.data_loader import (
    ZomatoDataLoader,
    DataLoaderError,
    SchemaValidationError
)


class TestZomatoDataLoader:
    """Test suite for ZomatoDataLoader class"""
    
    @pytest.fixture
    def sample_config(self, tmp_path):
        """Create a temporary config file for testing"""
        config_content = """
dataset:
  source: "Zomato/zomato-restaurants"
  cache_dir: "./data/cache"
  processed_path: "./data/processed/zomato_clean.csv"
  sample_size: null

budget_thresholds:
  low: [0, 500]
  medium: [500, 1500]
  high: [1500, 100000]

llm:
  provider: "groq"
  model: "llama3-70b-8192"
  temperature: 0.7
  max_tokens: 1000
  
filter:
  max_candidates: 20
  fuzzy_threshold: 80
"""
        config_path = tmp_path / "test_config.yaml"
        config_path.write_text(config_content)
        return str(config_path)
    
    @pytest.fixture
    def sample_data(self):
        """Create sample restaurant data for testing"""
        return pd.DataFrame({
            'name': ['Restaurant A', 'Restaurant B', 'Restaurant C'],
            'location': ['Delhi', 'Mumbai', 'Bangalore'],
            'cuisines': ['North Indian', 'Chinese', 'South Indian'],
            'aggregate_rating': [4.5, 4.0, 3.8],
            'votes': [100, 200, 150],
            'average_cost_for_two': [400, 800, 2000]
        })
    
    def test_initialization_valid_config(self, sample_config):
        """Test successful initialization with valid config"""
        loader = ZomatoDataLoader(sample_config)
        assert loader.config is not None
        assert 'dataset' in loader.config
        assert 'budget_thresholds' in loader.config
    
    def test_initialization_missing_config(self):
        """Test initialization with missing config file"""
        with pytest.raises(DataLoaderError):
            ZomatoDataLoader("nonexistent_config.yaml")
    
    def test_initialization_invalid_yaml(self, tmp_path):
        """Test initialization with invalid YAML"""
        bad_config = tmp_path / "bad_config.yaml"
        bad_config.write_text("invalid: yaml: content:\n\t\tbad")
        
        with pytest.raises(DataLoaderError):
            ZomatoDataLoader(str(bad_config))
    
    def test_validate_schema_valid(self, sample_config, sample_data):
        """Test schema validation with valid data"""
        loader = ZomatoDataLoader(sample_config)
        # Should not raise an exception
        loader._validate_schema(sample_data)
    
    def test_validate_schema_missing_columns(self, sample_config):
        """Test schema validation with missing required columns"""
        loader = ZomatoDataLoader(sample_config)
        invalid_data = pd.DataFrame({
            'name': ['Test'],
            'location': ['Delhi']
            # Missing other required columns
        })
        
        with pytest.raises(SchemaValidationError):
            loader._validate_schema(invalid_data)
    
    def test_categorize_budget_low(self, sample_config):
        """Test budget categorization for low budget"""
        loader = ZomatoDataLoader(sample_config)
        assert loader._categorize_budget(300) == 'low'
        assert loader._categorize_budget(500) == 'low'
    
    def test_categorize_budget_medium(self, sample_config):
        """Test budget categorization for medium budget"""
        loader = ZomatoDataLoader(sample_config)
        assert loader._categorize_budget(600) == 'medium'
        assert loader._categorize_budget(1000) == 'medium'
        assert loader._categorize_budget(1500) == 'medium'
    
    def test_categorize_budget_high(self, sample_config):
        """Test budget categorization for high budget"""
        loader = ZomatoDataLoader(sample_config)
        assert loader._categorize_budget(2000) == 'high'
        assert loader._categorize_budget(5000) == 'high'
    
    def test_categorize_budget_edge_cases(self, sample_config):
        """Test budget categorization edge cases"""
        loader = ZomatoDataLoader(sample_config)
        assert loader._categorize_budget(0) == 'low'
        assert loader._categorize_budget(-100) == 'low'  # Negative should default to low
    
    def test_clean_data_removes_nulls(self, sample_config):
        """Test that clean_data removes rows with null values in critical columns"""
        loader = ZomatoDataLoader(sample_config)
        
        data_with_nulls = pd.DataFrame({
            'name': ['Restaurant A', None, 'Restaurant C'],
            'location': ['Delhi', 'Mumbai', None],
            'cuisines': ['North Indian', 'Chinese', 'South Indian'],
            'aggregate_rating': [4.5, 4.0, 3.8],
            'votes': [100, 200, 150],
            'average_cost_for_two': [400, 800, 2000]
        })
        
        cleaned = loader._clean_data(data_with_nulls)
        # Should only have 1 valid row (Restaurant A)
        assert len(cleaned) == 1
        assert cleaned.iloc[0]['name'] == 'Restaurant A'
    
    def test_clean_data_normalizes_location(self, sample_config):
        """Test that location names are normalized"""
        loader = ZomatoDataLoader(sample_config)
        
        data = pd.DataFrame({
            'name': ['Restaurant A'],
            'location': ['   delhi  '],
            'cuisines': ['North Indian'],
            'aggregate_rating': [4.5],
            'votes': [100],
            'average_cost_for_two': [400]
        })
        
        cleaned = loader._clean_data(data)
        assert cleaned.iloc[0]['location'] == 'Delhi'
    
    def test_clean_data_adds_budget_category(self, sample_config, sample_data):
        """Test that budget_category column is added"""
        loader = ZomatoDataLoader(sample_config)
        cleaned = loader._clean_data(sample_data)
        
        assert 'budget_category' in cleaned.columns
        assert cleaned.iloc[0]['budget_category'] == 'low'  # 400
        assert cleaned.iloc[1]['budget_category'] == 'medium'  # 800
        assert cleaned.iloc[2]['budget_category'] == 'high'  # 2000
    
    def test_clean_data_handles_invalid_ratings(self, sample_config):
        """Test handling of invalid rating values"""
        loader = ZomatoDataLoader(sample_config)
        
        data = pd.DataFrame({
            'name': ['Restaurant A', 'Restaurant B'],
            'location': ['Delhi', 'Mumbai'],
            'cuisines': ['North Indian', 'Chinese'],
            'aggregate_rating': [-1, 6],  # Invalid ratings
            'votes': [100, 200],
            'average_cost_for_two': [400, 800]
        })
        
        cleaned = loader._clean_data(data)
        # Ratings should be clamped to 0-5
        assert 0 <= cleaned.iloc[0]['aggregate_rating'] <= 5
        assert 0 <= cleaned.iloc[1]['aggregate_rating'] <= 5
    
    @patch('src.data_loader.load_dataset')
    def test_load_raw_dataset_success(self, mock_load_dataset, sample_config, sample_data):
        """Test successful raw dataset loading from HuggingFace"""
        # Mock the HuggingFace dataset
        mock_dataset = {'train': Mock()}
        mock_dataset['train'].to_pandas = Mock(return_value=sample_data)
        mock_load_dataset.return_value = mock_dataset
        
        loader = ZomatoDataLoader(sample_config)
        df = loader.load_raw_dataset()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        mock_load_dataset.assert_called_once()
    
    @patch('src.data_loader.load_dataset')
    def test_load_raw_dataset_fallback_to_cache(self, mock_load_dataset, sample_config, sample_data, tmp_path):
        """Test fallback to cached data when HuggingFace fails"""
        # Make HuggingFace loading fail
        mock_load_dataset.side_effect = Exception("Network error")
        
        # Create a cached file
        cache_path = tmp_path / "zomato_clean.csv"
        sample_data.to_csv(cache_path, index=False)
        
        # Update config to point to temp cache
        loader = ZomatoDataLoader(sample_config)
        loader.dataset_config['processed_path'] = str(cache_path)
        
        df = loader.load_raw_dataset()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
    
    def test_save_processed_data(self, sample_config, sample_data, tmp_path):
        """Test saving processed data to CSV"""
        loader = ZomatoDataLoader(sample_config)
        output_path = tmp_path / "output.csv"
        
        loader._save_processed_data(sample_data, str(output_path))
        
        assert output_path.exists()
        loaded_df = pd.read_csv(output_path)
        assert len(loaded_df) == len(sample_data)
    
    @patch('src.data_loader.load_dataset')
    def test_load_and_process_complete_pipeline(self, mock_load_dataset, sample_config, sample_data, tmp_path):
        """Test complete load and process pipeline"""
        # Mock HuggingFace dataset
        mock_dataset = {'train': Mock()}
        mock_dataset['train'].to_pandas = Mock(return_value=sample_data)
        mock_load_dataset.return_value = mock_dataset
        
        loader = ZomatoDataLoader(sample_config)
        output_path = tmp_path / "output.csv"
        loader.dataset_config['processed_path'] = str(output_path)
        
        df = loader.load_and_process()
        
        assert isinstance(df, pd.DataFrame)
        assert 'budget_category' in df.columns
        assert output_path.exists()
    
    def test_get_stats(self, sample_config, sample_data):
        """Test getting dataset statistics"""
        loader = ZomatoDataLoader(sample_config)
        cleaned_data = loader._clean_data(sample_data)
        
        stats = loader._get_stats(cleaned_data)
        
        assert 'total_restaurants' in stats
        assert 'locations' in stats
        assert 'cuisines' in stats
        assert 'budget_distribution' in stats
        assert stats['total_restaurants'] == 3
    
    def test_load_from_cache_only(self, sample_config, sample_data, tmp_path):
        """Test loading only from cache without HuggingFace"""
        cache_path = tmp_path / "cached_data.csv"
        
        # Add budget_category for realistic cache
        sample_data['budget_category'] = ['low', 'medium', 'high']
        sample_data.to_csv(cache_path, index=False)
        
        loader = ZomatoDataLoader(sample_config)
        loader.dataset_config['processed_path'] = str(cache_path)
        
        df = loader.load_from_cache()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert 'budget_category' in df.columns
    
    def test_load_from_cache_missing_file(self, sample_config):
        """Test loading from cache when file doesn't exist"""
        loader = ZomatoDataLoader(sample_config)
        loader.dataset_config['processed_path'] = "nonexistent.csv"
        
        with pytest.raises(DataLoaderError):
            loader.load_from_cache()


class TestDataLoaderEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_dataset(self, tmp_path):
        """Test handling of empty dataset"""
        config_content = """
dataset:
  source: "test/test"
  cache_dir: "./data/cache"
  processed_path: "./data/processed/zomato_clean.csv"
  sample_size: null

budget_thresholds:
  low: [0, 500]
  medium: [500, 1500]
  high: [1500, 100000]
"""
        config_path = tmp_path / "config.yaml"
        config_path.write_text(config_content)
        
        loader = ZomatoDataLoader(str(config_path))
        empty_df = pd.DataFrame()
        
        # Should handle empty dataframe gracefully
        with pytest.raises(SchemaValidationError):
            loader._validate_schema(empty_df)
    
    def test_large_cost_values(self, tmp_path):
        """Test handling of very large cost values"""
        config_content = """
dataset:
  source: "test/test"
  cache_dir: "./data/cache"
  processed_path: "./data/processed/zomato_clean.csv"
  sample_size: null

budget_thresholds:
  low: [0, 500]
  medium: [500, 1500]
  high: [1500, 100000]
"""
        config_path = tmp_path / "config.yaml"
        config_path.write_text(config_content)
        
        loader = ZomatoDataLoader(str(config_path))
        
        # Test with very large cost
        category = loader._categorize_budget(1000000)
        assert category == 'high'
    
    def test_duplicate_restaurants(self, tmp_path):
        """Test handling of duplicate restaurant entries"""
        config_content = """
dataset:
  source: "test/test"
  cache_dir: "./data/cache"
  processed_path: "./data/processed/zomato_clean.csv"
  sample_size: null

budget_thresholds:
  low: [0, 500]
  medium: [500, 1500]
  high: [1500, 100000]
"""
        config_path = tmp_path / "config.yaml"
        config_path.write_text(config_content)
        
        loader = ZomatoDataLoader(str(config_path))
        
        data_with_dupes = pd.DataFrame({
            'name': ['Restaurant A', 'Restaurant A', 'Restaurant B'],
            'location': ['Delhi', 'Delhi', 'Mumbai'],
            'cuisines': ['North Indian', 'North Indian', 'Chinese'],
            'aggregate_rating': [4.5, 4.5, 4.0],
            'votes': [100, 100, 200],
            'average_cost_for_two': [400, 400, 800]
        })
        
        cleaned = loader._clean_data(data_with_dupes)
        # Duplicates might be kept or removed depending on implementation
        assert isinstance(cleaned, pd.DataFrame)

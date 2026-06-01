"""
Integration tests for RecommendationOrchestrator.

Tests the complete pipeline from input validation through to final recommendations.
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import pandas as pd

from src.orchestrator import (
    RecommendationOrchestrator,
    OrchestratorError,
    DataNotLoadedError
)
from src.models import UserPreferences, Recommendation, ValidationError
from src.llm_client import LLMError


class TestRecommendationOrchestrator:
    """Test suite for RecommendationOrchestrator."""
    
    def test_initialization(self, config_file):
        """Test orchestrator initialization."""
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        
        assert orchestrator.config is not None
        assert orchestrator.data_df is None
        assert orchestrator.filter_engine is None
        assert orchestrator.prompt_builder is None
        assert orchestrator.llm_client is None
        assert orchestrator.formatter is None
    
    def test_config_loading(self, config_file):
        """Test configuration loading."""
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        
        assert 'dataset' in orchestrator.config
        assert 'llm' in orchestrator.config
        assert 'filtering' in orchestrator.config
        assert orchestrator.config['llm']['provider'] == 'openai'
        assert orchestrator.config['llm']['model'] == 'gpt-4o-mini'
    
    def test_initialization_invalid_config(self, tmp_path):
        """Test initialization with invalid config file."""
        invalid_config = tmp_path / "invalid.yaml"
        
        with pytest.raises(OrchestratorError):
            orchestrator = RecommendationOrchestrator(config_path=str(invalid_config))
    
    @patch('src.orchestrator.ZomatoDataLoader')
    @patch('src.orchestrator.DataFilterEngine')
    @patch('src.orchestrator.PromptBuilder')
    @patch('src.orchestrator.LLMClient')
    @patch('src.orchestrator.ResponseFormatter')
    def test_pipeline_initialization(
        self,
        mock_formatter,
        mock_llm_client,
        mock_prompt_builder,
        mock_filter_engine,
        mock_data_loader,
        config_file,
        sample_restaurant_data
    ):
        """Test full pipeline initialization."""
        # Setup mocks
        mock_loader_instance = Mock()
        mock_loader_instance.load_data.return_value = sample_restaurant_data
        mock_data_loader.return_value = mock_loader_instance
        
        # Initialize orchestrator
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        orchestrator.initialize()
        
        # Verify all components were initialized
        assert orchestrator.data_df is not None
        assert len(orchestrator.data_df) == len(sample_restaurant_data)
        mock_data_loader.assert_called_once()
        mock_filter_engine.assert_called_once()
        mock_prompt_builder.assert_called_once()
        mock_llm_client.assert_called_once()
        mock_formatter.assert_called_once()
    
    def test_recommend_not_initialized(self, config_file):
        """Test recommend() called before initialize()."""
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        
        with pytest.raises(DataNotLoadedError):
            orchestrator.recommend(
                location='Delhi',
                budget='medium',
                cuisine='Italian',
                min_rating=4.0
            )
    
    @patch('src.orchestrator.ZomatoDataLoader')
    @patch('src.orchestrator.DataFilterEngine')
    @patch('src.orchestrator.PromptBuilder')
    @patch('src.orchestrator.LLMClient')
    @patch('src.orchestrator.ResponseFormatter')
    def test_recommend_happy_path(
        self,
        mock_formatter,
        mock_llm_client,
        mock_prompt_builder,
        mock_filter_engine,
        mock_data_loader,
        config_file,
        sample_restaurant_data
    ):
        """Test successful end-to-end recommendation."""
        # Setup mocks
        mock_loader_instance = Mock()
        mock_loader_instance.load_data.return_value = sample_restaurant_data
        mock_data_loader.return_value = mock_loader_instance
        
        # Mock filter engine
        filtered_df = sample_restaurant_data[sample_restaurant_data['location'] == 'Delhi'].head(5)
        mock_filter_instance = Mock()
        mock_filter_instance.filter.return_value = filtered_df
        mock_filter_engine.return_value = mock_filter_instance
        
        # Mock prompt builder
        mock_prompt_instance = Mock()
        mock_prompt_instance.build.return_value = "Test prompt"
        mock_prompt_builder.return_value = mock_prompt_instance
        
        # Mock LLM client
        mock_llm_instance = Mock()
        mock_llm_instance.generate.return_value = "LLM response with restaurant recommendations"
        mock_llm_client.return_value = mock_llm_instance
        
        # Mock formatter
        mock_formatter_instance = Mock()
        mock_recommendations = [
            Recommendation(
                rank=1,
                restaurant_name="Olive Bar & Kitchen",
                cuisine="Italian",
                rating=4.5,
                estimated_cost="₹1200 for two",
                explanation="Great Italian restaurant"
            ),
            Recommendation(
                rank=2,
                restaurant_name="Tonino",
                cuisine="Italian",
                rating=4.3,
                estimated_cost="₹900 for two",
                explanation="Excellent choice"
            )
        ]
        mock_formatter_instance.parse.return_value = mock_recommendations
        mock_formatter.return_value = mock_formatter_instance
        
        # Initialize and run
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        orchestrator.initialize()
        
        recommendations = orchestrator.recommend(
            location='Delhi',
            budget='medium',
            cuisine='Italian',
            min_rating=4.0,
            additional_prefs=['romantic'],
            top_n=5
        )
        
        # Verify results
        assert len(recommendations) == 2
        assert recommendations[0].restaurant_name == "Olive Bar & Kitchen"
        assert recommendations[1].restaurant_name == "Tonino"
        
        # Verify pipeline steps were called
        mock_filter_instance.filter.assert_called_once()
        mock_prompt_instance.build.assert_called_once()
        mock_llm_instance.generate.assert_called_once_with("Test prompt")
        mock_formatter_instance.parse.assert_called_once()
    
    @patch('src.orchestrator.ZomatoDataLoader')
    @patch('src.orchestrator.DataFilterEngine')
    @patch('src.orchestrator.PromptBuilder')
    @patch('src.orchestrator.LLMClient')
    @patch('src.orchestrator.ResponseFormatter')
    def test_recommend_invalid_input(
        self,
        mock_formatter,
        mock_llm_client,
        mock_prompt_builder,
        mock_filter_engine,
        mock_data_loader,
        config_file,
        sample_restaurant_data
    ):
        """Test recommendation with invalid input."""
        # Setup mocks
        mock_loader_instance = Mock()
        mock_loader_instance.load_data.return_value = sample_restaurant_data
        mock_data_loader.return_value = mock_loader_instance
        
        # Initialize orchestrator
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        orchestrator.initialize()
        
        # Test invalid budget
        with pytest.raises(ValidationError):
            orchestrator.recommend(
                location='Delhi',
                budget='invalid',  # Invalid budget
                cuisine='Italian',
                min_rating=4.0
            )
        
        # Test empty location
        with pytest.raises(ValidationError):
            orchestrator.recommend(
                location='',  # Empty location
                budget='medium',
                cuisine='Italian',
                min_rating=4.0
            )
    
    @patch('src.orchestrator.ZomatoDataLoader')
    @patch('src.orchestrator.DataFilterEngine')
    @patch('src.orchestrator.PromptBuilder')
    @patch('src.orchestrator.LLMClient')
    @patch('src.orchestrator.ResponseFormatter')
    def test_recommend_no_results_found(
        self,
        mock_formatter,
        mock_llm_client,
        mock_prompt_builder,
        mock_filter_engine,
        mock_data_loader,
        config_file,
        sample_restaurant_data
    ):
        """Test recommendation when no restaurants match filters."""
        # Setup mocks
        mock_loader_instance = Mock()
        mock_loader_instance.load_data.return_value = sample_restaurant_data
        mock_data_loader.return_value = mock_loader_instance
        
        # Mock filter engine to return empty DataFrame
        mock_filter_instance = Mock()
        mock_filter_instance.filter.return_value = pd.DataFrame()
        mock_filter_engine.return_value = mock_filter_instance
        
        # Initialize orchestrator
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        orchestrator.initialize()
        
        recommendations = orchestrator.recommend(
            location='NonexistentCity',
            budget='medium',
            cuisine='Italian',
            min_rating=4.0
        )
        
        # Should return empty list
        assert recommendations == []
    
    @patch('src.orchestrator.ZomatoDataLoader')
    @patch('src.orchestrator.DataFilterEngine')
    @patch('src.orchestrator.PromptBuilder')
    @patch('src.orchestrator.LLMClient')
    @patch('src.orchestrator.ResponseFormatter')
    def test_recommend_llm_failure_fallback(
        self,
        mock_formatter,
        mock_llm_client,
        mock_prompt_builder,
        mock_filter_engine,
        mock_data_loader,
        config_file,
        sample_restaurant_data
    ):
        """Test fallback when LLM fails."""
        # Setup mocks
        mock_loader_instance = Mock()
        mock_loader_instance.load_data.return_value = sample_restaurant_data
        mock_data_loader.return_value = mock_loader_instance
        
        # Mock filter engine
        filtered_df = sample_restaurant_data[sample_restaurant_data['location'] == 'Delhi'].head(5)
        mock_filter_instance = Mock()
        mock_filter_instance.filter.return_value = filtered_df
        mock_filter_engine.return_value = mock_filter_instance
        
        # Mock prompt builder
        mock_prompt_instance = Mock()
        mock_prompt_instance.build.return_value = "Test prompt"
        mock_prompt_builder.return_value = mock_prompt_instance
        
        # Mock LLM client to raise error
        mock_llm_instance = Mock()
        mock_llm_instance.generate.side_effect = LLMError("API failure")
        mock_llm_client.return_value = mock_llm_instance
        
        # Initialize and run
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        orchestrator.initialize()
        
        recommendations = orchestrator.recommend(
            location='Delhi',
            budget='medium',
            cuisine='Italian',
            min_rating=4.0,
            top_n=3
        )
        
        # Should return fallback recommendations
        assert len(recommendations) > 0
        assert len(recommendations) <= 3
        assert all(isinstance(r, Recommendation) for r in recommendations)
    
    @patch('src.orchestrator.ZomatoDataLoader')
    @patch('src.orchestrator.DataFilterEngine')
    @patch('src.orchestrator.PromptBuilder')
    @patch('src.orchestrator.LLMClient')
    @patch('src.orchestrator.ResponseFormatter')
    def test_recommend_formatter_failure_fallback(
        self,
        mock_formatter,
        mock_llm_client,
        mock_prompt_builder,
        mock_filter_engine,
        mock_data_loader,
        config_file,
        sample_restaurant_data
    ):
        """Test fallback when response formatter fails."""
        # Setup mocks
        mock_loader_instance = Mock()
        mock_loader_instance.load_data.return_value = sample_restaurant_data
        mock_data_loader.return_value = mock_loader_instance
        
        # Mock filter engine
        filtered_df = sample_restaurant_data[sample_restaurant_data['location'] == 'Delhi'].head(5)
        mock_filter_instance = Mock()
        mock_filter_instance.filter.return_value = filtered_df
        mock_filter_engine.return_value = mock_filter_instance
        
        # Mock prompt builder
        mock_prompt_instance = Mock()
        mock_prompt_instance.build.return_value = "Test prompt"
        mock_prompt_builder.return_value = mock_prompt_instance
        
        # Mock LLM client
        mock_llm_instance = Mock()
        mock_llm_instance.generate.return_value = "Malformed LLM response"
        mock_llm_client.return_value = mock_llm_instance
        
        # Mock formatter to return empty list (parse failure)
        mock_formatter_instance = Mock()
        mock_formatter_instance.parse.return_value = []
        mock_formatter.return_value = mock_formatter_instance
        
        # Initialize and run
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        orchestrator.initialize()
        
        recommendations = orchestrator.recommend(
            location='Delhi',
            budget='medium',
            cuisine='Italian',
            min_rating=4.0,
            top_n=3
        )
        
        # Should return fallback recommendations
        assert len(recommendations) > 0
        assert len(recommendations) <= 3
    
    @patch('src.orchestrator.ZomatoDataLoader')
    def test_get_pipeline_info_before_init(self, mock_data_loader, config_file):
        """Test get_pipeline_info before initialization."""
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        
        info = orchestrator.get_pipeline_info()
        
        assert info['initialized'] is False
        assert info['dataset_size'] == 0
        assert info['llm_provider'] == 'openai'
        assert info['llm_model'] == 'gpt-4o-mini'
    
    @patch('src.orchestrator.ZomatoDataLoader')
    @patch('src.orchestrator.DataFilterEngine')
    @patch('src.orchestrator.PromptBuilder')
    @patch('src.orchestrator.LLMClient')
    @patch('src.orchestrator.ResponseFormatter')
    def test_get_pipeline_info_after_init(
        self,
        mock_formatter,
        mock_llm_client,
        mock_prompt_builder,
        mock_filter_engine,
        mock_data_loader,
        config_file,
        sample_restaurant_data
    ):
        """Test get_pipeline_info after initialization."""
        # Setup mocks
        mock_loader_instance = Mock()
        mock_loader_instance.load_data.return_value = sample_restaurant_data
        mock_data_loader.return_value = mock_loader_instance
        
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        orchestrator.initialize()
        
        info = orchestrator.get_pipeline_info()
        
        assert info['initialized'] is True
        assert info['dataset_size'] == len(sample_restaurant_data)
        assert info['llm_provider'] == 'openai'
        assert info['llm_model'] == 'gpt-4o-mini'
        assert info['max_candidates'] == 20
        assert info['fuzzy_threshold'] == 80
    
    @patch('src.orchestrator.ZomatoDataLoader')
    @patch('src.orchestrator.DataFilterEngine')
    @patch('src.orchestrator.PromptBuilder')
    @patch('src.orchestrator.LLMClient')
    @patch('src.orchestrator.ResponseFormatter')
    def test_recommend_with_additional_prefs(
        self,
        mock_formatter,
        mock_llm_client,
        mock_prompt_builder,
        mock_filter_engine,
        mock_data_loader,
        config_file,
        sample_restaurant_data
    ):
        """Test recommendation with additional preferences."""
        # Setup mocks
        mock_loader_instance = Mock()
        mock_loader_instance.load_data.return_value = sample_restaurant_data
        mock_data_loader.return_value = mock_loader_instance
        
        filtered_df = sample_restaurant_data.head(5)
        mock_filter_instance = Mock()
        mock_filter_instance.filter.return_value = filtered_df
        mock_filter_engine.return_value = mock_filter_instance
        
        mock_prompt_instance = Mock()
        mock_prompt_instance.build.return_value = "Test prompt"
        mock_prompt_builder.return_value = mock_prompt_instance
        
        mock_llm_instance = Mock()
        mock_llm_instance.generate.return_value = "LLM response"
        mock_llm_client.return_value = mock_llm_instance
        
        mock_formatter_instance = Mock()
        mock_formatter_instance.parse.return_value = [
            Recommendation(
                rank=1,
                restaurant_name="Test Restaurant",
                cuisine="Italian",
                rating=4.5,
                estimated_cost="₹1200",
                explanation="Test"
            )
        ]
        mock_formatter.return_value = mock_formatter_instance
        
        # Initialize and run
        orchestrator = RecommendationOrchestrator(config_path=config_file)
        orchestrator.initialize()
        
        recommendations = orchestrator.recommend(
            location='Delhi',
            budget='medium',
            cuisine='Italian',
            min_rating=4.0,
            additional_prefs=['family-friendly', 'outdoor seating', 'live music']
        )
        
        # Verify that preferences were passed through
        call_args = mock_filter_instance.filter.call_args
        preferences = call_args[0][0]
        assert len(preferences.additional_prefs) == 3
        assert 'family-friendly' in preferences.additional_prefs


class TestFallbackRecommendations:
    """Test suite for fallback recommendation logic."""
    
    def test_create_fallback_recommendations(self, sample_restaurant_data):
        """Test fallback recommendation creation."""
        orchestrator = RecommendationOrchestrator()
        
        # Create fallback recommendations
        recommendations = orchestrator._create_fallback_recommendations(
            filtered_df=sample_restaurant_data.head(5),
            top_n=3
        )
        
        assert len(recommendations) == 3
        assert all(isinstance(r, Recommendation) for r in recommendations)
        assert recommendations[0].rank == 1
        assert recommendations[1].rank == 2
        assert recommendations[2].rank == 3
        
        # Should be sorted by rating
        assert recommendations[0].rating >= recommendations[1].rating
        assert recommendations[1].rating >= recommendations[2].rating
    
    def test_create_fallback_with_empty_data(self):
        """Test fallback with empty DataFrame."""
        orchestrator = RecommendationOrchestrator()
        
        recommendations = orchestrator._create_fallback_recommendations(
            filtered_df=pd.DataFrame(),
            top_n=3
        )
        
        assert len(recommendations) == 0

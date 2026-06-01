"""
Recommendation Orchestrator Module

Central orchestration layer that wires together all components:
- InputValidator: Validates user input
- DataFilterEngine: Filters restaurants
- PromptBuilder: Constructs LLM prompts
- LLMClient: Generates AI recommendations
- ResponseFormatter: Parses LLM output

Handles the complete pipeline from user preferences to final recommendations.
"""

import os
import time
import logging
from typing import List, Optional, Dict, Any
import pandas as pd
import yaml

from .models import UserPreferences, Recommendation, InputValidator, ValidationError
from .data_loader import ZomatoDataLoader
from .filter_engine import DataFilterEngine, FilterEngineError, NoResultsError
from .prompt_builder import PromptBuilder, PromptBuilderError
from .llm_client import LLMClient, LLMError
from .formatter import ResponseFormatter, FormatterError

logger = logging.getLogger(__name__)


class OrchestratorError(Exception):
    """Base exception for orchestrator errors"""
    pass


class DataNotLoadedError(OrchestratorError):
    """Raised when data is not loaded"""
    pass


class RecommendationOrchestrator:
    """
    Orchestrates the end-to-end recommendation pipeline.
    
    Pipeline flow:
    1. InputValidator.validate(preferences) → UserPreferences
    2. DataFilterEngine.filter(preferences) → DataFrame (≤20 rows)
       └── if empty → relax filters & retry
    3. PromptBuilder.build(preferences, filtered_df) → prompt string
    4. LLMClient.generate(prompt) → raw LLM text
       └── if fails → retry (3x) → fallback message
    5. ResponseFormatter.parse(raw_text) → list[Recommendation]
    6. Return list[Recommendation]
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the orchestrator with configuration.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.data_loader = None
        self.data_df = None
        self.filter_engine = None
        self.prompt_builder = None
        self.llm_client = None
        self.formatter = None
        
        logger.info(f"RecommendationOrchestrator initialized with config from {config_path}")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Failed to load config from {config_path}: {e}")
            raise OrchestratorError(f"Configuration load failed: {e}")
    
    def initialize(self):
        """
        Initialize all pipeline components.
        
        Loads data and sets up filter engine, prompt builder, LLM client, and formatter.
        Call this before using recommend().
        """
        start_time = time.time()
        logger.info("=== Initializing Recommendation Pipeline ===")
        
        # 1. Load and preprocess data
        logger.info("Step 1/5: Loading dataset...")
        try:
            self.data_loader = ZomatoDataLoader(self.config_path)
            self.data_df = self.data_loader.load_and_process()
            logger.info(f"✓ Dataset loaded: {len(self.data_df)} restaurants")
        except Exception as e:
            logger.error(f"Failed to load dataset: {e}")
            raise DataNotLoadedError(f"Dataset loading failed: {e}")
        
        # 2. Initialize filter engine
        logger.info("Step 2/5: Initializing filter engine...")
        try:
            self.filter_engine = DataFilterEngine(self.data_df, self.config_path)
            logger.info("✓ Filter engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize filter engine: {e}")
            raise OrchestratorError(f"Filter engine initialization failed: {e}")
        
        # 3. Initialize prompt builder
        logger.info("Step 3/5: Initializing prompt builder...")
        try:
            templates_dir = "prompts"
            self.prompt_builder = PromptBuilder(templates_dir)
            logger.info("✓ Prompt builder initialized")
        except Exception as e:
            logger.error(f"Failed to initialize prompt builder: {e}")
            raise OrchestratorError(f"Prompt builder initialization failed: {e}")
        
        # 4. Initialize LLM client
        logger.info("Step 4/5: Initializing LLM client...")
        try:
            provider = self.config.get("llm", {}).get("provider", "openai")
            model = self.config.get("llm", {}).get("model", "gpt-4o-mini")
            temperature = self.config.get("llm", {}).get("temperature", 0.7)
            max_tokens = self.config.get("llm", {}).get("max_tokens", 1024)
            api_key_env = self.config.get("llm", {}).get("api_key_env", "OPENAI_API_KEY")
            
            # Resolve the API key from environment variable name
            api_key = os.getenv(api_key_env)
            
            self.llm_client = LLMClient(
                provider=provider,
                model=model,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            logger.info(f"✓ LLM client initialized: {provider}/{model}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            raise OrchestratorError(f"LLM client initialization failed: {e}")
        
        # 5. Initialize formatter
        logger.info("Step 5/5: Initializing response formatter...")
        try:
            self.formatter = ResponseFormatter()
            logger.info("✓ Response formatter initialized")
        except Exception as e:
            logger.error(f"Failed to initialize formatter: {e}")
            raise OrchestratorError(f"Formatter initialization failed: {e}")
        
        elapsed = time.time() - start_time
        logger.info(f"=== Pipeline initialized in {elapsed:.2f}s ===\n")
    
    def _validate_initialized(self):
        """Check that pipeline has been initialized."""
        if self.data_df is None or self.filter_engine is None:
            raise DataNotLoadedError(
                "Pipeline not initialized. Call initialize() first."
            )
    
    def recommend(
        self,
        location: str,
        budget: str,
        cuisine: str,
        min_rating: float,
        additional_prefs: Optional[List[str]] = None,
        top_n: Optional[int] = None
    ) -> List[Recommendation]:
        """
        Generate restaurant recommendations based on user preferences.
        
        Args:
            location: City or locality name
            budget: Budget tier ("low", "medium", "high")
            cuisine: Desired cuisine type
            min_rating: Minimum acceptable rating (0-5)
            additional_prefs: Optional list of additional preferences
            top_n: Number of recommendations to return (default from config)
            
        Returns:
            List of Recommendation objects
            
        Raises:
            ValidationError: If inputs are invalid
            DataNotLoadedError: If pipeline not initialized
            OrchestratorError: For other pipeline failures
        """
        self._validate_initialized()
        
        start_time = time.time()
        logger.info("\n" + "="*60)
        logger.info("=== STARTING RECOMMENDATION PIPELINE ===")
        logger.info("="*60)
        
        # Get top_n from config if not specified
        if top_n is None:
            top_n = self.config.get("ui", {}).get("top_n_results", 5)
        
        # ===== STEP 1: Validate Input =====
        logger.info("\n[STEP 1/5] Validating user input...")
        step_start = time.time()
        try:
            preferences = InputValidator.validate(
                location=location,
                budget=budget,
                cuisine=cuisine,
                min_rating=min_rating,
                additional_prefs=additional_prefs
            )
            logger.info(f"✓ Input validated in {time.time() - step_start:.2f}s")
            logger.info(f"  Location: {preferences.location}")
            logger.info(f"  Budget: {preferences.budget}")
            logger.info(f"  Cuisine: {preferences.cuisine}")
            logger.info(f"  Min Rating: {preferences.min_rating}")
            if preferences.additional_prefs:
                logger.info(f"  Additional: {', '.join(preferences.additional_prefs)}")
        except ValidationError as e:
            logger.error(f"✗ Validation failed: {e}")
            raise
        
        # ===== STEP 2: Filter Restaurants =====
        logger.info("\n[STEP 2/5] Filtering restaurants...")
        step_start = time.time()
        try:
            filtered_df, relaxation_msg = self.filter_engine.filter(preferences)
            logger.info(f"✓ Filtering completed in {time.time() - step_start:.2f}s")
            logger.info(f"  Candidates found: {len(filtered_df)}")
            if relaxation_msg:
                logger.info(f"  Filter relaxation: {relaxation_msg}")
            
            if len(filtered_df) == 0:
                logger.warning("No restaurants found matching criteria")
                return []
            
        except FilterEngineError as e:
            logger.error(f"✗ Filtering failed: {e}")
            raise OrchestratorError(f"Filter engine error: {e}")
        
        # ===== STEP 3: Build Prompt =====
        logger.info("\n[STEP 3/5] Building LLM prompt...")
        step_start = time.time()
        try:
            prompt = self.prompt_builder.build(
                preferences=preferences,
                restaurants_df=filtered_df,
                top_n=top_n
            )
            prompt_size = len(prompt)
            logger.info(f"✓ Prompt built in {time.time() - step_start:.2f}s")
            logger.info(f"  Prompt size: {prompt_size} characters")
            
        except PromptBuilderError as e:
            logger.error(f"✗ Prompt building failed: {e}")
            raise OrchestratorError(f"Prompt builder error: {e}")
        
        # ===== STEP 4: Generate LLM Response =====
        logger.info("\n[STEP 4/5] Calling LLM...")
        step_start = time.time()
        try:
            llm_response = self.llm_client.generate(prompt)
            logger.info(f"✓ LLM response received in {time.time() - step_start:.2f}s")
            logger.info(f"  Response size: {len(llm_response)} characters")
            
        except LLMError as e:
            logger.error(f"✗ LLM call failed: {e}")
            # Return fallback recommendations from filtered data
            logger.info("Falling back to rule-based recommendations")
            return self._create_fallback_recommendations(filtered_df, top_n)
        
        # ===== STEP 5: Parse Response =====
        logger.info("\n[STEP 5/5] Parsing LLM response...")
        step_start = time.time()
        try:
            recommendations = self.formatter.parse(llm_response, fallback_to_raw=True)
            logger.info(f"✓ Response parsed in {time.time() - step_start:.2f}s")
            logger.info(f"  Recommendations extracted: {len(recommendations)}")
            
            # If parser returns empty list, fall back to rule-based
            if not recommendations:
                logger.warning("Parser returned empty recommendations list")
                logger.info("Falling back to rule-based recommendations")
                return self._create_fallback_recommendations(filtered_df, top_n)
            
        except FormatterError as e:
            logger.error(f"✗ Parsing failed: {e}")
            # Return fallback recommendations
            logger.info("Falling back to rule-based recommendations")
            return self._create_fallback_recommendations(filtered_df, top_n)
        
        # ===== PIPELINE COMPLETE =====
        total_time = time.time() - start_time
        logger.info("\n" + "="*60)
        logger.info(f"=== PIPELINE COMPLETED in {total_time:.2f}s ===")
        logger.info("="*60 + "\n")
        
        # Limit to top_n recommendations
        return recommendations[:top_n]
    
    def _create_fallback_recommendations(
        self, 
        filtered_df: pd.DataFrame, 
        top_n: int
    ) -> List[Recommendation]:
        """
        Create fallback recommendations when LLM fails.
        
        Args:
            filtered_df: Filtered restaurant DataFrame
            top_n: Number of recommendations to create
            
        Returns:
            List of basic Recommendation objects
        """
        logger.info("Creating fallback recommendations from filtered data")
        
        recommendations = []
        
        # Handle empty DataFrame
        if filtered_df.empty:
            logger.warning("Empty DataFrame provided for fallback recommendations")
            return recommendations
        
        # Sort by rating (desc) and votes (desc)
        if 'votes' in filtered_df.columns:
            sorted_df = filtered_df.sort_values(
                by=['aggregate_rating', 'votes'], 
                ascending=[False, False]
            )
        else:
            sorted_df = filtered_df.sort_values(
                by=['aggregate_rating'], 
                ascending=[False]
            )
        
        # Take top N
        top_restaurants = sorted_df.head(top_n)
        
        for idx, row in enumerate(top_restaurants.iterrows(), start=1):
            _, restaurant = row
            
            # Basic explanation
            explanation = (
                f"Highly rated restaurant with {restaurant['aggregate_rating']} stars. "
                f"Serves {restaurant['cuisines']}."
            )
            
            rec = Recommendation(
                rank=idx,
                restaurant_name=restaurant.get('name', 'Unknown'),
                cuisine=restaurant.get('cuisines', 'Not specified'),
                rating=float(restaurant.get('aggregate_rating', 0)),
                estimated_cost=f"₹{restaurant.get('average_cost_for_two', 0):.0f} for two",
                explanation=explanation,
                location=restaurant.get('location'),
                votes=int(restaurant.get('votes', 0)) if 'votes' in restaurant and pd.notna(restaurant['votes']) else None
            )
            recommendations.append(rec)
        
        logger.info(f"Created {len(recommendations)} fallback recommendations")
        return recommendations
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        """
        Get information about the pipeline state.
        
        Returns:
            Dictionary with pipeline information
        """
        return {
            "initialized": self.data_df is not None,
            "dataset_size": len(self.data_df) if self.data_df is not None else 0,
            "llm_provider": self.config.get("llm", {}).get("provider"),
            "llm_model": self.config.get("llm", {}).get("model"),
            "max_candidates": self.config.get("filtering", {}).get("max_candidates"),
            "fuzzy_threshold": self.config.get("filtering", {}).get("fuzzy_match_threshold"),
        }

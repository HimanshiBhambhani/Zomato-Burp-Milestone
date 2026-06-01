#!/usr/bin/env python3
"""
CLI Test Script for Recommendation Pipeline

Demonstrates end-to-end pipeline execution from command line.
Tests: input → filter → prompt → LLM → formatted output

Usage:
    python test_pipeline.py
    python test_pipeline.py --location Delhi --budget medium --cuisine Italian
"""

import os
import sys
import argparse
import logging
from typing import List

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.orchestrator import RecommendationOrchestrator, OrchestratorError
from src.models import ValidationError, Recommendation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_recommendations(recommendations: List[Recommendation]):
    """Pretty-print recommendations to console."""
    print("\n" + "="*80)
    print(f"{'🍽️  RECOMMENDATIONS':^80}")
    print("="*80 + "\n")
    
    if not recommendations:
        print("  ❌ No recommendations found. Try adjusting your preferences.\n")
        return
    
    for rec in recommendations:
        print(f"  {'─'*76}")
        print(f"  🥇 #{rec.rank} | {rec.restaurant_name}")
        print(f"  {'─'*76}")
        print(f"     Cuisine:  {rec.cuisine}")
        print(f"     Rating:   {'⭐' * int(rec.rating)} {rec.rating:.1f}/5.0")
        print(f"     Cost:     {rec.estimated_cost}")
        if rec.location:
            print(f"     Location: {rec.location}")
        if rec.votes:
            print(f"     Votes:    {rec.votes}")
        print(f"\n     💬 {rec.explanation}")
        print()
    
    print("="*80 + "\n")


def run_test_scenario(orchestrator: RecommendationOrchestrator, scenario: dict):
    """Run a single test scenario."""
    print("\n" + "🔍 " + "="*78)
    print(f"  TEST SCENARIO: {scenario['name']}")
    print("="*80)
    print(f"  Location:    {scenario['location']}")
    print(f"  Budget:      {scenario['budget']}")
    print(f"  Cuisine:     {scenario['cuisine']}")
    print(f"  Min Rating:  {scenario['min_rating']}")
    if scenario.get('additional_prefs'):
        print(f"  Additional:  {', '.join(scenario['additional_prefs'])}")
    print("="*80)
    
    try:
        recommendations = orchestrator.recommend(
            location=scenario['location'],
            budget=scenario['budget'],
            cuisine=scenario['cuisine'],
            min_rating=scenario['min_rating'],
            additional_prefs=scenario.get('additional_prefs', []),
            top_n=scenario.get('top_n', 5)
        )
        
        print_recommendations(recommendations)
        return True
        
    except ValidationError as e:
        print(f"\n  ❌ Validation Error: {e}\n")
        return False
    except OrchestratorError as e:
        print(f"\n  ❌ Pipeline Error: {e}\n")
        return False
    except Exception as e:
        print(f"\n  ❌ Unexpected Error: {e}\n")
        logger.exception("Unexpected error in test scenario")
        return False


def run_predefined_tests(orchestrator: RecommendationOrchestrator):
    """Run a suite of predefined test scenarios."""
    
    test_scenarios = [
        {
            "name": "Italian in Delhi (Medium Budget)",
            "location": "Delhi",
            "budget": "medium",
            "cuisine": "Italian",
            "min_rating": 4.0,
            "additional_prefs": ["romantic", "fine dining"],
            "top_n": 3
        },
        {
            "name": "North Indian in Mumbai (Low Budget)",
            "location": "Mumbai",
            "budget": "low",
            "cuisine": "North Indian",
            "min_rating": 3.5,
            "additional_prefs": ["family-friendly"],
            "top_n": 5
        },
        {
            "name": "Chinese in Bangalore (High Budget)",
            "location": "Bangalore",
            "budget": "high",
            "cuisine": "Chinese",
            "min_rating": 4.2,
            "additional_prefs": [],
            "top_n": 3
        },
    ]
    
    print("\n" + "🚀 " + "="*78)
    print("  RUNNING PREDEFINED TEST SCENARIOS")
    print("="*80 + "\n")
    
    results = []
    for scenario in test_scenarios:
        success = run_test_scenario(orchestrator, scenario)
        results.append((scenario['name'], success))
        print("\n" + "-"*80 + "\n")
    
    # Print summary
    print("\n" + "📊 " + "="*78)
    print("  TEST SUMMARY")
    print("="*80)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"  Passed: {passed}/{total}")
    print()
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"    {status} - {name}")
    print("="*80 + "\n")


def run_custom_test(orchestrator: RecommendationOrchestrator, args):
    """Run a custom test from command-line arguments."""
    scenario = {
        "name": "Custom CLI Test",
        "location": args.location,
        "budget": args.budget,
        "cuisine": args.cuisine,
        "min_rating": args.min_rating,
        "additional_prefs": args.additional_prefs.split(',') if args.additional_prefs else [],
        "top_n": args.top_n
    }
    
    run_test_scenario(orchestrator, scenario)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test the restaurant recommendation pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run predefined test scenarios
  python test_pipeline.py
  
  # Custom test
  python test_pipeline.py --location Delhi --budget medium --cuisine Italian --min-rating 4.0
  
  # With additional preferences
  python test_pipeline.py --location Mumbai --budget low --cuisine "North Indian" \\
      --min-rating 3.5 --additional "family-friendly,quick service"
        """
    )
    
    parser.add_argument('--location', type=str, help='Location/city name')
    parser.add_argument('--budget', type=str, choices=['low', 'medium', 'high'],
                       help='Budget tier')
    parser.add_argument('--cuisine', type=str, help='Cuisine type')
    parser.add_argument('--min-rating', type=float, default=3.5,
                       help='Minimum rating (0-5, default: 3.5)')
    parser.add_argument('--additional', type=str, dest='additional_prefs',
                       help='Additional preferences (comma-separated)')
    parser.add_argument('--top-n', type=int, default=5,
                       help='Number of recommendations (default: 5)')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to config file (default: config.yaml)')
    
    args = parser.parse_args()
    
    # Check if running custom test or predefined tests
    custom_test = args.location and args.budget and args.cuisine
    
    print("\n" + "🍽️ " + "="*78)
    print("  ZOMATO RECOMMENDATION PIPELINE - CLI TEST")
    print("="*80 + "\n")
    
    # Initialize orchestrator
    try:
        print("📦 Initializing pipeline...\n")
        orchestrator = RecommendationOrchestrator(config_path=args.config)
        orchestrator.initialize()
        
        # Print pipeline info
        info = orchestrator.get_pipeline_info()
        print(f"✓ Pipeline initialized successfully")
        print(f"  Dataset: {info['dataset_size']} restaurants")
        print(f"  LLM: {info['llm_provider']}/{info['llm_model']}")
        print(f"  Max candidates: {info['max_candidates']}")
        print(f"  Fuzzy threshold: {info['fuzzy_threshold']}")
        
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        logger.exception("Pipeline initialization failed")
        sys.exit(1)
    
    # Run tests
    if custom_test:
        run_custom_test(orchestrator, args)
    else:
        if args.location or args.budget or args.cuisine:
            print("\n⚠️  Warning: Incomplete parameters for custom test.")
            print("   --location, --budget, and --cuisine are all required.")
            print("   Running predefined tests instead.\n")
        run_predefined_tests(orchestrator)
    
    print("✨ Pipeline test completed!\n")


if __name__ == "__main__":
    main()

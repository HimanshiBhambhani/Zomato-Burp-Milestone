"""
Data Loader Module

Handles downloading, preprocessing, and caching of the Zomato restaurant dataset
from Hugging Face. Implements data cleaning, normalization, and budget tier derivation.
"""

import os
import logging
from typing import Optional
import pandas as pd
import yaml
from datasets import load_dataset

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoaderError(Exception):
    """Custom exception for data loading errors"""
    pass


class SchemaValidationError(DataLoaderError):
    """Raised when dataset schema doesn't match expectations"""
    pass


class ZomatoDataLoader:
    """
    Handles loading and preprocessing the Zomato restaurant dataset.
    """
    
    REQUIRED_COLUMNS = {
        "name", "location", "cuisines", "average_cost_for_two", 
        "aggregate_rating"
    }
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the data loader with configuration.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config = self._load_config(config_path)
        self.dataset_config = self.config["dataset"]
        self.budget_thresholds = self.config["budget_thresholds"]
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            raise DataLoaderError(f"Configuration file not found: {config_path}")
        except yaml.YAMLError as e:
            raise DataLoaderError(f"Invalid YAML in configuration: {e}")
    
    def load_raw_dataset(self) -> pd.DataFrame:
        """
        Load the Zomato dataset from Hugging Face.
        
        Returns:
            Raw dataframe from the dataset
            
        Raises:
            DataLoaderError: If dataset cannot be loaded
        """
        try:
            logger.info(f"Loading dataset from Hugging Face: {self.dataset_config['source']}")
            dataset = load_dataset(
                self.dataset_config['source'],
                cache_dir=self.dataset_config['cache_dir']
            )
            
            # Convert to pandas DataFrame (assuming 'train' split)
            if 'train' in dataset:
                df = dataset['train'].to_pandas()
            else:
                # Use the first available split
                split_name = list(dataset.keys())[0]
                df = dataset[split_name].to_pandas()
            
            logger.info(f"Dataset loaded successfully: {len(df)} rows")
            return df
            
        except Exception as e:
            logger.error(f"Failed to load dataset: {e}")
            # Try to load from cache
            cache_path = self.dataset_config['processed_path']
            if os.path.exists(cache_path):
                logger.warning(f"Falling back to cached processed data: {cache_path}")
                return pd.read_csv(cache_path)
            else:
                raise DataLoaderError(f"Could not load dataset and no cache available: {e}")
    
    def validate_schema(self, df: pd.DataFrame) -> None:
        """
        Validate that the dataset contains required columns.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            SchemaValidationError: If required columns are missing
        """
        # Normalize column names (handle case differences)
        df.columns = df.columns.str.lower().str.strip()
        
        # Map common column name variations
        column_mapping = {
            'restaurant name': 'name',
            'restaurant_name': 'name',
            'city': 'location',
            'cuisine': 'cuisines',
            'average cost for two': 'average_cost_for_two',
            'avg_cost_for_two': 'average_cost_for_two',
            'cost_for_two': 'average_cost_for_two',
            'rating': 'aggregate_rating',
            'ratings': 'aggregate_rating',
        }
        
        df.rename(columns=column_mapping, inplace=True)
        
        # Check for required columns
        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise SchemaValidationError(
                f"Dataset missing required columns: {missing}. "
                f"Available columns: {list(df.columns)}"
            )
        
        logger.info("Schema validation passed")
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess the raw dataset.
        
        Args:
            df: Raw dataframe
            
        Returns:
            Preprocessed dataframe
        """
        logger.info("Starting preprocessing pipeline...")
        
        # Make a copy to avoid modifying original
        df = df.copy()
        
        # 1. Normalize column names
        df.columns = df.columns.str.lower().str.strip()
        
        # 2. Handle column name variations (reapply mapping)
        column_mapping = {
            'restaurant name': 'name',
            'restaurant_name': 'name',
            'city': 'location',
            'cuisine': 'cuisines',
            'average cost for two': 'average_cost_for_two',
            'avg_cost_for_two': 'average_cost_for_two',
            'cost_for_two': 'average_cost_for_two',
            'rating': 'aggregate_rating',
            'ratings': 'aggregate_rating',
        }
        df.rename(columns=column_mapping, inplace=True)
        
        # Select only the columns we need (if others exist)
        available_cols = [col for col in df.columns if col in self.REQUIRED_COLUMNS or 
                         col in ['votes', 'has_online_delivery', 'has_table_booking']]
        df = df[available_cols]
        
        logger.info(f"Selected columns: {list(df.columns)}")
        
        # 3. Drop rows with missing critical fields
        initial_rows = len(df)
        df.dropna(subset=['name', 'location', 'aggregate_rating'], inplace=True)
        logger.info(f"Dropped {initial_rows - len(df)} rows with missing critical fields")
        
        # 4. Clean and normalize location names
        df['location'] = df['location'].str.strip().str.title()
        
        # 5. Clean cuisines field
        if 'cuisines' in df.columns:
            df['cuisines'] = df['cuisines'].fillna('Not Specified')
            df['cuisines'] = df['cuisines'].str.strip()
        
        # 6. Convert numeric fields
        df['aggregate_rating'] = pd.to_numeric(df['aggregate_rating'], errors='coerce')
        df['average_cost_for_two'] = pd.to_numeric(df['average_cost_for_two'], errors='coerce')
        
        # 7. Drop rows with invalid numeric values
        df.dropna(subset=['aggregate_rating', 'average_cost_for_two'], inplace=True)
        
        # 8. Remove zero/negative ratings and costs
        df = df[df['aggregate_rating'] > 0]
        df = df[df['average_cost_for_two'] > 0]
        
        # 9. Convert votes to numeric if present
        if 'votes' in df.columns:
            df['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0).astype(int)
        
        # 10. Derive budget tier
        df['budget'] = df['average_cost_for_two'].apply(self._derive_budget_tier)
        
        # 11. Remove duplicates (same name + location, keep highest rated)
        df = df.sort_values('aggregate_rating', ascending=False)
        df = df.drop_duplicates(subset=['name', 'location'], keep='first')
        
        # 12. Reset index
        df.reset_index(drop=True, inplace=True)
        
        logger.info(f"Preprocessing complete. Final dataset: {len(df)} rows, {len(df.columns)} columns")
        
        return df
    
    def _derive_budget_tier(self, cost: float) -> str:
        """
        Derive budget tier from average cost for two.
        
        Args:
            cost: Average cost for two people
            
        Returns:
            Budget tier: 'low', 'medium', or 'high'
        """
        if cost <= self.budget_thresholds['low']:
            return 'low'
        elif cost <= self.budget_thresholds['medium']:
            return 'medium'
        else:
            return 'high'
    
    def save_processed_data(self, df: pd.DataFrame, output_path: Optional[str] = None) -> None:
        """
        Save the preprocessed dataset to CSV.
        
        Args:
            df: Preprocessed dataframe
            output_path: Output file path (uses config default if None)
        """
        if output_path is None:
            output_path = self.dataset_config['processed_path']
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        logger.info(f"Processed data saved to: {output_path}")
    
    def get_dataset_summary(self, df: pd.DataFrame) -> dict:
        """
        Generate a summary of the dataset.
        
        Args:
            df: DataFrame to summarize
            
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'total_restaurants': len(df),
            'unique_locations': df['location'].nunique(),
            'locations': sorted(df['location'].unique().tolist()),
            'rating_range': (df['aggregate_rating'].min(), df['aggregate_rating'].max()),
            'cost_range': (df['average_cost_for_two'].min(), df['average_cost_for_two'].max()),
            'budget_distribution': df['budget'].value_counts().to_dict(),
        }
        
        if 'cuisines' in df.columns:
            # Get unique cuisines (splitting comma-separated values)
            all_cuisines = set()
            for cuisines_str in df['cuisines'].dropna():
                for cuisine in str(cuisines_str).split(','):
                    all_cuisines.add(cuisine.strip())
            summary['unique_cuisines'] = len(all_cuisines)
            summary['top_cuisines'] = sorted(list(all_cuisines))[:20]
        
        return summary
    
    def load_and_process(self) -> pd.DataFrame:
        """
        Full pipeline: load, validate, preprocess, and save dataset.
        
        Returns:
            Preprocessed dataframe
        """
        try:
            # Check if processed data already exists
            processed_path = self.dataset_config['processed_path']
            if os.path.exists(processed_path):
                logger.info(f"Loading existing processed data from: {processed_path}")
                df = pd.read_csv(processed_path)
                logger.info(f"Loaded {len(df)} rows from cache")
                return df
            
            # Load raw data
            df = self.load_raw_dataset()
            
            # Validate schema
            self.validate_schema(df)
            
            # Preprocess
            df = self.preprocess(df)
            
            # Save processed data
            self.save_processed_data(df)
            
            # Print summary
            summary = self.get_dataset_summary(df)
            logger.info(f"Dataset Summary: {summary['total_restaurants']} restaurants "
                       f"across {summary['unique_locations']} locations")
            
            return df
            
        except Exception as e:
            logger.error(f"Error in load_and_process: {e}")
            raise


def main():
    """Main function to run the data loader."""
    try:
        loader = ZomatoDataLoader()
        df = loader.load_and_process()
        
        # Display summary
        summary = loader.get_dataset_summary(df)
        print("\n" + "="*60)
        print("DATASET SUMMARY")
        print("="*60)
        print(f"Total Restaurants: {summary['total_restaurants']}")
        print(f"Unique Locations: {summary['unique_locations']}")
        print(f"Locations: {', '.join(summary['locations'][:10])}" + 
              (f" ... (+{len(summary['locations'])-10} more)" if len(summary['locations']) > 10 else ""))
        print(f"\nRating Range: {summary['rating_range'][0]:.1f} - {summary['rating_range'][1]:.1f}")
        print(f"Cost Range: ₹{summary['cost_range'][0]:.0f} - ₹{summary['cost_range'][1]:.0f}")
        print(f"\nBudget Distribution:")
        for budget, count in summary['budget_distribution'].items():
            print(f"  {budget}: {count} ({count/summary['total_restaurants']*100:.1f}%)")
        
        if 'unique_cuisines' in summary:
            print(f"\nUnique Cuisines: {summary['unique_cuisines']}")
            print(f"Sample Cuisines: {', '.join(summary['top_cuisines'][:15])}" + 
                  (f" ..." if len(summary['top_cuisines']) > 15 else ""))
        
        print("\n" + "="*60)
        print(f"✓ Data processing complete!")
        print(f"✓ Processed data saved to: {loader.dataset_config['processed_path']}")
        print("="*60 + "\n")
        
        # Display sample rows
        print("\nSample Data (first 3 rows):")
        print(df.head(3).to_string(index=False))
        
    except Exception as e:
        logger.error(f"Failed to process data: {e}")
        raise


if __name__ == "__main__":
    main()

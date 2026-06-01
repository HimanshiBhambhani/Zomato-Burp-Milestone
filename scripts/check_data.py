#!/usr/bin/env python3
"""
Script to check data storage details and schema.
Shows what we have instead of traditional database tables.
"""

import pandas as pd
from pathlib import Path
import yaml

print("📊 DATA STORAGE OVERVIEW")
print("=" * 80)

# Check what data files exist
data_dir = Path("data")

# Check for different file types
csv_files = list(data_dir.rglob("*.csv"))
parquet_files = list(data_dir.rglob("*.parquet"))
db_files = list(data_dir.rglob("*.db")) + list(data_dir.rglob("*.sqlite"))

print(f"\n✓ CSV Files: {len(csv_files)}")
for f in csv_files:
    size = f.stat().st_size / (1024*1024)  # MB
    print(f"  - {f.relative_to('.')}: {size:.2f} MB")

print(f"\n✓ Parquet Files: {len(parquet_files)}")
if parquet_files:
    for f in parquet_files:
        size = f.stat().st_size / (1024*1024)
        print(f"  - {f.relative_to('.')}: {size:.2f} MB")
else:
    print("  - None (We don't use Parquet format, only CSV)")

print(f"\n✓ Database Files: {len(db_files)}")
if db_files:
    for f in db_files:
        size = f.stat().st_size / (1024*1024)
        print(f"  - {f.relative_to('.')}: {size:.2f} MB")
else:
    print("  - None (No traditional DB, using CSV files)")

# Show config
print("\n" + "=" * 80)
print("📝 CONFIGURATION")
print("=" * 80)

with open("config.yaml") as f:
    config = yaml.safe_load(f)
    print(f"\nDataset Source: {config['dataset']['source']}")
    print(f"Cache Directory: {config['dataset']['cache_dir']}")
    print(f"Processed Path: {config['dataset']['processed_path']}")

# Check if data exists
processed_path = Path(config['dataset']['processed_path'])

if processed_path.exists():
    print("\n" + "=" * 80)
    print("📋 DATASET SCHEMA (Like Database Table)")
    print("=" * 80)
    
    df = pd.read_csv(processed_path)
    
    print(f"\nTable: 'restaurants' (stored as CSV)")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Memory: {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
    
    print(f"\n{'Column Name':<30} {'Type':<15} {'Null Count':<12} {'Sample Value'}")
    print("-" * 80)
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        null_count = df[col].isnull().sum()
        sample_val = str(df[col].iloc[0])[:30] if len(df) > 0 else "N/A"
        print(f"{col:<30} {dtype:<15} {null_count:<12} {sample_val}")
    
    print("\n" + "=" * 80)
    print("📊 DATA STATISTICS")
    print("=" * 80)
    
    print(f"\nUnique Locations: {df['location'].nunique()}")
    print(f"Unique Cuisines: {df['cuisines'].nunique()}")
    print(f"Rating Range: {df['aggregate_rating'].min():.1f} - {df['aggregate_rating'].max():.1f}")
    print(f"Cost Range: ₹{df['average_cost_for_two'].min():.0f} - ₹{df['average_cost_for_two'].max():.0f}")
    
    print("\nTop 5 Locations by Restaurant Count:")
    print(df['location'].value_counts().head(5).to_string())
    
    print("\n\nBudget Distribution:")
    print(df['budget'].value_counts().to_string())
    
    print("\n" + "=" * 80)
    print("🔍 SAMPLE RECORD")
    print("=" * 80)
    print(df.head(1).T.to_string())
    
else:
    print(f"\n⚠️  WARNING: No processed data found at: {processed_path}")
    print(f"\n💡 To load data, run:")
    print(f"   source .venv/bin/activate")
    print(f"   python -m src.data_loader")

print("\n" + "=" * 80)
print("📌 ARCHITECTURE NOTE")
print("=" * 80)
print("""
This project uses a FILE-BASED storage approach, not a traditional database:

Storage:          CSV file (data/processed/zomato_clean.csv)
In-memory:        Pandas DataFrame
Query method:     DataFrame operations (filter, sort, group)
Alternative:      Could use SQLite, PostgreSQL, or Parquet for production

Current design is optimized for:
✓ Fast prototyping
✓ Easy deployment (no DB setup needed)
✓ Streamlit compatibility
✓ Small-to-medium datasets (<1M rows)

For production with larger data, consider:
→ Parquet format (faster reads, compressed)
→ SQLite (file-based DB with SQL queries)
→ PostgreSQL/MySQL (full RDBMS)
""")

print("=" * 80)

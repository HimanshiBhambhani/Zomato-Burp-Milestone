#!/usr/bin/env python3
"""
Demo: CSV vs Parquet comparison using sample data
"""

import pandas as pd
from pathlib import Path
import tempfile
import os

print("=" * 80)
print("📦 CSV vs PARQUET DEMO")
print("=" * 80)

# Create sample restaurant data
sample_data = {
    'name': [
        'Olive Bar & Kitchen', 'Tonino', 'Pizza Express', 
        'The Spice Route', 'China Bistro', 'Mainland China',
        'Bukhara', 'Dum Pukht', 'Cafe Delhi Heights', 'Big Chill'
    ],
    'location': [
        'Delhi', 'Delhi', 'Delhi', 'Mumbai', 'Mumbai',
        'Mumbai', 'Delhi', 'Delhi', 'Delhi', 'Delhi'
    ],
    'cuisines': [
        'Italian, Mediterranean', 'Italian', 'Italian, Pizza',
        'Asian, Thai', 'Chinese, Asian', 'Chinese',
        'North Indian, Mughlai', 'North Indian, Awadhi',
        'Continental, Italian', 'Continental, Desserts'
    ],
    'average_cost_for_two': [1200, 900, 800, 2000, 1500, 1600, 3500, 4000, 700, 600],
    'aggregate_rating': [4.5, 4.3, 4.0, 4.7, 4.4, 4.2, 4.8, 4.9, 4.1, 4.0],
    'votes': [2500, 1800, 1500, 3200, 2100, 2300, 4500, 5000, 1200, 1000],
    'budget': ['medium', 'medium', 'medium', 'high', 'high', 'high', 'high', 'high', 'medium', 'medium']
}

df = pd.DataFrame(sample_data)

print(f"\n📊 Sample Dataset:")
print(f"   Rows: {len(df)}")
print(f"   Columns: {len(df.columns)}")

# Create temporary files
with tempfile.TemporaryDirectory() as tmpdir:
    csv_file = Path(tmpdir) / "sample.csv"
    parquet_file = Path(tmpdir) / "sample.parquet"
    
    # Save as CSV
    print("\n💾 Saving as CSV...")
    df.to_csv(csv_file, index=False)
    csv_size = csv_file.stat().st_size
    print(f"   ✓ CSV Size: {csv_size / 1024:.2f} KB")
    
    # Save as Parquet
    print("\n💾 Saving as Parquet...")
    df.to_parquet(parquet_file, engine='pyarrow', compression='snappy', index=False)
    parquet_size = parquet_file.stat().st_size
    print(f"   ✓ Parquet Size: {parquet_size / 1024:.2f} KB")
    
    # Comparison
    compression_ratio = (1 - parquet_size / csv_size) * 100
    
    print("\n" + "=" * 80)
    print("📊 FORMAT COMPARISON")
    print("=" * 80)
    
    print(f"\n{'Metric':<30} {'CSV':<15} {'Parquet':<15} {'Winner'}")
    print("-" * 80)
    print(f"{'File Size (KB)':<30} {csv_size/1024:>10.2f}     {parquet_size/1024:>10.2f}     {'Parquet ✓'}")
    print(f"{'Compression Ratio':<30} {'0%':>14} {f'{compression_ratio:.1f}%':>14}     {'Parquet ✓'}")
    print(f"{'Human Readable':<30} {'Yes':>14} {'No':>14}     {'CSV ✓'}")
    print(f"{'Read Speed':<30} {'Medium':>14} {'Fast':>14}     {'Parquet ✓'}")
    print(f"{'Write Speed':<30} {'Fast':>14} {'Medium':>14}     {'CSV ✓'}")
    print(f"{'Schema Enforcement':<30} {'No':>14} {'Yes':>14}     {'Parquet ✓'}")
    print(f"{'Columnar Storage':<30} {'No':>14} {'Yes':>14}     {'Parquet ✓'}")
    
    print("\n💾 Space Saved: {:.2f} KB ({:.1f}%)".format(
        (csv_size - parquet_size) / 1024, 
        compression_ratio
    ))
    
    # Read performance demo
    print("\n⚡ PERFORMANCE TEST:")
    print("-" * 80)
    
    import time
    
    # CSV read
    start = time.time()
    for _ in range(100):
        pd.read_csv(csv_file)
    csv_time = time.time() - start
    print(f"CSV Read (100x):     {csv_time:.4f} seconds")
    
    # Parquet read
    start = time.time()
    for _ in range(100):
        pd.read_parquet(parquet_file)
    parquet_time = time.time() - start
    print(f"Parquet Read (100x): {parquet_time:.4f} seconds")
    
    speedup = csv_time / parquet_time
    print(f"\n🚀 Parquet is {speedup:.1f}x faster for reading!")

print("\n" + "=" * 80)
print("📋 DATA PREVIEW (Parquet can store this efficiently)")
print("=" * 80)
print(df.head())

print("\n" + "=" * 80)
print("💡 WHEN TO USE EACH FORMAT")
print("=" * 80)

print("""
✅ Use CSV when:
   • Need human-readable format
   • Simple data exchange
   • Small datasets
   • Quick prototyping
   • Excel compatibility needed

✅ Use Parquet when:
   • Large datasets (>100MB)
   • Analytics/data science workloads
   • Need fast read performance
   • Want compression
   • Columnar data access patterns
   • Production data pipelines

🎯 For this project:
   • Development: CSV is fine (easy debugging)
   • Production: Switch to Parquet (better performance)
   • Both can coexist!
""")

print("\n" + "=" * 80)
print("🔧 HOW TO CREATE PARQUET FOR YOUR PROJECT")
print("=" * 80)

print("""
Step 1: Load your data (if not already loaded)
   source .venv/bin/activate
   python -m src.data_loader

Step 2: Convert to Parquet
   python convert_to_parquet.py

Step 3: Use in your code
   import pandas as pd
   df = pd.read_parquet('data/processed/zomato_clean.parquet')
""")

print("=" * 80)

#!/usr/bin/env python3
"""
Convert CSV data to Parquet format and provide comparison.
"""

import pandas as pd
from pathlib import Path
import os

print("=" * 80)
print("📦 CONVERTING CSV TO PARQUET FORMAT")
print("=" * 80)

# Check if CSV exists
csv_path = Path("data/processed/zomato_clean.csv")
parquet_path = Path("data/processed/zomato_clean.parquet")

if not csv_path.exists():
    print(f"\n❌ CSV file not found at: {csv_path}")
    print("\n💡 First, load the data:")
    print("   source .venv/bin/activate")
    print("   python -m src.data_loader")
    exit(1)

print(f"\n✓ Found CSV file: {csv_path}")

# Load CSV
print("\n📊 Loading CSV data...")
df = pd.read_csv(csv_path)
print(f"   Rows: {len(df):,}")
print(f"   Columns: {len(df.columns)}")

# Get CSV file size
csv_size = csv_path.stat().st_size
print(f"   CSV Size: {csv_size / (1024*1024):.2f} MB")

# Convert to Parquet
print("\n🔄 Converting to Parquet...")
df.to_parquet(parquet_path, engine='pyarrow', compression='snappy', index=False)
print(f"   ✓ Saved to: {parquet_path}")

# Get Parquet file size
parquet_size = parquet_path.stat().st_size
compression_ratio = (1 - parquet_size / csv_size) * 100

print(f"\n📊 COMPARISON:")
print("-" * 80)
print(f"{'Format':<15} {'Size (MB)':<15} {'Compression':<20} {'Speed'}")
print("-" * 80)
print(f"{'CSV':<15} {csv_size/(1024*1024):>10.2f}     {'Baseline':<20} {'Medium'}")
print(f"{'Parquet':<15} {parquet_size/(1024*1024):>10.2f}     {f'{compression_ratio:.1f}% smaller':<20} {'Fast'}")
print("-" * 80)
print(f"\n💾 Space Saved: {(csv_size - parquet_size) / (1024*1024):.2f} MB")

# Read and verify Parquet
print("\n🔍 READING PARQUET FILE...")
df_parquet = pd.read_parquet(parquet_path)
print(f"   ✓ Loaded {len(df_parquet):,} rows")
print(f"   ✓ All columns intact: {df.columns.tolist() == df_parquet.columns.tolist()}")
print(f"   ✓ Data integrity: {df.equals(df_parquet)}")

print("\n📋 SCHEMA (Parquet):")
print("-" * 80)
print(df_parquet.dtypes.to_string())

print("\n🔍 SAMPLE DATA:")
print("-" * 80)
print(df_parquet.head(3).to_string())

print("\n" + "=" * 80)
print("✅ SUCCESS! You now have Parquet format available")
print("=" * 80)

print(f"""
📁 Files available:
   CSV:     {csv_path}
   Parquet: {parquet_path}

💡 To use Parquet in your code:
   
   import pandas as pd
   df = pd.read_parquet('data/processed/zomato_clean.parquet')
   
🚀 Benefits:
   ✓ {compression_ratio:.1f}% smaller file size
   ✓ 2-5x faster read performance
   ✓ Efficient columnar storage
   ✓ Built-in compression
   ✓ Better for analytics workloads
""")

print("=" * 80)

import pandas as pd
from pathlib import Path

# Create sample data
sample_data = {
    'name': ['Olive Bar & Kitchen', 'Tonino', 'Pizza Express', 'The Spice Route', 'China Bistro',
             'Mainland China', 'Bukhara', 'Dum Pukht', 'Cafe Delhi Heights', 'Big Chill',
             "Karim's", 'Al Jawahar', 'Moti Mahal', 'Pind Balluchi', 'Biryani Blues',
             'Leopold Cafe', 'Britannia & Co', 'Trishna', 'Mahesh Lunch Home', 'The Table'],
    'location': ['Delhi', 'Delhi', 'Delhi', 'Mumbai', 'Mumbai', 'Mumbai', 'Delhi', 'Delhi', 'Delhi', 'Delhi',
                 'Delhi', 'Delhi', 'Delhi', 'Bangalore', 'Bangalore', 'Mumbai', 'Mumbai', 'Mumbai', 'Mumbai', 'Mumbai'],
    'cuisines': ['Italian, Mediterranean', 'Italian', 'Italian, Pizza', 'Asian, Thai', 'Chinese, Asian',
                 'Chinese', 'North Indian, Mughlai', 'North Indian, Awadhi', 'Continental, Italian', 'Continental, Desserts',
                 'Mughlai, North Indian', 'Mughlai, North Indian', 'North Indian, Mughlai', 'North Indian', 'Biryani, North Indian',
                 'Continental, European', 'Parsi, Iranian', 'Seafood, Coastal', 'Seafood, Mangalorean', 'European, Continental'],
    'average_cost_for_two': [1200, 900, 800, 2000, 1500, 1600, 3500, 4000, 700, 600, 400, 350, 800, 1000, 450, 1200, 800, 2500, 1800, 3000],
    'aggregate_rating': [4.5, 4.3, 4.0, 4.7, 4.4, 4.2, 4.8, 4.9, 4.1, 4.0, 4.2, 4.0, 4.3, 4.1, 3.9, 4.3, 4.5, 4.6, 4.4, 4.7],
    'votes': [2500, 1800, 1500, 3200, 2100, 2300, 4500, 5000, 1200, 1000, 3500, 2800, 2200, 1400, 900, 2100, 1900, 2800, 2400, 2700],
    'budget': ['medium', 'medium', 'medium', 'high', 'high', 'high', 'high', 'high', 'medium', 'medium', 'low', 'low', 'medium', 'medium', 'low', 'medium', 'medium', 'high', 'high', 'high']
}

df = pd.DataFrame(sample_data)
Path("data/processed").mkdir(parents=True, exist_ok=True)
parquet_path = "data/processed/zomato_clean.parquet"
df.to_parquet(parquet_path, engine='pyarrow', compression='snappy', index=False)

print(f"✓ Created Parquet file: {parquet_path}")
print(f"  Rows: {len(df)}")
print(f"  Size: {Path(parquet_path).stat().st_size / 1024:.2f} KB")

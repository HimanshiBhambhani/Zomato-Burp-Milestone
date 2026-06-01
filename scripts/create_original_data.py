"""Restore original 20 restaurant dataset"""
import pandas as pd
import numpy as np

# Original 20 restaurants
data = {
    'name': [
        'Dum Pukht', 'Bukhara', 'Indian Accent', 'Wasabi by Morimoto', 'Moti Mahal',
        'Karim\'s', 'Saravana Bhavan', 'Cafe Lota', 'Andhra Bhavan', 'Rajinder Da Dhaba',
        'Bombay Canteen', 'Trishna', 'Bastian', 'Peshawri', 'Masala Library',
        'Café Mysore', 'MTR', 'Truffles', 'Koshy\'s', 'Toit Brewpub'
    ],
    'cuisines': [
        'North Indian, Awadhi', 'North Indian, Mughlai', 'Modern Indian', 'Japanese, Asian',
        'North Indian, Mughlai', 'Mughlai, North Indian', 'South Indian, Vegetarian',
        'Indian, Cafe', 'South Indian, Andhra', 'North Indian, Punjabi',
        'Modern Indian', 'Seafood, Coastal', 'Seafood, European', 'North Indian, Mughlai',
        'Modern Indian, Molecular', 'South Indian, Vegetarian', 'South Indian, Vegetarian',
        'American, Continental', 'Continental, Bakery', 'Pub, Continental'
    ],
    'location': [
        'Delhi', 'Delhi', 'Delhi', 'Delhi', 'Delhi',
        'Delhi', 'Delhi', 'Delhi', 'Delhi', 'Delhi',
        'Mumbai', 'Mumbai', 'Mumbai', 'Mumbai', 'Mumbai',
        'Bangalore', 'Bangalore', 'Bangalore', 'Bangalore', 'Bangalore'
    ],
    'aggregate_rating': [4.9, 4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.2, 4.1, 4.0,
                         4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.2, 4.1, 4.0, 3.9],
    'votes': [5000, 4800, 4500, 3200, 4000, 5500, 3800, 2500, 2200, 3500,
              4200, 3800, 3500, 3000, 2800, 2500, 3200, 3800, 2800, 4200],
    'average_cost_for_two': [4000, 3800, 3500, 3200, 800, 600, 400, 500, 350, 450,
                              2500, 2200, 2800, 3000, 2500, 300, 350, 600, 400, 800]
}

df = pd.DataFrame(data)

# Add budget categories
def categorize_budget(cost):
    if cost < 500:
        return 'low'
    elif cost < 1500:
        return 'medium'
    else:
        return 'high'

df['budget_category'] = df['average_cost_for_two'].apply(categorize_budget)

# Save both formats
df.to_csv('data/processed/zomato_clean.csv', index=False)
df.to_parquet('data/processed/zomato_clean.parquet', index=False)

print(f"✓ Restored original dataset: {len(df)} restaurants")
print(f"  - Cities: {df['location'].nunique()}")
print(f"  - Budget distribution: {df['budget_category'].value_counts().to_dict()}")

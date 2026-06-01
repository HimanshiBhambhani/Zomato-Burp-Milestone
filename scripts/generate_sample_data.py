"""
Generate additional sample restaurant data for testing
"""

import pandas as pd
import random
from pathlib import Path

# Set random seed for reproducibility
random.seed(42)

# Expanded data for better coverage
locations = ["Delhi", "Mumbai", "Bangalore", "Pune", "Kolkata", "Chennai", "Hyderabad", "Jaipur"]

cuisines_list = [
    "North Indian", "South Indian", "Chinese", "Italian", "Continental",
    "Mughlai", "Fast Food", "Cafe", "Bakery", "Biryani",
    "Seafood", "Street Food", "Desserts", "Asian", "Thai",
    "Mexican", "Japanese", "Mediterranean", "American", "European",
    "Beverages", "Bengali", "Gujarati", "Rajasthani", "Punjabi",
    "Pizza", "Burger", "Sandwich", "Rolls", "Momos"
]

# Create diverse restaurant names
restaurant_prefixes = [
    "The", "Cafe", "Kitchen", "Bistro", "Grill", "Paradise", "Palace",
    "Corner", "Street", "House", "Junction", "Express", "Delight"
]

restaurant_types = [
    "Spice", "Garden", "Food", "Treats", "Bites", "Flavors", "Hub",
    "Station", "Point", "Lounge", "Diner", "Eatery", "Restaurant"
]

# Generate 200 diverse restaurants
restaurants = []

for i in range(200):
    # Random location (ensure good distribution)
    location = locations[i % len(locations)]
    
    # Select 1-3 cuisines
    num_cuisines = random.choice([1, 1, 2, 2, 3])  # More likely to have 1-2
    selected_cuisines = random.sample(cuisines_list, num_cuisines)
    cuisines = ", ".join(selected_cuisines)
    
    # Generate restaurant name
    if i < 50:
        # Some real-sounding names
        name = f"{random.choice(restaurant_prefixes)} {random.choice(restaurant_types)}"
    else:
        # More creative names
        name = f"{random.choice(['Spice', 'Golden', 'Silver', 'Royal', 'Urban', 'Classic', 'Modern', 'Tasty', 'Fresh', 'Quick', 'Grand', 'Elite'])} {random.choice(['Kitchen', 'Bistro', 'Cafe', 'Restaurant', 'Diner', 'Grill', 'House', 'Corner', 'Junction', 'Express'])}"
    
    # Add cuisine-specific names for some
    if "Italian" in cuisines and random.random() < 0.3:
        name = f"{random.choice(['La', 'Il', 'Bella', 'Casa'])} {random.choice(['Pasta', 'Pizza', 'Roma', 'Milano'])}"
    elif "Chinese" in cuisines and random.random() < 0.3:
        name = f"{random.choice(['Golden', 'Red', 'Blue'])} {random.choice(['Dragon', 'Wok', 'China', 'Phoenix'])}"
    elif "South Indian" in cuisines and random.random() < 0.3:
        name = f"{random.choice(['Dosa', 'Idli', 'Madras', 'Chennai', 'Udupi'])} {random.choice(['Corner', 'Express', 'Palace', 'House'])}"
    
    # Rating distribution: More restaurants in 3.5-4.5 range
    rating_choices = [3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9]
    rating = random.choice(rating_choices)
    
    # Budget tiers with distribution
    budget_tier = random.choices(
        ['low', 'medium', 'high'],
        weights=[30, 50, 20]  # More medium-budget options
    )[0]
    
    # Cost based on budget tier and location
    if budget_tier == 'low':
        cost = random.randint(200, 500)
    elif budget_tier == 'medium':
        cost = random.randint(500, 1500)
    else:
        cost = random.randint(1500, 4000)
    
    # Higher costs in metros
    if location in ["Mumbai", "Bangalore", "Delhi"]:
        cost = int(cost * 1.2)
    
    # Votes: Popular places have more votes
    if rating >= 4.3:
        votes = random.randint(1000, 10000)
    elif rating >= 4.0:
        votes = random.randint(500, 3000)
    else:
        votes = random.randint(100, 1000)
    
    restaurants.append({
        'name': name,
        'location': location,
        'cuisines': cuisines,
        'average_cost_for_two': cost,
        'aggregate_rating': rating,
        'budget': budget_tier,
        'votes': votes
    })

# Create DataFrame
df = pd.DataFrame(restaurants)

# Ensure we have good distribution
print(f"Generated {len(df)} restaurants")
print(f"\nLocation distribution:")
print(df['location'].value_counts())
print(f"\nBudget distribution:")
print(df['budget'].value_counts())
print(f"\nRating range: {df['aggregate_rating'].min():.1f} - {df['aggregate_rating'].max():.1f}")
print(f"\nTop cuisines:")
all_cuisines = []
for c in df['cuisines']:
    all_cuisines.extend([x.strip() for x in c.split(',')])
from collections import Counter
cuisine_counts = Counter(all_cuisines)
for cuisine, count in cuisine_counts.most_common(15):
    print(f"  {cuisine}: {count}")

# Save to CSV and Parquet
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

csv_path = output_dir / "zomato_clean.csv"
parquet_path = output_dir / "zomato_clean.parquet"

df.to_csv(csv_path, index=False)
df.to_parquet(parquet_path, index=False)

print(f"\n✓ Saved to {csv_path} ({len(df)} rows)")
print(f"✓ Saved to {parquet_path}")

# Show sample
print(f"\nSample data:")
print(df.head(5).to_string(index=False))

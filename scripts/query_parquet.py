#!/usr/bin/env python3
"""
Interactive Query Tool for Parquet Data
Run SQL-like queries on your restaurant data
"""

import pandas as pd
from pathlib import Path
import sys

def print_header(title):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)

def show_schema(df):
    """Show table schema"""
    print_header("📋 TABLE SCHEMA")
    print(f"\nRows: {len(df):,} | Columns: {len(df.columns)}\n")
    
    print(f"{'Column':<25} {'Type':<15} {'Non-Null':<12} {'Sample Value'}")
    print("-" * 80)
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = f"{df[col].count():,}"
        sample = str(df[col].iloc[0])[:30] if len(df) > 0 else "N/A"
        print(f"{col:<25} {dtype:<15} {non_null:<12} {sample}")

def run_query(df, query_name, description):
    """Execute a predefined query"""
    print_header(f"🔍 QUERY: {query_name}")
    print(f"Description: {description}\n")
    
    queries = {
        "1": {
            "name": "Top 10 Highest Rated Restaurants",
            "code": lambda: df.nlargest(10, 'aggregate_rating')[['name', 'location', 'cuisines', 'aggregate_rating', 'average_cost_for_two']]
        },
        "2": {
            "name": "Restaurants by Location Count",
            "code": lambda: df['location'].value_counts().head(10).to_frame('count')
        },
        "3": {
            "name": "Average Cost by Budget Tier",
            "code": lambda: df.groupby('budget')['average_cost_for_two'].agg(['mean', 'min', 'max', 'count']).round(2)
        },
        "4": {
            "name": "Italian Restaurants in Delhi",
            "code": lambda: df[(df['location'] == 'Delhi') & (df['cuisines'].str.contains('Italian', na=False))][['name', 'cuisines', 'aggregate_rating', 'average_cost_for_two']].head(10)
        },
        "5": {
            "name": "High-Budget Restaurants (Rating >= 4.5)",
            "code": lambda: df[(df['budget'] == 'high') & (df['aggregate_rating'] >= 4.5)][['name', 'location', 'cuisines', 'aggregate_rating', 'average_cost_for_two']].head(10)
        },
        "6": {
            "name": "Top 5 Cuisines by Restaurant Count",
            "code": lambda: df['cuisines'].value_counts().head(5).to_frame('count')
        },
        "7": {
            "name": "Rating Distribution",
            "code": lambda: df.groupby(pd.cut(df['aggregate_rating'], bins=[0, 2, 3, 4, 5])).size().to_frame('count')
        },
        "8": {
            "name": "Most Voted Restaurants",
            "code": lambda: df.nlargest(10, 'votes')[['name', 'location', 'aggregate_rating', 'votes']].head(10) if 'votes' in df.columns else pd.DataFrame({'error': ['votes column not found']})
        },
        "9": {
            "name": "Budget Distribution",
            "code": lambda: df['budget'].value_counts().to_frame('count')
        },
        "10": {
            "name": "Sample Records",
            "code": lambda: df.head(10)
        }
    }
    
    if query_name in queries:
        try:
            result = queries[query_name]["code"]()
            print(result.to_string())
            print(f"\n✓ Returned {len(result)} rows")
        except Exception as e:
            print(f"❌ Query Error: {e}")
    else:
        print("❌ Invalid query number")

def main():
    print("=" * 80)
    print(" 🗃️  PARQUET DATA QUERY TOOL")
    print("=" * 80)
    
    # Check for Parquet file
    parquet_path = Path("data/processed/zomato_clean.parquet")
    csv_path = Path("data/processed/zomato_clean.csv")
    
    if parquet_path.exists():
        print(f"\n✓ Found Parquet file: {parquet_path}")
        file_size = parquet_path.stat().st_size / (1024*1024)
        print(f"  Size: {file_size:.2f} MB")
        df = pd.read_parquet(parquet_path)
        print(f"  Loading... Done! ({len(df):,} rows)")
    elif csv_path.exists():
        print(f"\n⚠️  Parquet file not found, using CSV instead")
        print(f"✓ Found CSV file: {csv_path}")
        print(f"\n💡 To create Parquet file, run: python convert_to_parquet.py")
        df = pd.read_csv(csv_path)
        print(f"  Loading... Done! ({len(df):,} rows)")
    else:
        print(f"\n❌ No data files found!")
        print(f"\n💡 First, load the data:")
        print(f"   source .venv/bin/activate")
        print(f"   python -m src.data_loader")
        sys.exit(1)
    
    # Show schema once
    show_schema(df)
    
    # Available queries
    print_header("📚 AVAILABLE QUERIES")
    queries_menu = {
        "1": "Top 10 Highest Rated Restaurants",
        "2": "Restaurants by Location Count",
        "3": "Average Cost by Budget Tier",
        "4": "Italian Restaurants in Delhi",
        "5": "High-Budget Restaurants (Rating >= 4.5)",
        "6": "Top 5 Cuisines by Restaurant Count",
        "7": "Rating Distribution",
        "8": "Most Voted Restaurants",
        "9": "Budget Distribution",
        "10": "Sample Records (First 10 rows)",
        "schema": "Show table schema again",
        "all": "Run all queries",
        "custom": "Run custom pandas query",
        "q": "Quit"
    }
    
    for key, desc in queries_menu.items():
        print(f"  {key:<10} - {desc}")
    
    # Interactive mode
    print("\n" + "=" * 80)
    
    if len(sys.argv) > 1:
        # Non-interactive mode
        query_num = sys.argv[1]
        if query_num == "all":
            for i in range(1, 11):
                run_query(df, str(i), queries_menu[str(i)])
                print()
        elif query_num in queries_menu:
            run_query(df, query_num, queries_menu[query_num])
        else:
            print(f"❌ Unknown query: {query_num}")
    else:
        # Interactive mode
        print("💡 TIP: Run with argument for non-interactive mode")
        print("   Example: python query_parquet.py 1")
        print("   Example: python query_parquet.py all")
        
        while True:
            print("\n" + "-" * 80)
            choice = input("\nEnter query number (or 'q' to quit): ").strip().lower()
            
            if choice == 'q':
                print("\n👋 Goodbye!")
                break
            elif choice == 'schema':
                show_schema(df)
            elif choice == 'all':
                for i in range(1, 11):
                    run_query(df, str(i), queries_menu[str(i)])
                    input("\nPress Enter for next query...")
            elif choice == 'custom':
                print("\n📝 Enter your pandas query:")
                print("   Available: df (DataFrame)")
                print("   Example: df[df['location'] == 'Mumbai'].head()")
                print()
                custom = input(">>> ")
                try:
                    result = eval(custom)
                    if isinstance(result, pd.DataFrame) or isinstance(result, pd.Series):
                        print("\n" + result.to_string())
                    else:
                        print(f"\n{result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
            elif choice in queries_menu:
                run_query(df, choice, queries_menu[choice])
            else:
                print("❌ Invalid choice. Try again.")
    
    print("\n" + "=" * 80)
    print("💡 CUSTOM QUERY EXAMPLES")
    print("=" * 80)
    print("""
# Filter by location
df[df['location'] == 'Delhi']

# Filter by multiple conditions
df[(df['location'] == 'Mumbai') & (df['aggregate_rating'] >= 4.5)]

# Group by and aggregate
df.groupby('location')['aggregate_rating'].mean()

# Sort and limit
df.sort_values('average_cost_for_two', ascending=False).head(10)

# Search in text
df[df['cuisines'].str.contains('Italian', na=False)]

# Statistics
df.describe()
    """)
    
    print("=" * 80)

if __name__ == "__main__":
    main()

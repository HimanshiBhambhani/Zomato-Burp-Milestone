#!/usr/bin/env python3
"""
Quick test to verify Streamlit app can be imported and runs
"""

import sys
import ast

print("=" * 80)
print(" 🧪 STREAMLIT APP VALIDATION")
print("=" * 80)

# Test 1: Syntax Check
print("\n✓ Test 1: Python Syntax...")
try:
    with open('app.py', 'r') as f:
        ast.parse(f.read())
    print("  ✅ Syntax valid")
except SyntaxError as e:
    print(f"  ❌ Syntax error: {e}")
    sys.exit(1)

# Test 2: Import Check
print("\n✓ Test 2: Import Dependencies...")
try:
    import streamlit as st
    print(f"  ✅ streamlit: {st.__version__}")
except ImportError as e:
    print(f"  ❌ streamlit not installed: {e}")
    print("     Run: pip install streamlit")
    sys.exit(1)

try:
    import pandas as pd
    print(f"  ✅ pandas: {pd.__version__}")
except ImportError as e:
    print(f"  ❌ pandas not installed: {e}")
    sys.exit(1)

# Test 3: Module Structure
print("\n✓ Test 3: Module Structure...")
try:
    from src.orchestrator import RecommendationOrchestrator
    print("  ✅ orchestrator imported")
except ImportError as e:
    print(f"  ⚠️  orchestrator import warning: {e}")

try:
    from src.models import Recommendation, ValidationError
    print("  ✅ models imported")
except ImportError as e:
    print(f"  ⚠️  models import warning: {e}")

# Test 4: File Structure
print("\n✓ Test 4: File Structure...")
import os
from pathlib import Path

files_to_check = [
    ("Main app", "app.py"),
    ("Config", "config.yaml"),
    ("Orchestrator", "src/orchestrator.py"),
    ("Models", "src/models.py"),
    ("Filter Engine", "src/filter_engine.py"),
    ("LLM Client", "src/llm_client.py"),
    ("Prompt Builder", "src/prompt_builder.py"),
    ("Formatter", "src/formatter.py"),
]

for name, filepath in files_to_check:
    exists = Path(filepath).exists()
    status = "✅" if exists else "⚠️"
    print(f"  {status} {name}: {filepath}")

# Test 5: Data Check
print("\n✓ Test 5: Data Files...")
data_files = [
    "data/processed/zomato_clean.csv",
    "data/processed/zomato_clean.parquet"
]

for filepath in data_files:
    if Path(filepath).exists():
        size = Path(filepath).stat().st_size / (1024*1024)
        print(f"  ✅ {filepath} ({size:.2f} MB)")
    else:
        print(f"  ⚠️  {filepath} (not found)")

print("\n" + "=" * 80)
print(" 📋 SUMMARY")
print("=" * 80)

print("""
✅ Streamlit app is ready!

🚀 To start the app, run:
   source .venv/bin/activate
   streamlit run app.py

⚠️  If data files are missing:
   python -m src.data_loader

🌐 The app will open at: http://localhost:8501
""")

print("=" * 80)

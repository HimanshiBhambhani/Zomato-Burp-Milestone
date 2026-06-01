# Zomato AI Restaurant Recommender

AI-powered restaurant recommendation system that combines structured data with Large Language Models to provide personalized restaurant suggestions.

## 🎯 Project Overview

This project implements an intelligent restaurant recommendation service inspired by Zomato. It uses:
- Real-world Zomato restaurant dataset from Hugging Face
- Advanced filtering and fuzzy matching
- LLM-powered personalized recommendations with explanations
- Interactive Streamlit UI

## 📁 Project Structure

```
zomato-recommendation/
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── data_loader.py         # Dataset loading & preprocessing ✓
│   ├── models.py              # Data classes (Phase 2)
│   ├── filter_engine.py       # Filtering logic (Phase 2)
│   ├── prompt_builder.py      # LLM prompts (Phase 3)
│   ├── llm_client.py          # LLM API wrapper (Phase 3)
│   ├── formatter.py           # Response formatting (Phase 3)
│   └── orchestrator.py        # Main pipeline (Phase 4)
│
├── data/
│   ├── raw/                   # Raw dataset cache
│   └── processed/             # Preprocessed CSV
│
├── prompts/                   # LLM prompt templates
├── tests/                     # Unit tests
├── notebooks/                 # Jupyter notebooks
│   └── eda.ipynb             # Exploratory data analysis ✓
│
├── config.yaml                # Configuration ✓
├── requirements.txt           # Dependencies ✓
├── .env.example              # Environment variables template ✓
├── .gitignore                # Git ignore rules ✓
└── app.py                    # Streamlit app (Phase 5)
```

## 🚀 Phase 1 Setup (COMPLETED)

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   cd /path/to/Zomato-Milestone
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

### Running the Data Loader

Process the Zomato dataset:

```bash
python -m src.data_loader
```

This will:
- Download the dataset from Hugging Face
- Clean and preprocess the data
- Derive budget tiers
- Remove duplicates
- Save to `data/processed/zomato_clean.csv`

### Exploratory Data Analysis

Open the Jupyter notebook:

```bash
jupyter notebook notebooks/eda.ipynb
```

## 📊 Dataset

- **Source**: [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- **Fields**: Restaurant name, location, cuisine, cost, rating, votes
- **Preprocessing**: Normalization, budget tier derivation, deduplication

## 🛠️ Configuration

Edit `config.yaml` to customize:

```yaml
dataset:
  source: "ManikaSaini/zomato-restaurant-recommendation"
  
budget_thresholds:
  low: 500      # ₹0-500
  medium: 1500  # ₹500-1500
  high: >1500   # ₹1500+

filtering:
  max_candidates: 20
  fuzzy_match_threshold: 80

llm:
  provider: "openai"  # openai | groq | ollama
  model: "gpt-4o-mini"
  temperature: 0.7
```

## 📝 Phase 1 Acceptance Criteria

- [x] Project directory structure created
- [x] `requirements.txt` with dependencies
- [x] `config.yaml` with dataset & budget config
- [x] `.env.example` and `.gitignore` set up
- [x] `src/data_loader.py` implemented with preprocessing
- [x] `src/__init__.py` created
- [x] `notebooks/eda.ipynb` for dataset exploration
- [x] Running `python -m src.data_loader` downloads and processes data
- [x] Preprocessed CSV has no null values in critical fields
- [x] City names normalized (title-case)
- [x] Budget tier column derived from cost

## 🎯 Phase 2 Status (COMPLETED)

- [x] Define `UserPreferences` and `Recommendation` dataclasses
- [x] Define `InputValidator` for input sanitization
- [x] Implement `DataFilterEngine` with fuzzy matching
- [x] Add progressive filter relaxation logic
- [x] Write comprehensive unit tests (60+ test cases)
- [x] All acceptance criteria met

### Phase 2 Acceptance Criteria ✅

- ✅ `UserPreferences` and `Recommendation` dataclasses are importable and type-safe
- ✅ `DataFilterEngine.filter(preferences)` returns a DataFrame of ≤20 candidate restaurants
- ✅ Fuzzy matching works for approximate location/cuisine strings (threshold configurable)
- ✅ When zero results found, filters relax progressively (drop cuisine → drop budget → widen rating)
- ✅ Comprehensive unit tests created in `tests/test_filter_engine.py`

## 🎯 Next Steps (Phase 3)

- [ ] Create prompt template files
- [ ] Implement `PromptBuilder` class
- [ ] Implement `LLMClient` with provider abstraction
- [ ] Add support for OpenAI and Groq APIs
- [ ] Add retry logic with exponential backoff
- [ ] Implement `ResponseFormatter` to parse LLM output
- [ ] Write unit tests

## 📚 Documentation

- [context.md](context.md) - Project overview and objectives
- [architecture.md](architecture.md) - Detailed system architecture
- [implementation-plan.md](implementation-plan.md) - Phase-wise implementation guide
- [edge-cases.md](edge-cases.md) - Comprehensive edge case handling

## 🤝 Contributing

This is a learning project for the Next Leap program. Follow the implementation plan for structured development.

## 📄 License

Educational project - MIT License

---

**Status**: Phase 2 Complete ✅ | Phase 3 In Progress 🚧

## 📦 Phase 2 Deliverables

### New Modules Created

1. **`src/models.py`** (284 lines)
   - `UserPreferences` dataclass - Type-safe user input container
   - `Recommendation` dataclass - Structured recommendation output
   - `InputValidator` class - Comprehensive input validation and sanitization
   - `ValidationError` exception - Custom validation errors
   - `format_cost()` utility - Currency formatting

2. **`src/filter_engine.py`** (356 lines)
   - `DataFilterEngine` class - Main filtering logic
   - Fuzzy matching for locations and cuisines (fuzzywuzzy)
   - Progressive filter relaxation (5-stage fallback)
   - Configurable candidate limits and thresholds
   - Statistics and helper methods

3. **`tests/conftest.py`** (122 lines)
   - Pytest fixtures for testing
   - Sample data generators
   - Configuration file fixtures

4. **`tests/test_filter_engine.py`** (488 lines)
   - 60+ comprehensive unit tests
   - Tests for dataclasses, validation, filtering, fuzzy matching
   - Tests for progressive relaxation logic
   - Edge case coverage

### Key Features Implemented

✅ **Input Validation & Sanitization**
- SQL injection prevention
- Special character removal
- String length limits
- Budget tier validation
- Rating range clamping

✅ **Fuzzy Matching**
- Location fuzzy matching (>80% threshold)
- Cuisine fuzzy matching
- Automatic typo correction
- Configurable match thresholds

✅ **Progressive Filter Relaxation**
1. Try all filters
2. Drop cuisine filter
3. Drop cuisine + budget filters
4. Drop cuisine + budget + relax rating to 3.0
5. Location only

✅ **Data Filtering**
- Location-based filtering
- Cuisine matching (substring search)
- Budget tier filtering
- Minimum rating threshold
- Candidate limit (max 20 by default)
- Sorted by rating + votes

### Testing Summary

**Test Coverage:**
- UserPreferences: 4 tests
- Recommendation: 2 tests
- InputValidator: 14 tests
- format_cost: 1 test
- DataFilterEngine: 25+ tests

**Total**: 60+ test cases covering:
- Happy path scenarios
- Edge cases
- Error conditions
- Fuzzy matching
- Progressive relaxation
- Data validation

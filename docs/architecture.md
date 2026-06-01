# Architecture: AI-Powered Restaurant Recommendation System

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT / UI LAYER                            │
│  (Streamlit / Gradio / CLI)                                         │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │ Preference   │  │ Results Display  │  │ Conversation /       │  │
│  │ Input Form   │  │ (Cards / Table)  │  │ Follow-up Panel      │  │
│  └──────┬───────┘  └────────▲─────────┘  └──────────▲───────────┘  │
└─────────┼───────────────────┼────────────────────────┼──────────────┘
          │                   │                        │
          ▼                   │                        │
┌─────────────────────────────┼────────────────────────┼──────────────┐
│                    APPLICATION LAYER                                 │
│                                                                     │
│  ┌──────────────┐  ┌───────┴────────┐  ┌────────────┴───────────┐  │
│  │ Input        │  │ Recommendation │  │ Response Formatter     │  │
│  │ Validator    │──▶ Orchestrator   │──▶ & Renderer             │  │
│  └──────────────┘  └───────┬────────┘  └────────────────────────┘  │
│                            │                                        │
│           ┌────────────────┼────────────────┐                       │
│           ▼                ▼                ▼                       │
│  ┌────────────────┐ ┌─────────────┐ ┌──────────────┐              │
│  │ Data Filter    │ │ Prompt      │ │ LLM Client   │              │
│  │ Engine         │ │ Builder     │ │ (API Wrapper) │              │
│  └───────┬────────┘ └──────┬──────┘ └──────┬───────┘              │
└──────────┼─────────────────┼───────────────┼────────────────────────┘
           │                 │               │
           ▼                 │               ▼
┌─────────────────────┐      │     ┌─────────────────────┐
│   DATA LAYER        │      │     │   EXTERNAL SERVICES  │
│                     │      │     │                     │
│ ┌─────────────────┐ │      │     │ ┌─────────────────┐ │
│ │ Zomato Dataset  │ │      │     │ │ LLM Provider    │ │
│ │ (HuggingFace)   │ │      │     │ │ (OpenAI / Groq  │ │
│ │                 │ │      │     │ │  / Ollama)       │ │
│ └─────────────────┘ │      │     │ └─────────────────┘ │
│ ┌─────────────────┐ │      │     └─────────────────────┘
│ │ Preprocessed    │ │      │
│ │ Cache (CSV/DB)  │ │      │
│ └─────────────────┘ │      │
└─────────────────────┘      │
                             │
              Prompt Template│Store
              ┌──────────────┴──────────────┐
              │  prompts/                    │
              │  ├── system_prompt.txt       │
              │  ├── recommendation.txt      │
              │  └── summary.txt             │
              └─────────────────────────────┘
```

---

## 2. Component Breakdown

### 2.1 Client / UI Layer

| Component              | Responsibility                                                                 | Technology Options              |
| ---------------------- | ------------------------------------------------------------------------------ | ------------------------------- |
| **Preference Input**   | Collect location, budget, cuisine, min-rating, and additional prefs from user  | Streamlit widgets / Gradio / CLI |
| **Results Display**    | Render ranked restaurant cards with name, cuisine, rating, cost, explanation   | Streamlit columns / HTML cards  |
| **Follow-up Panel**    | Allow users to refine or ask follow-up questions about recommendations         | Chat input widget               |

### 2.2 Application Layer

#### 2.2.1 Input Validator

- Sanitizes and normalizes user inputs (e.g., title-case city names, map budget labels to numeric ranges)
- Validates that required fields are present
- Returns a structured `UserPreferences` object

```python
@dataclass
class UserPreferences:
    location: str
    budget: str            # "low" | "medium" | "high"
    cuisine: str
    min_rating: float
    additional_prefs: list[str]
```

#### 2.2.2 Data Filter Engine

- Accepts a `UserPreferences` object
- Queries the preprocessed dataset using Pandas filters
- Returns a shortlist of candidate restaurants (DataFrame or list of dicts)

```
Filter Pipeline:
  location match (exact / fuzzy)
  → cuisine match (contains / fuzzy)
  → budget range filter
  → min_rating threshold
  → limit to top N candidates (e.g., 20)
```

#### 2.2.3 Prompt Builder

- Takes filtered restaurant data + user preferences
- Constructs a structured prompt for the LLM using a template
- Injects restaurant details as structured text (or JSON) within the prompt

**Prompt Template Example:**

```
You are a restaurant recommendation assistant.

The user is looking for restaurants with these preferences:
- Location: {location}
- Budget: {budget}
- Cuisine: {cuisine}
- Minimum Rating: {min_rating}
- Additional Preferences: {additional_prefs}

Here are the matching restaurants:
{restaurant_data_table}

Please rank the top 5 restaurants and for each provide:
1. Restaurant Name
2. Why it's a good match
3. A short summary of the dining experience
```

#### 2.2.4 LLM Client (API Wrapper)

- Abstracts communication with the LLM provider
- Handles API key management, retries, rate-limiting, and error handling
- Supports swappable backends (OpenAI, Groq, Ollama, etc.)

```python
class LLMClient:
    def __init__(self, provider: str, model: str, api_key: str): ...
    def generate(self, prompt: str, temperature: float = 0.7) -> str: ...
```

#### 2.2.5 Recommendation Orchestrator

Central coordinator that ties all components together:

```
1. Receive validated UserPreferences
2. Call DataFilterEngine → get candidate restaurants
3. Call PromptBuilder → construct LLM prompt
4. Call LLMClient → get ranked recommendations
5. Call ResponseFormatter → parse and structure output
6. Return final results to UI
```

#### 2.2.6 Response Formatter & Renderer

- Parses the raw LLM text output into structured recommendation objects
- Handles edge cases (malformed LLM output, empty results)
- Formats output for the UI layer

```python
@dataclass
class Recommendation:
    rank: int
    restaurant_name: str
    cuisine: str
    rating: float
    estimated_cost: str
    explanation: str
```

---

## 3. Data Layer

### 3.1 Dataset Source

- **Source:** [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) on Hugging Face
- **Format:** CSV / Parquet via `datasets` library

### 3.2 Schema (Expected Fields)

| Field               | Type    | Description                           |
| ------------------- | ------- | ------------------------------------- |
| `name`              | string  | Restaurant name                       |
| `location`          | string  | City or locality                      |
| `cuisines`          | string  | Comma-separated cuisine types         |
| `average_cost`      | int     | Average cost for two                  |
| `aggregate_rating`  | float   | Overall rating (0–5)                  |
| `votes`             | int     | Number of user votes                  |
| `has_online_delivery`| bool   | Online delivery availability          |
| `has_table_booking` | bool    | Table booking availability            |

### 3.3 Data Preprocessing Pipeline

```
Raw HuggingFace Dataset
  │
  ▼
Load via `datasets` library or pandas
  │
  ▼
Clean & Normalize
  ├── Drop rows with missing name/location/rating
  ├── Normalize city names (strip whitespace, title case)
  ├── Split cuisines string → list
  ├── Map cost → budget tier (low/medium/high)
  └── Cast types (rating → float, cost → int)
  │
  ▼
Cache preprocessed data (CSV / SQLite / Pickle)
  │
  ▼
Ready for querying by DataFilterEngine
```

### 3.4 Budget Mapping Strategy

| Tier     | Cost Range (for two) | Logic                                    |
| -------- | -------------------- | ---------------------------------------- |
| Low      | ₹0 – ₹500           | `average_cost <= 500`                    |
| Medium   | ₹500 – ₹1500        | `500 < average_cost <= 1500`             |
| High     | ₹1500+               | `average_cost > 1500`                    |

> Thresholds are configurable via `config.yaml`.

---

## 4. Directory Structure

```
zomato-recommendation/
│
├── app.py                      # Entry point (Streamlit / Gradio app)
├── config.yaml                 # Configuration (API keys, thresholds, model params)
├── requirements.txt            # Python dependencies
├── README.md
│
├── data/
│   ├── raw/                    # Raw dataset download cache
│   └── processed/              # Cleaned & preprocessed dataset
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Dataset loading & preprocessing
│   ├── filter_engine.py        # Structured filtering on restaurant data
│   ├── prompt_builder.py       # LLM prompt construction from templates
│   ├── llm_client.py           # LLM API wrapper (OpenAI / Groq / Ollama)
│   ├── orchestrator.py         # Recommendation orchestration pipeline
│   ├── formatter.py            # Parse & format LLM output
│   └── models.py               # Data classes (UserPreferences, Recommendation)
│
├── prompts/
│   ├── system_prompt.txt       # System-level instructions for the LLM
│   ├── recommendation.txt      # Main recommendation prompt template
│   └── summary.txt             # Optional summary prompt template
│
├── tests/
│   ├── test_data_loader.py
│   ├── test_filter_engine.py
│   ├── test_prompt_builder.py
│   └── test_orchestrator.py
│
└── notebooks/
    └── eda.ipynb               # Exploratory data analysis on Zomato dataset
```

---

## 5. Data Flow Diagram

```
┌──────────┐    preferences    ┌──────────────┐
│  User    │──────────────────▶│  Input       │
│          │                   │  Validator   │
└──────────┘                   └──────┬───────┘
                                      │
                              UserPreferences
                                      │
                                      ▼
                               ┌──────────────┐     ┌──────────────────┐
                               │  Data Filter │────▶│  Zomato Dataset  │
                               │  Engine      │◀────│  (preprocessed)  │
                               └──────┬───────┘     └──────────────────┘
                                      │
                            filtered restaurants
                                      │
                                      ▼
                               ┌──────────────┐     ┌──────────────────┐
                               │  Prompt      │────▶│  Prompt          │
                               │  Builder     │◀────│  Templates       │
                               └──────┬───────┘     └──────────────────┘
                                      │
                                constructed prompt
                                      │
                                      ▼
                               ┌──────────────┐     ┌──────────────────┐
                               │  LLM Client  │────▶│  LLM Provider    │
                               │              │◀────│  (OpenAI / Groq) │
                               └──────┬───────┘     └──────────────────┘
                                      │
                               raw LLM response
                                      │
                                      ▼
                               ┌──────────────┐
                               │  Response    │
                               │  Formatter   │
                               └──────┬───────┘
                                      │
                          List[Recommendation]
                                      │
                                      ▼
                               ┌──────────────┐
                               │  UI / Display│──────▶  User sees ranked
                               │  Layer       │        recommendations
                               └──────────────┘
```

---

## 6. Technology Stack

| Layer             | Technology                                      | Rationale                                              |
| ----------------- | ----------------------------------------------- | ------------------------------------------------------ |
| **Language**      | Python 3.10+                                    | Rich ecosystem for data + AI                           |
| **UI Framework**  | Streamlit (primary) / Gradio (alternative)      | Rapid prototyping, built-in widgets                    |
| **Data Handling** | Pandas, HuggingFace `datasets`                  | Efficient tabular data manipulation                    |
| **LLM Provider**  | OpenAI API / Groq API / Ollama (local)          | Flexibility to swap models                             |
| **LLM Library**   | `openai` SDK / `langchain` (optional)           | Simplified API interaction                             |
| **Config**        | `pyyaml` / `python-dotenv`                      | Externalized config & secrets                          |
| **Testing**       | `pytest`                                        | Standard Python testing                                |
| **Caching**       | CSV / SQLite / `@st.cache_data`                 | Avoid re-downloading and re-processing on every run    |

---

## 7. Configuration Management

```yaml
# config.yaml

dataset:
  source: "ManikaSaini/zomato-restaurant-recommendation"
  cache_dir: "data/raw"
  processed_path: "data/processed/zomato_clean.csv"

budget_thresholds:
  low: 500
  medium: 1500

filtering:
  max_candidates: 20
  fuzzy_match_threshold: 80   # fuzzywuzzy score

llm:
  provider: "openai"          # openai | groq | ollama
  model: "gpt-4o-mini"
  temperature: 0.7
  max_tokens: 1024
  api_key_env: "OPENAI_API_KEY"

ui:
  top_n_results: 5
  title: "Zomato AI Restaurant Recommender"
```

---

## 8. API Contract (Internal)

### Orchestrator Interface

```python
class RecommendationOrchestrator:
    def __init__(self, config: dict): ...

    def recommend(self, preferences: UserPreferences) -> list[Recommendation]:
        """
        End-to-end pipeline:
        validate → filter → build prompt → call LLM → format → return
        """
        ...
```

### Key Data Contracts

```python
# Input
UserPreferences(
    location="Delhi",
    budget="medium",
    cuisine="Italian",
    min_rating=3.5,
    additional_prefs=["family-friendly"]
)

# Output
Recommendation(
    rank=1,
    restaurant_name="Olive Bar & Kitchen",
    cuisine="Italian, Mediterranean",
    rating=4.5,
    estimated_cost="₹1200 for two",
    explanation="Olive Bar & Kitchen is a top-rated Italian restaurant in Delhi..."
)
```

---

## 9. Error Handling Strategy

| Scenario                      | Handling                                                      |
| ----------------------------- | ------------------------------------------------------------- |
| Dataset unavailable           | Fallback to cached preprocessed file; show warning            |
| No restaurants match filters  | Relax filters progressively (drop cuisine → drop budget)      |
| LLM API failure               | Retry with exponential backoff (3 attempts); show fallback    |
| Malformed LLM response        | Return raw text with disclaimer; log for debugging            |
| Invalid user input            | Show validation error inline; do not proceed                  |
| Rate limiting                 | Queue requests; show "please wait" message                    |

---

## 10. Scalability & Future Enhancements

| Enhancement                     | Description                                                              |
| ------------------------------- | ------------------------------------------------------------------------ |
| **Vector Search (RAG)**         | Embed restaurant descriptions → semantic search before LLM call          |
| **User Profiles & History**     | Store past preferences/recommendations in a DB for personalization       |
| **Multi-turn Conversation**     | Let users refine recommendations via chat (LangChain memory)             |
| **Real-time Data**              | Integrate Zomato API for live ratings, menus, availability               |
| **Caching LLM Responses**      | Hash prompt → cache result to reduce API calls and latency               |
| **A/B Testing Prompts**         | Experiment with different prompt strategies to improve recommendation quality |
| **Deployment**                  | Containerize with Docker; deploy on Streamlit Cloud / AWS / GCP          |

---

## 11. Security Considerations

- **API Keys:** Never hardcode; use `.env` files and `python-dotenv`; add `.env` to `.gitignore`
- **User Input:** Sanitize all inputs before injecting into prompts (prompt injection prevention)
- **Data Privacy:** No PII in the Zomato dataset; if user accounts are added later, follow data protection regulations
- **Rate Limiting:** Implement client-side rate limiting to avoid excessive API spend

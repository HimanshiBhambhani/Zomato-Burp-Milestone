# Phase-Wise Implementation Plan

## AI-Powered Restaurant Recommendation System (Zomato Use Case)

> Derived from [context.md](context.md) and [architecture.md](architecture.md)

---

## Timeline Overview

| Phase | Name                              | Duration  | Key Deliverable                                   |
| ----- | --------------------------------- | --------- | ------------------------------------------------- |
| 1     | Project Setup & Data Ingestion    | 2–3 days  | Clean, cached dataset ready for querying           |
| 2     | Core Data Models & Filter Engine  | 2–3 days  | Structured filtering on restaurant data            |
| 3     | LLM Integration & Prompt Engine   | 3–4 days  | Working LLM-powered recommendation pipeline        |
| 4     | Orchestrator & End-to-End Pipeline| 2–3 days  | Full backend pipeline wired together               |
| 5     | UI Layer (Streamlit)              | 2–3 days  | Interactive frontend with input form & results     |
| 6     | Testing, Error Handling & Polish  | 2–3 days  | Robust, production-quality application             |
| 7     | Documentation & Deployment        | 1–2 days  | Deployed app with README and demo                  |

**Total estimated duration: ~14–21 days**

---

## Phase 1 — Project Setup & Data Ingestion

### Goal
Set up the repository structure, install dependencies, load the Zomato dataset from Hugging Face, and produce a clean preprocessed file.

### Tasks

| #   | Task                                                   | File(s) Involved                          |
| --- | ------------------------------------------------------ | ----------------------------------------- |
| 1.1 | Initialize project directory structure                 | All directories per architecture          |
| 1.2 | Create `requirements.txt` with initial dependencies    | `requirements.txt`                        |
| 1.3 | Create `config.yaml` with dataset & budget config      | `config.yaml`                             |
| 1.4 | Set up `.env` and `.gitignore` for secrets             | `.env`, `.gitignore`                      |
| 1.5 | Implement `data_loader.py` — download dataset          | `src/data_loader.py`                      |
| 1.6 | Implement preprocessing pipeline in `data_loader.py`   | `src/data_loader.py`                      |
| 1.7 | Create EDA notebook for dataset exploration            | `notebooks/eda.ipynb`                     |
| 1.8 | Validate & cache preprocessed data                     | `data/processed/zomato_clean.csv`         |

### Acceptance Criteria

- [ ] Running `python -m src.data_loader` downloads, cleans, and saves `data/processed/zomato_clean.csv`
- [ ] Preprocessed CSV has no null values in `name`, `location`, `aggregate_rating`
- [ ] City names are normalized (title-case, stripped)
- [ ] Budget tier column (`budget`) is derived from `average_cost`
- [ ] EDA notebook shows dataset shape, distributions, and sample rows

### Dependencies & Tools

```
pandas, datasets (huggingface), pyyaml, python-dotenv
```

---

## Phase 2 — Core Data Models & Filter Engine

### Goal
Define typed data classes and build the filtering logic that narrows restaurants based on user preferences.

### Tasks

| #   | Task                                                   | File(s) Involved                          |
| --- | ------------------------------------------------------ | ----------------------------------------- |
| 2.1 | Define `UserPreferences` dataclass                     | `src/models.py`                           |
| 2.2 | Define `Recommendation` dataclass                      | `src/models.py`                           |
| 2.3 | Implement `InputValidator` (sanitize, normalize)       | `src/models.py` or `src/filter_engine.py` |
| 2.4 | Implement `DataFilterEngine` class                     | `src/filter_engine.py`                    |
| 2.5 | Add fuzzy matching for location & cuisine              | `src/filter_engine.py`                    |
| 2.6 | Add progressive filter relaxation (fallback logic)     | `src/filter_engine.py`                    |
| 2.7 | Write unit tests for filter engine                     | `tests/test_filter_engine.py`             |

### Acceptance Criteria

- [ ] `UserPreferences` and `Recommendation` dataclasses are importable and type-safe
- [ ] `DataFilterEngine.filter(preferences)` returns a DataFrame of ≤20 candidate restaurants
- [ ] Fuzzy matching works for approximate location/cuisine strings (threshold configurable)
- [ ] When zero results found, filters relax progressively (drop cuisine → drop budget → widen rating)
- [ ] All unit tests pass via `pytest tests/test_filter_engine.py`

### Key Design Decisions

```python
# src/models.py
@dataclass
class UserPreferences:
    location: str
    budget: str            # "low" | "medium" | "high"
    cuisine: str
    min_rating: float
    additional_prefs: list[str]

# Filter pipeline (filter_engine.py):
#   location match → cuisine match → budget range → rating ≥ threshold → top N
```

---

## Phase 3 — LLM Integration & Prompt Engine

### Goal
Build the LLM client abstraction and the prompt construction module that converts filtered data + preferences into an effective LLM prompt.

### Tasks

| #   | Task                                                   | File(s) Involved                          |
| --- | ------------------------------------------------------ | ----------------------------------------- |
| 3.1 | Create prompt template files                           | `prompts/system_prompt.txt`               |
|     |                                                        | `prompts/recommendation.txt`              |
|     |                                                        | `prompts/summary.txt`                     |
| 3.2 | Implement `PromptBuilder` class                        | `src/prompt_builder.py`                   |
| 3.3 | Implement `LLMClient` class with provider abstraction  | `src/llm_client.py`                       |
| 3.4 | Add support for OpenAI API                             | `src/llm_client.py`                       |
| 3.5 | Add support for Groq API (alternative)                 | `src/llm_client.py`                       |
| 3.6 | Add retry logic with exponential backoff               | `src/llm_client.py`                       |
| 3.7 | Implement `ResponseFormatter` (parse LLM output)       | `src/formatter.py`                        |
| 3.8 | Write unit tests for prompt builder & formatter        | `tests/test_prompt_builder.py`            |

### Acceptance Criteria

- [ ] `PromptBuilder.build(preferences, restaurants_df)` returns a well-formed prompt string
- [ ] Prompt includes system instructions, user preferences, and tabular restaurant data
- [ ] `LLMClient.generate(prompt)` returns a string response from the configured provider
- [ ] API key is read from environment variable (never hardcoded)
- [ ] Retry logic handles transient failures (3 attempts, exponential backoff)
- [ ] `ResponseFormatter.parse(llm_response)` returns `list[Recommendation]`
- [ ] Malformed LLM output returns graceful fallback (raw text + disclaimer)

### Prompt Template Design

```
# prompts/system_prompt.txt
You are an expert restaurant recommendation assistant for Indian cities.
You provide concise, helpful recommendations with clear reasoning.

# prompts/recommendation.txt
The user is looking for restaurants with these preferences:
- Location: {location}
- Budget: {budget}
- Cuisine: {cuisine}
- Minimum Rating: {min_rating}
- Additional Preferences: {additional_prefs}

Here are the candidate restaurants:
{restaurant_data_table}

Rank the top {top_n} restaurants. For each, provide:
1. Restaurant Name
2. Cuisine
3. Rating
4. Estimated Cost for Two
5. Why this is a great match (2–3 sentences)
```

---

## Phase 4 — Orchestrator & End-to-End Pipeline

### Goal
Wire all components into the central `RecommendationOrchestrator` that executes the full pipeline: validate → filter → prompt → LLM → format → return.

### Tasks

| #   | Task                                                   | File(s) Involved                          |
| --- | ------------------------------------------------------ | ----------------------------------------- |
| 4.1 | Implement `RecommendationOrchestrator` class           | `src/orchestrator.py`                     |
| 4.2 | Load config from `config.yaml` at initialization       | `src/orchestrator.py`                     |
| 4.3 | Wire: Validator → FilterEngine → PromptBuilder → LLM → Formatter | `src/orchestrator.py`        |
| 4.4 | Add logging throughout the pipeline                    | `src/orchestrator.py`                     |
| 4.5 | Create a CLI test script for pipeline validation       | `test_pipeline.py` (root)                 |
| 4.6 | Write integration tests for orchestrator               | `tests/test_orchestrator.py`              |

### Acceptance Criteria

- [ ] `orchestrator.recommend(preferences)` returns `list[Recommendation]` end-to-end
- [ ] Pipeline runs in <10 seconds for a typical request (excluding LLM latency)
- [ ] CLI script demonstrates: input → filtered data → LLM call → formatted output
- [ ] Logging shows each pipeline step with timing
- [ ] Integration tests cover happy path and edge cases (no results, LLM failure)

### Orchestrator Flow

```
RecommendationOrchestrator.recommend(preferences):
│
├── 1. InputValidator.validate(preferences) → UserPreferences
│
├── 2. DataFilterEngine.filter(preferences) → DataFrame (≤20 rows)
│       └── if empty → relax filters & retry
│
├── 3. PromptBuilder.build(preferences, filtered_df) → prompt string
│
├── 4. LLMClient.generate(prompt) → raw LLM text
│       └── if fails → retry (3x) → fallback message
│
├── 5. ResponseFormatter.parse(raw_text) → list[Recommendation]
│
└── 6. Return list[Recommendation]
```

---

## Phase 5 — UI Layer (Streamlit)

### Goal
Build an interactive Streamlit frontend where users enter preferences and see AI-generated recommendations.

### Tasks

| #   | Task                                                   | File(s) Involved                          |
| --- | ------------------------------------------------------ | ----------------------------------------- |
| 5.1 | Create `app.py` Streamlit entry point                  | `app.py`                                  |
| 5.2 | Build sidebar with preference input widgets            | `app.py`                                  |
| 5.3 | Add "Get Recommendations" button + loading spinner     | `app.py`                                  |
| 5.4 | Render recommendation cards (name, cuisine, rating, cost, explanation) | `app.py`              |
| 5.5 | Add `@st.cache_data` for dataset loading               | `app.py`                                  |
| 5.6 | Add error/warning banners for edge cases               | `app.py`                                  |
| 5.7 | Style and polish the UI layout                         | `app.py`                                  |

### Acceptance Criteria

- [ ] `streamlit run app.py` launches the application
- [ ] Sidebar contains: Location dropdown, Budget selector, Cuisine input, Rating slider, Additional prefs text
- [ ] Clicking "Get Recommendations" shows a spinner, then displays top-5 cards
- [ ] Each card shows: Restaurant Name, Cuisine, Rating (stars), Cost, AI explanation
- [ ] Empty results show a friendly "No restaurants found" message with suggestions
- [ ] Dataset is cached after first load (no re-download on rerun)

### UI Wireframe

```
┌────────────────────────────────────────────────────────────┐
│  🍽️ Zomato AI Restaurant Recommender                      │
├──────────────┬─────────────────────────────────────────────┤
│  SIDEBAR     │  MAIN AREA                                  │
│              │                                              │
│ Location:    │  ┌─────────────────────────────────────────┐│
│ [Delhi    ▼] │  │ 🥇 Olive Bar & Kitchen                 ││
│              │  │ Italian, Mediterranean | ⭐ 4.5         ││
│ Budget:      │  │ ₹1200 for two                          ││
│ ○Low ●Med ○Hi│  │ "Great match because..."               ││
│              │  └─────────────────────────────────────────┘│
│ Cuisine:     │  ┌─────────────────────────────────────────┐│
│ [Italian   ] │  │ 🥈 Tonino                              ││
│              │  │ Italian | ⭐ 4.3                        ││
│ Min Rating:  │  │ ₹900 for two                           ││
│ [===●===] 3.5│  │ "Excellent choice for..."              ││
│              │  └─────────────────────────────────────────┘│
│ Additional:  │                                              │
│ [family...  ]│  ...more cards...                           │
│              │                                              │
│ [🔍 Get     ]│                                              │
│ [Recommend- ]│                                              │
│ [ations     ]│                                              │
└──────────────┴─────────────────────────────────────────────┘
```

---

## Phase 6 — Testing, Error Handling & Polish

### Goal
Harden the application with comprehensive tests, robust error handling, and production-quality polish.

### Tasks

| #   | Task                                                   | File(s) Involved                          |
| --- | ------------------------------------------------------ | ----------------------------------------- |
| 6.1 | Write unit tests for `data_loader.py`                  | `tests/test_data_loader.py`               |
| 6.2 | Write unit tests for `prompt_builder.py`               | `tests/test_prompt_builder.py`            |
| 6.3 | Write integration tests for full pipeline              | `tests/test_orchestrator.py`              |
| 6.4 | Implement all error handling per architecture §9       | All `src/` modules                        |
| 6.5 | Add input sanitization (prompt injection prevention)   | `src/models.py`, `src/prompt_builder.py`  |
| 6.6 | Add client-side rate limiting                          | `src/llm_client.py`                       |
| 6.7 | Test edge cases: empty results, API timeout, bad input | `tests/`                                  |
| 6.8 | Code review & refactor for quality                     | All files                                 |

### Acceptance Criteria

- [ ] `pytest` runs with ≥80% code coverage
- [ ] All error scenarios from architecture §9 are handled gracefully:

| Scenario                      | Expected Behavior                                |
| ----------------------------- | ------------------------------------------------ |
| Dataset unavailable           | Fallback to cache; show warning                  |
| No restaurants match filters  | Progressive filter relaxation                    |
| LLM API failure               | 3 retries with backoff; show fallback message    |
| Malformed LLM response        | Raw text + disclaimer                            |
| Invalid user input            | Inline validation error                          |
| Rate limiting                 | "Please wait" message                            |

- [ ] No hardcoded API keys anywhere in codebase
- [ ] User inputs are sanitized before prompt injection

### Test Strategy

```
tests/
├── test_data_loader.py       # Data download, cleaning, caching
├── test_filter_engine.py     # Filter logic, fuzzy match, relaxation
├── test_prompt_builder.py    # Template rendering, edge cases
├── test_orchestrator.py      # End-to-end with mocked LLM
└── conftest.py               # Shared fixtures (sample data, mock prefs)
```

---

## Phase 7 — Documentation & Deployment

### Goal
Write user-facing documentation, record a demo, and deploy the application.

### Tasks

| #   | Task                                                   | File(s) Involved                          |
| --- | ------------------------------------------------------ | ----------------------------------------- |
| 7.1 | Write `README.md` with setup & usage instructions      | `README.md`                               |
| 7.2 | Add inline docstrings to all public methods            | All `src/` modules                        |
| 7.3 | Create a demo screenshot or GIF                        | `docs/demo.gif`                           |
| 7.4 | Containerize with `Dockerfile` (optional)              | `Dockerfile`                              |
| 7.5 | Deploy to Streamlit Community Cloud                    | Streamlit Cloud config                    |
| 7.6 | Final end-to-end smoke test on deployed app            | —                                         |

### Acceptance Criteria

- [ ] `README.md` includes: project overview, setup steps, environment variable instructions, usage guide
- [ ] All public classes/methods have docstrings
- [ ] App is accessible via a public Streamlit Cloud URL (or Docker container runs locally)
- [ ] End-to-end smoke test passes on deployed version

### Deployment Options

| Platform              | Steps                                                          |
| --------------------- | -------------------------------------------------------------- |
| **Streamlit Cloud**   | Push to GitHub → Connect repo → Set secrets → Deploy           |
| **Docker (local)**    | `docker build -t zomato-rec .` → `docker run -p 8501:8501 …`  |
| **AWS / GCP**         | Containerize → Push to ECR/GCR → Deploy on ECS/Cloud Run      |

---

## Dependency Graph

```
Phase 1 ─── Project Setup & Data Ingestion
   │
   ▼
Phase 2 ─── Core Data Models & Filter Engine
   │
   ▼
Phase 3 ─── LLM Integration & Prompt Engine        (can start in parallel with Phase 2)
   │
   ▼
Phase 4 ─── Orchestrator & End-to-End Pipeline      (requires Phase 2 + Phase 3)
   │
   ▼
Phase 5 ─── UI Layer (Streamlit)                     (requires Phase 4)
   │
   ▼
Phase 6 ─── Testing, Error Handling & Polish         (runs alongside Phase 4–5)
   │
   ▼
Phase 7 ─── Documentation & Deployment               (requires all above)
```

> **Note:** Phases 2 and 3 can be worked on in parallel since they are independent modules. Phase 6 (testing) should begin alongside Phase 4 and continue through Phase 5.

---

## Risk Mitigation

| Risk                                  | Mitigation                                                         |
| ------------------------------------- | ------------------------------------------------------------------ |
| HuggingFace dataset schema changes    | Pin dataset version; validate schema on load                       |
| LLM API cost overruns during dev      | Use `gpt-4o-mini` or Groq free tier; cache responses               |
| LLM output format inconsistency      | Structured output parsing with fallback; consider JSON mode        |
| Fuzzy matching performance on large data | Pre-index unique locations/cuisines; cache fuzzy results         |
| Streamlit Cloud memory limits         | Preprocess data offline; load only processed CSV                   |

---

## Summary Checklist

- [ ] **Phase 1:** Dataset downloaded, cleaned, cached
- [ ] **Phase 2:** Data models defined, filter engine working with tests
- [ ] **Phase 3:** LLM client, prompt builder, response formatter working with tests
- [ ] **Phase 4:** Orchestrator wires everything; CLI demo works end-to-end
- [ ] **Phase 5:** Streamlit UI live with input form and recommendation cards
- [ ] **Phase 6:** ≥80% test coverage, all error scenarios handled
- [ ] **Phase 7:** README complete, app deployed, demo recorded

"""
FastAPI Backend Server for BURP Restaurant Recommendation Engine.

Provides REST API endpoints that the Next.js frontend calls:
- POST /api/recommend: Run the recommendation pipeline
- GET /api/health: Health check
"""

import os
import sys
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.orchestrator import RecommendationOrchestrator
from src.models import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="BURP API", version="1.0.0")

# CORS for local development and production
allowed_origins = [
    "http://localhost:3000",
]
# Add production frontend URL from env
frontend_url = os.getenv("FRONTEND_URL", "")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow all Vercel preview deploys
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the orchestrator on startup
orchestrator: Optional[RecommendationOrchestrator] = None


class RecommendRequest(BaseModel):
    location: str = Field(default="New Delhi", description="City or locality")
    budget: str = Field(default="medium", description="low, medium, or high")
    cuisine: str = Field(default="Italian", description="Cuisine type")
    rating: str = Field(default="4.0", description="Minimum rating")


class RecommendationResponse(BaseModel):
    name: str
    cuisine: str
    rating: float
    price_range: str
    ai_insight: str
    image_url: str = ""


class RecommendResponse(BaseModel):
    recommendations: List[RecommendationResponse]
    query: dict


# Load restaurant data for fast filtering
import pandas as pd
restaurant_df: Optional[pd.DataFrame] = None


def load_restaurant_data():
    global restaurant_df
    csv_path = os.path.join(os.path.dirname(__file__), "data", "processed", "zomato_clean.csv")
    if os.path.exists(csv_path):
        restaurant_df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(restaurant_df)} restaurants from CSV")
    else:
        logger.error(f"CSV not found at {csv_path}")


def filter_restaurants(location: str, budget: str, cuisine: str, min_rating: float) -> List[dict]:
    """Fast client-side filtering of restaurants without LLM."""
    if restaurant_df is None:
        return []

    df = restaurant_df.copy()

    # Filter by location (fuzzy)
    if location:
        location_lower = location.lower()
        df = df[df["location"].str.lower().str.contains(location_lower, na=False)]

    # Filter by budget
    budget_map = {"low": "low", "Low": "low", "mid": "medium", "Mid": "medium",
                  "medium": "medium", "high": "high", "High": "high"}
    mapped_budget = budget_map.get(budget, "")
    if mapped_budget:
        df = df[df["budget_category"].str.lower() == mapped_budget]

    # Filter by cuisine (fuzzy match)
    if cuisine:
        cuisine_lower = cuisine.lower()
        df = df[df["cuisines"].str.lower().str.contains(cuisine_lower, na=False)]

    # Filter by rating
    if min_rating > 0:
        df = df[df["aggregate_rating"] >= min_rating]

    # Sort by rating descending
    # Show more results when fewer filters are applied
    has_filters = bool(mapped_budget or cuisine or min_rating > 0)
    limit = 5 if has_filters else 10
    df = df.sort_values("aggregate_rating", ascending=False).head(limit)

    results = []
    for _, row in df.iterrows():
        results.append({
            "name": row["name"],
            "cuisine": row["cuisines"],
            "rating": float(row["aggregate_rating"]),
            "price_range": f"₹{int(row['average_cost_for_two'])} for two",
            "image_url": row.get("image_url", ""),
        })
    return results


orchestrator_error: Optional[str] = None

@app.on_event("startup")
async def startup():
    global orchestrator, orchestrator_error
    load_restaurant_data()
    try:
        orchestrator = RecommendationOrchestrator(config_path="config.yaml")
        orchestrator.initialize()
        logger.info("Orchestrator initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}")
        orchestrator_error = str(e)
        orchestrator = None


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "orchestrator_ready": orchestrator is not None,
        "orchestrator_error": orchestrator_error,
        "restaurants_loaded": restaurant_df is not None and len(restaurant_df) if restaurant_df is not None else 0
    }


@app.post("/api/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest):
    # Map budget values
    budget_map = {
        "low": "low", "Low": "low",
        "mid": "medium", "Mid": "medium", "medium": "medium",
        "high": "high", "High": "high",
    }
    budget = budget_map.get(request.budget, "medium")

    try:
        min_rating = float(request.rating) if request.rating else 4.0
    except ValueError:
        min_rating = 4.0

    # First try the full AI pipeline
    if orchestrator is not None and orchestrator.llm_client is not None:
        try:
            # Get filtered restaurants from our dataset (reliable source of truth)
            filtered = filter_restaurants(request.location, request.budget, request.cuisine, min_rating)
            
            if filtered:
                # Build a simple prompt asking LLM to generate insights for these restaurants
                restaurant_list = "\n".join([
                    f"- {r['name']} ({r['cuisine']}, rated {r['rating']}/5, {r['price_range']})"
                    for r in filtered
                ])
                insight_prompt = (
                    f"User wants: {request.cuisine} restaurants in {request.location}, "
                    f"budget: {request.budget}, minimum rating: {min_rating}/5.\n\n"
                    f"Here are the matching restaurants:\n{restaurant_list}\n\n"
                    f"For EACH restaurant, write ONE short sentence (max 20 words) explaining "
                    f"why it's a great pick for this user. Be specific about the food/vibe.\n"
                    f"Format: Restaurant Name: insight\n"
                    f"Do not add numbering or extra formatting."
                )
                
                llm_response = orchestrator.llm_client.generate(insight_prompt)
                
                # Parse LLM insights (simple "Name: insight" format)
                insight_map = {}
                for line in llm_response.strip().split("\n"):
                    if ":" in line:
                        parts = line.split(":", 1)
                        name_key = parts[0].strip().lower().strip("*- ")
                        insight_val = parts[1].strip()
                        if insight_val:
                            insight_map[name_key] = insight_val
                
                # Build recommendations with real AI insights
                recommendations = []
                for r in filtered:
                    # Match insight by name (try exact and fuzzy)
                    ai_insight = insight_map.get(r["name"].lower(), "")
                    if not ai_insight:
                        # Try partial match
                        for key, val in insight_map.items():
                            if r["name"].lower() in key or key in r["name"].lower():
                                ai_insight = val
                                break
                    if not ai_insight:
                        ai_insight = f"Highly rated {r['cuisine']} spot in {request.location}. A top pick for your preferences."
                    
                    recommendations.append(RecommendationResponse(
                        name=r["name"],
                        cuisine=r["cuisine"],
                        rating=r["rating"],
                        price_range=r["price_range"],
                        ai_insight=ai_insight,
                        image_url=r.get("image_url", ""),
                    ))

                return RecommendResponse(
                    recommendations=recommendations,
                    query={"location": request.location, "budget": request.budget,
                           "cuisine": request.cuisine, "rating": request.rating}
                )

        except Exception as e:
            logger.warning(f"AI pipeline failed, falling back to filter: {e}")

    # Fallback: use fast filtering
    filtered = filter_restaurants(request.location, request.budget, request.cuisine, min_rating)
    if not filtered:
        return RecommendResponse(recommendations=[], query={
            "location": request.location, "budget": request.budget,
            "cuisine": request.cuisine, "rating": request.rating})

    recommendations = []
    for r in filtered:
        recommendations.append(RecommendationResponse(
            name=r["name"],
            cuisine=r["cuisine"],
            rating=r["rating"],
            price_range=r["price_range"],
            ai_insight=f"Matches your {request.cuisine} preference in {request.location} within {request.budget} budget. Rated {r['rating']}/5 by diners.",
            image_url=r.get("image_url", ""),
        ))

    return RecommendResponse(
        recommendations=recommendations,
        query={"location": request.location, "budget": request.budget,
               "cuisine": request.cuisine, "rating": request.rating}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

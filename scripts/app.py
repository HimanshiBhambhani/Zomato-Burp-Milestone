"""
Zomato AI Restaurant Recommender - Streamlit App
Phase 5: Interactive UI Layer
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import logging
from typing import List, Optional

from src.orchestrator import RecommendationOrchestrator, OrchestratorError, DataNotLoadedError
from src.models import Recommendation, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration - Force sidebar visible
st.set_page_config(
    page_title="🍽️ Zomato AI Restaurant Recommender",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stitch Design System - Proper Color Implementation
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * { 
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }
    
    /* App Background - Stitch background color */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Force all text to use on-background color */
    .stApp {
        color: #191c1d;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #f8f9fa;
        padding-top: 2rem;
    }
    
    /* ============================================ */
    /* SIDEBAR - Stitch Design System */
    /* ============================================ */
    
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e1e3e4;
        padding: 1.5rem 1rem;
    }
    
    /* Sidebar Headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #191c1d;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Sidebar Labels */
    [data-testid="stSidebar"] label {
        color: #191c1d;
        font-weight: 600;
        font-size: 14px;
        line-height: 16px;
        letter-spacing: 0.05em;
    }
    
    /* All sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #191c1d;
    }
    
    /* Input fields */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] select {
        background-color: #f8f9fa;
        color: #191c1d;
        border: 1px solid #e4bebc;
        border-radius: 0.5rem;
        padding: 0.5rem;
        font-size: 16px;
    }
    
    /* Radio buttons */
    [data-testid="stSidebar"] [data-baseweb="radio"] {
        background-color: #f3f4f5;
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        color: #191c1d;
    }
    
    /* Primary Button in Sidebar */
    [data-testid="stSidebar"] button[kind="primary"] {
        background-color: #b7122a;
        color: #ffffff;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        width: 100%;
        height: 48px;
        font-size: 14px;
        letter-spacing: 0.05em;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] button[kind="primary"]:hover {
        background-color: #db313f;
        transform: scale(0.98);
    }
    
    /* All sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #b7122a;
        color: #ffffff;
        border-radius: 0.5rem;
        font-weight: 600;
        width: 100%;
        height: 48px;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #db313f;
    }
    
    /* ============================================ */
    /* MAIN CONTENT AREA */
    /* ============================================ */
    
    /* Page Title */
    h1 {
        color: #b7122a;
        font-size: 40px;
        font-weight: 700;
        line-height: 48px;
        letter-spacing: -0.02em;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle */
    .subtitle {
        color: #5b403f;
        font-size: 18px;
        font-weight: 400;
        line-height: 28px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Restaurant Cards - Surface color */
    /* Restaurant Cards - Surface color */
    .recommendation-card {
        background-color: #ffffff;
        border: 1px solid #e1e3e4;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .recommendation-card:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    /* Restaurant Name */
    .restaurant-name {
        color: #b7122a;
        font-size: 24px;
        font-weight: 600;
        line-height: 32px;
        margin-bottom: 0.5rem;
    }
    
    /* Medal Badge */
    .medal-badge {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    
    /* Rating Stars - Secondary color (gold) */
    .rating-stars {
        color: #feb700;
        font-size: 18px;
        font-weight: 400;
        margin: 0.5rem 0;
    }
    
    .rating-number {
        color: #191c1d;
        font-weight: 600;
    }
    
    /* Metadata (cuisine, location, cost) */
    .metadata-row {
        color: #5b403f;
        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
        margin: 0.5rem 0;
    }
    
    .metadata-item {
        color: #5b403f;
    }
    
    /* Cost Info */
    .cost-info {
        color: #191c1d;
        font-weight: 600;
        font-size: 16px;
    }
    
    /* Cuisine Badge */
    .cuisine-badge {
        background-color: #f3f4f5;
        color: #5b403f;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 14px;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    /* AI Explanation Box */
    .ai-explanation {
        background-color: #f8f9fa;
        border-left: 4px solid #b7122a;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
        color: #191c1d;
        font-size: 16px;
        line-height: 24px;
    }
    
    .ai-explanation-content {
        color: #191c1d;
    }
    
    /* Success/Info Messages */
    .stSuccess, .stInfo {
        background-color: #f3f4f5;
        color: #191c1d;
        border-radius: 0.5rem;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #b7122a;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #5b403f;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background-color: #ffffff;
        border: 2px dashed #e4bebc;
        border-radius: 1rem;
        margin: 2rem 0;
    }
    
    .empty-state-icon {
        font-size: 4rem;
    }
    
    .empty-state-title {
        color: #191c1d;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .empty-state-text {
        color: #5b403f;
        font-size: 16px;
        line-height: 24px;
    }
    
    /* Force visibility */
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: #191c1d;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_orchestrator():
    """Initialize and cache the orchestrator (runs once)."""
    try:
        orchestrator = RecommendationOrchestrator(config_path="config.yaml")
        orchestrator.initialize()
        return orchestrator, None
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}")
        return None, str(e)


@st.cache_data
def get_available_locations(_orchestrator):
    """Get list of available locations from the dataset."""
    try:
        if _orchestrator and _orchestrator.filter_engine:
            locations = _orchestrator.filter_engine.get_available_locations()
            return sorted(locations)
    except Exception as e:
        logger.warning(f"Could not get locations: {e}")
    return ["Delhi", "Mumbai", "Bangalore", "Pune", "Kolkata", "Chennai"]


@st.cache_data
def get_available_cuisines(_orchestrator):
    """Get list of popular cuisines from the dataset."""
    try:
        if _orchestrator and _orchestrator.filter_engine:
            cuisines = _orchestrator.filter_engine.get_available_cuisines()
            # Return top 20 most common cuisines
            return sorted(list(cuisines)[:20])
    except Exception as e:
        logger.warning(f"Could not get cuisines: {e}")
    return ["Italian", "Chinese", "North Indian", "South Indian", "Continental", "Thai", "Mexican"]


def render_stars(rating: float) -> str:
    """Render star rating as emoji."""
    full_stars = int(rating)
    half_star = 1 if (rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    return "⭐" * full_stars + ("½" if half_star else "") + "☆" * empty_stars


def render_recommendation_card(rec: Recommendation):
    """Render a single recommendation card with enhanced Stitch design."""
    
    # Medal emoji based on rank
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    medal = medals.get(rec.rank, f"#{rec.rank}")
    
    # Apply AI glow effect to top 3
    card_class = "recommendation-card ai-glow" if rec.rank <= 3 else "recommendation-card"
    
    # Format location and votes
    location_html = f'<span class="metadata-item">📍 {rec.location}</span>' if rec.location else ''
    votes_html = f'<span class="metadata-dot"></span><span class="metadata-item">👥 {rec.votes:,} votes</span>' if rec.votes else ''
    
    st.markdown(f"""
    <div class="{card_class}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span class="medal-badge">{medal}</span>
                <h3 class="restaurant-name">{rec.restaurant_name}</h3>
            </div>
        </div>
        
        <div class="rating-stars">
            <span>⭐</span> 
            <span class="rating-number">{rec.rating:.1f}/5.0</span>
        </div>
        
        <div class="metadata-row">
            <span class="cuisine-badge">🍴 {rec.cuisine}</span>
            <span class="metadata-dot"></span>
            <span class="cost-info">💰 {rec.estimated_cost}</span>
            {location_html}
            {votes_html}
        </div>
        
        <div class="ai-explanation">
            <div class="ai-explanation-content">
                {rec.explanation}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application logic."""
    
    # Header
    st.markdown('<div class="main-header">🍽️ Zomato AI Restaurant Recommender</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Discover perfect restaurants powered by AI ✨</div>', unsafe_allow_html=True)
    
    # Initialize orchestrator
    with st.spinner("🔄 Initializing recommendation engine..."):
        orchestrator, error = initialize_orchestrator()
    
    if error:
        st.error(f"""
        ❌ **Failed to initialize the recommendation system**
        
        **Error:** {error}
        
        **Possible solutions:**
        1. Make sure you've run: `python -m src.data_loader` to download data
        2. Check that `config.yaml` exists and is valid
        3. Ensure all dependencies are installed: `pip install -r requirements.txt`
        """)
        st.stop()
    
    if not orchestrator:
        st.error("❌ Orchestrator failed to initialize. Please check the logs.")
        st.stop()
    
    st.success("✅ Recommendation engine ready!")
    
    # Sidebar - Input Form
    with st.sidebar:
        st.header("🔍 Your Preferences")
        st.markdown("Tell us what you're looking for!")
        
        # Location
        available_locations = get_available_locations(orchestrator)
        location = st.selectbox(
            "📍 Location",
            options=available_locations,
            help="Select the city or area where you want to dine"
        )
        
        # Budget
        budget = st.radio(
            "💰 Budget",
            options=["low", "medium", "high"],
            index=1,
            format_func=lambda x: {
                "low": "💵 Low (₹0-500)",
                "medium": "💰 Medium (₹500-1500)",
                "high": "💎 High (₹1500+)"
            }[x],
            help="Select your budget range for two people"
        )
        
        # Cuisine
        available_cuisines = get_available_cuisines(orchestrator)
        cuisine = st.selectbox(
            "🍴 Cuisine",
            options=available_cuisines,
            help="What type of food are you craving?"
        )
        
        # Rating
        min_rating = st.slider(
            "⭐ Minimum Rating",
            min_value=0.0,
            max_value=5.0,
            value=3.5,
            step=0.5,
            help="Minimum acceptable rating (0-5)"
        )
        
        # Additional preferences
        additional_prefs_input = st.text_area(
            "✨ Additional Preferences (Optional)",
            placeholder="e.g., family-friendly, romantic, outdoor seating, live music",
            help="Enter comma-separated preferences",
            height=100
        )
        
        # Parse additional preferences
        additional_prefs = [
            pref.strip() 
            for pref in additional_prefs_input.split(",") 
            if pref.strip()
        ] if additional_prefs_input else []
        
        # Number of recommendations
        top_n = st.slider(
            "📊 Number of Recommendations",
            min_value=3,
            max_value=10,
            value=5,
            help="How many restaurant suggestions do you want?"
        )
        
        st.markdown("---")
        
        # Get Recommendations Button
        get_recommendations = st.button(
            "🔍 Get Recommendations",
            type="primary",
            use_container_width=True
        )
    
    # Main Area - Results
    if get_recommendations:
        st.markdown("---")
        st.header("🎯 Your Personalized Recommendations")
        
        # Show selected preferences
        with st.expander("📋 Your Search Criteria", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**📍 Location:** {location}")
                st.write(f"**💰 Budget:** {budget.title()}")
            with col2:
                st.write(f"**🍴 Cuisine:** {cuisine}")
                st.write(f"**⭐ Min Rating:** {min_rating}")
            with col3:
                if additional_prefs:
                    st.write(f"**✨ Additional:**")
                    for pref in additional_prefs:
                        st.write(f"  • {pref}")
        
        # Get recommendations
        with st.spinner("🤖 AI is analyzing restaurants and crafting recommendations..."):
            try:
                recommendations = orchestrator.recommend(
                    location=location,
                    budget=budget,
                    cuisine=cuisine,
                    min_rating=min_rating,
                    additional_prefs=additional_prefs,
                    top_n=top_n
                )
                
                if recommendations:
                    st.success(f"✨ Found {len(recommendations)} amazing restaurants for you!")
                    st.markdown("---")
                    
                    # Render each recommendation
                    for rec in recommendations:
                        render_recommendation_card(rec)
                    
                    # Footer with tips
                    st.markdown("---")
                    st.info("""
                    💡 **Tips:**
                    - Adjust your preferences in the sidebar to discover more options
                    - Try different cuisines or locations
                    - Lower the minimum rating to see more choices
                    - Add specific preferences to get more personalized results
                    """)
                    
                else:
                    st.warning("🔍 No restaurants found matching your criteria.")
                    st.markdown("""
                    ### Suggestions:
                    - Try a different cuisine type
                    - Adjust your budget range
                    - Lower the minimum rating requirement
                    - Select a different location
                    - Remove some additional preferences
                    """)
                
            except ValidationError as e:
                st.error(f"""
                ❌ **Invalid Input**
                
                {str(e)}
                
                Please check your preferences and try again.
                """)
            
            except DataNotLoadedError as e:
                st.error(f"""
                ❌ **Data Not Available**
                
                {str(e)}
                
                Please run `python -m src.data_loader` to download the dataset.
                """)
            
            except OrchestratorError as e:
                st.error(f"""
                ❌ **Recommendation Failed**
                
                {str(e)}
                
                Please try again or adjust your preferences.
                """)
            
            except Exception as e:
                st.error(f"""
                ❌ **Unexpected Error**
                
                An unexpected error occurred: {str(e)}
                
                Please try again or contact support if the issue persists.
                """)
                logger.exception("Unexpected error in recommendation")
    
    else:
        # Welcome message when no search has been performed
        st.markdown("---")
        st.info("👈 **Select your preferences in the sidebar and click 'Get Recommendations' to start!**")
        
        # Show some stats or info
        if orchestrator and orchestrator.data_df is not None:
            st.header("📊 Dataset Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🏪 Total Restaurants", f"{len(orchestrator.data_df):,}")
            
            with col2:
                unique_locations = orchestrator.data_df['location'].nunique()
                st.metric("📍 Cities", unique_locations)
            
            with col3:
                unique_cuisines = orchestrator.data_df['cuisines'].nunique()
                st.metric("🍴 Cuisines", unique_cuisines)
            
            with col4:
                avg_rating = orchestrator.data_df['aggregate_rating'].mean()
                st.metric("⭐ Avg Rating", f"{avg_rating:.2f}")
        
        # How it works
        st.markdown("---")
        st.header("🤖 How It Works")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 1️⃣ Select Preferences
            Choose your location, budget, cuisine, and rating requirements in the sidebar.
            """)
        
        with col2:
            st.markdown("""
            ### 2️⃣ AI Analysis
            Our AI analyzes thousands of restaurants to find the perfect matches for you.
            """)
        
        with col3:
            st.markdown("""
            ### 3️⃣ Get Recommendations
            Receive personalized recommendations with detailed explanations for each choice.
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        Made with ❤️ using Streamlit | Powered by AI 🤖 | Data from Zomato
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

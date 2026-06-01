"""
Unit tests for ResponseFormatter module
"""

import pytest
from src.formatter import ResponseFormatter, ParseError
from src.models import Recommendation


class TestResponseFormatter:
    """Test suite for ResponseFormatter"""
    
    def test_initialization(self):
        """Test ResponseFormatter initializes correctly"""
        formatter = ResponseFormatter()
        assert formatter is not None
    
    def test_parse_well_formed_structured(self):
        """Test parsing well-formed structured LLM response"""
        formatter = ResponseFormatter()
        
        llm_response = """
1. **Bukhara**
   Cuisine: North Indian
   Rating: 4.8/5
   Estimated Cost for Two: ₹3500
   Why this is a great match: Legendary restaurant known for authentic kebabs and dal bukhara.

2. **Indian Accent**
   Cuisine: Modern Indian
   Rating: 4.7/5
   Estimated Cost for Two: ₹3000
   Why this is a great match: Award-winning innovative Indian cuisine with global influences.
"""
        
        recommendations = formatter.parse(llm_response)
        
        # Should parse 2 recommendations
        assert len(recommendations) == 2
        
        # Check first recommendation
        assert recommendations[0].rank == 1
        assert "Bukhara" in recommendations[0].restaurant_name
        assert "North Indian" in recommendations[0].cuisine
        assert recommendations[0].rating == 4.8
        assert "3500" in recommendations[0].estimated_cost
        assert len(recommendations[0].explanation) > 0
        
        # Check second recommendation
        assert recommendations[1].rank == 2
        assert "Indian Accent" in recommendations[1].restaurant_name
    
    def test_parse_without_bold_formatting(self):
        """Test parsing response without bold restaurant names"""
        formatter = ResponseFormatter()
        
        llm_response = """
1. Bukhara
   Cuisine: North Indian
   Rating: 4.8/5
   Cost: ₹3500 for two
   A legendary restaurant with amazing food.

2. Indian Accent
   Cuisine: Modern Indian  
   Rating: 4.7/5
   Cost: ₹3000
   Innovative dishes with great presentation.
"""
        
        recommendations = formatter.parse(llm_response)
        
        # Should still parse successfully
        assert len(recommendations) == 2
        assert recommendations[0].restaurant_name.strip() != ""
        assert recommendations[1].restaurant_name.strip() != ""
    
    def test_parse_with_varied_field_labels(self):
        """Test parsing with different field label formats"""
        formatter = ResponseFormatter()
        
        llm_response = """
1. Restaurant A
   Type of Cuisine: Italian
   Star Rating: 4.5
   Price for 2: ₹1200
   This place has the best pasta in town.
"""
        
        recommendations = formatter.parse(llm_response)
        
        # Should extract available information
        assert len(recommendations) >= 1
        assert recommendations[0].restaurant_name == "Restaurant A"
    
    def test_parse_minimal_format(self):
        """Test parsing with minimal formatting"""
        formatter = ResponseFormatter()
        
        llm_response = """
1. Restaurant One - Great food, 4.5/5 rating, ₹800
2. Restaurant Two - Amazing ambiance, 4.2/5 stars, ₹1000  
"""
        
        recommendations = formatter.parse(llm_response)
        
        # Should at least extract restaurant names
        assert len(recommendations) >= 1
        assert recommendations[0].restaurant_name != ""
    
    def test_parse_empty_response(self):
        """Test parsing empty LLM response"""
        formatter = ResponseFormatter()
        
        recommendations = formatter.parse("")
        
        # Should return empty list
        assert recommendations == []
    
    def test_parse_malformed_fallback(self):
        """Test fallback behavior with malformed response"""
        formatter = ResponseFormatter()
        
        llm_response = "I recommend trying some restaurants in Delhi. They have great food!"
        
        # With fallback enabled (default)
        recommendations = formatter.parse(llm_response, fallback_to_raw=True)
        
        # Should return raw text as single recommendation
        assert len(recommendations) == 1
        assert recommendations[0].rank == 0
        assert llm_response in recommendations[0].explanation
    
    def test_parse_malformed_no_fallback(self):
        """Test parsing malformed response without fallback"""
        formatter = ResponseFormatter()
        
        llm_response = "This is not a properly formatted recommendation."
        
        # With fallback disabled
        with pytest.raises(ParseError):
            formatter.parse(llm_response, fallback_to_raw=False)
    
    def test_parse_mixed_formatting(self):
        """Test parsing with inconsistent formatting between items"""
        formatter = ResponseFormatter()
        
        llm_response = """
1. **Restaurant A**
   Cuisine: Indian
   Rating: 4.5
   Cost: ₹800
   Great place.

2. Restaurant B
   Chinese food, 4.0 rating, ₹600 for two
   Also recommended.

3. **Restaurant C** - Italian, 4.3/5, ₹1000
"""
        
        recommendations = formatter.parse(llm_response)
        
        # Should parse all or most recommendations
        assert len(recommendations) >= 2
    
    def test_validate_recommendations(self):
        """Test recommendation validation"""
        formatter = ResponseFormatter()
        
        recommendations = [
            Recommendation(
                rank=1,
                restaurant_name="Valid Restaurant",
                cuisine="Indian",
                rating=4.5,
                estimated_cost="₹800",
                explanation="Good food"
            ),
            Recommendation(
                rank=0,  # Invalid rank
                restaurant_name="",  # Empty name
                cuisine="Chinese",
                rating=6.0,  # Invalid rating
                estimated_cost="₹600",
                explanation=""  # Empty explanation
            ),
            Recommendation(
                rank=2,
                restaurant_name="Another Restaurant",
                cuisine="Italian",
                rating=-1.0,  # Negative rating
                estimated_cost="₹1000",
                explanation="Nice place"
            )
        ]
        
        valid = formatter.validate_recommendations(recommendations)
        
        # Should filter out invalid and fix others
        assert len(valid) == 2  # Empty name should be filtered
        
        # Check rating bounds are enforced
        for rec in valid:
            assert 0.0 <= rec.rating <= 5.0
            assert rec.rank > 0
            assert rec.restaurant_name.strip() != ""
            assert rec.explanation.strip() != ""
    
    def test_validate_empty_list(self):
        """Test validating empty recommendation list"""
        formatter = ResponseFormatter()
        
        valid = formatter.validate_recommendations([])
        
        assert valid == []
    
    def test_format_recommendations_as_text(self):
        """Test formatting recommendations back to text"""
        formatter = ResponseFormatter()
        
        recommendations = [
            Recommendation(
                rank=1,
                restaurant_name="Restaurant A",
                cuisine="North Indian",
                rating=4.5,
                estimated_cost="₹800 for two",
                explanation="Excellent food and service."
            ),
            Recommendation(
                rank=2,
                restaurant_name="Restaurant B",
                cuisine="Chinese",
                rating=4.2,
                estimated_cost="₹600 for two",
                explanation="Great value for money."
            )
        ]
        
        text = formatter.format_recommendations_as_text(recommendations)
        
        # Check text contains all information
        assert "Restaurant A" in text
        assert "Restaurant B" in text
        assert "North Indian" in text
        assert "4.5" in text
        assert "₹800" in text
        assert "1." in text
        assert "2." in text
    
    def test_format_empty_recommendations(self):
        """Test formatting empty recommendation list"""
        formatter = ResponseFormatter()
        
        text = formatter.format_recommendations_as_text([])
        
        # Should handle gracefully
        assert "no recommendations" in text.lower() or "not available" in text.lower()
    
    def test_parse_with_numbered_parentheses(self):
        """Test parsing with numbers in parentheses format 1) instead of 1."""
        formatter = ResponseFormatter()
        
        llm_response = """
1) Restaurant Alpha
   Cuisine: Indian
   Rating: 4.5/5
   Cost: ₹900
   Highly recommended.

2) Restaurant Beta  
   Cuisine: Chinese
   Rating: 4.0/5
   Cost: ₹700
   Good value.
"""
        
        recommendations = formatter.parse(llm_response)
        
        # Should handle this format
        assert len(recommendations) >= 1
    
    def test_parse_with_extra_whitespace(self):
        """Test parsing with irregular whitespace"""
        formatter = ResponseFormatter()
        
        llm_response = """
1. **Restaurant One**
   
   Cuisine:    North Indian
   
   Rating:  4.5/5  
   Cost:   ₹800   for two
   
   This is a great restaurant with amazing food.
   
2. **Restaurant Two**
   Cuisine: Chinese
   Rating: 4.0/5
   Cost: ₹600
   Also good.
"""
        
        recommendations = formatter.parse(llm_response)
        
        # Should handle extra whitespace
        assert len(recommendations) == 2
        assert recommendations[0].restaurant_name.strip() != ""
    
    def test_parse_with_multiline_explanation(self):
        """Test parsing with multi-line explanations"""
        formatter = ResponseFormatter()
        
        llm_response = """
1. **Bukhara**
   Cuisine: North Indian
   Rating: 4.8/5
   Cost: ₹3500
   Why this is a great match: This legendary restaurant is known for its authentic
   North Indian cuisine, especially the dal bukhara and kebabs. The rustic ambiance
   and consistent quality make it a must-visit.
"""
        
        recommendations = formatter.parse(llm_response)
        
        assert len(recommendations) == 1
        # Should capture full multi-line explanation
        assert len(recommendations[0].explanation) > 50
    
    def test_parse_without_cost_symbol(self):
        """Test parsing when cost doesn't have rupee symbol"""
        formatter = ResponseFormatter()
        
        llm_response = """
1. Restaurant A
   Cuisine: Indian
   Rating: 4.5/5
   Estimated Cost for Two: 800
   Great food.
"""
        
        recommendations = formatter.parse(llm_response)
        
        assert len(recommendations) == 1
        # Cost should still be extracted
        assert "800" in recommendations[0].estimated_cost or recommendations[0].estimated_cost == "Not specified"
    
    def test_parse_with_decimal_ratings(self):
        """Test parsing various rating formats"""
        formatter = ResponseFormatter()
        
        llm_response = """
1. Restaurant A - Rating: 4.5/5
2. Restaurant B - Rating: 4
3. Restaurant C - Rating: 3.75 out of 5
"""
        
        recommendations = formatter.parse(llm_response)
        
        # Should extract ratings in various formats
        assert len(recommendations) >= 2
        assert any(rec.rating > 0 for rec in recommendations)
    
    def test_reranking_after_validation(self):
        """Test that validation re-ranks recommendations sequentially"""
        formatter = ResponseFormatter()
        
        recommendations = [
            Recommendation(rank=5, restaurant_name="A", cuisine="Indian", 
                         rating=4.0, estimated_cost="₹500", explanation="Good"),
            Recommendation(rank=10, restaurant_name="B", cuisine="Chinese",
                         rating=4.5, estimated_cost="₹600", explanation="Great"),
            Recommendation(rank=2, restaurant_name="C", cuisine="Italian",
                         rating=4.2, estimated_cost="₹700", explanation="Nice"),
        ]
        
        valid = formatter.validate_recommendations(recommendations)
        
        # Should be re-ranked 1, 2, 3
        assert valid[0].rank == 1
        assert valid[1].rank == 2
        assert valid[2].rank == 3


@pytest.fixture
def sample_structured_response():
    """Sample well-formed LLM response"""
    return """
1. **Bukhara**
   Cuisine: North Indian
   Rating: 4.8/5
   Estimated Cost for Two: ₹3500
   Why this is a great match: Legendary restaurant known for authentic North Indian cuisine.

2. **Indian Accent**
   Cuisine: Modern Indian
   Rating: 4.7/5
   Estimated Cost for Two: ₹3000
   Why this is a great match: Award-winning restaurant with innovative dishes.

3. **Karim's**
   Cuisine: Mughlai
   Rating: 4.5/5
   Estimated Cost for Two: ₹800
   Why this is a great match: Historic restaurant famous for kebabs and biryani.
"""

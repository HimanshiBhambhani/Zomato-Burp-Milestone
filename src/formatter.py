"""
Response Formatter Module

Parses LLM text output into structured Recommendation objects.
Handles multiple parsing strategies and graceful fallbacks.
"""

import re
import logging
from typing import List, Optional
from .models import Recommendation

logger = logging.getLogger(__name__)


class FormatterError(Exception):
    """Base exception for formatter errors"""
    pass


class ParseError(FormatterError):
    """Raised when parsing fails"""
    pass


class ResponseFormatter:
    """
    Parses LLM responses into structured Recommendation objects.
    
    Uses multiple parsing strategies with fallbacks for robustness.
    """
    
    def __init__(self):
        """Initialize the response formatter."""
        logger.info("ResponseFormatter initialized")
    
    def parse(self, llm_response: str, fallback_to_raw: bool = True) -> List[Recommendation]:
        """
        Parse LLM response into Recommendation objects.
        
        Args:
            llm_response: Raw text from LLM
            fallback_to_raw: If True, return raw text as single recommendation on parse failure
            
        Returns:
            List of Recommendation objects
        """
        if not llm_response or not llm_response.strip():
            logger.warning("Empty LLM response received")
            return []
        
        # Try structured parsing
        try:
            recommendations = self._parse_structured(llm_response)
            if recommendations:
                logger.info(f"Successfully parsed {len(recommendations)} recommendations (structured)")
                return recommendations
        except ParseError as e:
            logger.debug(f"Structured parsing failed: {e}")
        
        # Try regex extraction
        try:
            recommendations = self._parse_with_regex(llm_response)
            if recommendations:
                logger.info(f"Successfully parsed {len(recommendations)} recommendations (regex)")
                return recommendations
        except ParseError as e:
            logger.debug(f"Regex parsing failed: {e}")
        
        # Fallback to raw text
        if fallback_to_raw:
            logger.warning("All parsing strategies failed. Returning raw text as single recommendation.")
            return [Recommendation(
                rank=0,
                restaurant_name="AI Recommendations",
                cuisine="Various",
                rating=0.0,
                estimated_cost="Varies",
                explanation=llm_response.strip()
            )]
        else:
            raise ParseError("Failed to parse LLM response with all strategies")
    
    def _parse_structured(self, text: str) -> List[Recommendation]:
        """
        Parse structured format where each recommendation is clearly numbered.
        
        Expected format:
        1. **Restaurant Name**
           Cuisine Type(s)
           Rating: X.X/5
           Estimated Cost for Two: ₹XXX
           Why this is a great match: ...
        
        Args:
            text: LLM response text
            
        Returns:
            List of Recommendation objects
        """
        recommendations = []
        
        # Split by numbered sections (1., 2., 3., etc.)
        # Pattern: digit(s) followed by period at start of line
        sections = re.split(r'\n(?=\d+\.)', text)
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Skip if doesn't start with a number
            if not re.match(r'^\d+\.', section):
                continue
            
            try:
                rec = self._parse_single_structured_recommendation(section)
                if rec:
                    recommendations.append(rec)
            except Exception as e:
                logger.debug(f"Failed to parse section: {e}")
                continue
        
        return recommendations
    
    def _parse_single_structured_recommendation(self, text: str) -> Optional[Recommendation]:
        """
        Parse a single structured recommendation.
        
        Args:
            text: Text for one recommendation
            
        Returns:
            Recommendation object or None
        """
        # Extract rank
        rank_match = re.match(r'^(\d+)\.', text)
        rank = int(rank_match.group(1)) if rank_match else 0
        
        # Extract restaurant name (usually in bold or first line after number)
        name_match = re.search(r'\*\*([^*]+)\*\*', text)
        if not name_match:
            # Try first line after number
            lines = text.split('\n')
            if len(lines) > 0:
                first_line = lines[0]
                name_text = re.sub(r'^\d+\.\s*', '', first_line).strip()
                name_text = re.sub(r'[*#]', '', name_text).strip()
                if name_text:
                    restaurant_name = name_text
                else:
                    return None
            else:
                return None
        else:
            restaurant_name = name_match.group(1).strip()
        
        # Extract cuisine
        cuisine_match = re.search(r'Cuisine[:\s]+([^\n]+)', text, re.IGNORECASE)
        cuisine = cuisine_match.group(1).strip() if cuisine_match else "Not specified"
        
        # Extract rating
        rating_match = re.search(r'Rating[:\s]+(\d+\.?\d*)', text, re.IGNORECASE)
        rating = float(rating_match.group(1)) if rating_match else 0.0
        
        # Extract cost
        cost_match = re.search(r'Cost[^\n]*[:\s]+₹?(\d+)', text, re.IGNORECASE)
        if cost_match:
            cost_value = cost_match.group(1)
            estimated_cost = f"₹{cost_value} for two"
        else:
            estimated_cost = "Not specified"
        
        # Extract explanation (usually after "Why this is a great match" or similar)
        explanation_match = re.search(
            r'(?:Why this is a great match|Recommendation|Explanation)[:\s]+([^\n]+(?:\n(?!\d+\.|\*\*)[^\n]+)*)',
            text,
            re.IGNORECASE
        )
        if explanation_match:
            explanation = explanation_match.group(1).strip()
        else:
            # Take text after the cost line
            lines = text.split('\n')
            explanation_lines = []
            found_basics = False
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if re.search(r'(cuisine|rating|cost)', line, re.IGNORECASE):
                    found_basics = True
                    continue
                if found_basics and not re.match(r'^\d+\.', line):
                    explanation_lines.append(line)
            
            explanation = ' '.join(explanation_lines) if explanation_lines else "Great restaurant option."
        
        return Recommendation(
            rank=rank,
            restaurant_name=restaurant_name,
            cuisine=cuisine,
            rating=rating,
            estimated_cost=estimated_cost,
            explanation=explanation
        )
    
    def _parse_with_regex(self, text: str) -> List[Recommendation]:
        """
        Parse using aggressive regex patterns.
        
        Args:
            text: LLM response text
            
        Returns:
            List of Recommendation objects
        """
        recommendations = []
        
        # Pattern to find restaurant names (often in bold or after numbers)
        # Look for numbered items with restaurant names
        pattern = r'(\d+)[\.\)]\s*\*?\*?([^*\n]+?)\*?\*?\s*\n'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            rank = int(match.group(1))
            restaurant_name = match.group(2).strip()
            
            # Get text around this match for extracting other fields
            start_pos = match.start()
            # Find next numbered item or end of text
            next_match = re.search(r'\n\d+[\.\)]', text[match.end():])
            if next_match:
                end_pos = match.end() + next_match.start()
            else:
                end_pos = len(text)
            
            section_text = text[start_pos:end_pos]
            
            # Extract fields from section
            cuisine_match = re.search(r'Cuisine[:\s]+([^\n]+)', section_text, re.IGNORECASE)
            cuisine = cuisine_match.group(1).strip() if cuisine_match else "Various"
            
            rating_match = re.search(r'(\d+\.?\d*)\s*/?5', section_text)
            rating = float(rating_match.group(1)) if rating_match else 0.0
            
            cost_match = re.search(r'₹(\d+)', section_text)
            estimated_cost = f"₹{cost_match.group(1)} for two" if cost_match else "Varies"
            
            # Get explanation (text after basic details)
            explanation_lines = []
            for line in section_text.split('\n')[2:]:  # Skip first 2 lines (number and basics)
                line = line.strip()
                if line and not re.match(r'(Cuisine|Rating|Cost)', line, re.IGNORECASE):
                    explanation_lines.append(line)
            
            explanation = ' '.join(explanation_lines) if explanation_lines else "Recommended restaurant."
            explanation = explanation[:500]  # Limit length
            
            recommendations.append(Recommendation(
                rank=rank,
                restaurant_name=restaurant_name,
                cuisine=cuisine,
                rating=rating,
                estimated_cost=estimated_cost,
                explanation=explanation
            ))
        
        return recommendations
    
    def validate_recommendations(self, recommendations: List[Recommendation]) -> List[Recommendation]:
        """
        Validate and clean recommendations.
        
        Args:
            recommendations: List of recommendations to validate
            
        Returns:
            Cleaned list of recommendations
        """
        valid_recommendations = []
        
        for rec in recommendations:
            # Skip if no restaurant name
            if not rec.restaurant_name or rec.restaurant_name.strip() == "":
                logger.debug("Skipping recommendation with no restaurant name")
                continue
            
            # Ensure rank is positive
            if rec.rank <= 0:
                rec.rank = len(valid_recommendations) + 1
            
            # Ensure rating is in valid range
            if rec.rating < 0:
                rec.rating = 0.0
            elif rec.rating > 5:
                rec.rating = 5.0
            
            # Ensure explanation is not empty
            if not rec.explanation or rec.explanation.strip() == "":
                rec.explanation = f"A great choice for {rec.cuisine} cuisine."
            
            valid_recommendations.append(rec)
        
        # Re-rank if needed
        for i, rec in enumerate(valid_recommendations, 1):
            rec.rank = i
        
        logger.debug(f"Validated {len(valid_recommendations)} recommendations")
        return valid_recommendations
    
    def format_recommendations_as_text(self, recommendations: List[Recommendation]) -> str:
        """
        Format recommendations back to readable text.
        
        Args:
            recommendations: List of Recommendation objects
            
        Returns:
            Formatted text
        """
        if not recommendations:
            return "No recommendations available."
        
        lines = []
        for rec in recommendations:
            lines.append(f"\n{rec.rank}. **{rec.restaurant_name}**")
            lines.append(f"   Cuisine: {rec.cuisine}")
            lines.append(f"   Rating: {rec.rating}/5")
            lines.append(f"   Cost: {rec.estimated_cost}")
            lines.append(f"   Why: {rec.explanation}")
        
        return "\n".join(lines)

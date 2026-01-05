"""Parser utilities to convert DSPy string outputs to Pydantic models."""

import re
from typing import Optional

from ideas.models import (
    AppIdea,
    ComplexityJustification,
    Feature,
    LiteAppIdea,
)


def _safe_truncate(text: str, max_length: int) -> str:
    """Safely truncate text to max length with ellipsis if needed.
    
    Args:
        text: Text to truncate
        max_length: Maximum allowed length
        
    Returns:
        Truncated text with '...' if it was too long
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."



def parse_features(features_text: str) -> list[Feature]:
    """Parse numbered feature list into Feature objects.
    
    Expected format:
    1. [Feature Name] (priority: core/important/nice-to-have): Description
    2. [Another Feature] (priority: important): Another description
    
    Args:
        features_text: Numbered list of features from DSPy output
        
    Returns:
        List of Feature objects
    """
    features = []
    
    # Pattern: N. [Name] (priority: X): Description
    pattern = r'\d+\.\s*\[?([^\](\n]+?)\]?\s*\(priority:\s*(core|important|nice-to-have)\):\s*(.+?)(?=\n\d+\.|\Z)'
    
    matches = re.finditer(pattern, features_text, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        name = match.group(1).strip()
        priority = match.group(2).strip().lower()
        description = match.group(3).strip()
        
        # Truncate to model limits: name max 100, description max 300
        features.append(Feature(
            name=_safe_truncate(name, 100),
            description=_safe_truncate(description, 300),
            priority=priority,
        ))
    
    # Fallback: simpler pattern if strict format not followed
    if not features:
        simple_pattern = r'\d+\.\s*([^\n:]+?):\s*(.+?)(?=\n\d+\.|\Z)'
        matches = re.finditer(simple_pattern, features_text, re.DOTALL)
        
        for match in matches:
            name = match.group(1).strip()
            description = match.group(2).strip()
            
            # Try to extract priority from description
            priority = "important"  # default
            if "core" in description.lower() or "essential" in description.lower():
                priority = "core"
            elif "nice" in description.lower() or "optional" in description.lower():
                priority = "nice-to-have"
            
            features.append(Feature(
                name=_safe_truncate(name, 100),
                description=_safe_truncate(description, 300),
                priority=priority,
            ))
    
    return features


def parse_complexity_justification(
    reasoning: str,
    core_features: list[Feature],
) -> ComplexityJustification:
    """Parse complexity reasoning and extract metrics.
    
    Args:
        reasoning: Explanation of complexity from DSPy output
        core_features: List of features to count
        
    Returns:
        ComplexityJustification object
    """
    # Count features by priority
    feature_count = sum(1 for f in core_features if f.priority in ("core", "important"))
    
    # Try to extract numbers from reasoning
    data_model_count = 5  # default
    integration_count = 0
    
    # Look for patterns like "8 models", "15+ models", etc.
    model_match = re.search(r'(\d+)\+?\s*(?:data\s*)?models?', reasoning, re.IGNORECASE)
    if model_match:
        data_model_count = int(model_match.group(1))
    
    # Look for integration count
    integration_match = re.search(r'(\d+)\s*(?:external\s*)?integrations?', reasoning, re.IGNORECASE)
    if integration_match:
        integration_count = int(integration_match.group(1))
    
    # Truncate reasoning if too long (max 800 chars in model)
    reasoning = _safe_truncate(reasoning, 800)
    
    return ComplexityJustification(
        feature_count=feature_count,
        data_model_count=data_model_count,
        integration_count=integration_count,
        reasoning=reasoning,
    )


def parse_app_idea(dspy_output: dict) -> AppIdea:
    """Parse complete DSPy output into AppIdea model.
    
    Args:
        dspy_output: Dictionary containing all DSPy output fields
        
    Returns:
        AppIdea object
        
    Raises:
        ValueError: If required fields are missing or parsing fails
    """
    try:
        # Parse features first (needed for complexity justification)
        core_features = parse_features(dspy_output.get('core_features', ''))
        
        if not core_features:
            raise ValueError("Failed to parse any features from output")
        
        # Parse complexity justification
        complexity_justification = parse_complexity_justification(
            reasoning=dspy_output.get('complexity_reasoning', ''),
            core_features=core_features,
        )
        
        # Build AppIdea with safe truncation for all fields
        # Model limits: name(50), tagline(150), description(1000), target_users(200)
        return AppIdea(
            name=_safe_truncate(dspy_output.get('app_name', '').strip(), 50),
            tagline=_safe_truncate(dspy_output.get('tagline', '').strip(), 150),
            description=_safe_truncate(dspy_output.get('description', '').strip(), 1000),
            target_users=_safe_truncate(dspy_output.get('target_users', '').strip(), 200),
            core_features=core_features,
            complexity_justification=complexity_justification,
        )
        
    except Exception as e:
        raise ValueError(f"Failed to parse DSPy output into AppIdea: {e}") from e


def parse_concepts(concepts_text: str) -> list[str]:
    """Parse numbered concept list into list of strings.
    
    Expected format:
    1. Concept name: Brief description
    2. Another concept: Another description
    
    Args:
        concepts_text: Numbered list of concepts from DSPy output
        
    Returns:
        List of concept strings
    """
    concepts = []
    
    # Pattern: N. Text (everything until next number or end)
    pattern = r'\d+\.\s*(.+?)(?=\n\d+\.|\Z)'
    
    matches = re.finditer(pattern, concepts_text, re.DOTALL)
    
    for match in matches:
        concept = match.group(1).strip()
        # Truncate to max 200 chars per concept
        concepts.append(_safe_truncate(concept, 200))
    
    return concepts


def parse_lite_app_idea(dspy_output: dict) -> LiteAppIdea:
    """Parse DSPy output into LiteAppIdea model.
    
    Args:
        dspy_output: Dictionary containing DSPy output fields
        
    Returns:
        LiteAppIdea object
        
    Raises:
        ValueError: If required fields are missing or parsing fails
    """
    try:
        # Parse concepts
        concepts = parse_concepts(dspy_output.get('concepts', ''))
        
        if not concepts:
            raise ValueError("Failed to parse any concepts from output")
        
        # Build LiteAppIdea with safe truncation
        return LiteAppIdea(
            name=_safe_truncate(dspy_output.get('app_name', '').strip(), 50),
            tagline=_safe_truncate(dspy_output.get('tagline', '').strip(), 150),
            description=_safe_truncate(dspy_output.get('description', '').strip(), 1000),
            concepts=concepts,
        )
        
    except Exception as e:
        raise ValueError(f"Failed to parse DSPy output into LiteAppIdea: {e}") from e

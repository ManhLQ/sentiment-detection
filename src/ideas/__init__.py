"""App Idea Generator module for DSPy-based idea generation.

This module provides functionality to generate comprehensive app ideas
based on domain, complexity, technology constraints, and learning goals.
"""

from ideas.examples import TRAINING_EXAMPLES, get_examples_by_complexity
from ideas.formatters import (
    format_as_colored_text,
    format_as_json,
    format_as_markdown,
    save_to_file,
)
from ideas.generator import AppIdeaGenerator, create_idea_from_dict, create_request_from_dict
from ideas.models import (
    AppIdea,
    ComplexityJustification,
    ComplexityLevel,
    Feature,
    IdeaRequest,
)
from ideas.modules import IdeaGenerator, IdeaValidator
from ideas.parsers import (
    parse_app_idea,
    parse_complexity_justification,
    parse_features,
)
from ideas.signatures import (
    GenerateAppIdea,
    ValidateAppIdea,
)

__all__ = [
    # Main API
    "AppIdeaGenerator",
    "IdeaRequest",
    "AppIdea",
    "ComplexityLevel",
    
    # Models
    "Feature",
    "ComplexityJustification",
    
    # Formatters
    "format_as_json",
    "format_as_markdown",
    "format_as_colored_text",
    "save_to_file",
    
    # Examples
    "TRAINING_EXAMPLES",
    "get_examples_by_complexity",
    
    # Advanced (for custom workflows)
    "IdeaGenerator",
    "IdeaRefiner",
    "IdeaValidator",
    "TechStackGenerator",
    "parse_app_idea",
    "create_idea_from_dict",
    "create_request_from_dict",
]

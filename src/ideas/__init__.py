"""App Idea Generator module for DSPy-based idea generation.

This module provides functionality to generate comprehensive app ideas
based on domain, complexity, technology constraints, and learning goals.
"""

from ideas.examples import TRAINING_EXAMPLES, get_examples_by_complexity
from ideas.formatters import (
    format_as_colored_text,
    format_as_json,
    format_as_markdown,
    format_lite_as_colored_text,
    format_lite_as_json,
    format_lite_as_markdown,
    save_to_file,
)
from ideas.generator import (
    AppIdeaGenerator,
    IdeaRefinerOrchestrator,
    LiteAppIdeaGenerator,
    create_idea_from_dict,
    create_request_from_dict,
)
from ideas.models import (
    AppIdea,
    ComplexityJustification,
    ComplexityLevel,
    Feature,
    IdeaRequest,
    LiteAppIdea,
    RefinementRequest,
)
from ideas.modules import IdeaGenerator, IdeaRefiner, IdeaValidator, LiteIdeaGenerator
from ideas.parsers import (
    parse_app_idea,
    parse_complexity_justification,
    parse_features,
    parse_lite_app_idea,
)
from ideas.signatures import (
    GenerateAppIdea,
    GenerateLiteAppIdea,
    RefineAppIdea,
    ValidateAppIdea,
)

__all__ = [
    # Main API
    "AppIdeaGenerator",
    "LiteAppIdeaGenerator",
    "IdeaRequest",
    "AppIdea",
    "LiteAppIdea",
    "ComplexityLevel",
    
    # Models
    "Feature",
    "ComplexityJustification",
    
    # Formatters
    "format_as_json",
    "format_as_markdown",
    "format_as_colored_text",
    "format_lite_as_json",
    "format_lite_as_markdown",
    "format_lite_as_colored_text",
    "save_to_file",
    
    # Examples
    "TRAINING_EXAMPLES",
    "get_examples_by_complexity",
    
    # Advanced (for custom workflows)
    "IdeaGenerator",
    "LiteIdeaGenerator",
    "IdeaValidator",
    "parse_app_idea",
    "parse_lite_app_idea",
    "create_idea_from_dict",
    "create_request_from_dict",
    
    # Refinement
    "IdeaRefinerOrchestrator",
    "RefinementRequest",
    "IdeaRefiner",
    "RefineAppIdea",
]

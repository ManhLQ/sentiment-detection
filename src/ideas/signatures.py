"""DSPy signatures for the app idea generator module."""

import dspy


class GenerateAppIdea(dspy.Signature):
    """Generate a complete, concrete app idea based on domain and complexity.
    
    The generated idea should be:
    - Practical and buildable within the specified complexity
    - Focused on solving a real problem or use case
    - Interesting and valuable to implement
    - Unique enough to avoid being a generic CRUD app
    
    Focus purely on WHAT to build (features, use cases, value) not HOW to build it (tech stack).
    """
    
    # Input fields
    domain: str = dspy.InputField(
        desc="Domain or seed idea (e.g., 'project management', 'fitness tracking', 'developer tools')"
    )
    
    complexity: str = dspy.InputField(
        desc="Complexity level: 'low' (1-2 weeks, 2-4 features, simple data model), "
             "'medium' (3-6 weeks, 4-8 features, moderate integrations), or "
             "'high' (2-3 months, 8+ features, complex architecture)"
    )
    
    additional_requirements: str = dspy.InputField(
        desc="Any additional requirements or constraints, or 'none' if not specified"
    )
    
    # Output fields
    app_name: str = dspy.OutputField(
        desc="Catchy, memorable name for the app (2-4 words max)"
    )
    
    tagline: str = dspy.OutputField(
        desc="One-sentence tagline that captures the essence of the app"
    )
    
    description: str = dspy.OutputField(
        desc="Detailed description of the app in 2-4 sentences, explaining what it does and why it's useful"
    )
    
    target_users: str = dspy.OutputField(
        desc="Who would use this app and in what context"
    )
    
    core_features: str = dspy.OutputField(
        desc="List of 3-8 core features (depending on complexity), formatted as numbered list. "
             "Each feature should have format: 'N. [Feature Name] (priority: core/important/nice-to-have): Description'"
    )
    
    complexity_reasoning: str = dspy.OutputField(
        desc="2-3 sentence explanation of why this idea matches the requested complexity level, "
             "mentioning feature count, data model complexity, and integration requirements"
    )
    
    estimated_build_time: str = dspy.OutputField(
        desc="Rough estimate of build time (e.g., '2-3 weeks', '1-2 months')"
    )
    
    unique_selling_point: str = dspy.OutputField(
        desc="What makes this idea interesting, unique, or different from typical apps in this domain"
    )


class ValidateAppIdea(dspy.Signature):
    """Validate that a generated app idea meets all specified constraints.
    
    This signature checks for:
    - Complexity alignment
    - Feature quality and completeness
    - Feasibility and practicality
    - Value proposition clarity
    """
    
    # Input fields
    app_idea: str = dspy.InputField(
        desc="The app idea to validate (JSON format)"
    )
    
    required_complexity: str = dspy.InputField(
        desc="Required complexity level: low, medium, or high"
    )
    
    # Output fields
    is_valid: str = dspy.OutputField(
        desc="'yes' if the idea meets all constraints, 'no' otherwise"
    )
    
    validation_issues: str = dspy.OutputField(
        desc="List of validation issues found, or 'none' if valid. "
             "Format as bullet points with specific issues"
    )
    
    complexity_match: str = dspy.OutputField(
        desc="'yes' if complexity matches requirement, 'no' with explanation if not"
    )
    
    suggestions: str = dspy.OutputField(
        desc="Suggestions for improvement, or 'none' if idea is already good"
    )

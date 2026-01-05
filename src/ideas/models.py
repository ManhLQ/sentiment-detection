"""Data models for the app idea generator module."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ComplexityLevel(str, Enum):
    """Complexity levels for app ideas."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IdeaRequest(BaseModel):
    """Input model for app idea generation request."""
    
    domain: str = Field(
        ...,
        description="Domain or seed idea (e.g., 'project management', 'fitness tracking')",
        min_length=3,
        max_length=200,
    )
    
    complexity: ComplexityLevel = Field(
        default=ComplexityLevel.MEDIUM,
        description="Desired complexity level for the app",
    )
    
    additional_requirements: Optional[str] = Field(
        default=None,
        description="Any additional requirements or constraints",
        max_length=500,
    )


class Feature(BaseModel):
    """A single feature of the app."""
    
    name: str = Field(
        ...,
        description="Feature name",
        min_length=3,
        max_length=100,
    )
    
    description: str = Field(
        ...,
        description="Brief description of what this feature does",
        min_length=10,
        max_length=300,
    )
    
    priority: str = Field(
        ...,
        description="Priority level: 'core', 'important', or 'nice-to-have'",
    )
    
    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        """Validate priority is one of the allowed values."""
        allowed = {"core", "important", "nice-to-have"}
        if v.lower() not in allowed:
            raise ValueError(f"Priority must be one of {allowed}")
        return v.lower()


class ComplexityJustification(BaseModel):
    """Justification for complexity level."""
    
    feature_count: int = Field(
        ...,
        description="Number of features (core + important)",
        ge=1,
        le=50,
    )
    
    data_model_count: int = Field(
        ...,
        description="Estimated number of data models/entities",
        ge=1,
        le=100,
    )
    
    integration_count: int = Field(
        default=0,
        description="Number of external integrations",
        ge=0,
        le=20,
    )
    
    reasoning: str = Field(
        ...,
        description="Explanation of why this matches the requested complexity",
        min_length=50,
        max_length=800,
    )


class AppIdea(BaseModel):
    """Complete app idea output."""
    
    name: str = Field(
        ...,
        description="Catchy, memorable name for the app",
        min_length=3,
        max_length=50,
    )
    
    tagline: str = Field(
        ...,
        description="One-sentence tagline describing the app",
        min_length=10,
        max_length=150,
    )
    
    description: str = Field(
        ...,
        description="Detailed description of the app (2-4 sentences)",
        min_length=50,
        max_length=1000,
    )
    
    target_users: str = Field(
        ...,
        description="Who would use this app",
        min_length=10,
        max_length=200,
    )
    
    core_features: list[Feature] = Field(
        ...,
        description="List of features (3-8 depending on complexity)",
        min_length=3,
        max_length=15,
    )
    
    complexity_justification: ComplexityJustification = Field(
        ...,
        description="Why this idea matches the requested complexity",
    )
    
    estimated_build_time: str = Field(
        ...,
        description="Rough estimate of build time (e.g., '2-3 weeks', '1-2 months')",
    )
    
    unique_selling_point: str = Field(
        ...,
        description="What makes this idea interesting or unique",
        min_length=20,
        max_length=500,
    )
    
    @field_validator("core_features")
    @classmethod
    def validate_feature_priorities(cls, features: list[Feature]) -> list[Feature]:
        """Ensure at least one core feature exists."""
        core_count = sum(1 for f in features if f.priority == "core")
        if core_count == 0:
            raise ValueError("At least one feature must be marked as 'core'")
        return features

"""Main orchestrator for app idea generation with validation."""

import json
from typing import Optional

import dspy
from ideas.models import AppIdea, IdeaRequest
from ideas.modules import IdeaGenerator, IdeaValidator
from ideas.parsers import parse_app_idea


class AppIdeaGenerator:
    """Orchestrator for generating validated app ideas using DSPy."""
    
    def __init__(self, max_refinement_iterations: int = 2):
        """Initialize the generator.
        
        Args:
            max_refinement_iterations: Maximum number of refinement attempts
        """
        self.generator = IdeaGenerator()
        self.validator = IdeaValidator()
        self.max_refinement_iterations = max_refinement_iterations
    
    def generate(self, request: IdeaRequest) -> AppIdea:
        """Generate an app idea from a request.
        
        Args:
            request: IdeaRequest with requirements
            
        Returns:
            Generated AppIdea
            
        Raises:
            ValueError: If generation or parsing fails
        """
        # Generate idea
        prediction = self.generator(
            domain=request.domain,
            complexity=request.complexity.value,
            additional_requirements=request.additional_requirements,
        )
        
        # Parse DSPy output to AppIdea
        dspy_output = {
            'app_name': prediction.app_name,
            'tagline': prediction.tagline,
            'description': prediction.description,
            'target_users': prediction.target_users,
            'core_features': prediction.core_features,
            'complexity_reasoning': prediction.complexity_reasoning,
            'estimated_build_time': prediction.estimated_build_time,
            'unique_selling_point': prediction.unique_selling_point,
        }
        
        return parse_app_idea(dspy_output)
    
    def validate(
        self,
        idea: AppIdea,
        request: IdeaRequest,
    ) -> tuple[bool, Optional[str]]:
        """Validate an app idea against original request.
        
        Args:
            idea: Generated AppIdea
            request: Original IdeaRequest
            
        Returns:
            Tuple of (is_valid, validation_issues)
        """
        # Convert to JSON for validation
        idea_json = idea.model_dump_json(indent=2)
        
        # Validate
        validation = self.validator(
            app_idea=idea_json,
            required_complexity=request.complexity.value,
        )
        
        is_valid = validation.is_valid.lower().strip() == 'yes'
        issues = None if is_valid else validation.validation_issues
        
        return is_valid, issues
    
    def generate_with_validation(
        self,
        request: IdeaRequest,
        verbose: bool = False,
        debug: bool = False,
    ) -> tuple[AppIdea, dict]:
        """Generate an idea with automatic validation and refinement.
        
        Args:
            request: IdeaRequest with requirements
            verbose: Print generation progress
            debug: Show DSPy prompt history
            
        Returns:
            Tuple of (final_idea, metadata)
            metadata contains: attempts, validation_passed, issues
        """
        metadata = {
            'attempts': 0,
            'validation_passed': False,
            'issues': None,
        }
        
        for attempt in range(self.max_refinement_iterations + 1):
            metadata['attempts'] = attempt + 1
            
            if verbose:
                print(f"\n🎨 Generating idea (attempt {attempt + 1})...")
            
            # Generate idea
            idea = self.generate(request)
            
            if verbose:
                print(f"✨ Generated: {idea.name}")
            
            # Show DSPy history if debug mode
            if debug:
                print("\n" + "="*80)
                print("DSPy Prompt History (Generation)")
                print("="*80)
                dspy.inspect_history(n=1)
                print("="*80 + "\n")
            
            # Validate
            is_valid, issues = self.validate(idea, request)
            
            if debug:
                print("\n" + "="*80)
                print("DSPy Prompt History (Validation)")
                print("="*80)
                dspy.inspect_history(n=1)
                print("="*80 + "\n")
            
            if is_valid:
                metadata['validation_passed'] = True
                if verbose:
                    print("✅ Validation passed!")
                return idea, metadata
            
            if verbose:
                print(f"⚠️  Validation issues: {issues}")
            
            # Store issues for last attempt
            metadata['issues'] = issues
            
            # If not last attempt, retry generation
            if attempt < self.max_refinement_iterations:
                if verbose:
                    print("🔄 Retrying generation...")
        
        # Return last idea even if validation failed
        if verbose:
            print(f"⚠️  Returning idea after {metadata['attempts']} attempts (validation not passed)")
        
        return idea, metadata


def create_idea_from_dict(data: dict) -> AppIdea:
    """Create AppIdea from dictionary (for loading from JSON).
    
    Args:
        data: Dictionary with AppIdea fields
        
    Returns:
        AppIdea object
    """
    return AppIdea.model_validate(data)


def create_request_from_dict(data: dict) -> IdeaRequest:
    """Create IdeaRequest from dictionary (for loading from JSON).
    
    Args:
        data: Dictionary with IdeaRequest fields
        
    Returns:
        IdeaRequest object
    """
    return IdeaRequest.model_validate(data)

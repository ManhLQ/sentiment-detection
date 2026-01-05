"""DSPy module wrappers for app idea generation."""

import dspy
from typing import Optional

from ideas.signatures import (
    GenerateAppIdea,
    GenerateLiteAppIdea,
    RefineAppIdea,
    ValidateAppIdea,
)


class IdeaGenerator(dspy.Module):
    """Main module for generating app ideas using DSPy ChainOfThought with few-shot examples."""
    
    def __init__(self, use_examples: bool = True):
        """Initialize the generator.
        
        Args:
            use_examples: Whether to include example context in prompts
        """
        super().__init__()
        self.use_examples = use_examples
        self.generate = dspy.ChainOfThought(GenerateAppIdea)
        
        # Prepare example context if enabled
        if use_examples:
            from ideas.examples import TRAINING_EXAMPLES
            self.example_context = self._build_example_context(TRAINING_EXAMPLES)
        else:
            self.example_context = ""
    
    def _build_example_context(self, examples) -> str:
        """Build a context string from training examples for few-shot learning.
        
        This creates a formatted string showing the LLM what good outputs look like.
        """
        context_parts = ["Here are some example app ideas for reference:\n"]
        
        for i, example in enumerate(examples, 1):
            request = example["request"]
            idea = example["idea"]
            
            context_parts.append(f"\n--- Example {i} ---")
            context_parts.append(f"Domain: {request.domain}")
            context_parts.append(f"Complexity: {request.complexity.value}")
            
            context_parts.append(f"\nGenerated Idea:")
            context_parts.append(f"App Name: {idea.name}")
            context_parts.append(f"Tagline: {idea.tagline}")
            context_parts.append(f"Description: {idea.description}")
            context_parts.append(f"Target Users: {idea.target_users}")
            
            # Show a couple features as examples
            context_parts.append(f"Features (sample):")
            for j, feature in enumerate(idea.core_features[:2], 1):
                context_parts.append(f"  {j}. [{feature.name}] (priority: {feature.priority}): {feature.description}")
        
        context_parts.append("\n--- End of Examples ---\n")
        context_parts.append("Now generate a new, unique idea based on the user's requirements, following the same structure and quality as the examples above.\n")
        
        return '\n'.join(context_parts)
    
    def forward(
        self,
        domain: str,
        complexity: str,
        additional_requirements: Optional[str] = None,
    ) -> dspy.Prediction:
        """Generate an app idea based on requirements.
        
        Args:
            domain: Domain or seed idea
            complexity: Complexity level (low/medium/high)
            additional_requirements: Additional constraints (or 'none')
            
        Returns:
            DSPy Prediction with generated app idea fields
        """
        # Normalize None to 'none'
        additional_requirements = additional_requirements or 'none'
        
        # Prepend example context to domain if using examples
        if self.use_examples:
            domain_with_context = f"{self.example_context}\n\nUser Request:\nDomain: {domain}"
        else:
            domain_with_context = domain
        
        return self.generate(
            domain=domain_with_context,
            complexity=complexity,
            additional_requirements=additional_requirements,
        )


class LiteIdeaGenerator(dspy.Module):
    """Lightweight module for generating simplified app ideas."""
    
    def __init__(self):
        """Initialize the lite generator."""
        super().__init__()
        self.generate = dspy.ChainOfThought(GenerateLiteAppIdea)
    
    def forward(
        self,
        domain: str,
        complexity: str,
        additional_requirements: Optional[str] = None,
    ) -> dspy.Prediction:
        """Generate a lite app idea based on requirements.
        
        Args:
            domain: Domain or seed idea
            complexity: Complexity level (low/medium/high)
            additional_requirements: Additional constraints (or 'none')
            
        Returns:
            DSPy Prediction with generated lite app idea fields
        """
        # Normalize None to 'none'
        additional_requirements = additional_requirements or 'none'
        
        return self.generate(
            domain=domain,
            complexity=complexity,
            additional_requirements=additional_requirements,
        )


class IdeaValidator(dspy.Module):
    """Module for validating app ideas against constraints."""
    
    def __init__(self):
        super().__init__()
        self.validate = dspy.ChainOfThought(ValidateAppIdea)
    
    def forward(
        self,
        app_idea: str,
        required_complexity: str,
    ) -> dspy.Prediction:
        """Validate an app idea against requirements.
        
        Args:
            app_idea: JSON representation of AppIdea
            required_complexity: Required complexity level
            
        Returns:
            DSPy Prediction with validation results
        """
        return self.validate(
            app_idea=app_idea,
            required_complexity=required_complexity,
        )


class IdeaRefiner(dspy.Module):
    """Module for refining existing app ideas based on feedback."""
    
    def __init__(self):
        super().__init__()
        self.refine = dspy.ChainOfThought(RefineAppIdea)
    
    def forward(
        self,
        original_document: str,
        feedback: str,
        full_regeneration: bool = False,
    ) -> dspy.Prediction:
        """Refine an app idea based on user feedback.
        
        Args:
            original_document: Original markdown document
            feedback: User feedback
            full_regeneration: Whether to regenerate entire document
            
        Returns:
            DSPy Prediction with refined document and changes summary
        """
        return self.refine(
            original_document=original_document,
            feedback=feedback,
            full_regeneration='yes' if full_regeneration else 'no',
        )


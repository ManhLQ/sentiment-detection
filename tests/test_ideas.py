"""Component tests for the ideas module.

Tests the training examples and parser functionality without requiring LLM calls.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ideas import TRAINING_EXAMPLES, parse_app_idea


def test_examples():
    """Test that all training examples are valid."""
    print("Testing training examples...\n")
    
    for i, example in enumerate(TRAINING_EXAMPLES, 1):
        request = example["request"]
        idea = example["idea"]
        
        print(f"{i}. {idea.name}")
        print(f"   Domain: {request.domain}")
        print(f"   Complexity: {request.complexity.value}")
        print(f"   Features: {len(idea.core_features)}")
        
        # Validate the idea
        try:
            # This will raise if validation fails
            idea.model_validate(idea.model_dump())
            print(f"   ✅ Valid")
        except Exception as e:
            print(f"   ❌ Invalid: {e}")
            return False
        
        print()
    
    print("✅ All {} examples are valid!\n".format(len(TRAINING_EXAMPLES)))
    return True


def test_parser():
    """Test the parser with sample DSPy output."""
    print("\nTesting parser...")
    
    sample_output = {
        'app_name': 'TestApp',
        'tagline': 'A test application for validation',
        'description': 'This is a test app to verify the parser works correctly with all required fields.',
        'target_users': 'Developers and testers',
        'core_features': '''1. [Feature One] (priority: core): First core feature description
2. [Feature Two] (priority: important): Second important feature
3. [Feature Three] (priority: nice-to-have): Third optional feature''',
        'complexity_reasoning': 'This is a simple app with 3 features and minimal data models.',
    }
    
    try:
        idea = parse_app_idea(sample_output)
        print("✅ Parsed successfully!")
        print(f"   Name: {idea.name}")
        print(f"   Features: {len(idea.core_features)}")
        return True
    except Exception as e:
        print(f"❌ Parser failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("Ideas Module Component Tests")
    print("=" * 80)
    
    if not test_examples():
        return 1
    
    if not test_parser():
        return 1
    
    print("\n" + "=" * 80)
    print("✅ All tests passed!")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())

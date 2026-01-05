"""Test truncation functionality."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ideas.parsers import parse_app_idea


def test_long_field_truncation():
    """Test that long fields are properly truncated."""
    print("Testing field truncation...")
    
    # Create output with fields that exceed max lengths
    sample_output = {
        'app_name': 'A' * 100,  # Max is 50
        'tagline': 'B' * 200,  # Max is 150
        'description': 'C' * 1200,  # Max is 1000
        'target_users': 'D' * 300,  # Max is 200
        'core_features': '''1. [Feature One] (priority: core): ''' + 'E' * 400 + '''
2. [Feature Two] (priority: important): Another feature description
3. [Feature Three] (priority: nice-to-have): Third feature description''',
        'complexity_reasoning': 'F' * 900,  # Max is 800
        'estimated_build_time': '2-3 weeks',
        'unique_selling_point': 'H' * 600,  # Max is 500
    }
    
    try:
        idea = parse_app_idea(sample_output)
        
        # Verify truncation
        assert len(idea.name) <= 50, f"Name too long: {len(idea.name)}"
        assert len(idea.tagline) <= 150, f"Tagline too long: {len(idea.tagline)}"
        assert len(idea.description) <= 1000, f"Description too long: {len(idea.description)}"
        assert len(idea.target_users) <= 200, f"Target users too long: {len(idea.target_users)}"
        assert len(idea.unique_selling_point) <= 500, f"USP too long: {len(idea.unique_selling_point)}"
        assert len(idea.complexity_justification.reasoning) <= 800, f"Reasoning too long: {len(idea.complexity_justification.reasoning)}"
        
        # Check features
        for feature in idea.core_features:
            assert len(feature.name) <= 100, f"Feature name too long: {len(feature.name)}"
            assert len(feature.description) <= 300, f"Feature description too long: {len(feature.description)}"
        
        print("✅ All fields properly truncated!")
        print(f"   Name: {len(idea.name)} chars (max 50)")
        print(f"   Tagline: {len(idea.tagline)} chars (max 150)")
        print(f"   Description: {len(idea.description)} chars (max 1000)")
        print(f"   Target users: {len(idea.target_users)} chars (max 200)")
        print(f"   USP: {len(idea.unique_selling_point)} chars (max 500)")
        print(f"   Reasoning: {len(idea.complexity_justification.reasoning)} chars (max 800)")
        print(f"   Features: {len(idea.core_features)} features parsed")
        
        return True
    except Exception as e:
        print(f"❌ Truncation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_long_field_truncation()
    sys.exit(0 if success else 1)

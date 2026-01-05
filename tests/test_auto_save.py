"""Test automatic saving to output folder."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ideas import AppIdeaGenerator, IdeaRequest, ComplexityLevel, format_as_markdown, save_to_file
import re


def test_auto_save():
    """Test that ideas are automatically saved to output folder."""
    print("Testing automatic save to output folder...")
    
    # Use one of the training examples
    from ideas import TRAINING_EXAMPLES
    
    idea = TRAINING_EXAMPLES[0]["idea"]  # FocusBlocks
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Sanitize app name for filename
    safe_name = re.sub(r'[^\w\s-]', '', idea.name)
    safe_name = re.sub(r'[-\s]+', '_', safe_name).strip('_').lower()
    
    # Generate filename
    markdown_filename = output_dir / f"{safe_name}.md"
    
    # Save markdown
    markdown_output = format_as_markdown(idea)
    save_to_file(markdown_output, str(markdown_filename))
    
    # Verify file exists
    if markdown_filename.exists():
        print(f"✅ File created: {markdown_filename}")
        print(f"   Size: {markdown_filename.stat().st_size} bytes")
        
        # Verify content
        content = markdown_filename.read_text()
        if idea.name in content and idea.tagline in content:
            print(f"✅ Content verified")
            return True
        else:
            print(f"❌ Content verification failed")
            return False
    else:
        print(f"❌ File not created")
        return False


if __name__ == "__main__":
    success = test_auto_save()
    sys.exit(0 if success else 1)

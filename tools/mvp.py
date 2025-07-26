#!/usr/bin/env python3
"""
AVAAD MVP: Practical story validation that tests what stories actually claim
"""

import sys
from pathlib import Path

# Import practical validator
try:
    from practical_validator import validate_story_practical
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from practical_validator import validate_story_practical


def check_story(story_id: str) -> bool:
    """Practical story validation - tests what the story actually claims to deliver."""
    
    print(f"🔍 AVAAD Practical Validation for Story {story_id}")
    print(f"📋 Testing actual functionality claimed in the story...")
    
    try:
        # Use practical validation
        is_valid, message = validate_story_practical(story_id)
        
        if is_valid:
            print(f"✅ YES, story {story_id} is done - {message}")
            print("🎉 All claimed functionality works as expected!")
            return True
        else:
            print(f"❌ NO, story {story_id} is NOT done - {message}")
            print("Tell the AI agent: 'Fix the issues before marking complete'")
            return False
        
    except Exception as e:
        print(f"⚠️  ERROR: Validation failed - {str(e)}")
        print("Make sure you're in the project root and dependencies are installed.")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mvp.py STORY_ID")
        print("Example: python mvp.py 6.2")
        sys.exit(1)
    
    story_id = sys.argv[1]
    is_complete = check_story(story_id)
    
    # Exit code: 0 for complete, 1 for incomplete
    sys.exit(0 if is_complete else 1)
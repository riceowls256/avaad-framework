#!/usr/bin/env python3
"""
AVAAD MVP: Comprehensive story validation with AI security and cost tracking
"""

import sys
import os
from pathlib import Path

# Import validators
try:
    from practical_validator import validate_story_practical
    from core.validators.llm_output_validator import LLMOutputValidator
    from core.cost_tracker import CostTracker
    from core.security.prompt_injection_detector import PromptInjectionDetector
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    sys.path.append(str(Path(__file__).parent / "core" / "validators"))
    sys.path.append(str(Path(__file__).parent / "core" / "security"))
    from practical_validator import validate_story_practical
    from core.validators.llm_output_validator import LLMOutputValidator
    from core.cost_tracker import CostTracker
    from core.security.prompt_injection_detector import PromptInjectionDetector


def check_story(story_id: str, comprehensive: bool = False) -> bool:
    """Comprehensive story validation with AI security and cost tracking."""
    
    print(f"🔍 AVAAD Comprehensive Validation for Story {story_id}")
    print("=" * 60)
    
    try:
        # 1. Traditional practical validation
        print("📋 1. Checking practical functionality...")
        is_practical_valid, practical_message = validate_story_practical(story_id)
        
        if not is_practical_valid:
            print(f"❌ Practical validation failed: {practical_message}")
            return False
        
        print("✅ Practical validation passed")
        
        # 2. LLM Output Validation (if comprehensive mode)
        if comprehensive:
            print("🤖 2. Validating AI agent claims...")
            validator = LLMOutputValidator()
            
            # Look for agent output file
            output_file = Path(f"logs/story-{story_id}-agent-output.txt")
            if output_file.exists():
                with open(output_file, 'r') as f:
                    agent_output = f.read()
                
                validation = validator.validate_agent_output(
                    story_id, 
                    agent_output, 
                    files_changed=[]  # Would need to be populated
                )
                
                print(f"   AI Validation Score: {validation.score:.1%}")
                if not validation.is_valid:
                    print("   ❌ AI agent claims validation failed:")
                    for issue in validation.issues[:3]:  # Show first 3 issues
                        print(f"     • {issue}")
                    return False
                print("   ✅ AI claims validated")
            else:
                print("   ⚠️  No agent output found for validation")
        
        # 3. Security check
        if comprehensive:
            print("🛡️  3. Checking for security issues...")
            detector = PromptInjectionDetector()
            
            # Check agent interactions
            interaction_file = Path(f"logs/story-{story_id}-interactions.json")
            if interaction_file.exists():
                alerts = detector.scan_agent_interactions(str(interaction_file))
                
                high_alerts = [a for a in alerts if a.level in ['HIGH', 'CRITICAL']]
                if high_alerts:
                    print("   ❌ Security issues detected:")
                    for alert in high_alerts:
                        print(f"     • {alert.title}: {alert.description}")
                    return False
                print("   ✅ No security issues detected")
            else:
                print("   ⚠️  No agent interactions found for security check")
        
        # 4. Cost tracking
        if comprehensive:
            print("💰 4. Checking cost impact...")
            tracker = CostTracker()
            roi = tracker.calculate_roi(story_id)
            
            if roi['total_cost'] > 0:
                print(f"   AI Cost: ${roi['total_cost']:.2f}")
                print(f"   ROI: {roi['roi_score']:.1f}%")
                
                if roi['roi_score'] < 0:
                    print("   ❌ Negative ROI - consider optimizing AI usage")
                    return False
                print("   ✅ Cost-effective AI usage")
        
        # Success!
        print("\n🎉 Story validation complete!")
        print("✅ All checks passed - story is ready for completion")
        return True
        
    except Exception as e:
        print(f"⚠️  ERROR: Validation failed - {str(e)}")
        print("Run with --simple for basic validation only")
        return False


def main():
    """Main CLI entry point with enhanced options."""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python mvp.py STORY_ID [--comprehensive]")
        print("Example: python mvp.py 6.2")
        print("Example: python mvp.py 6.2 --comprehensive")
        print("\nOptions:")
        print("  --comprehensive  Include AI security and cost validation")
        sys.exit(1)
    
    story_id = sys.argv[1]
    comprehensive = len(sys.argv) > 2 and sys.argv[2] == "--comprehensive"
    
    is_complete = check_story(story_id, comprehensive)
    
    # Exit code: 0 for complete, 1 for incomplete
    sys.exit(0 if is_complete else 1)
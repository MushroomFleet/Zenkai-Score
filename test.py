import os
import sys
from pathlib import Path

print("=== Testing Zenkai-Score V2.0 ===")

# Import the ZenkaiScore class
try:
    from zenkai_score import ZenkaiScore
    print("Successfully imported ZenkaiScore")
    
    # Create scorer instance
    scorer = ZenkaiScore()
    print("Successfully initialized ZenkaiScore")
    
    # Test scoring with the included test image
    script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    test_image = script_dir / "test_cat.jpg"
    
    if test_image.exists():
        print(f"\nAttempting to score test image: {test_image}")
        score = scorer.score_image(test_image)
        print(f"Aesthetic score: {score:.2f}/10.0")
        
        if score > 0:
            print("✓ Test passed successfully!")
        else:
            print("✗ Test failed: Score is 0")
    else:
        print(f"✗ Test image not found at: {test_image}")
    
except Exception as e:
    print(f"✗ Error during test: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed.")

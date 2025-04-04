import os
import sys
import torch
from os.path import expanduser
from PIL import Image

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    # Import the ZenkaiScore class from our package
    from zenkai_score.core import ZenkaiScore
    print("Successfully imported ZenkaiScore")
    
    # Create scorer instance
    scorer = ZenkaiScore()
    print("Successfully created ZenkaiScore instance")
    
    # Get information about the model
    print(f"Model name: {scorer.model.model_name}")
    print(f"Model device: {scorer.model.device}")
    
    # Score test image
    print("Attempting to score test_cat.jpg...")
    score = scorer.score_image("test_cat.jpg")
    print(f"Aesthetic score: {score}")
    
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

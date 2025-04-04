import os
import sys
# Add current directory to path so we can import zenkai_score
sys.path.insert(0, os.path.abspath('.'))

from zenkai_score.core import ZenkaiScore

# Create scorer instance
scorer = ZenkaiScore()

# Score test image
score = scorer.score_image("test_cat.jpg")
print(f"Aesthetic score: {score}")

# Print information about the model being used
print(f"Model: {scorer.model.model_name}")
print(f"Device: {scorer.model.device}")

# Also print the raw model output before normalization for comparison with notebook
import torch
from PIL import Image
import open_clip

# Use the same approach as the notebook for comparison
model_name = scorer.model.model_name
model, _, preprocess = open_clip.create_model_and_transforms(model_name, pretrained='openai')

# Process the image
image = preprocess(Image.open("test_cat.jpg")).unsqueeze(0)

# Get the LAION aesthetic model from our scorer
amodel = scorer.model.mlp

with torch.no_grad():
    # Encode and normalize
    image_features = model.encode_image(image)
    image_features /= image_features.norm(dim=-1, keepdim=True)
    
    # Get raw prediction
    prediction = amodel(image_features)
    print(f"Raw model output: {prediction.item()}")
    print(f"This should be close to the notebook value of ~4.9982")

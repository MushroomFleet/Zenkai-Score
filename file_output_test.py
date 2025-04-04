import os
import torch
import torch.nn as nn
from os.path import expanduser
from urllib.request import urlretrieve
from PIL import Image
import sys

# Redirect stdout to file
log_file = open("model_test_output.log", "w")
sys.stdout = log_file

print("=== Testing Aesthetic Model Integration ===")

# Function from the notebook
def get_aesthetic_model(clip_model="vit_l_14"):
    """load the aethetic model"""
    print(f"Loading aesthetic model: {clip_model}")
    home = expanduser("~")
    cache_folder = home + "/.cache/emb_reader"
    path_to_model = cache_folder + "/sa_0_4_"+clip_model+"_linear.pth"
    
    print(f"Looking for model at: {path_to_model}")
    if not os.path.exists(path_to_model):
        os.makedirs(cache_folder, exist_ok=True)
        url_model = (
            "https://github.com/LAION-AI/aesthetic-predictor/blob/main/sa_0_4_"+clip_model+"_linear.pth?raw=true"
        )
        print(f"Downloading model from {url_model} to {path_to_model}")
        urlretrieve(url_model, path_to_model)
    
    # Check if file exists and has content
    if os.path.exists(path_to_model):
        file_size = os.path.getsize(path_to_model)
        print(f"Model file exists, size: {file_size} bytes")
    else:
        print(f"Error: Model file does not exist at {path_to_model}")
        
    if clip_model == "vit_l_14":
        m = nn.Linear(768, 1)
    elif clip_model == "vit_b_32":
        m = nn.Linear(512, 1)
    else:
        raise ValueError()
    
    try:
        s = torch.load(path_to_model)
        print(f"Model loaded successfully: {type(s)}")
        print(f"Model keys: {s.keys() if isinstance(s, dict) else 'Not a dict'}")
        
        m.load_state_dict(s)
        m.eval()
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)
        
    return m

print("\n=== Testing notebook-style model loading ===")
try:
    amodel = get_aesthetic_model(clip_model="vit_l_14")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load model: {e}")

# If we have open_clip, try to score an image
try:
    import open_clip
    
    print("\n=== Attempting to score test_cat.jpg... ===")
    
    # Create model and transforms
    model, _, preprocess = open_clip.create_model_and_transforms('ViT-L-14', pretrained='openai')
    
    # Process image
    image = preprocess(Image.open("test_cat.jpg")).unsqueeze(0)
    
    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        prediction = amodel(image_features)
        print(f"Raw score: {prediction.item()}")
        
        # Map to 1-10 range as in our implementation
        normalized_score = min(max(prediction.item() + 5, 1.0), 10.0)
        print(f"Normalized score (1-10): {normalized_score}")
        
except ImportError:
    print("open_clip not available, skipping image scoring")
except Exception as e:
    print(f"Error during image scoring: {e}")

# Now test our integrated model
print("\n=== Testing our integrated model ===")
try:
    sys.path.insert(0, os.path.abspath('.'))
    from zenkai_score.core import ZenkaiScore
    
    # Create scorer instance
    scorer = ZenkaiScore()
    
    # Score test image
    score = scorer.score_image("test_cat.jpg")
    print(f"Integrated model aesthetic score: {score}")
    
    # Print information about the model being used
    print(f"Model: {scorer.model.model_name}")
    print(f"Device: {scorer.model.device}")
    
    # Check paths
    print("\n=== Checking paths ===")
    alt_cache_dir = os.path.expanduser("~/.cache/emb_reader")
    weights_path = os.path.join(alt_cache_dir, f"sa_0_4_vit_l_14_linear.pth")
    print(f"Expected weights path: {weights_path}")
    print(f"File exists: {os.path.exists(weights_path)}")
    if os.path.exists(weights_path):
        print(f"File size: {os.path.getsize(weights_path)} bytes")
    
except Exception as e:
    print(f"Error testing integrated model: {e}")

# Close log file
log_file.close()

# Reset stdout
sys.stdout = sys.__stdout__
print("Test completed. Results written to model_test_output.log")

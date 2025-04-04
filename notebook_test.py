import os
import torch
import torch.nn as nn
from os.path import expanduser
from urllib.request import urlretrieve
from PIL import Image
import sys

# Function from the notebook
def get_aesthetic_model(clip_model="vit_l_14"):
    """load the aethetic model"""
    home = expanduser("~")
    cache_folder = home + "/.cache/emb_reader"
    path_to_model = cache_folder + "/sa_0_4_"+clip_model+"_linear.pth"
    
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

print("Testing notebook-style model loading")
amodel = get_aesthetic_model(clip_model="vit_l_14")
print("Model loaded successfully!")

# If we have open_clip, try to score an image
try:
    import open_clip
    
    print("\nAttempting to score test_cat.jpg...")
    
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

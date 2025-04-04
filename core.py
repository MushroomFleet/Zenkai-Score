import os
import torch
import torch.nn as nn
from os.path import expanduser
from urllib.request import urlretrieve
from PIL import Image
from pathlib import Path
from typing import List, Tuple, Dict, Union, Optional, Callable
import sys

class ZenkaiScore:
    """Core engine for Zenkai-Score aesthetic image scoring system"""
    
    def __init__(self, device: Optional[str] = None):
        """Initialize the Zenkai-Score engine
        
        Args:
            device: Device to run inference on ('cpu', 'cuda', etc.)
        """
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        
        # Load aesthetic model
        self.aesthetic_model = self.get_aesthetic_model()
        
        # Load CLIP model
        try:
            import open_clip
            self.model, _, self.preprocess = open_clip.create_model_and_transforms(
                'ViT-L-14', 
                pretrained='openai',
                quick_gelu=True  # Enable QuickGELU activation as used in training
            )
        except ImportError:
            print("Error: open_clip not available. Please install with 'pip install open-clip-torch'")
            sys.exit(1)
    
    def get_aesthetic_model(self, clip_model="vit_l_14"):
        """Load the aesthetic model following the notebook approach
        
        Args:
            clip_model: CLIP model variant to use
            
        Returns:
            Loaded aesthetic model
        """
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
            raise ValueError(f"Unsupported clip model: {clip_model}")
        
        try:
            s = torch.load(path_to_model)
            m.load_state_dict(s)
            m.eval()
        except Exception as e:
            print(f"Error loading model: {e}")
            sys.exit(1)
            
        return m
    
    def score_image(self, image_path: Union[str, Path]) -> float:
        """Score a single image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Aesthetic score between 1.0 and 10.0, or 0.0 on error
        """
        # Convert to Path object for uniform handling
        image_path = Path(image_path)
        
        # Validate image exists
        if not image_path.exists():
            print(f"Error: Image file not found at {image_path}")
            return 0.0
            
        # Validate file extension
        if image_path.suffix.lower() not in self.image_extensions:
            print(f"Error: Unsupported file format {image_path.suffix} for {image_path}")
            return 0.0
        
        try:
            # Load and preprocess image
            image = self.preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0)
            
            with torch.no_grad():
                # Extract image features
                image_features = self.model.encode_image(image)
                # Normalize features
                image_features /= image_features.norm(dim=-1, keepdim=True)
                # Get raw aesthetic score
                raw_score = self.aesthetic_model(image_features).item()
                # Normalize to 1-10 scale
                normalized_score = min(max(raw_score + 5, 1.0), 10.0)
                
                return normalized_score
        
        except torch.cuda.OutOfMemoryError:
            print(f"CUDA out of memory when processing {image_path}. Try using CPU device instead.")
            return 0.0
        except Exception as e:
            print(f"Error scoring image {image_path}: {e}")
            return 0.0
            
    def scan_directory(self, 
                      dir_path: Union[str, Path], 
                      recursive: bool = False,
                      progress_callback: Optional[Callable[[int, int], None]] = None) -> List[Tuple[str, float]]:
        """Scan a directory for images and score them
        
        Args:
            dir_path: Directory path to scan
            recursive: Whether to scan subdirectories
            progress_callback: Optional callback function for progress updates
            
        Returns:
            List of (image_path, score) tuples
        """
        results = []
        dir_path = Path(dir_path)
        
        # Validate directory exists
        if not dir_path.exists():
            print(f"Error: Directory not found at {dir_path}")
            return []
            
        if not dir_path.is_dir():
            print(f"Error: {dir_path} is not a directory")
            return []
        
        try:
            # Get all image files
            if recursive:
                image_files = [
                    p for p in dir_path.glob('**/*') 
                    if p.is_file() and p.suffix.lower() in self.image_extensions
                ]
            else:
                image_files = [
                    p for p in dir_path.glob('*') 
                    if p.is_file() and p.suffix.lower() in self.image_extensions
                ]
                
            if not image_files:
                print(f"Warning: No image files found in {dir_path}")
                return []
                
            total_files = len(image_files)
            print(f"Found {total_files} images to process")
            
            # Process one by one
            for i, img_path in enumerate(image_files):
                score = self.score_image(img_path)
                results.append((str(img_path), score))
                
                if progress_callback:
                    progress_callback(i + 1, total_files)
                    
            return results
            
        except Exception as e:
            print(f"Error scanning directory {dir_path}: {e}")
            return results  # Return any results we've gotten so far

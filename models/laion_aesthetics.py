import os
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Union, Optional, Tuple, List

# Use relative import for the base class
from .base import AestheticModel

class LAIONAestheticModel(AestheticModel):
    """LAION Aesthetic Predictor V2+ based on OpenCLIP embeddings"""
    
    def __init__(self, 
                 device: str = 'cpu',
                 model_name: str = "ViT-L-14", 
                 pretrained: str = "openai",
                 cache_dir: Optional[str] = None):
        """Initialize LAION Aesthetic Predictor
        
        Args:
            device: Computing device ('cpu' or 'cuda')
            model_name: OpenCLIP model variant ('ViT-L-14', 'ViT-H-14', etc.)
            pretrained: Pretrained weights source
            cache_dir: Directory to cache model weights
        """
        super().__init__(device)
        self.model_name = model_name
        self.pretrained = pretrained
        self.cache_dir = cache_dir or os.path.expanduser("~/.cache/zenkai-score")
        self.model = None
        self.processor = None
        self.mlp = None
        self.preprocess = None
        self.load()
        
    def load(self):
        """Load CLIP model and MLP aesthetic predictor"""
        os.makedirs(self.cache_dir, exist_ok=True)
        
        try:
            # Import here to avoid requiring these dependencies for package import
            import open_clip
            
            # Load base CLIP model
            self.model, _, self.preprocess = open_clip.create_model_and_transforms(
                self.model_name,
                pretrained=self.pretrained,
                device=self.device,
                cache_dir=self.cache_dir
            )
            
            # Load MLP aesthetic predictor
            self.mlp = self._load_aesthetic_mlp()
            
        except ImportError as e:
            raise ImportError(f"Failed to import required libraries: {e}. Please install with 'pip install open_clip_torch'")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    
    def _load_aesthetic_mlp(self):
        """Load the MLP that predicts aesthetic scores from CLIP embeddings"""
        # Define a simple linear layer architecture as in the notebook
        input_dim = {"ViT-L-14": 768, "ViT-B-32": 512}.get(self.model_name, 768)
        
        mlp = torch.nn.Linear(input_dim, 1)
        
        # Look for model in both potential cache locations
        alt_cache_dir = os.path.expanduser("~/.cache/emb_reader")
        weights_path = os.path.join(alt_cache_dir, f"sa_0_4_{self.model_name.lower().replace('-', '_')}_linear.pth")
        
        # Check if weights exist
        if not os.path.exists(weights_path):
            raise FileNotFoundError(
                f"Aesthetic model weights not found at {weights_path}. "
                "Please run the setup script first: 'python -m zenkai_score --setup'"
            )
        
        state_dict = torch.load(weights_path, map_location=self.device)
        mlp.load_state_dict(state_dict)
        mlp.to(self.device)
        mlp.eval()
        
        return mlp
    
    def _process_image(self, image_path: Union[str, Path]) -> torch.Tensor:
        """Process image for model input"""
        try:
            image = Image.open(image_path).convert("RGB")
            image_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
            return image_tensor
        except Exception as e:
            raise ValueError(f"Error processing image {image_path}: {e}")
    
    def predict(self, image_path: Union[str, Path]) -> float:
        """Predict aesthetic score for an image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Aesthetic score normalized to range 1.0-10.0
        """
        try:
            # Process image
            image_tensor = self._process_image(image_path)
            
            # Extract image features with CLIP - using the same approach as in the notebook
            with torch.no_grad():
                # Encode image
                image_features = self.model.encode_image(image_tensor)
                
                # Normalize features (matching the notebook's normalization approach)
                image_features /= image_features.norm(dim=-1, keepdim=True)
                
                # Predict aesthetic score with linear model
                raw_score = self.mlp(image_features).item()
                
                # Map the raw score to our 1-10 scale
                # Based on notebook examples (which output values around 5)
                # we'll scale to a more intuitive 1-10 range 
                normalized_score = min(max(raw_score + 5, 1.0), 10.0)
                
                return normalized_score
                
        except Exception as e:
            print(f"Error scoring image {image_path}: {e}")
            return 0.0
            
    def batch_predict(self, image_paths: List[Union[str, Path]]) -> List[float]:
        """Predict aesthetic scores for multiple images
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            List of aesthetic scores
        """
        batch_size = 16  # Adjust based on available memory
        all_scores = []
        
        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i:i+batch_size]
            batch_tensors = []
            
            for path in batch_paths:
                try:
                    image_tensor = self._process_image(path)
                    batch_tensors.append(image_tensor)
                except Exception as e:
                    print(f"Error processing image {path}: {e}")
                    all_scores.append(0.0)
            
            if batch_tensors:
                # Stack tensors and process batch
                batch_input = torch.cat(batch_tensors, dim=0)
                
                with torch.no_grad():
                    batch_features = self.model.encode_image(batch_input)
                    # Use the same normalization as in predict method
                    batch_features = batch_features / batch_features.norm(dim=-1, keepdim=True)
                    batch_scores = self.mlp(batch_features).squeeze().cpu().numpy()
                    
                    # Apply the same normalization as in predict method
                    # Map raw scores to 1-10 scale
                    batch_scores = np.clip(batch_scores + 5, 1.0, 10.0)
                    
                    all_scores.extend(batch_scores.tolist())
            
        return all_scores

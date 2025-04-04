from abc import ABC, abstractmethod
from typing import Union, List, Optional
from pathlib import Path
import torch

class AestheticModel(ABC):
    """Base interface for aesthetic scoring models"""
    
    def __init__(self, device: str = 'cpu'):
        """Initialize the aesthetic model
        
        Args:
            device: Computing device ('cpu', 'cuda', etc.)
        """
        self.device = device
        
    @abstractmethod
    def load(self):
        """Load model weights and prepare for inference
        
        This method should handle:
        - Loading model architecture
        - Loading weights from disk
        - Moving model to the correct device
        - Setting the model to evaluation mode
        """
        pass
        
    @abstractmethod
    def predict(self, image_path: Union[str, Path]) -> float:
        """Score a single image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Aesthetic score normalized to range 1.0-10.0
        """
        pass
        
    def batch_predict(self, image_paths: List[Union[str, Path]]) -> List[float]:
        """Predict aesthetic scores for multiple images
        
        Default implementation calls predict() for each image sequentially.
        Subclasses should override this for efficient batch processing.
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            List of aesthetic scores in the same order as image_paths
        """
        return [self.predict(path) for path in image_paths]
    
    def to(self, device: str) -> "AestheticModel":
        """Move model to specified device
        
        Args:
            device: Target device ('cpu', 'cuda', etc.)
            
        Returns:
            Self for method chaining
        """
        self.device = device
        return self
    
    @staticmethod
    def available_devices() -> List[str]:
        """Get list of available devices for inference
        
        Returns:
            List of available devices
        """
        devices = ['cpu']
        if torch.cuda.is_available():
            devices.extend([f'cuda:{i}' for i in range(torch.cuda.device_count())])
        return devices
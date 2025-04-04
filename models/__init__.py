"""
Zenkai-Score Model Registry

This module provides a registry of available aesthetic scoring models
and utilities for model loading.
"""

from typing import Dict, Type, Any, Optional, List, Union, Callable
import torch

# Use relative imports for modules within the same package
from .base import AestheticModel
from .laion_aesthetics import LAIONAestheticModel

# Registry of available models
MODEL_REGISTRY = {
    "laion_aesthetic": LAIONAestheticModel,
    "laion_aesthetic_vit_l_14": lambda **kwargs: LAIONAestheticModel(model_name="ViT-L-14", **kwargs),
    "laion_aesthetic_vit_b_32": lambda **kwargs: LAIONAestheticModel(model_name="ViT-B-32", **kwargs),
}

def get_model(model_name: str, **kwargs) -> AestheticModel:
    """Get model instance by name
    
    Args:
        model_name: Name of the model to load
        **kwargs: Additional arguments to pass to the model constructor
        
    Returns:
        Initialized model instance
    """
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model_name}. Available models: {', '.join(MODEL_REGISTRY.keys())}")
        
    return MODEL_REGISTRY[model_name](**kwargs)

def list_available_models() -> List[str]:
    """List all available aesthetic scoring models
    
    Returns:
        List of available model names
    """
    return list(MODEL_REGISTRY.keys())

def get_recommended_model(device: Optional[str] = None) -> str:
    """Get recommended model based on available hardware
    
    Args:
        device: Target device or None to auto-detect
        
    Returns:
        Name of recommended model
    """
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    if device == 'cpu':
        # For CPU, recommend the smallest model
        return "laion_aesthetic_vit_b_32"
    else:
        # For GPU, recommend the best quality model that will fit in memory
        try:
            total_mem = torch.cuda.get_device_properties(0).total_memory
            if total_mem >= 8 * 1024 * 1024 * 1024:  # 8GB+
                return "laion_aesthetic_vit_l_14"
            else:
                return "laion_aesthetic_vit_b_32"
        except Exception:
            # Default to medium size if we can't query GPU
            return "laion_aesthetic_vit_l_14"

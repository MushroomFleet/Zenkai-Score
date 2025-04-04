import os
import sys
from pathlib import Path
from typing import List, Optional
import shutil

from zenkai_score.utils.model_utils import download_model_weights

# Model configuration with download URLs and hashes
WEIGHT_DOWNLOAD_URLS = {
    "ViT-L-14": {
        "url": "https://github.com/LAION-AI/aesthetic-predictor/blob/main/sa_0_4_vit_l_14_linear.pth?raw=true",
        "md5": "placeholder_md5"  # Will be updated after download
    },
    "ViT-B-32": {
        "url": "https://github.com/LAION-AI/aesthetic-predictor/blob/main/sa_0_4_vit_b_32_linear.pth?raw=true",
        "md5": "placeholder_md5"  # Will be updated after download
    }
}

def setup_zenkai_score(cache_dir: Optional[str] = None, 
                      models_to_download: Optional[List[str]] = None,
                      force_download: bool = False) -> None:
    """Set up Zenkai-Score for first use
    
    Args:
        cache_dir: Directory to cache model weights
        models_to_download: List of model variants to download
        force_download: Force re-download even if files exist
    """
    # Support both cache locations
    cache_dir = cache_dir or os.path.expanduser("~/.cache/zenkai-score")
    alt_cache_dir = os.path.expanduser("~/.cache/emb_reader")
    
    models_to_download = models_to_download or ["ViT-L-14"]  # Default to ViT-L-14
    
    print(f"Setting up Zenkai-Score in {cache_dir}...")
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(alt_cache_dir, exist_ok=True)
    
    # Check for PyTorch and CUDA
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {cuda_available}")
        if cuda_available:
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU devices: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"  Device {i}: {torch.cuda.get_device_name(i)}")
    except ImportError:
        print("PyTorch not installed. Please install PyTorch: pip install torch")
        return
    
    # Check for other dependencies
    try:
        import open_clip
        print(f"OpenCLIP available: {open_clip.__version__}")
    except ImportError:
        print("OpenCLIP not installed. Please install: pip install open_clip_torch")
        return
    
    # Download and validate model weights
    for model_name in models_to_download:
        if model_name in WEIGHT_DOWNLOAD_URLS:
            model_info = WEIGHT_DOWNLOAD_URLS[model_name]
            # Use the same filename format as in the notebook
            output_path = os.path.join(alt_cache_dir, f"sa_0_4_{model_name.lower().replace('-', '_')}_linear.pth")
            
            download_needed = force_download or not os.path.exists(output_path)
            
            if download_needed:
                print(f"Downloading model weights for {model_name}...")
                success = download_model_weights(
                    model_info["url"],
                    output_path,
                    model_info["md5"]
                )
                
                if not success:
                    print(f"Failed to download model weights for {model_name}.")
                    continue
            else:
                print(f"Model weights for {model_name} already exist at {output_path}")
            
            # Validate the downloaded model
            print(f"Validating {model_name} model...")
            backup_path = output_path + ".bak"
            
            try:
                # Attempt to load the model to verify integrity
                from zenkai_score.models.laion_aesthetics import LAIONAestheticModel
                
                # Create a backup in case validation corrupts the file
                if os.path.exists(output_path) and not os.path.exists(backup_path):
                    shutil.copy2(output_path, backup_path)
                
                # Attempt to load model
                model = LAIONAestheticModel(model_name=model_name, device='cpu')
                
                # Remove backup if validation succeeds
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                    
                print(f"✓ Successfully validated {model_name} model.")
            except Exception as e:
                print(f"WARNING: Model validation failed: {e}")
                print("This might indicate corrupted model weights.")
                
                # Restore from backup if available
                if os.path.exists(backup_path):
                    print("Restoring model weights from backup...")
                    shutil.copy2(backup_path, output_path)
                    os.remove(backup_path)
                    print("Model weights restored from backup.")
                else:
                    print("No backup available to restore from.")
                    
                print(f"You may need to re-run setup with --force to re-download {model_name}.")
        else:
            print(f"Warning: Unknown model variant {model_name}")
    
    print("\nSetup complete! Zenkai-Score is ready to use.")
    print("\nExample usage:")
    print("  python -m zenkai_score /path/to/images --recursive")

if __name__ == "__main__":
    # Allow direct execution of setup.py
    args = sys.argv[1:]
    cache_dir = None
    models = ["ViT-L-14"]
    force = False
    
    if "--cache-dir" in args:
        idx = args.index("--cache-dir")
        if idx + 1 < len(args):
            cache_dir = args[idx + 1]
    
    if "--models" in args:
        idx = args.index("--models")
        if idx + 1 < len(args):
            models = args[idx + 1].split(",")
    
    if "--force" in args:
        force = True
        
    setup_zenkai_score(cache_dir=cache_dir, models_to_download=models, force_download=force)

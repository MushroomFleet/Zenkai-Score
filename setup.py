import os
import sys
from pathlib import Path
from urllib.request import urlretrieve
import shutil

def setup_zenkai_score(force_download: bool = False) -> None:
    """Set up Zenkai-Score for first use
    
    Args:
        force_download: Force re-download even if files exist
    """
    # Cache directory
    from os.path import expanduser
    cache_dir = expanduser("~/.cache/emb_reader")
    
    print(f"Setting up Zenkai-Score V2.0 in {cache_dir}...")
    os.makedirs(cache_dir, exist_ok=True)
    
    # Check for dependencies
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
        print(f"OpenCLIP available")
    except ImportError:
        print("OpenCLIP not installed. Please install: pip install open-clip-torch")
        return
    
    # Download model weights
    model_name = "vit_l_14"
    output_path = os.path.join(cache_dir, f"sa_0_4_{model_name}_linear.pth")
    url = f"https://github.com/LAION-AI/aesthetic-predictor/blob/main/sa_0_4_{model_name}_linear.pth?raw=true"
    
    download_needed = force_download or not os.path.exists(output_path)
    
    if download_needed:
        print(f"Downloading model weights...")
        try:
            print(f"Downloading from {url} to {output_path}")
            urlretrieve(url, output_path)
            print("Download completed successfully")
        except Exception as e:
            print(f"Failed to download model weights: {e}")
            return
    else:
        print(f"Model weights already exist at {output_path}")
    
    # Test loading model to verify
    try:
        import torch
        import torch.nn as nn
        
        s = torch.load(output_path)
        m = nn.Linear(768, 1)
        m.load_state_dict(s)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    print("\nSetup complete! Zenkai-Score V2.0 is ready to use.")
    print("\nExample usage:")
    print("  python -m zenkai_score /path/to/images --recursive")

def main():
    # Parse command line options
    import argparse
    parser = argparse.ArgumentParser(description="Zenkai-Score V2.0 Setup")
    parser.add_argument("--force", action="store_true", help="Force re-download of model weights")
    args = parser.parse_args()
    
    setup_zenkai_score(force_download=args.force)

if __name__ == "__main__":
    main()

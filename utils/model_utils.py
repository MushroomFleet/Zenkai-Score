import os
import requests
import hashlib
import csv
from tqdm import tqdm
from pathlib import Path
from typing import List, Tuple, Optional

def download_model_weights(url: str, output_path: str, expected_md5: Optional[str] = None) -> bool:
    """Download model weights with progress bar and verification
    
    Args:
        url: URL to download from
        output_path: Path to save the file
        expected_md5: Expected MD5 hash for verification
        
    Returns:
        True if download was successful
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Don't download if file already exists and hash matches
    if os.path.exists(output_path) and expected_md5:
        if verify_file_hash(output_path, expected_md5):
            print(f"Model weights already exist at {output_path} and hash verified.")
            return True
    
    # Download with progress bar
    print(f"Downloading model weights from {url}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_path, 'wb') as f, tqdm(
        desc=os.path.basename(output_path),
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)
    
    # Verify hash if provided
    if expected_md5:
        if verify_file_hash(output_path, expected_md5):
            print("Downloaded file verified successfully.")
            return True
        else:
            print("WARNING: File hash verification failed!")
            return False
    
    return True

def verify_file_hash(file_path: str, expected_md5: str) -> bool:
    """Verify file hash matches expected value
    
    Args:
        file_path: Path to file
        expected_md5: Expected MD5 hash
        
    Returns:
        True if hash matches
    """
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest() == expected_md5

def save_to_csv(results: List[Tuple[str, float]], output_path: str) -> None:
    """Save results to CSV file
    
    Args:
        results: List of (image_path, score) tuples
        output_path: Path to output CSV file
    """
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Image Path", "Aesthetic Score"])
        for path, score in results:
            writer.writerow([path, f"{score:.2f}"])
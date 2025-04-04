import os
import torch
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional, Union, Callable

class ZenkaiScore:
    """Core engine for Zenkai-Score aesthetic image scoring system"""
    
    def __init__(self, model=None, device: Optional[str] = None):
        """Initialize the Zenkai-Score engine
        
        Args:
            model: Aesthetic scoring model instance
            device: Device to run inference on ('cpu', 'cuda', etc.)
        """
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = model
        if self.model is None:
            # Load default model if none provided
            from zenkai_score.models import get_model
            self.model = get_model("laion_aesthetic_vit_l_14", device=self.device)
            
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    def score_image(self, image_path: Union[str, Path]) -> float:
        """Score a single image with better error handling
        
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
            return self.model.predict(str(image_path))
        except torch.cuda.OutOfMemoryError:
            print(f"CUDA out of memory when processing {image_path}. Falling back to CPU...")
            # Try processing on CPU as fallback
            original_device = self.model.device
            self.model.device = 'cpu'
            
            try:
                score = self.model.predict(str(image_path))
                self.model.device = original_device
                return score
            except Exception as inner_e:
                print(f"CPU fallback also failed for {image_path}: {inner_e}")
                self.model.device = original_device
                return 0.0
        except (torch.cuda.CudaError, RuntimeError) as e:
            if "CUDA" in str(e):
                print(f"CUDA error when processing {image_path}: {e}")
                return 0.0
            else:
                # Re-raise non-CUDA runtime errors
                raise
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            return 0.0
        except PermissionError:
            print(f"Error: Permission denied when accessing {image_path}")
            return 0.0
        except Exception as e:
            print(f"Error scoring image {image_path}: {e}")
            return 0.0
            
    def scan_directory(self, 
                      dir_path: Union[str, Path], 
                      recursive: bool = False,
                      batch_size: int = 16,
                      progress_callback: Optional[Callable[[int, int], None]] = None) -> List[Tuple[str, float]]:
        """Scan a directory for images and score them
        
        Args:
            dir_path: Directory path to scan
            recursive: Whether to scan subdirectories
            batch_size: Number of images to process in one batch
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
            
            # Process in batches for efficiency
            for i in range(0, total_files, batch_size):
                batch_paths = image_files[i:i+batch_size]
                
                try:
                    # Use batch prediction if available
                    if hasattr(self.model, 'batch_predict'):
                        batch_scores = self.model.batch_predict([str(p) for p in batch_paths])
                        batch_results = list(zip([str(p) for p in batch_paths], batch_scores))
                        results.extend(batch_results)
                    else:
                        # Fallback to individual processing
                        for img_path in batch_paths:
                            score = self.score_image(img_path)
                            results.append((str(img_path), score))
                except torch.cuda.OutOfMemoryError:
                    print(f"CUDA out of memory when processing batch. Reducing batch size and trying again...")
                    # Process one by one as fallback
                    for img_path in batch_paths:
                        score = self.score_image(img_path)
                        results.append((str(img_path), score))
                
                if progress_callback:
                    progress_callback(min(i + batch_size, total_files), total_files)
                    
            return results
            
        except Exception as e:
            print(f"Error scanning directory {dir_path}: {e}")
            return results  # Return any results we've gotten so far
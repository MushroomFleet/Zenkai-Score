import argparse
import time
import csv
from pathlib import Path
from typing import List, Tuple

from zenkai_score.core import ZenkaiScore

def save_to_csv(results: List[Tuple[str, float]], output_path: str):
    """Save scoring results to CSV file
    
    Args:
        results: List of (path, score) tuples
        output_path: Output CSV file path
    """
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Image', 'Aesthetic Score'])
        for path, score in results:
            writer.writerow([path, f"{score:.2f}"])
    
    print(f"Results saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Zenkai-Score V2.0: Image Aesthetic Scoring")
    
    # Setup argument
    parser.add_argument("--setup", action="store_true", help="Run first-time setup to download models")
    parser.add_argument("--force", action="store_true", help="Force re-download of model weights during setup")
    
    # Core arguments
    parser.add_argument("path", nargs="?", help="Path to image directory or single image")
    parser.add_argument("--recursive", "-r", action="store_true", help="Scan subdirectories recursively")
    parser.add_argument("--output", "-o", default="zenkai_scores.csv", help="Output CSV file path")
    
    # Device argument
    parser.add_argument("--device", "-d", default=None, help="Device to run on (cpu, cuda, etc.)")
    
    args = parser.parse_args()
    
    # Handle setup if requested
    if args.setup:
        from zenkai_score.setup import setup_zenkai_score
        setup_zenkai_score(force_download=args.force)
        return
    
    # Validate that a path was provided for scoring
    if args.path is None:
        parser.error("A path to an image or directory is required unless --setup is specified.")
    
    start_time = time.time()
    
    print(f"Initializing Zenkai-Score V2.0...")
    
    # Initialize scorer
    try:
        scorer = ZenkaiScore(device=args.device)
        
        path = Path(args.path)
        
        # Check if path is a file or directory
        if path.is_file():
            print(f"Scoring single image: {path}")
            score = scorer.score_image(path)
            results = [(str(path), score)]
        else:
            print(f"Scanning {'recursively ' if args.recursive else ''}in {args.path}...")
            
            # Simple progress tracking
            total_files = 0
            processed_files = 0
            
            def update_progress(current, total):
                nonlocal total_files, processed_files
                total_files = total
                processed_files = current
                print(f"Processing: {current}/{total} images", end="\r")
            
            results = scorer.scan_directory(
                args.path, 
                recursive=args.recursive,
                progress_callback=update_progress
            )
            print()  # New line after progress
        
        print(f"Saving results to {args.output}...")
        save_to_csv(results, args.output)
        
        # Print summary
        if results:
            avg_score = sum(score for _, score in results) / len(results)
            print(f"Processed {len(results)} images in {time.time() - start_time:.2f}s")
            print(f"Average aesthetic score: {avg_score:.2f}")
            
            # Print top 5 images
            sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
            print("\nTop 5 most aesthetic images:")
            for path, score in sorted_results[:5]:
                print(f"  {Path(path).name}: {score:.2f}")
        else:
            print("No images found to process.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

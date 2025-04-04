import argparse
import time
from pathlib import Path
from tqdm import tqdm

from zenkai_score.core import ZenkaiScore
from zenkai_score.models import get_model
from zenkai_score.utils.model_utils import save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Zenkai-Score: Image Aesthetic Scoring")
    
    # Core arguments
    parser.add_argument("path", help="Path to image directory")
    parser.add_argument("--recursive", "-r", action="store_true", help="Scan subdirectories recursively")
    parser.add_argument("--output", "-o", default="zenkai_scores.csv", help="Output CSV file path")
    
    # Model arguments
    parser.add_argument("--model", "-m", 
                      default="laion_aesthetic_vit_l_14", 
                      choices=["laion_aesthetic_vit_l_14", "laion_aesthetic_vit_h_14", "laion_aesthetic_vit_b_16"],
                      help="Aesthetic scoring model to use")
    parser.add_argument("--device", "-d", default=None, help="Device to run on (cpu, cuda:0, etc.)")
    parser.add_argument("--batch-size", "-b", type=int, default=16, help="Batch size for processing")
    
    # Setup arguments
    parser.add_argument("--setup", action="store_true", help="Run first-time setup")
    parser.add_argument("--cache-dir", default=None, help="Directory to cache model weights")
    
    args = parser.parse_args()
    
    # Handle setup if requested
    if args.setup:
        from zenkai_score.setup import setup_zenkai_score
        setup_zenkai_score(cache_dir=args.cache_dir, models_to_download=[args.model.split("_")[-3:]])
        return
    
    start_time = time.time()
    
    print(f"Initializing Zenkai-Score with {args.model} model...")
    
    # Initialize model
    model = get_model(args.model, device=args.device, cache_dir=args.cache_dir)
    scorer = ZenkaiScore(model=model)
    
    print(f"Scanning {'recursively ' if args.recursive else ''}in {args.path}...")
    with tqdm(total=0, unit="img") as pbar:
        def update_progress(current, total):
            pbar.total = total
            pbar.n = current
            pbar.refresh()
            
        results = scorer.scan_directory(
            args.path, 
            recursive=args.recursive,
            batch_size=args.batch_size,
            progress_callback=update_progress
        )
    
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

if __name__ == "__main__":
    main()
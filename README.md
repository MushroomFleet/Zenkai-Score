# Zenkai-Score v2.0

A streamlined image aesthetic scoring system based on LAION's aesthetic model.

## Overview

Zenkai-Score is a tool that analyzes and rates images based on their aesthetic qualities. It uses a machine learning model built on OpenCLIP embeddings and the LAION aesthetic predictor to assign scores from 1 to 10 to each image.

## Features

- Score individual images or entire directories
- Recursive directory scanning
- CSV report generation
- Support for various image formats (JPG, PNG, BMP, TIFF, WebP)
- GPU acceleration (when available)

## Installation

### Windows (Easiest)

1. Clone the repository:
   ```
   git clone https://github.com/MushroomFleet/Zenkai-Score.git
   cd Zenkai-Score
   ```

2. Run the included installer batch file:
   ```
   install.bat
   ```
   This will:
   - Create a Python virtual environment
   - Install all dependencies
   - Download required model weights
   - Set up the package for use

3. Use the provided batch file to run Zenkai-Score:
   ```
   Zenkai-Score.bat path\to\images
   ```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/zenkai-score.git
cd Zenkai-Score

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e zenkai_score

# Run setup to download model weights
python -m zenkai_score --setup
```

## Requirements

- Python 3.7+
- PyTorch 1.7+
- open-clip-torch 2.0+
- PIL/Pillow 7.0+
- tqdm 4.45+

## Usage

```bash
# Run first-time setup (downloads model weights)
python -m zenkai_score --setup

# Score a single image
python -m zenkai_score path/to/image.jpg

# Score all images in a directory
python -m zenkai_score path/to/images/

# Score all images in a directory and its subdirectories
python -m zenkai_score path/to/images/ --recursive

# Specify output file
python -m zenkai_score path/to/images/ --output scores.csv

# Specify device (CPU or CUDA)
python -m zenkai_score path/to/images/ --device cpu
```

## Testing the Installation

The package includes a test script and sample image to verify your installation:

```bash
# From the zenkai-score directory
python test.py
```

This will use the included test_cat.jpg image to verify that the model loads correctly and can score images.

## Python API

```python
from zenkai_score import ZenkaiScore

# Create scorer
scorer = ZenkaiScore(device='cuda')  # or 'cpu'

# Score a single image
score = scorer.score_image("path/to/image.jpg")
print(f"Image score: {score}")

# Score a directory of images
results = scorer.scan_directory("path/to/images/", recursive=True)
for path, score in results:
    print(f"{path}: {score}")
```

## Understanding Scores

Zenkai-Score rates images on a scale from 1.0 to 10.0:

- **1.0-3.0**: Low aesthetic quality
- **3.0-5.0**: Below average
- **5.0-7.0**: Average aesthetic quality
- **7.0-8.5**: Good aesthetic quality
- **8.5-10.0**: Exceptional aesthetic quality

The scoring is based on the LAION aesthetic predictor model, which was trained on millions of human aesthetic preference ratings.

## How It Works

1. Images are processed through OpenAI's CLIP ViT-L-14 model to extract visual features
2. These features are passed through a linear model trained by LAION to predict aesthetic quality
3. The raw score is normalized to a 1-10 scale for intuitive interpretation

## Troubleshooting

### Model Download Issues

If the model fails to download:
- Check your internet connection
- The model weights are stored in `~/.cache/emb_reader/sa_0_4_vit_l_14_linear.pth`
- You can force re-download with `python -m zenkai_score --setup --force`

### CUDA/GPU Issues

If you encounter CUDA errors:
- Try running with `--device cpu` to use CPU instead
- Make sure your PyTorch installation supports your GPU

### Import Errors

If you get import errors:
- Make sure you've installed all dependencies: `pip install -r requirements.txt`
- Make sure you've installed the package: `pip install -e zenkai_score`

## For More Information

See the included QUICKSTART.md for a condensed guide to get started quickly.

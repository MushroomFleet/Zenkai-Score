# Zenkai-Score V2.0 Quick Start Guide

This quick start guide will help you get Zenkai-Score up and running in minutes.

## Windows Installation (Easiest)

1. Clone and enter the repository:
   ```
   git clone https://github.com/yourusername/zenkai-score.git
   cd zenkai-score
   ```

2. Run the installer batch file:
   ```
   zenkai_score\install.bat
   ```
   This will:
   - Create a Python virtual environment
   - Install all dependencies
   - Download required model weights

3. Run Zenkai-Score:
   ```
   zenkai_score\Zenkai-Score.bat path\to\images
   ```

## Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/zenkai-score.git
   cd zenkai-score
   ```

2. Create a Python virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r zenkai_score/requirements.txt
   ```

4. Install the Zenkai-Score package:
   ```bash
   pip install -e zenkai_score
   ```

5. Run setup to download model weights:
   ```bash
   python -m zenkai_score --setup
   ```

## Scoring Images

Score a single image:
```bash
python -m zenkai_score path/to/image.jpg
```

Score all images in a directory:
```bash
python -m zenkai_score path/to/images/
```

Score recursively and specify an output file:
```bash
python -m zenkai_score path/to/images/ --recursive --output results.csv
```

## Command Line Options

- `--recursive`, `-r`: Scan subdirectories recursively
- `--output`, `-o`: Specify output CSV file path (default: zenkai_scores.csv)
- `--device`, `-d`: Specify device to run on (cpu, cuda, etc.)
- `--setup`: Run first-time setup to download models
- `--force`: Force re-download of model weights during setup

## Testing the Installation

To test if Zenkai-Score is working correctly, run:
```bash
python zenkai_score/test.py
```

This will attempt to score the included test image and report the result.

## Where Model Weights Are Stored

Model weights are downloaded to:
```
~/.cache/emb_reader/sa_0_4_vit_l_14_linear.pth

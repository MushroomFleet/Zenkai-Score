# ✨🎨 Zenkai-Score: AI-Powered Aesthetic Image Scoring 🎨✨

## 🚀🔥 What is Zenkai-Score? 🔥🚀

Zenkai-Score is a **blazingly fast** 🏎️💨 and **ridiculously accurate** 🎯 tool for scoring the aesthetic quality of your images! Using state-of-the-art AI models, Zenkai-Score analyzes your precious pixels and assigns them a score from 1-10 based on their visual awesomeness! 🧠👁️✨

![Zen Aesthetic](https://api.placeholder/600/300)

### 🌟 Key Features 🌟

- 🖼️ Score images on a 1-10 aesthetic scale with AI precision!
- 📁 Process entire directories of images with a single command!
- 🔍 Recursively scan folders to find ALL your beautiful photos!
- 📊 Generate CSV reports for easy sorting and filtering!
- 🧠 Powered by LAION Aesthetic Predictor V2+ with OpenCLIP!
- 🚄 Optimized batch processing for MAXIMUM SPEED! 🚄
- 💻 Simple command-line interface for both novices and power users!

## 💾 Installation 💾

### 🪄 Windows Magic Installation 🪄

Simply run the included `install.bat` file and BOOM! 💥 You're ready to go!

```batch
install.bat
```

This magical script will:
1. 🏗️ Create a fresh Python virtual environment
2. 📦 Install all required dependencies 
3. 📥 Download the necessary model weights
4. 🎉 Set everything up for INSTANT GRATIFICATION! 🎉

### 🐧 Manual Installation (Linux/Mac/Rebellious Windows Users) 🐧

```bash
# Create a virtual environment (because mixing dependencies is for CHUMPS! 🙅‍♂️)
python -m venv venv

# Activate the virtual environment (UNLIMITED POWER! ⚡)
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies (the DIGITAL NUTRIENTS your program needs! 🍲)
pip install -r requirements.txt

# Run first-time setup (MODEL DOWNLOADING TIME! 📥⏱️)
python -m zenkai_score --setup
```

## 🎮 Usage 🎮

### 🖱️ Windows One-Click Launcher 🖱️

Run `Zenkai-Score.bat` followed by your desired options:

```batch
Zenkai-Score.bat C:\path\to\your\amazing\images --recursive
```

### 🐧 Command Line Usage (Any OS) 🐧

```bash
# Activate the virtual environment (ENHANCE YOUR PYTHON! 💪)
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Run Zenkai-Score with your chosen options (GO! GO! GO! 🚀)
python -m zenkai_score /path/to/your/images --recursive
```

### 📋 Command Options 📋

```
python -m zenkai_score [PATH] [OPTIONS]

Arguments:
  PATH                  Directory containing images to score (REQUIRED! 📁)

Options:
  --recursive, -r       Scan subdirectories recursively (DEEPER LEVELS! 🕳️)
  --output, -o          Specify output CSV file path (SAVE ANYWHERE! 💾)
  --model, -m           Choose aesthetic model (BRAIN SELECTION! 🧠)
                        Options: laion_aesthetic_vit_l_14 (default), 
                                laion_aesthetic_vit_h_14, 
                                laion_aesthetic_vit_b_16
  --batch-size, -b      Set processing batch size (SPEED VS MEMORY! ⚖️)
  --device, -d          Select processing device (CPU/CUDA) (HARDWARE CHOICE! 🖥️)
  --setup               Run first-time setup (MODEL DOWNLOADING! 📥)
```

### 🔥 Examples 🔥

Score a single directory of vacation photos:
```bash
python -m zenkai_score C:\Users\YourName\Pictures\Vacation2023
```

Score your ENTIRE photo collection (recursively):
```bash
python -m zenkai_score C:\Users\YourName\Pictures -r
```

Use the HIGHEST QUALITY model and save results to a specific location:
```bash
python -m zenkai_score C:\Photos -m laion_aesthetic_vit_h_14 -o vacation_scores.csv
```

Process smaller batches on a memory-constrained system:
```bash
python -m zenkai_score C:\huge_image_collection -b 4
```

## 📈 Understanding Your Results 📈

Zenkai-Score outputs a CSV file with image paths and their aesthetic scores:

| Image Path | Aesthetic Score |
|------------|-----------------|
| /path/to/amazing_sunset.jpg | 8.74 |
| /path/to/blurry_cat.jpg | 3.21 |
| /path/to/perfect_portrait.jpg | 9.56 |

Score interpretation:
- 🙈 **1.0-3.0**: Aesthetically challenged (we can't all be winners!)
- 😐 **3.1-5.0**: Meh... could be better (room for improvement!)
- 😊 **5.1-7.0**: Pretty good! (solid work!)
- 😍 **7.1-9.0**: Excellent! (share these on social media!)
- 🤯 **9.1-10.0**: MIND-BLOWING AESTHETIC PERFECTION! (submit to contests immediately!)

## 🐍 Python API Usage 🐍

Want to integrate Zenkai-Score into your Python project? It's RIDICULOUSLY EASY! 🎯

```python
from zenkai_score.core import ZenkaiScore

# Initialize the aesthetic scoring engine (POWER UP! 💪)
scorer = ZenkaiScore()

# Score a single image (JUDGE THAT JPEG! 👨‍⚖️)
score = scorer.score_image("path/to/image.jpg")
print(f"This image scores: {score:.2f}/10")

# Process an entire directory (BATCH ATTACK! 📊)
results = scorer.scan_directory("path/to/directory", recursive=True)

# Find your TOP 5 images (THE ELITE SQUAD! 🏆)
sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
for path, score in sorted_results[:5]:
    print(f"{path}: {score:.2f}")
```

## 🔧 Troubleshooting 🔧

### ❓ Common Issues ❓

- 😵 **Error loading model weights?** 
  - Run `python -m zenkai_score --setup` to download them!
  - Check your internet connection! 📶
  - Make sure you have enough disk space! 💽

- 🐢 **Processing too slow?** 
  - Try using a smaller model with `-m laion_aesthetic_vit_b_16` 🏎️
  - Increase batch size with `-b 32` (if you have the RAM!) 🐏
  - Make sure you're using a GPU if available with `-d cuda` ⚡

- 🧠 **Out of memory?** 
  - Reduce batch size with `-b 4` 📉
  - Use a smaller model variant 🤏
  - Close Chrome with its 500 open tabs! 🙄

- 📂 **Can't find images?** 
  - Double-check your path! 🔍
  - Try using `--recursive` to search subdirectories! 🕳️
  - Make sure your files have supported extensions (.jpg, .png, etc) 📑

## 🔮 Future Enhancements 🔮

We've barely scratched the surface of what Zenkai-Score could become! 🚀

- 📊 Interactive dashboard with score visualizations! 
- 🖼️ HTML gallery generation sorted by aesthetic score!
- 🤖 Custom model training for YOUR specific aesthetic preferences!
- 🔗 Integration with photo management software!
- 📱 Mobile app for on-the-go aesthetic scoring!
- 🌈 Style-specific scoring (landscapes, portraits, architecture, etc)!
- 🔍 Similar image finding based on aesthetic embeddings!

## 💖 Acknowledgements 💖

Zenkai-Score wouldn't exist without these AMAZING projects:

- 🧠 LAION for their groundbreaking aesthetic predictors
- 🖼️ OpenCLIP for powerful visual embeddings
- 🔬 The computational aesthetics research community
- 🤗 Open source contributors everywhere!

## 🎉 Enjoy Zenkai-Score! 🎉

Remember: Aesthetic beauty is subjective, but with AI, we can PRETEND it's objective! 🤣

May your images be beautiful and your scores be high! 📸✨
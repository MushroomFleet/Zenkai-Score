from setuptools import setup, find_packages

setup(
    name="zenkai_score",
    version="2.0.0",
    description="Image aesthetic scoring system based on LAION model",
    author="Zenkai Score Team",
    packages=find_packages(),
    install_requires=[
        "torch>=1.7.0",
        "open-clip-torch>=2.0.0",
        "pillow>=7.0.0",
        "tqdm>=4.45.0",
    ],
    entry_points={
        "console_scripts": [
            "zenkai-score=zenkai_score.cli:main",
        ],
    },
    python_requires=">=3.7",
)

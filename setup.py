"""
Setup script for Film Dubbing Application
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="film-dubbing-app",
    version="1.0.0",
    author="Film Dubbing Team",
    description="Professional film dubbing application with AI-powered translation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stanhrynkiewicz-bot/Filmy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai-whisper>=20231117",
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "numpy>=1.24.0",
        "moviepy>=1.0.3",
        "pydub>=0.25.1",
        "deep-translator>=1.11.4",
        "TTS>=0.22.0",
        "PyQt5>=5.15.9",
        "Pillow>=10.0.0",
        "SoundFile>=0.12.1",
        "scipy>=1.11.0",
        "ffmpeg-python>=0.2.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "dubbing-app=dubbing_app:main",
        ],
    },
)

#  Space-Filling Curves & Image Processing

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Mathématiques](https://img.shields.io/badge/Math%C3%A9matiques-Mod%C3%A9lisation-orange)
![TIPE](https://img.shields.io/badge/TIPE-2025-success)


##  About The Project
This repository contains the source code and analysis for my **TIPE (Travaux d'Initiative Personnelle Encadrés)** project. It explores the mathematical properties of **space-filling curves** (specifically Hilbert, Morton/Z-Order, and Peano curves) and proposes a software implementation of their applications in **image processing**, **dithering**, and **lossless compression optimization**.

The main objective is to demonstrate how changing the spatial traversal of a standard matrix image (from linear to fractal) can significantly optimize the efficiency of standard data compression algorithms.

##  Architecture & Features

The codebase is structured modularly around several key components:

### 1. Mathematical Modeling (`src/curves/`)
- Recursive generation and coordinate calculation for **Hilbert**, **Morton**, and **Peano** curves.
- Adaptation of these bijective mappings $f: [0,1] \to [0,1]^2$ to discrete pixel grids.

### 2. Image Processing (`src/processing/`)
Complete implementation of error-diffusion algorithms:
- **Atkinson Algorithm** (adapted to follow generated fractal paths).
- **Floyd-Steinberg Algorithm**.
- Grayscale conversion and N-bit color quantization.

### 3. Metrics & Compression (`src/metrics/`)
- Calculation of **Shannon Entropy** using `scipy.stats` on processed images.
- Simulation of a lossless compression pipeline by comparing raw payload size with `gzip` encoding.

### 4. Color Palette Sorting (`src/processing/color_sorting.py`)
- Experiments on sorting RGB palettes (64 colors) using different heuristics: *Sweep* (lexicographical), *Scan* (boustrophedon), and fractal paths (Hilbert, Morton).

##  Key Results

Guiding the dithering algorithm (Atkinson) along a Hilbert curve preserves 2D spatial locality much better than a standard linear scan ("Raster/Serpent"). This spatial grouping of similar pixels allows run-length encoding compressors (like GZIP) to perform exceptionally well.

**Performance on a standard test image:**
- Algorithmic gain (Hilbert vs. Linear traversal) for the exact same dithering method: **~3.2% additional compression**.
- **Global size reduction:** Compressing the 1-bit Hilbert-dithered image reduces the original raw 8-bit image size by **up to 89%**.
- Complexity analysis (`benchmarks/`) shows that the Morton path is roughly 10× faster to compute than Hilbert, but at the cost of reduced compression efficiency due to larger spatial jumps.
  **Algorithmic Performance Benchmarks:**
![Sorting Benchmark](assets/benchmark_sorting_comparison.png)
*Time to sort 64 RGB colors using different space-filling curves*

![Time Complexity](assets/benchmark_time_complexity.png)
*Computation time scaling: Morton is ~10× faster than Hilbert, but Hilbert provides superior spatial locality for compression*

## 📂 Repository Structure
```
├── README.md                           # Main documentation
├── requirements.txt                    # Python dependencies
├── main_pipeline.py                    #  A recap of what the project is about
├── notebooks/
│   └── demo_TIPE.ipynb                 #  Interactive Jupyter Notebook demo
├── presentation/                       # TIPE presentation slides
├── data/
│   ├── input/                          # Source images (hopper.png)
│   └── output/                         # Processed/compressed images
├── benchmarks/                         # Algorithmic complexity scripts
│   ├── complexite_temporelle.py        # Hilbert vs. Morton computation time
│   └── complexite_tri.py               # Sorting heuristics benchmark
└── src/                                # Core modules package
    ├── curves/                         # Trajectory generation (Hilbert, Morton, Peano)
    ├── processing/                     # Dithering and color manipulation
    └── metrics/                        # Entropy and compression analysis
```
## Installation
Make sure you have Python 3.8+ installed. Clone this repository and install the dependencies:
```
git clone https://github.com/sami-ennedoui/TIPE-SpaceFillingCurves.git
cd TIPE-SpaceFillingCurves
pip install -r requirements.txt
```
## Quick start guide
#### 1. Run the end to end pipeline
The main script executes the full processing chain: image loading, dithering (Hilbert vs. Linear), entropy calculation, and data export:
```
cd TIPE-SpaceFillingCurves
python main_pipeline.py
```
#### 2. Interactive Demo
For a visual exploration of the algorithms, check out the Jupyter Notebook:
```
jupyter notebook notebooks/demo_TIPE.ipynb
```
#### 3. Algorithmic benchmarks
To reproduce the time complexity studies:
```
python benchmarks/complexite_temporelle.py
python benchmarks/complexite_tri.py
```
## Built with 
- `numpy`, `scipy` (Matrix calculations, statistics, and entropy)
- `Pillow` (Image I/O manipulation)
- `matplotlib`, `reportlab` (Datavisualization and PDF generation)
- `Hilbertcurve`, `pymorton` (Generation of the Hilbert and morton ordering)

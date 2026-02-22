from __future__ import annotations

import os
from pathlib import Path
import gzip
import numpy as np
from PIL import Image
from scipy.stats import entropy as shannon_entropy
from hilbertcurve.hilbertcurve import HilbertCurve


# ----------------------------
# I/O utilities
# ----------------------------
def load_grayscale_image(path: str | Path, size: tuple[int, int] = (256, 256)) -> np.ndarray:
    """
    Load an image as grayscale in [0, 1], resized to `size`.
    If the file does not exist, generate a synthetic grayscale gradient.
    """
    path = Path(path)
    if path.exists():
        img = Image.open(path).convert("L").resize(size)
    else:
        width, height = size
        gradient = np.tile(np.linspace(0, 255, width, dtype=np.uint8), (height, 1))
        img = Image.fromarray(gradient, mode="L")

    return np.asarray(img, dtype=np.float32) / 255.0


def save_1bit_png(image01: np.ndarray, path: str | Path) -> None:
    """
    Save a binary (0/1) image as a true 1-bit PNG.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.fromarray((image01 > 0.5).astype(np.uint8) * 255, mode="L")
    img_1bit = img.convert("1")
    img_1bit.save(path, compress_level=0)


# ----------------------------
# Space-filling paths
# ----------------------------
def hilbert_path(width: int, height: int) -> list[tuple[int, int]]:
    """
    Return pixel coordinates ordered by 2D Hilbert curve (covering the smallest power-of-two square).
    """
    n = max(width, height)
    p = 1
    order = 0
    while p < n:
        p <<= 1
        order += 1

    curve = HilbertCurve(order, 2)
    coords = []
    for y in range(p):
        for x in range(p):
            d = curve.distance_from_point([x, y])
            if 0 <= x < width and 0 <= y < height:
                coords.append((d, x, y))

    coords.sort(key=lambda t: t[0])
    return [(x, y) for _, x, y in coords]


def raster_path(width: int, height: int) -> list[tuple[int, int]]:
    """
    Standard left-to-right, top-to-bottom raster scan.
    """
    return [(x, y) for y in range(height) for x in range(width)]


# ----------------------------
# Dithering
# ----------------------------
def atkinson_dither_grayscale(image01: np.ndarray, path: list[tuple[int, int]]) -> np.ndarray:
    """
    Atkinson error diffusion dithering following a given pixel traversal path.
    Input/output in {0,1} with internal error propagation on float copy.
    """
    h, w = image01.shape
    work = image01.copy()
    out = np.zeros_like(work)

    neighbors = [(1, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (0, 2)]

    for x, y in path:
        old = work[y, x]
        new = 1.0 if old > 0.5 else 0.0
        out[y, x] = new

        err = (old - new) / 8.0
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                work[ny, nx] += err

    return out


# ----------------------------
# Metrics
# ----------------------------
def shannon_entropy_bits_per_pixel(image01: np.ndarray) -> float:
    """
    Shannon entropy (bits/pixel) estimated from a 256-bin histogram over [0,1].
    """
    hist, _ = np.histogram(image01.flatten(), bins=256, range=(0, 1), density=True)
    hist = hist[hist > 0]
    return float(shannon_entropy(hist, base=2))


def gzip_size_bytes_of_raw_u8(image01: np.ndarray) -> int:
    """
    Compute gzip-compressed size of raw uint8 bytes (like your TIPE scripts do).
    """
    raw = (image01 * 255).astype(np.uint8).tobytes()
    return len(gzip.compress(raw))


# ----------------------------
# Main demo
# ----------------------------
def main() -> None:
    input_path = Path("data/input/hopper.png")
    output_dir = Path("data/output")

    print("=== TIPE Demo: Hilbert traversal for dithering & compression ===")
    image = load_grayscale_image(input_path, size=(256, 256))
    h, w = image.shape
    print(f"Loaded image shape: {image.shape}")

    print("Building traversal paths...")
    path_h = hilbert_path(w, h)
    path_r = raster_path(w, h)

    print("Running Atkinson dithering...")
    d_h = atkinson_dither_grayscale(image, path_h)
    d_r = atkinson_dither_grayscale(image, path_r)

    print("Saving outputs...")
    save_1bit_png(d_h, output_dir / "dither_hilbert_1bit.png")
    save_1bit_png(d_r, output_dir / "dither_raster_1bit.png")

    print("\n--- Metrics (dithered images) ---")
    ent_h = shannon_entropy_bits_per_pixel(d_h)
    ent_r = shannon_entropy_bits_per_pixel(d_r)
    gz_h = gzip_size_bytes_of_raw_u8(d_h)
    gz_r = gzip_size_bytes_of_raw_u8(d_r)

    print(f"Raster  : entropy={ent_r:.4f} bits/pixel | gzip(raw)={gz_r} bytes")
    print(f"Hilbert : entropy={ent_h:.4f} bits/pixel | gzip(raw)={gz_h} bytes")

    if gz_r > 0:
        gain = 100.0 * (gz_r - gz_h) / gz_r
        print(f"\nCompression gain (Hilbert vs raster): {gain:.2f}%")

    # Optional: show "global" reduction relative to raw 8-bit grayscale payload
    raw_gray_bytes = w * h  # 1 byte per pixel (uint8 grayscale)
    global_reduction = 100.0 * (raw_gray_bytes - gz_h) / raw_gray_bytes
    print(f"Global reduction vs raw 8-bit grayscale (Hilbert dither + gzip): {global_reduction:.2f}%")


if __name__ == "__main__":
    main()

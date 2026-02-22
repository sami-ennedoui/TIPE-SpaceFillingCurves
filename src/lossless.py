import numpy as np
from PIL import Image
from pymorton import interleave2
from hilbertcurve.hilbertcurve import HilbertCurve
import os
import gzip
import bz2
import lzma
import shutil

def charger_image_rgb():
    if os.path.exists("hopper.png"):
        img = Image.open("hopper.png").convert("RGB")
    else:
        largeur, hauteur = 256, 256
        gradient = np.tile(np.linspace(0, 255, largeur, dtype=np.uint8), (hauteur, 1))
        img = np.stack([gradient, gradient, gradient], axis=2)
        img = Image.fromarray(img, mode="RGB")
    img_np = np.array(img) / 255.0
    return img_np

def coords_hilbert(w, h):
    n = max(w, h)
    p = 1
    ordre = 0
    while p < n:
        p <<= 1
        ordre += 1
    courbe = HilbertCurve(ordre, 2)
    coords = []
    for y in range(p):
        for x in range(p):
            d = courbe.distance_from_point([x, y])
            if 0 <= x < w and 0 <= y < h:
                coords.append((d, x, y))
    coords.sort()
    return [(x, y) for _, x, y in coords]

def coords_morton(w, h):
    n = max(w, h)
    p = 1
    while p < n:
        p <<= 1
    coords = []
    for y in range(p):
        for x in range(p):
            code = interleave2(x, y)
            if 0 <= x < w and 0 <= y < h:
                coords.append((code, x, y))
    coords.sort()
    return [(x, y) for _, x, y in coords]

def coords_serpent(w, h):
    coords = []
    for y in range(h):
        for x in range(w):
            coords.append((x, y))
    return coords

def atkinson_dither(image_channel, coords):
    h, w = image_channel.shape
    img = image_channel.copy()
    sortie = np.zeros_like(img)
    voisins = [(1, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (0, 2)]
    for x, y in coords:
        ancien_pixel = img[y, x]
        nouveau_pixel = float(ancien_pixel > 0.5)
        sortie[y, x] = nouveau_pixel
        erreur = (ancien_pixel - nouveau_pixel) / 8
        for dx, dy in voisins:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                img[ny, nx] += erreur
    return sortie

def dither_rgb_1bit(image_rgb, coords):
    R = atkinson_dither(image_rgb[:, :, 0], coords)
    G = atkinson_dither(image_rgb[:, :, 1], coords)
    B = atkinson_dither(image_rgb[:, :, 2], coords)
    image_rgb_dithered = np.stack([R, G, B], axis=2)
    return image_rgb_dithered

def exporter_png_rgb(image_np, nom_fichier):
    img = Image.fromarray((image_np * 255).astype(np.uint8), mode="RGB")
    img.save(nom_fichier, compress_level=0)

def exporter_png_1bit(image_np, nom_fichier):
    img = Image.fromarray((image_np > 0.5).astype(np.uint8) * 255, mode="L")
    img_1bit = img.convert("1")
    img_1bit.save(nom_fichier, compress_level=0)

def compresser_gzip(nom_fichier):
    with open(nom_fichier, "rb") as f_in:
        with gzip.open(nom_fichier + ".gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    return os.path.getsize(nom_fichier + ".gz")

def compresser_bz2(nom_fichier):
    with open(nom_fichier, "rb") as f_in:
        with bz2.open(nom_fichier + ".bz2", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    return os.path.getsize(nom_fichier + ".bz2")

def compresser_lzma(nom_fichier):
    with open(nom_fichier, "rb") as f_in:
        with lzma.open(nom_fichier + ".xz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    return os.path.getsize(nom_fichier + ".xz")

image_orig_rgb = charger_image_rgb()
hauteur, largeur = image_orig_rgb.shape[0], image_orig_rgb.shape[1]
image_orig_gray = np.mean(image_orig_rgb, axis=2)

coords_h = coords_hilbert(largeur, hauteur)
coords_m = coords_morton(largeur, hauteur)
coords_s = coords_serpent(largeur, hauteur)

image_h_rgb = dither_rgb_1bit(image_orig_rgb, coords_h)
image_m_rgb = dither_rgb_1bit(image_orig_rgb, coords_m)
image_s_rgb = dither_rgb_1bit(image_orig_rgb, coords_s)

exporter_png_rgb(image_orig_rgb, "original.png")
exporter_png_rgb(image_h_rgb, "hilbert.png")
exporter_png_rgb(image_m_rgb, "morton.png")
exporter_png_rgb(image_s_rgb, "scan.png")

taille_gzip_original = compresser_gzip("original.png")
taille_bz2_original = compresser_bz2("original.png")
taille_lzma_original = compresser_lzma("original.png")

taille_gzip_hilbert = compresser_gzip("hilbert.png")
taille_bz2_hilbert = compresser_bz2("hilbert.png")
taille_lzma_hilbert = compresser_lzma("hilbert.png")

taille_gzip_morton = compresser_gzip("morton.png")
taille_bz2_morton = compresser_bz2("morton.png")
taille_lzma_morton = compresser_lzma("morton.png")

taille_gzip_scan = compresser_gzip("scan.png")
taille_bz2_scan = compresser_bz2("scan.png")
taille_lzma_scan = compresser_lzma("scan.png")

print("Original :", taille_gzip_original, taille_bz2_original, taille_lzma_original)
print("Hilbert :", taille_gzip_hilbert, taille_bz2_hilbert, taille_lzma_hilbert)
print("Morton :", taille_gzip_morton, taille_bz2_morton, taille_lzma_morton)
print("Scan :", taille_gzip_scan, taille_bz2_scan, taille_lzma_scan)

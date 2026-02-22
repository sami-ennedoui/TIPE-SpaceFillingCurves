import numpy as np
from PIL import Image
from hilbertcurve.hilbertcurve import HilbertCurve
import os

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

def exporter_png_1bit(image_np, nom_fichier):
    img = Image.fromarray((image_np > 0.5).astype(np.uint8) * 255, mode="L")
    img_1bit = img.convert("1")  # vrai PNG 1 bit
    img_1bit.save(nom_fichier, compress_level=0)

def exporter_png_gray(image_np, nom_fichier):
    img = Image.fromarray((image_np * 255).astype(np.uint8), mode="L")
    img.save(nom_fichier, compress_level=0)

image_orig_rgb = charger_image_rgb()
hauteur, largeur = image_orig_rgb.shape[0], image_orig_rgb.shape[1]
image_orig_gray = np.mean(image_orig_rgb, axis=2)

coords_h = coords_hilbert(largeur, hauteur)

image_h_bw = atkinson_dither(image_orig_gray, coords_h)

exporter_png_gray(image_orig_gray, "original_gray.png")
exporter_png_1bit(image_h_bw, "dithered_hilbert.png")

print(f"Taille de original_gray.png : {os.path.getsize('original_gray.png')} octets")
print(f"Taille de dithered_hilbert.png : {os.path.getsize('dithered_hilbert.png')} octets")

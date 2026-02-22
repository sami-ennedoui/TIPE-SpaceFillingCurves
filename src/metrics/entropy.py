import numpy as np
from PIL import Image
from pymorton import interleave2
from hilbertcurve.hilbertcurve import HilbertCurve
import os
import gzip
import shutil
from scipy.stats import entropy
def calculer_entropy(image_np):
    hist, _ = np.histogram(image_np.flatten(), bins=256, range=(0,1), density=True)
    hist = hist[hist > 0]  # éviter log(0)
    return entropy(hist, base=2)

# === Fonction pour sauvegarder RAW + compresser GZIP ===
def exporter_raw_gzip(image_np, nom_base):
    raw_name = nom_base + ".raw"
    gzip_name = nom_base + ".raw.gz"
    
    image_bytes = (image_np * 255).astype(np.uint8).tobytes()
    with open(raw_name, "wb") as f:
        f.write(image_bytes)
    
    with open(raw_name, "rb") as f_in:
        with gzip.open(gzip_name, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # Supprimer fichier RAW temporaire
    os.remove(raw_name)
    
    # Retourner la taille du gzip
    return os.path.getsize(gzip_name)

def charger_image_rgb():
    if os.path.exists("hopper.png"):
        img = Image.open("hopper.png").convert("RGB")
    else:
        largeur, hauteur = 256, 256
        gradient = np.tile(np.linspace(0, 255, largeur, dtype=np.uint8), (hauteur, 1))
        img = np.stack([gradient, gradient, gradient], axis=2)
        img = Image.fromarray(img, mode="RGB")
    img_np = np.array(img) / 255.0
    print(f"Image chargée : {img_np.shape}")
    return img_np

# Courbes
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

# Atkinson (canal unique) 
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

# Dither RGB par canal
def dither_rgb_1bit(image_rgb, coords):
    R = atkinson_dither(image_rgb[:, :, 0], coords)
    G = atkinson_dither(image_rgb[:, :, 1], coords)
    B = atkinson_dither(image_rgb[:, :, 2], coords)
    image_rgb_dithered = np.stack([R, G, B], axis=2)
    return image_rgb_dithered

# Export PNG 1-bit (grayscale)
def exporter_png_1bit(image_np, nom_fichier):
    img = Image.fromarray((image_np > 0.5).astype(np.uint8) * 255, mode="L")
    img_1bit = img.convert("1")  # vrai PNG 1 bit
    img_1bit.save(nom_fichier, compress_level=0)

# Export PNG palette (RGB compressé)
def exporter_png_palette(image_np, nom_fichier):
    img = Image.fromarray((image_np * 255).astype(np.uint8), mode="RGB")
    img_palette = img.convert("P", palette=Image.ADAPTIVE, colors=8)
    img_palette.save(nom_fichier, compress_level=0)

# Export PNG RGB (plein)
def exporter_png_rgb(image_np, nom_fichier):
    img = Image.fromarray((image_np * 255).astype(np.uint8), mode="RGB")
    img.save(nom_fichier, compress_level=0)

# === Main ===
image_orig_rgb = charger_image_rgb()
hauteur, largeur = image_orig_rgb.shape[0], image_orig_rgb.shape[1]

# Grayscale image for 1-bit export
image_orig_gray = np.mean(image_orig_rgb, axis=2)

# Generate coordinate lists for curves
coords_h = coords_hilbert(largeur, hauteur)
coords_m = coords_morton(largeur, hauteur)
coords_s = coords_serpent(largeur, hauteur)

# Perform dithering on grayscale
image_h_bw = atkinson_dither(image_orig_gray, coords_h)
image_m_bw = atkinson_dither(image_orig_gray, coords_m)
image_s_bw = atkinson_dither(image_orig_gray, coords_s)

# Perform dithering + quantization on RGB channels
image_h_rgb = dither_rgb_1bit(image_orig_rgb, coords_h)
image_m_rgb = dither_rgb_1bit(image_orig_rgb, coords_m)
image_s_rgb = dither_rgb_1bit(image_orig_rgb, coords_s)

# Now define the image lists (after the above variables exist)
images_bw = [
    ("Hilbert", image_h_bw),
    ("Morton", image_m_bw),
    ("Serpent", image_s_bw),
]

images_rgb = [
    ("Hilbert", image_h_rgb),
    ("Morton", image_m_rgb),
    ("Serpent", image_s_rgb),
]

# Save output files
exporter_png_rgb(image_orig_rgb, "doriginal.png")

exporter_png_1bit(image_h_bw, "dhilbert_bw.png")
exporter_png_1bit(image_m_bw, "dmorton_bw.png")
exporter_png_1bit(image_s_bw, "dsnake_bw.png")

exporter_png_palette(image_h_rgb, "dhilbert_palette.png")
exporter_png_palette(image_m_rgb, "dmorton_palette.png")
exporter_png_palette(image_s_rgb, "dsnake_palette.png")

# === Analyze file sizes ===
fichiers = [
    "doriginal.png",
    "dhilbert_bw.png",
    "dmorton_bw.png",
    "dsnake_bw.png",
    "dhilbert_palette.png",
    "dmorton_palette.png",
    "dsnake_palette.png"
]

print("\nComparaison des tailles de fichiers (en octets) :")
for f in fichiers:
    taille = os.path.getsize(f)
    print(f"{f} : {taille} octets")

# === Analyse BW ===
print("\n== Résultats BW ==\n")
print(f"{'Méthode':<10} | Entropie (bits/pixel) | Taille gzip (octets)")
print("-" * 50)
for nom, img in images_bw:
    ent = calculer_entropy(img)
    size_gz = exporter_raw_gzip(img, f"export_{nom}_bw")
    print(f"{nom:<10} | {ent:>8.4f}              | {size_gz:>10} ")

# === Analyse RGB ===
print("\n== Résultats RGB ==\n")
print(f"{'Méthode':<10} | Entropie (bits/pixel) | Taille gzip (octets)")
print("-" * 50)
for nom, img in images_rgb:
    ent = calculer_entropy(img)
    size_gz = exporter_raw_gzip(img, f"export_{nom}_rgb")
    print(f"{nom:<10} | {ent:>8.4f}              | {size_gz:>10} ")

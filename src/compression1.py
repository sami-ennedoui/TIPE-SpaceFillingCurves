import numpy as np
from PIL import Image
from pymorton import interleave2
from hilbertcurve.hilbertcurve import HilbertCurve
def charger_image_rgb():
    img = Image.open("hopper.png").convert("RGB")
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

# Main
image_orig_rgb = charger_image_rgb()
hauteur, largeur = image_orig_rgb.shape[0], image_orig_rgb.shape[1]
# Grayscale image pour export 1 bit
image_orig_gray = np.mean(image_orig_rgb, axis=2)

# Courbes
coords_h = coords_hilbert(largeur, hauteur)
coords_m = coords_morton(largeur, hauteur)
coords_s = coords_serpent(largeur, hauteur)

# Dither Grayscale
image_h_bw = atkinson_dither(image_orig_gray, coords_h)
image_m_bw = atkinson_dither(image_orig_gray, coords_m)
image_s_bw = atkinson_dither(image_orig_gray, coords_s)

# Dither RGB + quantization
image_h_rgb = dither_rgb_1bit(image_orig_rgb, coords_h)
image_m_rgb = dither_rgb_1bit(image_orig_rgb, coords_m)
image_s_rgb = dither_rgb_1bit(image_orig_rgb, coords_s)

# Sauvegardes
exporter_png_rgb(image_orig_rgb, "doriginal.png")

exporter_png_1bit(image_h_bw, "dhilbert_bw.png")
exporter_png_1bit(image_m_bw, "dmorton_bw.png")
exporter_png_1bit(image_s_bw, "dsnake_bw.png")

exporter_png_palette(image_h_rgb, "dhilbert_palette.png")
exporter_png_palette(image_m_rgb, "dmorton_palette.png")
exporter_png_palette(image_s_rgb, "dsnake_palette.png")

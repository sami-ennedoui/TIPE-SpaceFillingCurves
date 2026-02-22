import numpy as np
from PIL import Image

def quantifier(pixel):
    return 255 if pixel > 127 else 0
def quantifier_image(image):
    h, l, c = image.shape
    resultat = np.copy(image)
    for canal in range(c):
        for y in range(h):
            for x in range(l):
                resultat[y, x, canal] = quantifier(resultat[y, x, canal])
    return resultat.astype(np.uint8)

def diffusion_atkinson(image):
    h, l, c = image.shape
    resultat = np.copy(image).astype(float)
    for canal in range(c):
        for y in range(h):
            for x in range(l):
                ancien = resultat[y, x, canal]
                nouveau = quantifier(ancien)
                resultat[y, x, canal] = nouveau
                erreur = (ancien - nouveau) / 8
                if x + 1 < l:
                    resultat[y, x + 1, canal] += erreur
                if x + 2 < l:
                    resultat[y, x + 2, canal] += erreur
                if y + 1 < h:
                    if x - 1 >= 0:
                        resultat[y + 1, x - 1, canal] += erreur
                    resultat[y + 1, x, canal] += erreur
                    if x + 1 < l:
                        resultat[y + 1, x + 1, canal] += erreur
                if y + 2 < h:
                    resultat[y + 2, x, canal] += erreur
    np.clip(resultat, 0, 255, out=resultat)
    return resultat.astype(np.uint8)

def diffusion_floyd_steinberg(image):
    h, l, c = image.shape
    resultat = np.copy(image).astype(float)
    for canal in range(c):
        for y in range(h):
            for x in range(l):
                ancien = resultat[y, x, canal]
                nouveau = quantifier(ancien)
                resultat[y, x, canal] = nouveau
                erreur = ancien - nouveau
                if x + 1 < l:
                    resultat[y, x + 1, canal] += erreur * 7 / 16
                if y + 1 < h:
                    if x - 1 >= 0:
                        resultat[y + 1, x - 1, canal] += erreur * 3 / 16
                    resultat[y + 1, x, canal] += erreur * 5 / 16
                    if x + 1 < l:
                        resultat[y + 1, x + 1, canal] += erreur * 1 / 16
    np.clip(resultat, 0, 255, out=resultat)
    return resultat.astype(np.uint8)

def creer_image_test():
    return np.array([
        [[230, 50, 50], [180, 40, 40], [190, 45, 45], [200, 50, 50], [210, 55, 55]],
        [[100, 80, 80], [120, 90, 90], [130, 100, 100], [110, 85, 85], [140, 105, 105]],
        [[160, 150, 150], [170, 160, 160], [180, 170, 170], [190, 180, 180], [200, 190, 190]],
        [[50, 60, 70], [60, 70, 80], [70, 80, 90], [80, 90, 100], [90, 100, 110]],
        [[20, 30, 40], [30, 40, 50], [40, 50, 60], [50, 60, 70], [60, 70, 80]]
    ], dtype=np.uint8)
def sauvegarder_image(nom, matrice, facteur=50):
    img = Image.fromarray(matrice, mode='RGB')
    taille = (matrice.shape[1] * facteur, matrice.shape[0] * facteur)
    img = img.resize(taille, resample=Image.NEAREST)
    img.save(nom)
image_originale = creer_image_test()
image_quantifiee = quantifier_image(image_originale)
image_atkinson = diffusion_atkinson(image_originale)
image_floyd = diffusion_floyd_steinberg(image_originale)

sauvegarder_image('originale.png', image_originale)
sauvegarder_image('quantifiee.png', image_quantifiee)
sauvegarder_image('atkinson.png', image_atkinson)
sauvegarder_image('floyd.png', image_floyd)

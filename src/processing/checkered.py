from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def creer_noiretblanc1():
    dessin = canvas.Canvas("blacknwhite1.pdf", pagesize=letter)
    largeur, hauteur = letter
    taille_case = inch * 2
    for i in range(2):
        for j in range(2):
            x = i * taille_case
            y = hauteur - (j + 1) * taille_case
            dessin.setFillColorRGB(0, 0, 0) if i == j else dessin.setFillColorRGB(1, 1, 1)
            dessin.rect(x, y, taille_case, taille_case, fill=1, stroke=0)
    dessin.save()

def creer_noiretblanc2():
    dessin = canvas.Canvas("blacknwhite2.pdf", pagesize=letter)
    largeur, hauteur = letter
    lignes, colonnes = 50, 50
    largeur_case = largeur / colonnes
    hauteur_case = hauteur / lignes
    for i in range(colonnes):
        for j in range(lignes):
            x = i * largeur_case
            y = hauteur - (j + 1) * hauteur_case
            dessin.setFillColorRGB(0, 0, 0) if (i + j) % 2 == 0 else dessin.setFillColorRGB(1, 1, 1)
            dessin.rect(x, y, largeur_case, hauteur_case, fill=1, stroke=0)
    dessin.save()

def creer_noiretblanc3():
    dessin = canvas.Canvas("blacknwhite3.pdf", pagesize=letter)
    largeur, hauteur = letter
    lignes, colonnes = 750,750
    largeur_case = largeur / colonnes
    hauteur_case = hauteur / lignes
    for i in range(colonnes):
        for j in range(lignes):
            x = i * largeur_case
            y = hauteur - (j + 1) * hauteur_case
            dessin.setFillColorRGB(0, 0, 0) if (i + j) % 2 == 0 else dessin.setFillColorRGB(1, 1, 1)
            dessin.rect(x, y, largeur_case, hauteur_case, fill=1, stroke=0)
    dessin.save()

creer_noiretblanc1()
creer_noiretblanc2()
creer_noiretblanc3()
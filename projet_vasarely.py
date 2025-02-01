"""
Auteur : Nicolas Melaerts
Date : Octobre 2019
But du programme : Réaliser à l'aide du module turtle un pavage d'hexagones avec une sphère de déformation
Entrées : inf_gauche : coordonnées (x, y) du coin inférieur gauche du pavage
          sup_droit : coordonnées (x, y) du coin supérieur droit du pavage
          longueur: distance entre le centre et n'importe quel point de l'hexagone
          col: tuple contenant les trois couleurs qui vont être utilisées pour dessiner les hexagones
          centre: tuple de trois composantes donnant les coordonnées du centre de la sphère de déformation
          rayon: rayon de la sphère de déformation
Sortie : pavage d'hexagone tricolor avec une sphère de déformation

"""
from math import pi, sin, cos, sqrt, acos, asin, atan2
import turtle

def deformation(p, centre, rayon):
    """ Calcul des coordonnées d'un point suite à la déformation engendrée par la sphère émergeante
        Entrées :
          p : coordonnées (x, y, z) du point du dalage à tracer (z = 0) AVANT déformation
          centre : coordonnées (X0, Y0, Z0) du centre de la sphère
          rayon : rayon de la sphère
        Sorties : coordonnées (xprim, yprim, zprim) du point du dallage à tracer APRÈS déformation
    """
    x, y, z = p
    xprim, yprim, zprim = x, y, z
    xc, yc, zc = centre
    if rayon**2 > zc**2:
        zc = zc if zc <= 0 else -zc
        r = sqrt(
            (x - xc) ** 2 + (y - yc) ** 2)  # distance horizontale depuis le point à dessiner jusqu'à l'axe de la sphère
        rayon_emerge = sqrt(rayon ** 2 - zc ** 2)           # rayon de la partie émergée de la sphère
        rprim = rayon * sin(acos(-zc / rayon) * r / rayon_emerge)
        if 0 < r <= rayon_emerge:                 # calcul de la déformation dans les autres cas
            xprim = xc + (x - xc) * rprim / r           # les nouvelles coordonnées sont proportionnelles aux anciennes
            yprim = yc + (y - yc) * rprim / r
        if r <= rayon_emerge:
            beta = asin(rprim / rayon)
            zprim = zc + rayon * cos(beta)
            if centre[2] > 0:
                zprim = -zprim
    return (xprim, yprim, zprim)

if __name__ == "__main__": # code de test
    for i in range(-150,150,50):
        for j in range(-150,150,50):
            print(deformation((i,j,0), (0,0,100), 100))
        print()

def hexagone(p, longueur, col, centre, rayon) :
    """
    Fonction qui trace un hexagone
    Entrées :
     p: tuple de trois composantes donnant la valeur des trois coordonnées, du point avant déformation
     où l'hexagone doit être peint
     longueur: distance entre le centre et n'importe quel point de l'hexagone
     col: tuple contenant les trois couleurs qui vont être utilisées pour dessiner les hexagones
     centre: tuple de trois composantes donnant les coordonnées du centre de la sphère de déformation
     rayon: rayon de la sphère de déformation
    Sorties :
     Si les coordonnées (p) de l'hexagone qui doit être peint se trouve dans la sphère de déformation, il sera déformé
     sinon ce sera un hexagone régulier
    """
    (x, y, z) = p
    (pprim_x, pprim_y, pprim_z) = deformation((x, y, z), centre, rayon)
    (col1, col2, col3) = col
    angle = -pi/3
    turtle.up()
    turtle.goto(pprim_x, pprim_y)       # coordonnées du centre de l'hexagone
    losange=0
    while losange != 3:                 # un losange qui pivote pour former un hexagone
        angle += pi/3
        turtle.color(col1)
        turtle.begin_fill()
        for i in range(3):          # pour chaques losanges à partir du centre de l'hexagone
            x_d, y_d, z_d = deformation((x+longueur*cos(angle), y+longueur*sin(angle), z), centre, rayon)
            # calcule nouvelles coordonnées des points
            turtle.goto(x_d, y_d)
            angle += pi/3
        turtle.goto(pprim_x, pprim_y)
        turtle.end_fill()
        col1 = col3                     # changement de couleur du losange
        col3 = col2
        losange += 1
    turtle.up()

def pavage(inf_gauche, sup_droit, longueur, col, centre, rayon) :
    """
    Réalisation du pavage d'hexagone avec une sphère de déformation
    Entrées :
     inf_gauche: coordonnées du coin inférieur gauche
     sup_droit: coordonnées du coin supérieur droit
     longueur: distance entre le centre et n'importe quel point de l'hexagone
     col: tuple contenant les trois couleurs qui vont être utilisées pour dessiner les hexagones
     centre: tuple de trois composantes donnant les coordonnées du centre de la sphère de déformation
     rayon: rayon de la sphère de déformation
    Sortie : pavage d'hexagones avec des hexagones déformés dans la sphère de déformation
    """
    (x, y, z) = (inf_gauche, inf_gauche, 0)
    y = y-(longueur*sin(pi/3))
    while y <= sup_droit:       # le pavage ne continue pas au-delà de sup_droit
        y = y+(longueur*sin(pi/3))                # la distance entre deux lignes
        x = inf_gauche
        while x <= (sup_droit+longueur):            # première ligne d'hexagones qui ne dépasse pas sup_droit
            p = (x, y, 0)                          # nouvelles coordonnées des points où doit être peint l'hexagone
            hexagone(p, longueur, col, centre, rayon)
            x = x+(3*longueur)                        # distance entre deux hexagones d'une même ligne
        y = y+(longueur*sin(pi/3))
        x = inf_gauche
        x = x + (1.5 * longueur) - (3*longueur)
        # deuxième ligne d'hexagone décalée de 1.5*longueur par rapport à la première ligne
        while x <= (sup_droit-(3*longueur)):       # ne dépasse pas sup_droit
            x = x+(3*longueur)
            p = (x, y, 0)
            hexagone(p, longueur, col, centre, rayon)

turtle.speed(10)
pavage(-305, 305, 50, ("lime", "black", "blue"), (-50, -50, 0), 300)
turtle.getcanvas().postscript(file="pavage.eps")
turtle.done()

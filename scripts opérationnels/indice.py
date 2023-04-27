import cv2
import numpy as np


def determine_weather_index(sky_image):
    '''
    determine un indice basé sur l'analyse d'image 
    cette analyse d'image est très simple et ne permet pas en elle meme de determiner l'état météo d'un endroit
    Il faut correler l'indice de l'image à des données quantitatives tels que l'humidité et la temperature pour rendre l'estimation plus precise
    '''
    # on convertie l'image passée sous forme de matrice de pixels en niveaux de gris
    image_nb = cv2.cvtColor(sky_image, cv2.COLOR_BGR2GRAY)

    # calcul de l'intensité moyenne des pixels
    intensite_moyenne = np.mean(image_nb)

    # calcul de l'ecart-type des pixels de l'image en niveaux de gris
    ecart_type = np.std(image_nb)

    #L'indice météorologique est calculé en utilisant une formule qui utilise ces valeurs, 
    # où l'indice est d'autant plus élevé que la moyenne est faible et l'écart-type est élevé.
    indice = 1 - (intensite_moyenne / 255) + (ecart_type / (2 * 255))

    indice_max = (255 / 255) + (255 / (2 * 255))

    # on normalise l'indice pour le ramener à une intervale de 0 à 1 
    indice_final = indice / indice_max

    return indice_final * 100  # mulitplier par 100 pour qu'il prenne plus d'importance dans la mesure du KNN

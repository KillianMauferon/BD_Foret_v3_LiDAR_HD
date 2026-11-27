import os
import numpy as np
import laspy

# Mise en place des chemins d'accès aux dossiers d'entrée et de sortie
dossier_lidar_essences = "data/output/LiDAR_essences"
dossier_output = "data/output/LiDAR_essence_potree"

# Création du dossier de sortie s'il n'existe pas
os.makedirs(dossier_output, exist_ok=True)

# Création de la liste des couleurs associées à chaque essence issue du style du projet QGIS fournis
# L'ordre des couleurs dans la liste est important
# En effet il corrrespond à l'ordre des codes associés à chaque essencce dans le fichier CSV créé dans le code 8_essences
# ATTENTION : La liste des couleurs associées à chaque essence diffère en fonction de la zone d'étude
# IL EST DONC NÉCESSAIRE DE MODIFIER CETTE LISTE EN FONCTION DE LA ZONE D'ÉTUDE
couleurs = [
    "#28ffa7", "#59ffff", "#afca59", "#ff6633", "#a666ff", "#a3ff73",
    "#aef1b0", "#40ff26", "#7eb87f", "#a9b67b", "#5ba55d", "#f8c350",
    "#004d2e", "#d399ff", "#4bc2e7", "#a6a6a6", "#c19a67", "#e8863c",
    "#00ff80", "#50693f", "#b1a3eb", "#4d80ff", "#ffff00", "#4d33ff",
    "#9926ff", "#915633", "#1bbbbf", "#1ae6e6", "#66ffcc"
]

def hexadecimales_to_rvb(couleurs):
    """Fonction qui convertit notre liste de couleurs hexadécimales issue de QGIS
    en un tableau ayant pour chaque colonne les valeurs RVB (Rouge, Vert, Bleu) correspondantes"""

    # Création de notre tableau RVB
    table_RVB = []

    # Boucle parcourant la liste des couleurs hexadécimales afin de récupérer les valeurs RVB correspondantes
    for code_hexa in couleurs:

        # Récupération des valeurs RVB à partir du code hexadécimal
        # Le code hexadécimal est composé de 6 caractères :
        # - Les deux premiers correspondent à la valeur rouge
        rouge = int(code_hexa[1:3], 16)

        # - Les deux suivants correspondent à la valeur verte
        vert = int(code_hexa[3:5], 16)

        # - Les deux derniers correspondent à la valeur bleue
        bleu = int(code_hexa[5:7], 16)
        
        # Ajout des valeurs RVB dans notre tableau
        table_RVB.append([rouge, vert, bleu])

    return np.array(table_RVB) 


def rvb_vers_tsv(rvb, echelle = 65535):
    """Fonction qui convertit un tableau RVB en un tableau TSV (Teinte, Saturation, Valeur)
    avec T (0-360 degres), S (0-100 %), V (0-100 %)"""

    # Normalisation des valeurs RVB entre 0 et 1
    rouge = rvb[:, 0] / echelle
    vert = rvb[:, 1] / echelle
    bleu = rvb[:, 2] / echelle

    # Récupération des valeurs maximales et minimales de chaque ligne du tableau RVB
    maxi = np.maximum.reduce([rouge, vert, bleu])
    mini = np.minimum.reduce([rouge, vert, bleu])

    # Calcul de la différence entre les valeurs maximales et minimales
    delta = maxi - mini

    # Création du tableau des différentes teintes
    teinte = np.zeros(len(rvb))

    # Création du tableau des différentes saturations
    saturation = np.zeros(len(rvb))

    # Création du tableau des différentes valeurs
    valeur = np.zeros(len(rvb))

    # Boucle sur chaque ligne du tableau RVB afin de calculer la teinte, la saturation et la valeur
    for i in range(len(rvb)):

        # Calcul de la teinte
        if delta[i] == 0 : 
            teinte[i] = 0
        else:
            if maxi[i] == rouge[i]:
                teinte[i] = 60 * (((vert[i] - bleu[i]) / delta[i]) % 6)
            elif maxi[i] == vert[i]:
                teinte[i] = 60 * ((bleu[i] - rouge[i]) / delta[i] + 2)
            elif maxi[i] == bleu[i]:
                teinte[i] = 60 * ((rouge[i] - vert[i]) / delta[i] + 4)

        teinte[i] = teinte[i] % 360

        # Calcul de la saturation
        if maxi[i] == 0 :
            saturation[i] = 0
        else :
            saturation[i] = (delta[i] / maxi[i]) * 100

        # Calcul de la valeur
        valeur[i] = maxi[i] * 100

    return teinte, saturation, valeur


def tsv_vers_rvb(teinte, saturation, valeur):
    """Fonction qui convertit un tableau TSV en un tableau RVB (Rouge, Vert, Bleu)
    avec R (0-65535), V (0-65535), B (0-65535) pour un nuage de point LiDAR HD"""

    # Normalisation des valeurs S et V entre 0 et 1
    saturation = saturation / 100
    valeur = valeur / 100

    # Création du tableau des rouges
    rouge = np.zeros(len(teinte))

    # Création du tableau des verts
    vert = np.zeros(len(teinte))

    # Création du tableau des bleus
    bleu = np.zeros(len(teinte))

    for i in range(len(teinte)):

        # Calcul des valeurs intermédiaires :
        # - chroma : L'intensité pure de la couleur
        chroma = valeur[i] * saturation[i]

        # - x : La composante secondaire de teinte
        x = chroma * (1 - abs(((teinte[i]  / 60) % 2) - 1))

        # - m : La base de gris
        m = valeur[i] - chroma

        # Détermination des valeurs RVB en fonction de l'intervalle de teinte
        if teinte[i] < 60 :
            rouge[i] = chroma
            vert[i] = x
        elif teinte[i] >= 60 and teinte[i] < 120 :
            rouge[i] = x
            vert[i] = chroma 
        elif teinte[i] >= 120 and teinte[i] < 180 :
            vert[i] = chroma
            bleu[i] = x
        elif teinte[i] >= 180 and teinte[i] < 240 :
            vert[i] = x
            bleu[i] = chroma
        elif teinte[i] >= 240 and teinte[i] < 300 :
            rouge[i] = x
            bleu[i] = chroma  
        elif teinte[i] >= 300 :
            rouge[i] = chroma
            bleu[i] = x 

        # On ramène les valeurs RVB entre 0 et 65535
        rouge[i] = (rouge[i] + m)*65535
        vert[i] = (vert[i] + m)*65535
        bleu[i] = (bleu[i] + m)*65535
    
    return np.stack([rouge, vert, bleu], axis=1)

# Conversion de la liste des couleurs hexadécimales en un tableau RVB
tableau_rvb = hexadecimales_to_rvb(couleurs)

# Boucle sur le dossier LiDAR avec les essences afin de parcourir tous les fichiers un par un
for nom in os.listdir(dossier_lidar_essences):

    # On ne traite que les nuages de points LiDAR (.laz)
    if not nom.endswith(".laz"):
        continue

    print("Traitement de la dalle", nom)

    # Récupération du chemin d'accès au fichier LiDAR
    lidar_essence = os.path.join(dossier_lidar_essences, nom)

    # Lecture du nuage de points LiDAR
    las = laspy.read(lidar_essence)

    # Récupération des trois tableaux (rouge, vert et bleu) afin de les associer au sein d'un seul tableau
    rvb = np.stack([las.red, las.green, las.blue], axis=1)

    # Récupération de la couleur RVB des points du LiDAR afin de les transformer au format TSV
    teinte, saturation, valeur = rvb_vers_tsv(rvb)

    # Récupération de la couleur RVB des essences afin de les transformer au format TSV
    teinte_essence, saturation_essence, valeur_essence = rvb_vers_tsv(tableau_rvb[las.classification - 1], 255)

    # La luminosité de la couleur de chaque essence est modulée en fonction de la luminosité originale du point LiDAR
    valeur_modulee = np.clip(valeur_essence * valeur / np.median(valeur), 0, 100)

    # Conversion de la couleur de notre nuage de point de TSV vers RVB avec la luminosité modulée
    rvb = tsv_vers_rvb(teinte_essence, saturation_essence, valeur_modulee)

    # On redéfinis les couleurs rouge, vert et bleu de notre nuage de points avec celles que nous venons de calculer
    las.red = rvb[:, 0].astype(np.uint16)
    las.green = rvb[:, 1].astype(np.uint16)
    las.blue = rvb[:, 2].astype(np.uint16)

    # Création du fichier du nuage de points LiDAR avec les nouvelles couleurs
    las.write(os.path.join(dossier_output, nom))
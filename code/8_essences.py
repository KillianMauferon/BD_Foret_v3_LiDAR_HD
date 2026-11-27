import os
import laspy
import numpy as np
import geopandas as gpd

# Mise en place des chemins d'accès aux dossiers d'entrée et de sortie
# Nous récupérons uniquement les points LiDAR de la classe supérieur à 7 mètres
# En effet pour la modélisation 3D nous souhaitons uniquement coloriser les points se trouvant dans la partie supérieure du nuage de points LiDAR
dossier_lidar_sup_7m = "data/output/LiDAR_classes/classe_sup_7m"
dossier_output = "data/output/LiDAR_essences"

# Récupération du chemin d'accès au fichier .gpkg de la BD Forêt v3 
gpkg_bd_foret = "data/input/BD_FORET/data/bdfv3_D068.gpkg"

# Création du dossier de sortie s'il n'existe pas
os.makedirs(dossier_output, exist_ok = True)

# Création du GeoDataFrame contenant les essences forestière de chaque polygone de la BD Forêt v3
bd_foret = gpd.read_file(gpkg_bd_foret, columns = ["libelle_essence"])

# Récupération de la liste des essences présentes et les tris par ordre alphabétique
essences = sorted(bd_foret["libelle_essence"].dropna().unique())

# Création d'un dictionnaire qui associe à chaque essence un code unique (1 pour le Aulne, ..., 29 pour le saule)
# ATTENTION : Le code associé à chaque essence diffère en fonction de la zone d'étude
# Il faudra donc faire attention à bien modifier :
#   - La liste des couleurs associées à chaque essence dans le code 9_RVB_to_TSV_to_RVB
#   - La liste des codes couleurs associés à chaque essence dans le .html de visualisation 3D
dico_essences = {essence: i + 1 for i, essence in enumerate(essences)}

# Création de notre fichier CSV contenant le code associé à chaque essence
with open(os.path.join(dossier_output, "table_essences.csv"), "w", encoding = "utf-8-sig") as fichier_csv:
    fichier_csv.write("code;essence\n")
    for essence, code in dico_essences.items():
        fichier_csv.write(f"{code};{essence}\n")

# Boucle sur le dossier des nuages de points LiDAR dont la hauteur est supérieure à 7 mètres afin de parcourir tous les fichiers un par un
for nom in os.listdir(dossier_lidar_sup_7m):

    print("Traitement de la dalle", nom)

    # Récupération du chemin d'accès au fichier LiDAR
    lidar_sup_7m = os.path.join(dossier_lidar_sup_7m, nom)

    # Lecture du nuage de points LiDAR
    nuage_de_points = laspy.read(lidar_sup_7m)

    # Création du GeoDataFrame contenant chaque point LiDAR sous forme de points géométriques
    points_lidar = gpd.GeoDataFrame(geometry=gpd.points_from_xy(nuage_de_points.x, nuage_de_points.y), crs=2154)

    # Jointure spatiale entre le GeodataFrame des points LiDAR et le GeoDataFrame de la BD Forêt v3
    # Nous faisons une jointure spatiale de type "left" afin de conserver tous les points (même ceux dehors des polygones de la BD Forêt)
    # Nous utilisons la méthode "within" afin de récupérer l'essence associée au polygone dans lequel le point se situe
    joined = gpd.sjoin(points_lidar, bd_foret, how = "left", predicate = "within")

    # Création d'un tableau numpy contenant pour chaque point LiDAR le code associé à son essence
    # Pour se faire nous utilisons le dictionnaire qui nous a permis de créer le fichier CSV contenant le code associé à chaque essence
    # Nous sommes obligé d'avoir une colonne avec des entiers et non avec des floats comme nous l'avions préccédement
    # De plus les Nan sont remplacés par des 0 afin de pouvoir les supprimer par la suite 
    # En effet l'objectif est de pouvoir classifier chaque essence dans Potree pour la visualisation 3D
    # Mais pour cela Potree prend uniquement en charge les entiers
    codes = joined["libelle_essence"].map(dico_essences).fillna(0).astype(np.uint8).to_numpy()

    # Nous remplaçons le champs classification du nuage de points LiDAR par le tableau numpy que nous venons de créer
    # En effet dans Potree c'est le champs classification qui va permettre d'afficher la légende de notre nuage de points
    # Et l'objectif est de pouvoir visualiser la légende liée aux différentes essences
    nuage_de_points.classification = codes

    # Suppression des points LiDAR se trouvant hors polygone, ils n'ont aucun intérêt pour la visualisation vu qu'ils n'ont pas d'essence
    nuage_de_points.points = nuage_de_points.points[codes != 0]

    # Création du fichier du nuage de points LiDAR avec son essence associée
    nuage_de_points.write(os.path.join(dossier_output, nom))
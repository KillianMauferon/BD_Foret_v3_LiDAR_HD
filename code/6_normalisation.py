import os
import json
import subprocess

# Mise en place des chemins d'accès aux dossiers d'entrée et de sortie
dossier_lidar = "data/input/LiDAR_RVB" # Si pas de LiDAR colorisé --> "data/input/LiDAR"
dossier_output = "data/output/LiDAR_normalise"

# Récupération du chemin d'accès au fichier .vrt du MNT de notre zone d'étude 
mnt = "data/input/vrt/mosaique.vrt"

# Emprise de notre zone d'étude au format PDAL sous la forme ([xmin,xmax],[ymin,ymax])
# L'emprise est rognée de 1 mètre afin d'éviter les problèmes de bordure lors du calcul de la hauteur
# En effet les points LiDAR situés en bordure se trouve en dehors de l'emprise du MNT
# Et cela provoque des valeurs NaN pour la hauteur au-dessus du sol (HAG) ce qui pose problème pour les étapes suivantes
emprise = "([1007001,1009999],[6781001,6783999])"

# Création du dossier de sortie s'il n'existe pas
os.makedirs(dossier_output, exist_ok = True)

# Boucle sur le dossier LiDAR afin de parcourir tous les fichiers un par un
for nom in os.listdir(dossier_lidar):

    # On ne traite que les nuages de points LiDAR (.copc.laz)
    if not nom.endswith(".copc.laz"):
        continue

    print("Traitement de la dalle", nom)

    # Récupération du chemin d'accès au fichier LiDAR
    lidar = os.path.join(dossier_lidar, nom)

    # Création du chemin d'accès au fichier de sortie en remplaçant l'extension .copc.laz par _normalisee.laz
    output = os.path.join(dossier_output, nom.replace(".copc.laz", "_normalisee.laz"))

    # Mise en place du pipeline PDAL pour normaliser le nuage de points LiDAR
    # Un pipeline PDAL est un fichier JSON contenant une liste d'étapes que PDAL va exécuter dans l'ordre (ici 4 étapes)
    # La première étape permet de lire le fichier LiDAR
    # La deuxième étape permet de conserver uniquement les points présents dans l'emprise que l'on a défini au début du script
    # La troisième étape permet de créer un nouveau champs "HeightAboveGround"
    # Ce dernier correspond à la différence entre l'altitude du point et l'altitude du MNT à cet endroit
    # La dernière étape permet de créer un nouveau fichier dans le dossier de sortie indiqué au début du script
    # Ce fichier est compressé au format .laz et contient le champ créé à la troisième étape
    pipeline = {
        "pipeline": [
            {"type": "readers.las", "filename": lidar},
            {"type": "filters.crop", "bounds": emprise},
            {"type": "filters.hag_dem", "raster": mnt},
            {
                "type": "writers.las",
                "filename": output,
                "compression": "laszip",
                "extra_dims": "HeightAboveGround = float32"
            }
        ]
    }

    # Création de notre fichier JSON contenant le pipeline PDAL que nous venons de créer
    with open("pipeline_normalisation.json", "w") as fichier_JSON:
        json.dump(pipeline, fichier_JSON)

    # Exécution du pipeline PDAL à partir de notre fichier JSON
    subprocess.run(["pdal", "pipeline", "pipeline_normalisation.json"], check = True)
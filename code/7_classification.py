import os
import json
import subprocess

# Mise en place des chemins d'accès aux dossiers d'entrée et de sortie
dossier_lidar_normalise = "data/output/LiDAR_normalise"
dossier_output = "data/output/LiDAR_classes"

# Création de la liste des classes contenant le nom de la classe et l'expression associée pour filtrer les points LiDAR
# La première classe correspond aux points dont le HAG est compris entre 0 et 2 mètres
# De plus nous conservons uniquement les points classés comme végétation (classe 3, 4 et 5) et sol (classe 2)
# La deuxième classe correspond aux points dont le HAG est compris entre 2 et 7 mètres
# De plus nous conservons uniquement les points classés comme végétation (classe 3, 4 et 5)
# La troisième classe correspond aux points dont le HAG est supérieur à 7 mètres
# De plus nous conservons uniquement les points classés comme végétation (classe 3, 4 et 5)
classes = [
    (
        "classe_0_2m",
        "((HeightAboveGround >= 0) && (HeightAboveGround < 2)) && ((Classification == 2) || (Classification == 3) || (Classification == 4) || (Classification == 5))"
    ),
    (
        "classe_2_7m",
        "((HeightAboveGround >= 2) && (HeightAboveGround <= 7)) && ((Classification == 3) || (Classification == 4) || (Classification == 5))"
    ),
    (
        "classe_sup_7m",
        "(HeightAboveGround > 7) && ((Classification == 3) || (Classification == 4) || (Classification == 5))"
    )
]

# Boucle sur le dossier LiDAR afin de parcourir tous les fichiers un par un
for nom in os.listdir(dossier_lidar_normalise):

    # Récupération du chemin d'accès au fichier LiDAR
    lidar_normalise = os.path.join(dossier_lidar_normalise, nom)

    # Boucle sur la liste des classes afin de parcourir chacune des trois classes pour chaque dalle LiDAR
    for nom_classe, expression in classes:

        print("Traitement de la dalle", nom, "pour la classe", nom_classe)

        # Création d'un dossier en sortie pour chacune des classes
        dossier_classe = os.path.join(dossier_output, nom_classe)

        # Création des dossiers de sortie s'ils n'existent pas
        os.makedirs(dossier_classe, exist_ok = True)

        # Création du chemin d'accès au fichier de sortie en ajoutant le nom de la classe
        output = os.path.join(dossier_classe, nom.replace(".laz", "_" + nom_classe + ".laz"))

        # Mise en place du pipeline PDAL pour filtrer les points LiDAR selon l'expression associée à la classe
        # Un pipeline PDAL est un fichier JSON contenant une liste d'étapes que PDAL va exécuter dans l'ordre (ici 3 étapes)
        # La première étape permet de lire le fichier LiDAR normalisé
        # La deuxième étape permet de filtrer les points LiDAR selon l'expression associée à la classe
        # La dernière étape permet de créer un nouveau fichier dans le dossier de sortie associé à la bonne classe
        # Ce fichier est compressé au format .laz et conserve le champ "HeightAboveGround" créé lors de la normalisation
        pipeline = {
            "pipeline": [
                {"type": "readers.las", "filename": lidar_normalise},
                {
                    "type": "filters.expression",
                    "expression": expression
                },
                {
                    "type": "writers.las",
                    "filename": output,
                    "compression": "laszip",
                    "extra_dims": "HeightAboveGround = float32"
                }
            ]
        }

        # Création de notre fichier JSON contenant le pipeline PDAL que nous venons de créer
        pipeline_path = "pipeline_" + nom_classe + ".json"
        with open(pipeline_path, "w") as fichier_JSON:
            json.dump(pipeline, fichier_JSON)

        # Exécution du pipeline PDAL à partir de notre fichier JSON
        subprocess.run(["pdal", "pipeline", pipeline_path], check = True)
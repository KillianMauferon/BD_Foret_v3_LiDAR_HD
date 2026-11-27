# BD_Foret_v3_LiDAR_HD

Bienvenue sur le dépôt github du projet : Enrichissement et mise en valeur de la BD forêt v3 à partir du LiDAR HD

## Répartition des rôles

| | |
|---|---|
| **Chef de projet** | Amédéo TAISNE |
| **Responsable données et reproductibilité** | Killian MAUFERON |
| **Responsable livrables et communication** | Cécilia DEBEAUPUIS |
| **Responsable usage de l'IA** | Antoine CORBEAUX |

## Objectifs

Les différents objectifs attendus par le commanditaire sont :

-    Enrichissement de la BD Forêt v3 à partir de données issues du LiDAR HD
-    Modélisation 3D de la BD Forêt afin de mettre en valeur cette dernière lors de la campagne de communication

## Structure du dépot

```
BD_Foret_v3_LiDAR_HD/
--- /code/
--- /data/
--------- /input/
--------- /output/
--- /visualisation/
--- /livrables/

```

## Data nécessaires en entrée

Les datas sont envoyés à part, si vous n'avez pas les données à disposition voici où les trouver :

-   La BD Forêt v3 (pas encore disponible pour le grand public)
-   Les dalles LiDAR HD de votre zone d'étude (https://cartes.gouv.fr/telechargement/IGNF_NUAGES-DE-POINTS-LIDAR-HD)
-   Les dalles LiDAR HD colorisées (pas obligatoire pour faire tourner les codes) sont disponible uniquement via notre transfert de données
-   Le MNH issu du LiDAR HD de votre zone d'étude (https://cartes.gouv.fr/telechargement/IGNF_MNH-LIDAR-HD)
-   Le MNT issu du LiDAR HD de votre zone d'étude (https://cartes.gouv.fr/telechargement/IGNF_MNT-LIDAR-HD)
-   Le MNT 25m issu de la BD Alti de votre zone d'étude (https://cartes.gouv.fr/rechercher-une-donnee/dataset/IGNF_BD-ALTI)

## Bibliothèque et environnement nécessaire pour faire fonctionner les codes

### Pour les codes en R :

Pour installer le language de programmation R : https://cloud.r-project.org/ 

Pour installer RStudio : https://posit.co/download/rstudio-desktop/

Les bibliothèques nécessaires sont automatiquement téléchargement lors du lancement du code.

### Pour les codes en Python :

Pour installer le language de programmation python : https://www.python.org/downloads/ 

Pour installer VSCode : https://code.visualstudio.com/Download 

Les bibliothèques nécessaires sont :

-   os
-   json
-   subprocess
-   laspy
-   numpy
-   geopandas

Pour certaines bibliothèques il est nécessaire d'avoir un environnement pdal et gdal. Pour cela il faut dabord installer conda, voici le tutoriel d'installation : https://www.anaconda.com/docs/getting-started/miniconda/install/windows-gui-install

Une fois que conda est installé ouvrez votre powershell conda et taper les lignes suivantes :

Pour l'installation de pdal :
-   conda create --yes --name pdal-env --channel conda-forge pdal python-pdal
-   conda activate pdal-env

Pour l'installation de gdal :
-   conda install -c conda-forge gdal


## Visualisation Potree

### Installation de l'environnement Potree et de Potree Converter

Pour l'installation de Potree et du convertiseur Potree voici le tutoriel d'installation : https://github.com/potree/potree

Une fois Potree installé vous devez ajouter le fichier "Potree_LiDAR.html" dans le dossier "Votre_Chemin/potree".

Une fois avoir lancé la page web (comme indiqué dans le tuto) et avoir mis le fichier .html au bon endroit vous pouvez aller sur votre page web "http://localhost:1234/Potree_LiDAR.html"

Vous devez arriver sur votre page web mais aucune donnée n'est affichée. Pour cela vous devez lancer tous les codes python fournis dans le dossier code. Une fois les codes effectués vous avez tout ce qu'il vous faut dans le dossier output. Maintenant il ne vous reste plus qu'à exporter les différents nuages de points dans Potree.

### Import des nuages de points dans Potree

Ouvrez un nouveau powershell et entrez les lignes suivantes dans le même ordre :

-    cd "Votre_Chemin\PotreeConverter" 
-   .\PotreeConverter.exe "Votre_Chemin\data\input\LiDAR_RVB" -o "Votre_Chemin\potree\pointclouds\lidar_hd_rvb"
-   .\PotreeConverter.exe "Votre_Chemin\data\input\MNT_25m" -o "Votre_Chemin\potree\pointclouds\MNT_25m"
-   .\PotreeConverter.exe "Votre_Chemin\data\output\LiDAR_essence_potree" -o "Votre_Chemin\potree\pointclouds\strate_arboree"
-   .\PotreeConverter.exe "Votre_Chemin\data\output\LiDAR_classes\classe_0_2m" -o "Votre_Chemin\potree\pointclouds\strate_herbace"
-   .\PotreeConverter.exe "Votre_Chemin\data\output\LiDAR_classes\classe_2_7m" -o "Votre_Chemin\potree\pointclouds\strate_arbustive"

Une fois toutes ces étapes effectuées vous pouvez relancer la page web et les données s'affichent maintenant
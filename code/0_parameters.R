#-------------------------------------------------------
########################################################
##### 0_parameters : chemins et réglages
########################################################
#-------------------------------------------------------
# Tous les réglages du projet sont ici. Les chemins sont relatifs au dossier du projet

#-------------------------------------------------------
##### Chemins des données
#-------------------------------------------------------
DOSSIER_LIDAR    <- "../data/input/LiDAR"
DOSSIER_MNT      <- "../data/input/MNT"
DOSSIER_MNH      <- "../data/input/MNH"
FICHIER_BDFORET  <- "../data/input/BD_FORET/data/BDFV3_zone_etude.shp"

DOSSIER_PROCESSED <- "../data/input/vrt"

#-------------------------------------------------------
##### Dossiers de résultats (un par étape)
#-------------------------------------------------------
SORTIE_IMPORT   <- "../data/output/result_enrich/1_verifications"
SORTIE_MNH      <- "../data/output/result_enrich/2_MNH_hauteurs_polygones"
SORTIE_MORAN    <- "../data/output/result_enrich/3_correlation_spatiale"
SORTIE_ARBUSTIVE <- "../data/output/result_enrich/4_lidarforfuel_tous_polygones"
SORTIE_FIGURES  <- "../data/output/result_enrich/5_figures"
SORTIE_BDFV3_FUSION <- "../data/output/result_enrich/6_BDFV3_fusion"

for (d in c(SORTIE_IMPORT, SORTIE_MNH, SORTIE_MORAN,
            SORTIE_ARBUSTIVE, SORTIE_FIGURES, SORTIE_BDFV3_FUSION)) {
  dir.create(d, showWarnings = FALSE, recursive = TRUE)
}
rm(d)

#-------------------------------------------------------
##### Réglages généraux
#-------------------------------------------------------
# Sol de référence pour la hauteur des points :
#   "MNT_IGN" : MNT LiDAR HD de l'IGN (conseillé en relief)
#   "PACKAGE" : sol reconstruit par lidarforfuel
SOL <- "MNT_IGN"

COUVERTURE_MIN <- 0.95   # part minimale d'un polygone couverte par les dalles (0 à 1)
MODE_TEST      <- TRUE   # TRUE = 3 premiers polygones seulement à l'étape 4

#-------------------------------------------------------
##### Étape 2 : MNH
#-------------------------------------------------------
RES_MNH      <- 1   # résolution du MNH calculé si data/mnh est vide (m)
H_MIN_ARBRES <- 5   # pixels du MNH plus bas ignorés (sol, sous-bois)

#-------------------------------------------------------
##### Étape 3 : corrélation spatiale
#-------------------------------------------------------
TAILLE_PIXELS_MORAN <- 20   # taille des pixels de hauteur moyenne (m)

#-------------------------------------------------------
##### Étapes 4 : lidarforfuel
#-------------------------------------------------------
# Essences : LMA (g/m²) et WD (kg/m³) selon code_essence de la BD Forêt v3.
# Pin sylvestre (code 52) : LMA ≈ 160 (SLA 60-63 cm²/g), WD ≈ 430 (400-460).
# Les essences absentes prennent les valeurs par défaut du package.
ESSENCES <- data.frame(
  code_essence = c("52"),
  LMA          = c(160),
  WD           = c(430)
)
LMA_DEFAUT <- 140   # aussi utilisé pour le sous-étage (< 2 m)
WD_DEFAUT  <- 591

EPAISSEUR   <- 0.5    # épaisseur des couches du profil vertical (m)
SEUIL       <- 0.02   # seuil de densité (kg/m³) pour repérer les strates
BUFFER      <- 50     # marge autour du polygone pour les calculs (m)
BUFFER_TRAJ <- 200    # marge pour reconstruire la trajectoire de l'avion (m)
RESOLUTION  <- 10     # pixels des cartes de la parcelle (m)
SAUVER_NUAGE <- FALSE # écrire le nuage prétraité de la parcelle (.laz lourd) ?

# Strates (m)
H_MIN <- 2   # bas de la strate arbustive
H_MAX <- 7   # haut de la strate arbustive

# Conversion densité -> recouvrement (mêmes valeurs que le package)
G     <- 0.5
OMEGA <- 0.77

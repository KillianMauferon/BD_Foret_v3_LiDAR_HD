#-------------------------------------------------------
########################################################
##### _workflow : BD Forêt v3 + LiDAR HD
########################################################
#-------------------------------------------------------
# Lance tout le projet, dans l'ordre.

# packages
source("./0_library_pck.R", echo = TRUE, encoding = "UTF-8")

# chemins et réglages
source("./0_parameters.R", echo = TRUE, encoding = "UTF-8")

# dalles, BD Forêt, parcelle, MNT
source("./1_import_data.R", echo = TRUE, encoding = "UTF-8")

# hauteurs MNH
source("./2_MNH_Lidar.R", echo = TRUE, encoding = "UTF-8")

# indice de Moran
source("./3_correlation_spatiale_hauteur.R", echo = TRUE, encoding = "UTF-8")

# couverture de la régé : tous les polygones
source("./4_lidarforfuel_tous_polygones.R", echo = TRUE, encoding = "UTF-8")

# carte de la couverture de la régé
source("./5_fusion_des_sorties.R", echo = TRUE, encoding = "UTF-8")

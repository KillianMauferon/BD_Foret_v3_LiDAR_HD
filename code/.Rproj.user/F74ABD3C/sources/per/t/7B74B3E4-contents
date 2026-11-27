#-------------------------------------------------------
########################################################
##### 0_check and install missing packages
########################################################
#-------------------------------------------------------

# fonction pour l'instalation des packages manquants
tmp_fun <- function(pkg){
  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if (length(new.pkg)) 
    install.packages(new.pkg, dependencies = TRUE)
  sapply(pkg, require, character.only = TRUE)
}

# list of packages
packages <- c("lidR", "sf", "terra", "ggplot2", "dplyr", "remotes")

# lidR : nuages de points LiDAR
# sf : vecteurs (polygones)
# terra : rasters (MNT, MNH, cartes)
# ggplot2 : carte de l'indice de Moran (étape 2b)
# remotes : pour installer lidarforfuel depuis GitHub

tmp_fun(packages)


# lidarforfuel n'est pas sur le CRAN : installation depuis GitHub
if (!require("lidarforfuel")) {
  remotes::install_github("oliviermartin7/lidarforfuel")
  library(lidarforfuel)
}

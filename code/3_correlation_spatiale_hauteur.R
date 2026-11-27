#-------------------------------------------------------
########################################################
##### 3_correlation_spatiale_hauteur : indice de moran
########################################################
#-------------------------------------------------------
# pour savoir s'il y a des zones distinctes à l'intérieur des polygones de la BDFV3


polygones_BDFV3_moran <- bdforet #BDFV3 ou l'on ajoutera la valeur de l'indice de moran

#-------------------------------------------------------
##### carte de la hauteur moyenne de la canopée par pixel
#-------------------------------------------------------

#test de la taille des pixels
mnh_extent <- ext(mnh)
if ((reste <- (mnh_extent[2] - mnh_extent[1]) %% TAILLE_PIXELS_MORAN) != 0 || 
    (reste <- (mnh_extent[4] - mnh_extent[3]) %% TAILLE_PIXELS_MORAN) != 0) { 
  stop("pixel size is not matching")}

# raster contenant pour chaque pixel la valeur moyenne du mnh
hauteur_moyenne <- terra::aggregate(mnh, fact = 2*TAILLE_PIXELS_MORAN, fun = mean)

# enregistrement
rast_file <- file.path(SORTIE_MORAN, "hauteur_moyenne.tif")
terra::writeRaster(hauteur_moyenne, filename = rast_file, overwrite = TRUE)


#-------------------------------------------------------
##### autocorrélation spatiale (Moran) dans chaque polygone
#-------------------------------------------------------

#fonction sur un polygone de la BDFV3 qui return l'indice de moran calculé sur les pixels contenus dans le polygone
moran_polygone <- function(polygone_f, map_pixel, window) {
  # prend les pixels contenus dans le polygone
  r <- crop(map_pixel, vect(polygone_f), mask = TRUE)
  
  # trop peu de pixels valides (moins de 10 pixels dans le polygone) ou raster trop petit pour la fenêtre 3x3
  if (ncol(r) < 3 || nrow(r) < 3 || sum(!is.na(values(r))) < 10) {
    return(NA)
  }
  
  tryCatch(
    terra::autocor(r, w = window, method = "moran", global = TRUE),
    error = function(e) {NA}
  )
}

# moran pour chaque polygone de la BDFV3
Moran_foret <- function(polygones_BDFV3_moran, map_pixel) {
  # voisinage 3x3 (queen), pixel central exclu
  window <- matrix(c(1,1,1,1,0,1,1,1,1), nrow = 3, ncol = 3)
  vapply(
    seq_len(nrow(polygones_BDFV3_moran)),
    function(i) moran_polygone(polygones_BDFV3_moran[i, ], map_pixel, window),
    numeric(1)
  )
}

polygones_BDFV3_moran$moran <- Moran_foret(polygones_BDFV3_moran, hauteur_moyenne)
summary(polygones_BDFV3_moran$moran)

#-------------------------------------------------------
##### visualisation de moran (carte)
#-------------------------------------------------------

carte_moran <- ggplot(polygones_BDFV3_moran) +
  geom_sf(aes(fill = moran), color = NA) +
  scale_fill_gradient2(
    low = "#b2182b", mid = "white", high = "#2166ac",
    midpoint = 0, limits = c(-1, 1),
    na.value = "grey85",
    name = "Indice de Moran I"
  ) +
  labs(title = "Autocorrelation spatiale de la hauteur de canopee") +
  theme_minimal()

#-------------------------------------------------------
##### export de la carte moran en png et en gpkg
#-------------------------------------------------------

ggsave(plot = carte_moran, file.path(SORTIE_FIGURES, "carte_moran.png"))

sf::st_write(polygones_BDFV3_moran, file.path(SORTIE_MORAN, "polygons_moran.gpkg"), delete_dsn = TRUE)

#-------------------------------------------------------
##### Test : croisement avec BDFV3 sur fid = 21116
#-------------------------------------------------------

hauteur_moyenne_21116 <- crop(hauteur_moyenne, vect(BDFV3_fid_21116), snap = "in", mask=T, touches = F)
terra::plot(hauteur_moyenne_21116)

rast_file <- file.path(SORTIE_MORAN, "hauteur_moyenne_21116.tif")
terra::writeRaster(hauteur_moyenne_21116, filename = rast_file, overwrite = TRUE)









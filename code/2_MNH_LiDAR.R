####################COMPUTE MEAN HEIGHT#########################################


#-------------------------------------------------------
##### ID pour chaque polygone de la bdfv3
#-------------------------------------------------------
bdforet$ID <- seq_len(nrow(bdforet))


#-------------------------------------------------------
##### Pixels d'arbres seulement (> 5 m) - filtre 
#-------------------------------------------------------
mnh_arbres <- ifel(mnh > H_MIN_ARBRES, mnh, NA)

# ------------------------------------------------------------------------------
# Extract individual MNH pixel values for every polygon
# ------------------------------------------------------------------------------
#fonction extract de terra pour extraire les hauteurs du mnt dans chaque polygone de la BDFV3
extract_df <- terra::extract(
  mnh_arbres, terra::vect(bdforet),
  cells = TRUE, ID = TRUE
)

#'we check if height field is there '
if (!("height" %in% names(extract_df))) {
  stop("Expected a 'height' column in the extracted MNH values.")
}

# Statistiques de hauteur sur un polygone de la bdforet; NA si pas de pixels valides.
stats_hauteur <- function(z) {
  z <- z[!is.na(z)]
  if (length(z) == 0) return(rep(NA_real_, 8))
  if (length(z) < 4) return(c(mean(z), NA_real_, quantile(z, c(0.10, 0.25, 0.50, 0.75, 0.90, 0.95))))
  else return(c(mean(z), sd(z), quantile(z, c(0.10, 0.25, 0.50, 0.75, 0.90, 0.95))))
}

# Keep one metric row per parcel, even if a polygone has no valid MNH pixels.
polygones_metrics <- do.call(rbind, lapply(seq_len(nrow(bdforet)), function(i) {
  c(bdforet_id = i, stats_hauteur(extract_df$height[extract_df$ID == i]))
}))
row.names(polygones_metrics) <- NULL
colnames(polygones_metrics) <- c("bdforet_id", "mean", "sd", "p10", "p25", "p50", "p75", "p90", "p95")


# Join metrics to the original plot attributes, preserving plot order.
polygones_attributes <- sf::st_drop_geometry(bdforet)
polygone_MNH <- merge(polygones_attributes, polygones_metrics, by.x = "ID", by.y = "bdforet_id",
                   all.x = TRUE, sort = FALSE)

##Comparaison des hauteurs de la BDFV3 et du lidar
polygone_MNH$diff_hauteurs <- (polygone_MNH$mean - polygone_MNH$hauteur_vegetation_moyenne)/polygone_MNH$mean

comparaison_h <- ggplot(sf::st_drop_geometry(polygone_MNH), aes(x = hauteur_vegetation_moyenne, y = mean)) +
  geom_point()

comparaison_h

#Arrondir les chiffres à un chiffres après la virgule
polygone_MNH <- polygone_MNH %>%
  mutate(across(where(is.numeric), ~ round(.x, 1)))

#jointure à la BDFV3
polygone_MNH <- dplyr::left_join(bdforet, 
                          polygone_MNH|> dplyr::select(fid_bdforet, mean, sd, p10,p25,p50,p75,p90,p95, diff_hauteurs), 
                          by = "fid_bdforet")

#enregistrement
sf::st_write(polygone_MNH, file.path(SORTIE_MNH, "polygone_MNH.gpkg"), delete_dsn = TRUE)



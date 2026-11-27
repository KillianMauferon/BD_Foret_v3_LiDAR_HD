#-------------------------------------------------------
########################################################
##### 4_lidarforfuel
########################################################
#-------------------------------------------------------
# Taux de couverture de la régénération par polygone de la BDFV3
# couverture et profil parcelle pour 21116 (pour visualiser)

#-------------------------------------------------------
##### Fonction 1 : profil vertical d'une zone
#-------------------------------------------------------
# Elle utilise les objets créés à l'étape 1 : dalles et mnt.
# zone : un polygone de la  BD Forêt
# renvoie : le tableau du profil (H = hauteur, PAD = densité de végétation...)

profil_vertical <- function(zone) {
  
  # 1. Trajectoire de l'avion (donne l'angle de tir de chaque point)
  dalles_traj <- dalles
  opt_select(dalles_traj)   <- "xyztrnpc"   # colonnes utiles seulement
  opt_progress(dalles_traj) <- FALSE
  trajectoire <- get_traj(clip_roi(dalles_traj, st_buffer(zone, BUFFER_TRAJ)))
  
  # 2. Nuage de points autour de la zone : sol (2) et végétation (3, 4, 5)
  las <- clip_roi(dalles, st_buffer(zone, BUFFER))
  las <- filter_poi(las, Classification %in% c(2, 3, 4, 5))
  
  # 3. Prétraitement lidarforfuel, puis retrait du bruit
  las <- fPCpretreatment(las, traj = trajectoire)
  las <- filter_poi(las, Classification != LASNOISE)
  
  # 4. Hauteur des points avec le MNT de l'IGN : hauteur = altitude - MNT
  las@data$Z <- las$Zref - extract(mnt, cbind(las$X, las$Y))[, 1]
  las@data$Z[las$Classification == 2] <- 0           # sol = 0 m
  las <- filter_poi(las, !is.na(Z) & Z > -1)
  las <- las_update(las)
  
  # 5. Points de la zone seule (sans la marge)
  las <- clip_roi(las, zone)
  
  # 6. Profil vertical : densité de végétation (PAD) par couche de EPAISSEUR m
  #    (WD = valeur par défaut du package, sans effet sur le taux de couverture)
  profil <- fCBDprofile_fuelmetrics(datatype = las, WD = 591, d = EPAISSEUR)[[2]]
  if (is.null(profil)) stop("trop peu de points")
  profil
}

#-------------------------------------------------------
##### Fonction 2 : taux de couverture de la régénération
#-------------------------------------------------------
# profil : profil déjà calculé par profil_vertical(zone). Si on ne le donne pas,
#          il est calculé ici (cas de l'étape 4 : taux_couverture_rege(zone)).
# renvoie : le taux de couverture de la régénération (%), entre H_MIN_REGE et H_MAX_REGE
taux_couverture_rege <- function(profil) {

  # 7. Taux de couverture de la régénération (loi de Beer-Lambert)
  couches <- profil$H > H_MIN & profil$H <= H_MAX
  pai <- sum(profil$PAD[couches]) * EPAISSEUR       # surface végétale (m²/m²)
  round(100 * (1 - exp(-G * OMEGA * pai)))
}

#-------------------------------------------------------
##### Application aux polygones de la BDFV3
#-------------------------------------------------------

polygones_arbustive <- bdforet #BDFV3 ou l'on ajoutera la valeur pour le couvert de la strate arbustive
if (MODE_TEST) polygones_arbustive <- polygones_arbustive[1:3, ]   # 3 polygones pour tester

polygones_arbustive$taux_couverture_rege_pct <- NA
for (i in 1:nrow(polygones_arbustive)) {
  cat("Polygone", i, "/", nrow(polygones_arbustive), "\n")
  polygones_arbustive$taux_couverture_rege_pct[i] <- tryCatch(
    suppressWarnings(taux_couverture_rege(profil_vertical(st_geometry(polygones_arbustive[i, ])))),
    error = function(e) { cat("   -> erreur :", conditionMessage(e), "\n"); NA })
}

#-------------------------------------------------------
##### Export en gpkg
#-------------------------------------------------------

st_write(polygones_arbustive, file.path(SORTIE_ARBUSTIVE, "BDFV3_couverture_rege.gpkg"),
         delete_dsn = TRUE, quiet = TRUE)


#-------------------------------------------------------
##### Carte du taux de couverture de la régénération par polygone
#-------------------------------------------------------

carte_rege <- ggplot(polygones_arbustive) +
  geom_sf(aes(fill = taux_couverture_rege_pct), color = NA) +
  scale_fill_gradient(
    low = "lemonchiffon", high = "darkolivegreen",
    limits = c(0,100),
    na.value = "grey85",
    
  ) +
  labs(title = "Couverture de la strate arbustive (%)") +
  theme_minimal()

carte_rege

ggsave(plot = carte_rege, file.path(SORTIE_FIGURES, "carte_couverture_rege.png"))


#-------------------------------------------------------
##### Parcelle 21116
#-------------------------------------------------------
profil_21116 <- profil_vertical(BDFV3_fid_21116)

taux_21116 <- taux_couverture_rege(profil_21116)
cat("Parcelle 21116 : taux de couverture de la régénération =", taux_21116, "%\n")


#-------------------------------------------------------
##### Graphique : profil vertical moyen de la parcelle 21116
#-------------------------------------------------------
png(file.path(SORTIE_FIGURES, "profil_parcelle.png"), width = 1400, height = 1600, res = 200)
plot(profil_21116$PAD, profil_21116$H, type = "l", lwd = 2, col = "darkgreen",
     xlab = "Densite de surface vegetale PAD (m2/m3)", ylab = "Hauteur (m)",
     main = "Profil vertical moyen - parcelle 21116")
abline(h = c(H_MIN, H_MAX), lty = 2, col = "orange")
legend("topright", legend = paste0("regeneration (", H_MIN, "-", H_MAX, " m)"),
       lty = 2, col = "orange", bty = "n")
dev.off()
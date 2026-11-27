#-------------------------------------------------------
########################################################
##### 1_import_data : dalles, BD Forêt, parcelle, MNT
########################################################
#-------------------------------------------------------

#-------------------------------------------------------
##### Dalles LiDAR HD
#-------------------------------------------------------

dalles <- readLAScatalog(DOSSIER_LIDAR)
st_crs(dalles) <- 2154          # Lambert-93
emprise <- st_union(st_as_sf(dalles))
# Les dalles .copc.laz du LiDAR HD sont déjà indexées : pas besoin de .lax

#-------------------------------------------------------
##### MNH LiDAR HD (mosaïque virtuelle des dalles)
#-------------------------------------------------------
mnh_files <- list.files(
  DOSSIER_MNH, pattern = "\\.tif$",
  full.names = TRUE, recursive = TRUE
)
if (length(mnh_files) == 0) {
  stop("Aucune dalle MNH '*.tif' dans './data/mnh'.")
}

vrt_file <- file.path(DOSSIER_PROCESSED, "MNH_mosaic.vrt") #enregistrement comme vrt
mnh <- terra::vrt(mnh_files, filename = vrt_file, overwrite = TRUE)
names(mnh) <- "height"


#-------------------------------------------------------
##### MNT LiDAR HD (mosaïque virtuelle des dalles)
#-------------------------------------------------------
mnt_files <- list.files(
  DOSSIER_MNT, pattern = "\\.tif$",
  full.names = TRUE, recursive = TRUE
)
if (length(mnh_files) == 0) {
  stop("Aucune dalle MNT '*.tif' dans './data/mnt'.")
}

vrt_file <- file.path(DOSSIER_PROCESSED, "MNT_mosaic.vrt") #enregistrement comme vrt
mnt <- terra::vrt(mnt_files, filename = vrt_file, overwrite = TRUE)
names(mnt) <- "height_mnt"
crs(mnh) <- "EPSG:2154"   # Lambert-93

#-------------------------------------------------------
##### BD Forêt v3 : polygones couverts par les dalles
#-------------------------------------------------------
bdforet <- st_read(FICHIER_BDFORET, quiet = TRUE)
bdforet <- st_transform(bdforet, 2154)
bdforet <- st_make_valid(bdforet)

# Le .shp coupe les noms de colonnes à 10 caractères : on remet les noms complets
noms_complets <- c(libelle_tf = "libelle_tff",
                   libelle_es = "libelle_essence",
                   code_essen = "code_essence",
                   densite_co = "densite_couvert_arbore",
                   hauteur_ve = "hauteur_vegetation_moyenne",
                   hauteur__1 = "hauteur_vegetation_ecart_type",
                   libelle_dp = "libelle_dpt")
for (court in names(noms_complets)) {
  names(bdforet)[names(bdforet) == court] <- noms_complets[court]
}

# Accents : le .dbf est en Latin-1 -> conversion en UTF-8
for (col in names(bdforet)) {
  if (is.character(bdforet[[col]]) && !all(validUTF8(bdforet[[col]]))) {
    bdforet[[col]] <- iconv(bdforet[[col]], from = "latin1", to = "UTF-8")
  }
}

# Une colonne « fid » gêne l'écriture en GeoPackage : on la renomme
names(bdforet)[names(bdforet) == "fid"] <- "fid_bdforet"


#-------------------------------------------------------
##### Parcelle d'étude 21116
#-------------------------------------------------------
BDFV3_fid_21116 <- bdforet |>
  filter(bdforet$fid_bdforet == 19679)



#-------------------------------------------------------
##### Vérification visuelle (enregistrée, pas affichée)
#-------------------------------------------------------
png(file.path(SORTIE_IMPORT, "verification_donnees.png"), width = 1600, height = 1600, res = 200)
plot(st_geometry(st_as_sf(dalles)), border = "grey40",
     main = "Dalles (gris), polygones BD Foret (bleu), parcelle 21116 (rouge)")
plot(st_geometry(bdforet), add = TRUE, border = "blue")
plot(st_geometry(BDFV3_fid_21116), add = TRUE, border = "red", lwd = 3)
dev.off()

#rm(court, col, noms_complets, part_couverte, fichiers_mnt)

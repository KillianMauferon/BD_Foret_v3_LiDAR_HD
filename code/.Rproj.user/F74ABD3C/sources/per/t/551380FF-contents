#-------------------------------------------------------
########################################################
##### 5_fusion_sorties : rassembler toutes les nouvelles valeurs
########################################################
#-------------------------------------------------------
# nouveau gpkg avec les données de la BDFV3
# + les nouvelles données calculées 


#-------------------------------------------------------
##### rappel : les données à rassembler
#-------------------------------------------------------


#### La BD FORET V3 :
# bdforet

#### Les sorties des différents codes :
# 2_MNH_LiDAR : polygone_MNH -> mean, sd, p10,p25,p50,p75,p90,p95
# 3_correlation_spatiale_hauteur : polygones_BDFV3_moran -> moran
# 4_lidarforfuel_tous_polygones : polygones_arbustive -> taux_couverture_rege_pct

#-------------------------------------------------------
##### fusion des données 
#-------------------------------------------------------

#### BDFV3_FUSION = La BD FORET V3 + les nouvelles valeurs

BDFV3_FUSION <- bdforet |>
  left_join(
    polygone_MNH |>
      st_drop_geometry() |>
      select(fid_bdforet, mean, sd, p10, p25, p50, p75, p90, p95, diff_hauteurs),
    by = "fid_bdforet")

BDFV3_FUSION <- BDFV3_FUSION |>
  left_join(
    polygones_BDFV3_moran |>
      st_drop_geometry() |>
      select(fid_bdforet, moran),
    by = "fid_bdforet")

BDFV3_FUSION <- BDFV3_FUSION |>
  left_join(
    polygones_arbustive |>
      st_drop_geometry() |>
      select(fid_bdforet, taux_couverture_rege_pct),
    by = "fid_bdforet"
  )

#-------------------------------------------------------
##### export en gpkg
#-------------------------------------------------------

sf::st_write(BDFV3_FUSION, file.path(SORTIE_BDFV3_FUSION, "BDFV3_SORTIE.gpkg"), delete_dsn = TRUE)










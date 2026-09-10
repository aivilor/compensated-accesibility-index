import pandas as pd
import geopandas as gpd


#BARCELONA
df_bcn = pd.read_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Barcelona/opendatabcn_sanitat_hospitals-i-centres-atencio-primaria.csv", encoding='utf-16')
df_bcn['register_id'] = df_bcn['register_id'].apply(lambda x: x.replace('\ufeff', '') if isinstance(x, str) else x)
df_bcn["register_id"] = df_bcn["register_id"].astype(int)
df_bcn["register_id"] = df_bcn["register_id"].astype(str)

#LOC 1 BARCELONA
df_loc1_bcn = df_bcn[df_bcn["secondary_filters_name"].isin(['Hospitals i clíniques'])]
df_loc1_bcn = df_loc1_bcn[["register_id", "name", "geo_epgs_25831_x", "geo_epgs_25831_y"]]
df_loc1_bcn["regimen"]= "PÚB."
df_loc1_bcn["dimension"]= "salud"
df_loc1_bcn["capacidad"]= 1
df_loc1_bcn["localidad"]= "Barcelona"
gdf_loc1_bcn = gpd.GeoDataFrame(df_loc1_bcn, 
                                geometry=gpd.points_from_xy(df_loc1_bcn.geo_epgs_25831_x, df_loc1_bcn.geo_epgs_25831_y), crs="EPSG:25831")
#gdf_loc1_bcn.to_crs(epsg=25830, inplace=True)                                
gdf_loc1_bcn.rename(columns={"register_id": "id", "name": "nombre"}, inplace=True)
gdf_loc1_bcn["id"] = gdf_loc1_bcn["id"].astype(str)
gdf_loc1_bcn = gdf_loc1_bcn[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
gdf_loc1_bcn.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc1_Barcelona.geojson")
gdf_loc1_bcn[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc1_Barcelona.csv")

#LOC 2 BARCELONA
df_loc2_bcn = df_bcn[df_bcn["secondary_filters_name"].isin(["CAPs"])]
df_loc2_bcn = df_loc2_bcn[["register_id", "name", "geo_epgs_25831_x", "geo_epgs_25831_y"]]
df_loc2_bcn["regimen"]= "PÚB."
df_loc2_bcn["dimension"]= "salud"
df_loc2_bcn["capacidad"]= 1
df_loc2_bcn["localidad"]= "Barcelona"
gdf_loc2_bcn = gpd.GeoDataFrame(df_loc2_bcn, 
                                geometry=gpd.points_from_xy(df_loc2_bcn.geo_epgs_25831_x, df_loc2_bcn.geo_epgs_25831_y), crs="EPSG:25831")
#gdf_loc2_bcn.to_crs(epsg=25830, inplace=True)                                
gdf_loc2_bcn.rename(columns={"register_id": "id", "name": "nombre"}, inplace=True)
gdf_loc2_bcn["id"] = gdf_loc2_bcn["id"].astype(str)
gdf_loc2_bcn = gdf_loc2_bcn[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
gdf_loc2_bcn.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc2_Barcelona.geojson")
gdf_loc2_bcn[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc2_Barcelona.csv")


# EDUCACION BARCELONA
df_edu_bcn = pd.read_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Barcelona/opendatabcn_llista-equipaments_educacio-csv.csv", encoding='utf-16')
df_edu_bcn['register_id'] = df_edu_bcn['register_id'].apply(lambda x: x.replace('\ufeff', '') if isinstance(x, str) else x)
df_edu_bcn["register_id"] = df_edu_bcn["register_id"].astype(int)
df_edu_bcn["register_id"] = df_edu_bcn["register_id"].astype(str)

#LOC 3 BARCELONA
df_loc3_bcn = df_edu_bcn[df_edu_bcn["secondary_filters_name"] =='Educació primària']
df_loc3_bcn = df_loc3_bcn[["register_id", "name", "geo_epgs_25831_x", "geo_epgs_25831_y"]]
df_loc3_bcn["regimen"]= "PÚB."
df_loc3_bcn["dimension"]= "educacion"
df_loc3_bcn["capacidad"]= 1
df_loc3_bcn["localidad"]= "Barcelona"
df_loc3_bcn = gpd.GeoDataFrame(df_loc3_bcn, 
                                geometry=gpd.points_from_xy(df_loc3_bcn.geo_epgs_25831_x, df_loc3_bcn.geo_epgs_25831_y), crs="EPSG:25831")
#df_loc3_bcn.to_crs(epsg=25830, inplace=True)                                
df_loc3_bcn.rename(columns={"register_id": "id", "name": "nombre"}, inplace=True)
df_loc3_bcn["id"] = df_loc3_bcn["id"].astype(str)
df_loc3_bcn = df_loc3_bcn[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
df_loc3_bcn.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc3_Barcelona.geojson")
df_loc3_bcn[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc3_Barcelona.csv")


#LOC 4 BARCELONA
df_loc4_bcn = df_edu_bcn[df_edu_bcn["secondary_filters_name"] =='Educació secundària']
df_loc4_bcn = df_loc4_bcn[["register_id", "name", "geo_epgs_25831_x", "geo_epgs_25831_y"]]
df_loc4_bcn["regimen"]= "PÚB."
df_loc4_bcn["dimension"]= "educacion"
df_loc4_bcn["capacidad"]= 1
df_loc4_bcn["localidad"]= "Barcelona"
df_loc4_bcn = gpd.GeoDataFrame(df_loc4_bcn, 
                                geometry=gpd.points_from_xy(df_loc4_bcn.geo_epgs_25831_x, df_loc4_bcn.geo_epgs_25831_y), crs="EPSG:25831")
#df_loc4_bcn.to_crs(epsg=25830, inplace=True)                                
df_loc4_bcn.rename(columns={"register_id": "id", "name": "nombre"}, inplace=True)
df_loc4_bcn["id"] = df_loc4_bcn["id"].astype(str)
df_loc4_bcn = df_loc4_bcn[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
df_loc4_bcn.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc4_Barcelona.geojson")
df_loc4_bcn[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc4_Barcelona.csv")



#MURCIA
#df_murcia_ce = df = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/Mediterranean cities/Datos/Murcia/Coord Cen San Esrishape 20221231/Coord CE 20221231_custom_point.shp") #centros especialidades
#df_murcia_cl = df = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/Mediterranean cities/Datos/Murcia/Coord CL 20221231_custom_point.shp") #consultorios locales
#df_murcia_cpal = df = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/Mediterranean cities/Datos/Murcia/Coord CPAL 20221231_custom_point.shp") #cuidados paliativos
#df_murcia_cs = df = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/Mediterranean cities/Datos/Murcia/Coord CS 20221231_custom_point.shp") #centros de salud
#df_murcia_hosp_priv = df = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/Mediterranean cities/Datos/MurciaCoord Cen San Esrishape 20221231/Coord Hosp priv 20221231_custom_point.shp") #hospitales privados
#df_murcia_hosp_pub = df = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/Mediterranean cities/Datos/Murcia/Coord Cen San Esrishape 20221231/Coord Hosp pub 20221231_custom_point.shp") #hospitales públicos
#df_murcia_of = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/Mediterranean cities/Datos/Murcia/Coord Cen San Esrishape 20221231/Coord OF 20221231_font_point.shp") #oficinas de farmacia

#LOC 1 MURCIA
df_murcia_hosp_pub = df = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Murcia/Coord Hosp pub 20221231_custom_point.shp") #hospitales públicos
df_murcia_hosp_pub = df_murcia_hosp_pub[df_murcia_hosp_pub["Municipio"]=="Murcia"]
df_loc1_mur = df_murcia_hosp_pub[["Hosp_Descr", "N_camas_in", "geometry"]] #Está el número de camas disponible pero no se va a utilizar
df_loc1_mur["dimension"]="salud"
df_loc1_mur["capacidad"]=1
df_loc1_mur["localidad"]="Murcia"
df_loc1_mur["id"]= list(range(df_loc1_mur.shape[0]))
df_loc1_mur["regimen"]= "PÚB."
df_loc1_mur.rename(columns={"Hosp_Descr":"nombre"}, inplace=True)
df_loc1_mur=df_loc1_mur[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
df_loc1_mur[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc1_Murcia.csv")
df_loc1_mur.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc1_Murcia.geojson")

#LOC 2 MURCIA
df_murcia_cs = df = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Murcia/Coord CS 20221231_custom_point.shp") #centros de salud
df_murcia_cl = df = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Murcia/Coord CL 20221231_custom_point.shp") #consultorios locales
df_murcia_cs = df_murcia_cs[df_murcia_cs["Municipio"]=="Murcia"]
df_murcia_cl = df_murcia_cl[df_murcia_cl["Municipio"]=="Murcia"]
df_murcia_cl = df_murcia_cl[["CL_Descri", "geometry"]]
df_murcia_cl.rename(columns={"CL_Descri":"nombre"}, inplace=True)
df_murcia_cs = df_murcia_cs[["CS_Descri", "geometry"]]
df_murcia_cl.rename(columns={"CS_Descri":"nombre"}, inplace=True)
df_loc2_mur = pd.concat([df_murcia_cl,df_murcia_cs])
df_loc2_mur["dimension"]="salud"
df_loc2_mur["capacidad"]=1
df_loc2_mur["localidad"]="Murcia"
df_loc2_mur["id"]= list(range(df_loc2_mur.shape[0]))
df_loc2_mur["regimen"]= "PÚB."
df_loc2_mur=df_loc2_mur[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
df_loc2_mur.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc2_Murcia.geojson")
df_loc2_mur[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc2_Murcia.csv")

#EDUCACION MURCIA

df_edu_mur = pd.read_json("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Murcia/centros_educativos_Murcia.json")
df_edu_mur = df_edu_mur[df_edu_mur["titularidad"]=="P"]
df_edu_mur = df_edu_mur[df_edu_mur["muncen"]=="MURCIA"]

df_edu_mur["lat"] = df_edu_mur["geo-referencia"].apply(lambda x: x["lat"] if isinstance(x, dict) else None)
df_edu_mur["lon"] = df_edu_mur["geo-referencia"].apply(lambda x: x["lon"] if isinstance(x, dict) else None)
df_edu_mur = df_edu_mur[["codcen", "dencen", "tipo","lat", "lon"]]

#LOC 3 MURCIA
gdf_loc3_mur = df_edu_mur[df_edu_mur["tipo"]== 'Colegio Público']
gdf_loc3_mur["regimen"]= "PÚB."
gdf_loc3_mur["dimension"]= "educacion"
gdf_loc3_mur["capacidad"]= 1
gdf_loc3_mur["localidad"]= "Murcia"
gdf_loc3_mur = gpd.GeoDataFrame(gdf_loc3_mur, 
                                geometry=gpd.points_from_xy(gdf_loc3_mur.lon, gdf_loc3_mur.lat), crs="EPSG:4326")
gdf_loc3_mur.to_crs(epsg=25830)
gdf_loc3_mur.rename(columns={"codcen": "id", "dencen": "nombre"}, inplace=True)
gdf_loc3_mur["id"] = gdf_loc3_mur["id"].astype(str)
gdf_loc3_mur = gdf_loc3_mur[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
gdf_loc3_mur.to_crs(epsg=25830, inplace=True)
gdf_loc3_mur.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc3_Murcia.geojson")
gdf_loc3_mur[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc3_Murcia.csv")

#LOC 4 MURCIA
gdf_loc4_mur = df_edu_mur[df_edu_mur["tipo"]== 'Instituto de Educación Secundaria (IES)']
gdf_loc4_mur["regimen"]= "PÚB."
gdf_loc4_mur["dimension"]= "educacion"
gdf_loc4_mur["capacidad"]= 1
gdf_loc4_mur["localidad"]= "Murcia"
gdf_loc4_mur = gpd.GeoDataFrame(gdf_loc4_mur, 
                                geometry=gpd.points_from_xy(gdf_loc4_mur.lon, gdf_loc4_mur.lat), crs="EPSG:4326")
gdf_loc4_mur.to_crs(epsg=25830)
gdf_loc4_mur.rename(columns={"codcen": "id", "dencen": "nombre"}, inplace=True)
gdf_loc4_mur["id"] = gdf_loc4_mur["id"].astype(str)
gdf_loc4_mur = gdf_loc4_mur[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
gdf_loc4_mur.to_crs(epsg=25830, inplace=True)
gdf_loc4_mur.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc4_Murcia.geojson")
gdf_loc4_mur[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc4_Murcia.csv")



#VALENCIA

#LOC 1 VALENCIA
df_hosp_vlc = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Valencia/hospitales.geojson")
df_loc1_vlc = df_hosp_vlc[df_hosp_vlc["CEN_LOCA"]=="250"][["CEN_COD", "CEN_DESCLA", "geometry"]]
df_loc1_vlc["dimension"]="salud"
df_loc1_vlc["capacidad"]=1
df_loc1_vlc["localidad"]="Valencia"
df_loc1_vlc["regimen"]= "PÚB."
df_loc1_vlc.rename(columns={"CEN_COD":"id","CEN_DESCLA":"nombre"}, inplace=True)
df_loc1_vlc=df_loc1_vlc[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
df_loc1_vlc[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc1_Valencia.csv")
df_loc1_vlc.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc1_Valencia.geojson")

#LOC 2 VALENCIA
df_caux_vlc = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Valencia/centros_auxiliares.geojson")
df_caux_vlc = df_caux_vlc[df_caux_vlc["CEN_LOCA"]=="250"][["CEN_COD", "CEN_DESCLA", "geometry"]]
df_csal_vlc = gpd.read_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Valencia/centros_salud.geojson")
df_csal_vlc = df_csal_vlc[df_csal_vlc["CEN_LOCA"]=="250"][["CEN_COD", "CEN_DESCLA", "geometry"]]
df_loc2_vlc = pd.concat([df_caux_vlc, df_csal_vlc])
df_loc2_vlc["dimension"]="salud"
df_loc2_vlc["capacidad"]=1
df_loc2_vlc["localidad"]="Valencia"
df_loc2_vlc["regimen"]= "PÚB."
df_loc2_vlc.rename(columns={"CEN_COD":"id","CEN_DESCLA":"nombre"}, inplace=True)
df_loc2_vlc=df_loc2_vlc[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
df_loc2_vlc[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc2_Valencia.csv")
df_loc2_vlc.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc2_Valencia.geojson")



#EDUCACION VALENCIA
df1 = pd.read_excel("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Valencia/Listado_Centros_Provincias.xlsx")
df2 = pd.read_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/Valencia/escolarizacion_2025.csv", )
df2 = df2[(df2["NOM_PROV_VA"]== "VALENCIA/VALÈNCIA")]
df2["DESC_TIPO_ES"].replace({"OTROS": "PÚBLICO"}, inplace=True)
df1.rename(columns={"Código":"Codigo"}, inplace=True)
df_merge = df1.merge(df2, how="left", left_on="Codigo", right_on="COD_CENTRO")
df_merge = df_merge[df_merge["NOM_MUN_OF"]=="VALÈNCIA"]
df_merge = df_merge[df_merge["Régimen"]=="Público"]
df_merge["Régimen"].replace({"Público":"PÚB."},inplace=True)

df_merge = df_merge[["Codigo", "Denominación Genérica ES","Régimen", "Localidad", "Denominación", "COD_CURSO", "TOTAL_MATRICULACIONES", "Longitud", "Latitud" ]]
atributos_map = {"Codigo":"id", "Denominación_Generica_ES":"tipo", "Denominación":"nombre", "TOTAL_MATRICULACIONES":"capacidad", "Localidad":"localidad", "Régimen":"regimen"}

 #LOC 3 VALENCIA
df_primaria = df_merge[(df_merge["Denominación Genérica ES"].str.contains("PRIMARIA"))]
prim = ['1PRI', '2PRI', '3PRI', '4PRI', '5PRI', '6PRI', 'EPRI', 'EEPRI']
df_prim = df_primaria[df_primaria["COD_CURSO"].isin(prim)]
df_prim = df_prim.groupby(["Codigo", "Denominación Genérica ES","Régimen", "Localidad", "Denominación", "Longitud", "Latitud" ]).sum(["TOTAL_MATRICULACIONES"])
df_prim.reset_index(inplace=True)
df_loc3_vlc = gpd.GeoDataFrame(df_prim, geometry=gpd.points_from_xy(df_prim.Longitud, df_prim.Latitud), crs="EPSG:4326")
df_loc3_vlc = df_loc3_vlc[["Codigo", "Denominación Genérica ES","Régimen", "Localidad", "Denominación", "TOTAL_MATRICULACIONES", "geometry"]]
df_loc3_vlc.rename(columns =  atributos_map, inplace=True)
df_loc3_vlc = df_loc3_vlc.to_crs("epsg:25830")
df_loc3_vlc["dimension"] = "educacion"
df_loc3_vlc = df_loc3_vlc[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]
df_loc3_vlc[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc3_Valencia.csv")
df_loc3_vlc.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc3_Valencia.geojson")

#LOC 4 VALENCIA
df_secundaria = df_merge[(df_merge["Denominación Genérica ES"].str.contains("SECUNDARIA"))]
eso = ['1ESO', '2ESO', '3ESO', '4ESO', 'EEESO', 'EESO']
df_eso = df_secundaria[df_secundaria["COD_CURSO"].isin(eso)]
df_eso = df_eso.groupby(["Codigo", "Denominación Genérica ES","Régimen", "Localidad", "Denominación", "Longitud", "Latitud" ]).sum(["TOTAL_MATRICULACIONES"])
df_eso.reset_index(inplace=True)
df_loc4_vlc = gpd.GeoDataFrame(df_eso, geometry=gpd.points_from_xy(df_eso.Longitud, df_eso.Latitud), crs="EPSG:4326")
df_loc4_vlc.rename(columns =  atributos_map, inplace=True)
df_loc4_vlc = df_loc4_vlc.to_crs("epsg:25830")
df_loc4_vlc["dimension"] = "educacion"
df_loc4_vlc = df_loc4_vlc[["id", "dimension", "nombre", "regimen", "localidad", "capacidad", "geometry"]]    
df_loc4_vlc[["id", "capacidad"]].to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_loc4_Valencia.csv")
df_loc4_vlc.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc4_Valencia.geojson")


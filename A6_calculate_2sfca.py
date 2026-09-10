import pandas as pd
import math
import geopandas as gpd
import numpy as np


def gaussian_condition_factory(user, t):
    dict_aux_speed = {
        "normatividad": 5 * t / 60 * 1000,
        "infancia": 4.53 * t / 60 * 1000,
        "vejez": 4.13 * t / 60 * 1000}
    do = dict_aux_speed[user]
    def condition(dij):
        if dij < do:
            return ((math.exp(-0.5 * (dij / do) ** 2) - math.exp(-0.5)) / (1 - math.exp(-0.5)))
        else:
            return 0
    return condition

def get_Aj(ciudad, loc, t, user, regimen):

    chunksize = 10**6
    chunk_list = []
    for chunk in pd.read_csv(r"/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/resultados/isochrone_results_walk_{}_origins_to_services.csv".format(ciudad),encoding='latin-1', sep=";",low_memory=False, chunksize=chunksize):
        chunk_list.append(chunk)  

    df_origenes = gpd.read_file(r"/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/{}/origenes_{}.geojson".format(ciudad, ciudad))
    df_origenes = df_origenes[["nationalCa", "geometry"]]

    loc_aux = []
    for i in range(len(chunk_list)):
        loc_aux.append(chunk_list[i][chunk_list[i]["service_type"]=="loc{}".format(loc)])
    df = pd.concat(loc_aux)      
    regimenes = {"total": ["PÚB.","PRIV. CONC.", "PRIV.", "publico", "Público", "privado", "concertado", "Púb.", "Priv.", "Priv. Conc."],
                 "publico": ["PÚB.", "publico", "Púb.", "Público"],
                 "privado": ["PRIV.", "privado", "Priv."],
                 "concertado": ["PRIV. CONC.", "concertado", "Priv. Conc."]}
    
    pobs = {1:"total", 2:"total", 3:"6_11", 4:"12_16" }
    df["service_id"] = df["service_id"].astype(int)
    df["service_id"] = df["service_id"].astype(str)
    df = df[df["nationalCa"]!="none"]
    df_loc = gpd.read_file(r"/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/locs/loc{}_{}.geojson".format(loc,ciudad))
    ####AQUÍ SELECCIONAR REGIMEN
    sel_regimen = list(df_loc[df_loc["regimen"].isin(regimenes[regimen])]["id"].values)
    df_loc = df_loc[df_loc["id"].isin(sel_regimen)]
    fnames = dict(zip([str(i) for i in df_loc["id"].values], list(df_loc["capacidad"].values)))
    #df['service_capacity'] = df["service_id"].map(fnames) 
    df['service_capacity']=1   #PARA PODER COMPARAR TODAS LAS CIUDADES (la linea anterior falla con int/str/float)
    #STEP 1: r-1 
    df_r = df[(df["service_type"]=="loc{}".format(loc)) & (df["accumulated_time"]<=t)]
    df_r.set_index(["service_id", "nationalCa", "service_capacity"], inplace=True)
    df_r = df_r[[pobs[loc], "accumulated_distance"]]
    df_r["G_ij"] = df_r["accumulated_distance"].apply(gaussian_condition_factory(user, t))
    df_r_final = pd.DataFrame(df_r.groupby(by=["service_id","service_capacity"])["G_ij"].sum())
    df_r_final = df_r_final.reset_index()
    df_r_final["r1"] = df_r_final["service_capacity"]/df_r_final["G_ij"]
    df_r_final = df_r_final[["service_id","G_ij", "r1"]]

    #STEP 2: Aj
    df_r_Aj = df_r.copy()
    df_r_Aj.reset_index(inplace=True)
    df_r_Aj = df_r_Aj.merge(df_r_final[["service_id", "r1"]], how="left", on="service_id")
    df_r_Aj["Aj_Sum"] = df_r_Aj["G_ij"] * df_r_Aj["r1"] 
    df_Aj_final = pd.DataFrame(df_r_Aj.groupby(by=["nationalCa"])["Aj_Sum"].sum())
    df_resultados = df_origenes.merge(df_Aj_final, on='nationalCa', how='left').fillna(0)
    
    df_r_final.to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/resultados/{}/r_loc{}_t{}_{}.csv".format(ciudad,loc,t,ciudad))
    df_resultados.to_file("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/resultados/{}/2sfca_loc{}_t{}_{}.geojson".format(ciudad,loc,t,ciudad))
    return df_r_final, df_resultados
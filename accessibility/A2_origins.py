import geopandas as gpd
import requests
import pandas as pd
import numpy as np
from shapely.geometry import shape
import pandas as pd
import re

def get_zone_shape_spain(input_path, natcode):
    df_municipios = gpd.read_file(input_path)
    df_municipios = df_municipios[df_municipios["NATCODE"]==natcode]
    return df_municipios


def parse_mixed_column(series: pd.Series) -> pd.Series:

    def to_int(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, (int, float)):
            return int(val)
        s = str(val).strip()
        if re.fullmatch(r'[+-]?\d+', s):
            return int(s)
        m = re.fullmatch(r'(\d+)[A-Za-z]+\s*', s)
        if m:
            return int(m.group(1))
        m = re.match(r'^([+-]\d+)', s)
        if m:
            return int(m.group(1))
        return np.nan
    return series.apply(to_int).astype("Int64")


def hamilton_round(df, float_col, result_col=None, total=None):

    if result_col is None:
        result_col = float_col
    values = df[float_col].values
    if total is None:
        total = int(round(values.sum()))
    floors = np.floor(values).astype(int)
    remainders = values - floors
    remainder_seats = total - floors.sum()
    ranks = pd.Series(remainders).rank(method='first', ascending=False)
    extra = (ranks <= remainder_seats).astype(int).values
    result = df.copy()
    result[result_col] = floors + extra
    return result

def get_partes (s, indices):
        return [s[indices[i]:indices[i+1]] if i <len(indices)-1 else s[indices[i]:indices[-1]]  for i in range(len(indices))] 

def separacion_registro_inmueble(path):
    with open(path,"rb") as f:
        lines = f.readlines()
    
    indices = [0,2,6,19,22,23,25,28,30,44,48,49,50,58,73,92,94,119,122,125,165,195,200,205,230,234,235,239,240,245,249,251,254,257,282,287,
               289,292,294,297,302,307,337,349,350,362,366,367,371,375,379,391,403,415,427,428,440,441,451,461,470,482,483,487,499, 503,507,
               509,513,521,525,527,535,538,542,555,558,589,597,612,624,636,648,652,656,661,662,751,752]
    
    columnas = ['TIPO', 'NADA','NADA', 'NADA','NADA','COD_DELEGACION_MEH','COD_MUNICIPIO','CLASE_INMUEBLE',
                           'REF_CATASTRAL','N_CARGO','NADA','NADA','NADA','N_FIJO_INMUEBLE','ID_INMUEBLE_AYUN',
                           'N_FINCA','COD_PROVINCIA','PROVINCIA','COD_MUNICIPIO_DGC','COD_MUNICIPIO_INE','MUNICIPIO',
                           'ENTIDAD_MENOR','COD_VIA','TIPO_VIA','N1_POLICIA','L1','N2_POLICIA','L2','KM','BLOQUE',
                           'ESCALERA','PLANTA','PUERTA','DIRECCION','COD_POSTAL','DISTRITO','COD_MUN_AGREGACION',
                           'COD_ZONA_CONCENTRACION','COD_POLIGONO_R','COD_PARCELA','COD_PARAJE','PARAJE','NADA','NADA',
                           'NADA','NADA','NADA', 'N_ORDEN_INMUEBLE','ANTIGUEDAD','NADA','NADA', 'NADA','NADA','NADA', 
                           'TIPO_INMUEBLE','NADA','NADA', 'SUPERFICIE_FINCA','SUPERFICIE_SOLAR','COEFICIENTE_PROPIEDAD',
                           'NADA','NADA', 'NADA','NADA','NADA','NADA','NADA', 'NADA','NADA','NADA','NADA','NADA', 'NADA',
                           'NADA','NADA','NADA','NADA', 'NADA','NADA','NADA','NADA','NADA', 'NADA','NADA','NADA','NADA','NADA',
                           'NADA','NADA']
    
    fichero_cat = [get_partes(line.strip().decode('ascii', errors='ignore'), indices) for line in lines[1:]]    
    df_cat = pd.DataFrame(fichero_cat, columns = columnas)
    df_cat15 = df_cat[df_cat["TIPO"]=="15"]
    df_cat15 = df_cat15[['TIPO',  'COD_DELEGACION_MEH','COD_MUNICIPIO','CLASE_INMUEBLE',
                           'REF_CATASTRAL','N_CARGO','N_FIJO_INMUEBLE','ID_INMUEBLE_AYUN',
                           'N_FINCA','COD_PROVINCIA','PROVINCIA','COD_MUNICIPIO_DGC','COD_MUNICIPIO_INE','MUNICIPIO',
                           'ENTIDAD_MENOR','COD_VIA','TIPO_VIA','N1_POLICIA','L1','N2_POLICIA','L2','KM','BLOQUE',
                           'ESCALERA','PLANTA','PUERTA','DIRECCION','COD_POSTAL','DISTRITO','COD_MUN_AGREGACION',
                           'COD_ZONA_CONCENTRACION','COD_POLIGONO_R','COD_PARCELA','COD_PARAJE','PARAJE',
                            'N_ORDEN_INMUEBLE','ANTIGUEDAD',  'TIPO_INMUEBLE', 'SUPERFICIE_FINCA','SUPERFICIE_SOLAR',
                         'COEFICIENTE_PROPIEDAD']]

    df_tipos = df_cat15[df_cat15["TIPO_INMUEBLE"]=="V"]

    df_tipos["PLANTA"] = parse_mixed_column(df_tipos["PLANTA"])
    df_tipos["PLANTA"] = df_tipos["PLANTA"].fillna(0)

    df_plantas = pd.DataFrame(df_tipos[["REF_CATASTRAL", "PLANTA"]].groupby("REF_CATASTRAL")["PLANTA"].max())
    df_plantas.reset_index(inplace=True)
    return df_plantas

def get_origenes(path, ciudad):

    #RUN
    df_parcelas = gpd.read_file("{}/{}/parcelas_{}.gml".format(path, ciudad["nombre"], ciudad["nombre"]))
    df_parcelas.to_crs(epsg=ciudad["epsg"], inplace=True)
    df_parcelas.rename(columns={"nationalCadastralReference":"nationalCa"}, inplace=True)
    df_cat15 = separacion_registro_inmueble("{}/{}/cat_{}.CAT".format(path, ciudad["nombre"], ciudad["nombre"]))
    df_parcelas_residencial = df_parcelas[df_parcelas["nationalCa"].isin(df_cat15["REF_CATASTRAL"].unique())]
    df_parcelas_residencial = df_parcelas_residencial.merge(df_cat15, how="left", left_on="nationalCa", right_on="REF_CATASTRAL")
    df_parcelas_residencial["PLANTA"] = df_parcelas_residencial["PLANTA"]+1
    df_parcelas_residencial["ALTURA"]= df_parcelas_residencial["PLANTA"]*3
    df_parcelas_residencial["VOLUMEN"]= df_parcelas_residencial["ALTURA"] * df_parcelas_residencial["areaValue"]
    df_parcelas_residencial.rename(columns={"areaValue":"AREA"}, inplace=True)
    return df_parcelas_residencial[["nationalCa", "AREA","PLANTA", "ALTURA", "VOLUMEN","geometry"]]


def get_secciones(year, ciudad):

    BASE_URL = (
    f"https://www.ine.es/geoserver/ogc/features/v1/collections/"
    f"WMS_INE_SECCIONES_G01:Secciones_{year}/items")

    df_secciones = pd.read_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/secciones_pob.csv", sep=";")
    df_secciones["Municipio"] = df_secciones["Municipios"].str.split(" ").str[0]
    df_subset = df_secciones[(df_secciones["Municipio"]=='{}'.format(ciudad["COD_MUNICIPIO"])) & (df_secciones["Sexo"]=='Total')&(df_secciones["Edad"]!='Todas las edades')& (df_secciones["Periodo"]==year)& ~(df_secciones["Secciones"].isna())]
    df_subset["CUSEC"] = df_subset["Secciones"].str.split(" ").str[0]
    df_subset = df_subset[~df_subset["Total"].isna()]
    df_subset["Total"] = df_subset["Total"].astype(str)
    df_subset["Total"] = df_subset["Total"].str.replace(".0$","", regex=True)
    df_subset["Total"] = df_subset["Total"].str.replace(".","")
    df_subset["Total"] = df_subset["Total"].str.replace("","0")
    df_subset["Total"] = df_subset["Total"].astype(int)

    #Total
    df_total = df_secciones[(df_secciones["Municipio"]=='{}'.format(ciudad["COD_MUNICIPIO"])) & (df_secciones["Sexo"]=='Total')&(df_secciones["Edad"]=='Todas las edades')& (df_secciones["Periodo"]==year)& ~(df_secciones["Secciones"].isna())]
    df_total["CUSEC"] = df_total["Secciones"].str.split(" ").str[0]
    df_total = df_total[~df_total["Total"].isna()]
    df_total["Total"] = df_total["Total"].astype(str)
    df_total["Total"] = df_total["Total"].str.replace(".0$","", regex=True)
    df_total["Total"] = df_total["Total"].str.replace(".","")
    df_total["Total"] = df_total["Total"].astype(int)
    df_total = df_total[["CUSEC", "Total"]]
    df_total.rename(columns={"Total":"total"}, inplace=True)

    #3-5 años
    df1 = df_subset[df_subset["Edad"]=="De 5 a 9 años"][["CUSEC","Total"]]
    df1["Total"] =  df1["Total"]*1/5
    df2 = df_subset[df_subset["Edad"]=="De 0 a 4 años"][["CUSEC","Total"]]
    df2["Total"] =  df2["Total"]*2/5
    df_3_5 = df1.merge(df2, how="left", on="CUSEC")
    df_3_5["3_5"] = df_3_5["Total_x"] + df_3_5["Total_y"]
    df_3_5 = df_3_5[["CUSEC","3_5"]]

    #6-11 años
    df1 = df_subset[df_subset["Edad"]=="De 5 a 9 años"][["CUSEC","Total"]]
    df1["Total"] =  df1["Total"]*4/5
    df2 = df_subset[df_subset["Edad"]=="De 10 a 14 años"][["CUSEC","Total"]]
    df2["Total"] =  df2["Total"]*2/5
    df_6_11 = df1.merge(df2, how="left", on="CUSEC")
    df_6_11["6_11"] = df_6_11["Total_x"] + df_6_11["Total_y"]
    df_6_11 = df_6_11[["CUSEC","6_11"]]

    #12-16 años
    df1 = df_subset[df_subset["Edad"]=="De 10 a 14 años"][["CUSEC","Total"]]
    df1["Total"] =  df1["Total"]*3/5
    df2 = df_subset[df_subset["Edad"]=="De 15 a 19 años"][["CUSEC","Total"]]
    df2["Total"] =  df2["Total"]*2/5
    df_12_16 = df1.merge(df2, how="left", on="CUSEC")
    df_12_16["12_16"] = df_12_16["Total_x"] + df_12_16["Total_y"]
    df_12_16 = df_12_16[["CUSEC","12_16"]]

    #17-18 años
    df_17_18 = df_subset[df_subset["Edad"]=="De 15 a 19 años"][["CUSEC","Total"]]
    df_17_18["17_18"] =  df2["Total"]*2/5
    df_17_18 = df_17_18[["CUSEC","17_18"]]

    df_pob = pd.DataFrame(df_17_18["CUSEC"])

    for dataframe in [df_3_5, df_6_11, df_12_16, df_17_18, df_total]:
        print(dataframe.columns)
        df_pob = df_pob.merge(dataframe, how="left", on="CUSEC")


    params = {
        "f"          : "application/geo+json",
        "limit"      : 1500,
        "filter"     : f"CUSEC LIKE '{ciudad["COD_MUNICIPIO"]}%'",
        "filter-lang": "cql2-text",
    }
    
    resp = requests.get(BASE_URL, params=params, timeout=60)
    resp.raise_for_status()
    
    # CUSEC → geometry dict (your logic)
    dict_aux = {
        feat["properties"]["CUSEC"]: feat["geometry"]
        for feat in resp.json()["features"]
    }
    
    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        {"CUSEC": list(dict_aux.keys())},
        geometry=[shape(geom) for geom in dict_aux.values()],
        crs="EPSG:4326",  
    ).to_crs("EPSG:{}".format(ciudad["epsg"])) 
    
    #gdf.to_file("/Users/aidavillalba/Desktop/secciones.geojson")

    gdf_secciones = gdf.merge(df_pob, how="left", on="CUSEC")
    gdf_secciones = gdf_secciones[~(gdf_secciones["total"].isna())]
    return gdf_secciones

def get_poblacion(path, ciudad, year):
    gdf_parcelas = get_origenes(path, ciudad)
    gdf_secciones = get_secciones(year, ciudad)
    gdf_secciones.to_crs(ciudad["epsg"], inplace=True)

    df_ZT = get_zone_shape_spain("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/recintos_municipales_inspire_peninbal_etrs89", ciudad["natcode"])
    df_ZT = df_ZT.to_crs(epsg=ciudad["epsg"])
    df_ZT["buffer"]= df_ZT.buffer(distance=1000)

    df_ZT_buffer = df_ZT[["NATCODE", "buffer"]]
    df_ZT_buffer.rename(columns={"buffer":"geometry"}, inplace=True)
    df_ZT_buffer = gpd.GeoDataFrame(df_ZT_buffer, geometry="geometry", crs=df_ZT.crs)
    
    gdf_intersects = gdf_parcelas.sjoin(gdf_secciones, how="left", predicate="intersects")
    gdf_intersects_residencial = gdf_intersects[~gdf_intersects["total"].isna()]
    gdf_intersects_residencial = gdf_intersects_residencial[["nationalCa","CUSEC", "total", "3_5", "6_11", "12_16", "17_18", "geometry", "ALTURA","AREA","VOLUMEN"]]

    gdf_volumen_sum = gdf_intersects_residencial.groupby(by="CUSEC").sum("VOLUMEN")
    gdf_volumen_sum.reset_index(inplace=True)

    volumen_sum = gdf_volumen_sum.set_index("CUSEC")["VOLUMEN"]

    # Vectorized population estimation for all columns at once
    cols_to_estimate = ["total", "3_5", "6_11", "12_16", "17_18"]  # extend this list as needed

    weight = gdf_intersects_residencial["VOLUMEN"] / gdf_intersects_residencial["CUSEC"].map(volumen_sum)

    for col in cols_to_estimate:
        gdf_intersects_residencial[f"pob_estimated_{col}"] = gdf_intersects_residencial[col] * weight

    # Single overlay (shared geometry, no need to repeat)
    gdf_intersects_residencial_Z = gpd.overlay(
        gdf_intersects_residencial,
        df_ZT[["NATCODE", "geometry"]],
        how="intersection"
    )

    # Apply hamilton_round for each column
    for col in cols_to_estimate:
        gdf_pob = hamilton_round(gdf_intersects_residencial_Z, f"pob_estimated_{col}", col)

    
    #Eliminación outliers area
    q_area = gdf_pob["AREA"].quantile(0.99)
    gdf_pob = gdf_pob[gdf_pob["AREA"] < q_area]
    #Eliminación outliers altura
    q_altura = gdf_pob["AREA"].quantile(0.99)
    gdf_pob = gdf_pob[gdf_pob["AREA"] < q_altura]
    
    #gdf_pob.to_file("/Users/aidavillalba/Desktop/parcelas_secciones.geojson")

    gdf_pob["centroide"] = gdf_pob["geometry"].centroid
    gdf_pob = gdf_pob.loc[:, gdf_pob.columns != "geometry"]
    gdf_pob.rename(columns={"centroide":"geometry"}, inplace=True)

    gdf_pob.set_geometry("geometry", inplace=True, crs="epsg:{}".format(ciudad["epsg"]))
    gdf_pob["TIPO"]="PORTAL"
    gdf_pob = gdf_pob[["nationalCa", "TIPO","ALTURA", "AREA", "VOLUMEN", "total", "3_5", "6_11", "12_16", "17_18", "geometry"]]
    gdf_pob.set_crs("epsg:{}".format(ciudad["epsg"]), allow_override=True, inplace=True)
    gdf_pob.to_file("{}/{}/origenes_{}.geojson".format(path, ciudad["nombre"], ciudad["nombre"]), driver="GeoJSON")
    
    #EXPORT PARADIGM
    gdf_pob["15_99"]=0
    gdf_pob["18_99"]=0
    gdf_pob = gdf_pob[["nationalCa", "3_5", "6_11", "12_16", "17_18", "15_99", "18_99","total"]]
    gdf_pob.to_csv("/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/atributos/atributos_origenes_{}.csv".format(ciudad["nombre"]))

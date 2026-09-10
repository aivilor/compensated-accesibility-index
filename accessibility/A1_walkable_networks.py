import osmnx as ox
import geopandas as gpd
import networkx as nx
import jsonpickle
#import geonetworkx 
import osmnx as ox
import json
from networkx.readwrite import json_graph
import warnings
import pandas as pd
import math
import numpy as np
import warnings
from shapely.geometry import  LineString
from pyproj import Transformer


def get_zone_shape_spain(natcode):
    input_path ="/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos/recintos_municipales_inspire_peninbal_etrs89"
    df_municipios = gpd.read_file(input_path)
    df_municipios = df_municipios[df_municipios["NATCODE"]==natcode]
    return df_municipios

def pesos_red(G, travel_speed):
    #Preprocesamiento del grafo para calcular los pesos de las aristas (tiempo)
    meters_per_minute = travel_speed * 1000 / 60  # km/h a m/min
    for u, v, k, data in G.edges(data=True, keys=True):
        data['time'] = data['length'] / meters_per_minute
    return G

def get_red_caminable(ciudad, travel_speed, output_path):
    
    df_ZT = get_zone_shape_spain(ciudad["natcode"])
    df_ZT.to_crs("EPSG:4326",inplace=True)
    ZT = df_ZT["geometry"].iloc[0]

    #Downloading network from OSM
    G_walk = ox.graph_from_polygon(polygon = ZT, network_type = 'walk')
    G_proj_walk_vlc = ox.project_graph(G_walk, to_crs=ciudad["epsg"]) #BARCELONA ESTÁ EN EL SISTEMA DE REFERENCIA 25831, VALENCIA EN EL 25830
        
    #Weighting the network
    G_jsonVLC = pesos_red(G_proj_walk_vlc, travel_speed)
    G_jsonVLC = nx.MultiGraph(G_jsonVLC)

    #Creating attributes lon and lat for PARADIGM run
    transformer = Transformer.from_crs(ciudad["epsg"], "EPSG:4326", always_xy=True)

    for node_id, data in G_jsonVLC.nodes(data=True):
        lon, lat = transformer.transform(data['x'], data['y'])
        data['lat'] = np.float64(lat)
        data['lon'] = np.float64(lon)


    for u, v, data in G_jsonVLC.edges(data=True):
        data["source"]=u
        data["target"]=v

    #Convertir a diccionario
    G_json = json_graph.node_link_data(G_jsonVLC)
    #Serializar diccionario (codificacion)
    json_string = jsonpickle.encode(G_json)
    #Guardar como diccionario codificado
    with open("{}/network_walk_{}_{}.txt".format(output_path,travel_speed,ciudad["nombre"]), "w") as text_file:
        text_file.write(json_string)

import geopandas as gpd
import osmnx as ox
import jsonpickle
import networkx as nx
from networkx.readwrite import json_graph
import json

path = "/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos"

def get_relaciones_origenes(path, ciudad, red):
    df_origenes = gpd.read_file(r"{}/{}/origenes_{}.geojson".format(path,ciudad["nombre"],ciudad["nombre"]), driver="GeoJSON", crs=ciudad["epsg"])
    #Red
    with open(r"/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/redes/network_{}_5_{}.txt".format(red,ciudad["nombre"]), 'r') as file:
        file_content = file.read()
    recreated_obj = jsonpickle.decode(file_content)
    G_jsonVLC = json_graph.node_link_graph(recreated_obj)
    G_jsonVLC = nx.MultiGraph(G_jsonVLC)
    #Relaciones con la red
    nodos_cercanos = ox.distance.nearest_nodes(G_jsonVLC, df_origenes.geometry.x, df_origenes.geometry.y, return_dist=False)
    relacion_nodos = dict(zip(df_origenes.nationalCa, nodos_cercanos.tolist()))
    with open(r'/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/relaciones/origenes/relacion_origenes_{}_{}.json'.format(red, ciudad["nombre"]), 'w') as fp:
        json.dump(relacion_nodos, fp)

def get_relaciones_destinos(path, ciudad, red,loc):
    df_destinos = gpd.read_file(r"{}/locs/loc{}_{}.geojson".format(path,loc,ciudad["nombre"]), driver="GeoJSON", crs=ciudad["epsg"])
    #Red
    with open(r"/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/redes/network_{}_5_{}.txt".format(red,ciudad["nombre"]), 'r') as file:
        file_content = file.read()
    recreated_obj = jsonpickle.decode(file_content)
    G_jsonVLC = json_graph.node_link_graph(recreated_obj)
    G_jsonVLC = nx.MultiGraph(G_jsonVLC)
    #Relaciones con la red
    nodos_cercanos = ox.distance.nearest_nodes(G_jsonVLC, df_destinos.geometry.x, df_destinos.geometry.y, return_dist=False)
    relacion_nodos = dict(zip(df_destinos.id, nodos_cercanos.tolist()))
    #relacion_nodos = {str(k).lstrip('\ufeff'): v for k, v in relacion_nodos.items()}
    with open(r'/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/relaciones/loc{}/relacion_loc{}_{}_{}.json'.format(loc,loc, red,ciudad["nombre"]), 'w') as fp:
        json.dump(relacion_nodos, fp)

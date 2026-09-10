import Codigo.A1_walkable_networks as A1_walkable_networks
import C2_origins
import C3_destinations
import C4_relationships_paradigm

year = 2025
path = "/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/Datos"
municipios= {
            "Valencia": {"nombre":"Valencia","COD_MUNICIPIO": "46250", "natcode":"34104646250", "epsg":25830},
             "Barcelona": {"nombre":"Barcelona","COD_MUNICIPIO": "08019", "natcode":"34090808019", "epsg":25831},
             "Murcia": {"nombre":"Murcia","COD_MUNICIPIO": "30030", "natcode":"34143030030", "epsg":25830},
             #"Malaga": {"nombre":"Malaga","COD_MUNICIPIO": "29067", "natcode":"34012929067", "epsg":25830},
             }

for ciudad in list(municipios.keys()):
    A1_walkable_networks.get_red_caminable(municipios[ciudad], travel_speed=5, output_path = "/Users/aidavillalba/Desktop/Artículos/2026/02_Mediterranean cities/paradigm/data/redes".format(ciudad,ciudad))
    C2_origins.get_poblacion(path, municipios[ciudad], year)
    C4_relationships_paradigm.get_relaciones_origenes(path, municipios[ciudad], "walk")
    for loc in [1,2,3,4]:
        C4_relationships_paradigm.get_relaciones_destinos(path, municipios[ciudad], "walk",loc)


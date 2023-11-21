import geopandas as gpd
from shapely.geometry import Point

def getProvince(latitude, longitude):
    # Cargar el archivo GeoJSON en un GeoDataFrame
    gdf = gpd.read_file('provincias-espanolas.geojson')
    # Crear un objeto Point con las coordenadas dadas
    point = Point(longitude, latitude)
    # Iterar sobre las filas del GeoDataFrame y verificar si el punto está dentro de alguna provincia
    for index, row in gdf.iterrows():
        if point.within(row['geometry']):
            return row['provincia']
    return 'Fail'

def getCoordinates(selected_province):
    # Cargar el archivo GeoJSON en un GeoDataFrame
    gdf = gpd.read_file('provincias-espanolas.geojson')
    # Filtrar el GeoDataFrame para obtener la geometría de la provincia seleccionada
    selected_province_geometry = gdf[gdf['provincia'] == selected_province]['geometry'].iloc[0]
    # Obtener las coordenadas del centro de la geometría
    center_coordinates = selected_province_geometry.centroid.coords[0]
    # Retornar latitud y longitud
    return center_coordinates[1], center_coordinates[0]
import geopandas as gpd
import streamlit_folium as st_folium
import folium

def render_country_map(gdf):
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=5)
    folium.GeoJson(gdf).add_to(m)
    return st_folium.folium_static(m)
import geopandas as gpd
import pandas as pd
import streamlit as st
#import folium
from streamlit_folium import st_folium
import pydeck as pdk
import json
import leafmap.foliumap as leafmap
import branca.colormap as cm

@st.cache_resource
def load_geojson(path):
    return gpd.read_file(path)

#@st.cache_data
def merge_geojson_data(gdf, df, geojson_key="Provinces", data_key="Provinces"):
    df[data_key] = df[data_key].str.strip()
    gdf[geojson_key] = gdf[geojson_key].str.strip()
    return gdf.merge(df, left_on=geojson_key, right_on=data_key, how="left")


# def highlight_selected_province(gdf, variable, selected_province):
#     projected_gdf = gdf.to_crs(epsg=3857)
#     centroid_projected = projected_gdf.geometry.unary_union.centroid
#     centroid_latlon = gpd.GeoSeries([centroid_projected], crs=3857).to_crs(4326).geometry[0]

    # m = folium.Map(location=[centroid_latlon.y, centroid_latlon.x], zoom_start=6, )

    # folium.Choropleth(
    #     geo_data=gdf,
    #     data=gdf,
    #     columns=["Provinces", variable],
    #     key_on="feature.properties.Provinces",
    #     fill_color="YlGnBu",
    #     fill_opacity=0.9,
    #     line_opacity=0.2,
    #     legend_name=variable,
    #     linew_weight=0.5
    # ).add_to(m)

    # selected = gdf[gdf["Provinces"] == selected_province]
    # if not selected.empty:
    #     folium.GeoJson(
    #         selected,
    #         style_function=lambda _: {
    #             "fillColor": "red",
    #             "color": "black",
    #             "weight": 0.5,
    #             "fillOpacity": 0.6
    #         },
    #         tooltip=folium.GeoJsonTooltip(fields=["Provinces", variable])
    #     ).add_to(m)

    # # Add a GeoJson layer with popup for click info
    # geojson_layer = folium.GeoJson(
    #     gdf,
    #     name="Provinces",
    #     style_function=lambda feature: {
    #         #"fillColor": "#74c476",
    #         "color": "black",
    #         "weight": 0.3,      # <<< reduce this for thin borders
    #         "fillOpacity": 0
    #     },
    #     tooltip=folium.GeoJsonTooltip(fields=["Provinces", variable]),
    #     popup=folium.GeoJsonPopup(fields=["Provinces", variable])
    
    # )
    # geojson_layer.add_to(m)

    # # Render map with streamlit-folium and capture last clicked feature
    # map_data = st_folium(m, use_container_width=True, height=600)

    # Replace 2 GeoJsons with a single one that does all

    # Process click event data from streamlit-folium
    # if map_data and map_data.get("last_clicked"):
    #     clicked_props = map_data["last_clicked"]["properties"]
    #     clicked_province = clicked_props.get("Provinces")
    #     if clicked_province:
    #         # Filter data for clicked province
    #         province_stats = gdf[gdf["Provinces"] == clicked_province].iloc[0]
    #         st.write(f"### Statistics for {clicked_province}")
    #         st.write(f"**{variable}:** {province_stats[variable]}")


def highlight_selected_province(gdf, variable, selected_province):
    gdf = gdf.to_crs(epsg=4326)

    # Create popup HTML column
    gdf["popup"] = (
        "<b>Province:</b> " + gdf["Provinces"] +
        "<br><b>" + variable + ":</b> " + gdf[variable].astype(str)
    )

    # Create a colormap from min to max values
    min_val, max_val = gdf[variable].min(), gdf[variable].max()
    colormap = cm.LinearColormap(
        colors=["yellow", "green", "blue"],
        vmin=min_val,
        vmax=max_val,
        caption=variable,
    )

    geojson_data = json.loads(gdf.to_json())

    # Center the map
    bounds = gdf.total_bounds
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]

    m = leafmap.Map(center=center, zoom=6)

    # Style function: color by variable, highlight selected province in red
    def style_function(feature):
        province = feature["properties"]["Provinces"]
        value = feature["properties"].get(variable, None)
        if province == selected_province:
            fill_color = "red"
            fill_opacity = 0.7
        else:
            # Handle missing values gracefully
            fill_color = colormap(value) if value is not None else "#gray"
            fill_opacity = 0.8
        return {
            "fillColor": fill_color,
            "color": "black",
            "weight": 1,
            "fillOpacity": fill_opacity,
        }

    m.add_geojson(
        geojson_data,
        layer_name="Provinces",
        style_function=style_function,
        info_mode="on_hover",
        # no popup argument here — 'popup' field auto used
    )

    # Add colormap legend to map
    colormap.add_to(m)

    m.to_streamlit(height=600)

    # Show stats for selected province
    if selected_province and selected_province in gdf["Provinces"].values:
        province_stats = gdf[gdf["Provinces"] == selected_province].iloc[0]
        st.markdown(f"### 📍 Statistics for **{selected_province}**")
        st.write(f"**{variable}:** {province_stats[variable]:,.2f}")
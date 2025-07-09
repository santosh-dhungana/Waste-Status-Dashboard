import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium
import folium
import os
import base64
from utils.css_injector import inject_global_css

inject_global_css()

# Data: locations with names and URLs
locations = [
    {"name": "Mathare", "lat": -1.2634, "lon": 36.8569, "url": "https://storymaps.arcgis.com/stories/41eb4771bfb44f0ebb3d6e915f65bd59"},
    {"name": "Turkey", "lat": 39.9208, "lon": 32.8541, "url": "https://en.wikipedia.org/wiki/Turkey"},
    {"name": "Lebanon", "lat": 33.8547, "lon": 35.8623, "url": "https://en.wikipedia.org/wiki/Lebanon"},
    {"name": "Libya", "lat": 26.3351, "lon": 17.2283, "url": "https://en.wikipedia.org/wiki/Libya"},
    {"name": "Syria", "lat": 34.8021, "lon": 38.9968, "url": "https://en.wikipedia.org/wiki/Syria"},
]

# Create DataFrame and GeoDataFrame
df = pd.DataFrame(locations)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")

# Sidebar: Location selector
st.sidebar.title("📄 Story Maps PDFs")
location_names = [loc["name"] for loc in locations]
selected_location = st.sidebar.selectbox("Select a location", location_names)

# Sidebar: Load and display corresponding PDF
pdf_path = f"data/pdfs/{selected_location}.pdf"

if os.path.exists(pdf_path):
    # with open(pdf_path, "rb") as f:
    #     base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
    # st.sidebar.markdown(pdf_display, unsafe_allow_html=True)

    with st.sidebar:
        #st.markdown("### 📄 Report Available")
        st.markdown(
            f'<a href="{pdf_path}" target="_blank">📑 <b>Open PDF Report for {selected_location}</b></a>',
            unsafe_allow_html=True
        )
else:
    st.sidebar.warning("PDF not found for this location.")


# Center map roughly at average location
avg_lat = df['lat'].mean()
avg_lon = df['lon'].mean()

m = folium.Map(location=[avg_lat, avg_lon], zoom_start=3, tiles='CartoDB positron')

# Prepare GeoJSON FeatureCollection with properties
features = []
for _, row in gdf.iterrows():
    feature = {
        "type": "Feature",
        "properties": {
            "name": row["name"],
            "url": row["url"]
        },
        "geometry": {
            "type": "Point",
            "coordinates": [row["lon"], row["lat"]]
        }
    }
    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# JavaScript function to bind popup and click event
click_js = """
function onEachFeature(feature, layer) {
    // Tooltip with styled name on hover
    layer.bindTooltip(
        '<span style="color: blue; text-decoration: underline; cursor: pointer;">' +'Click on to view story maps for ' + feature.properties.name + '</span>',
        {sticky: true}
    );
    // When clicked, open the url in new tab
    layer.on('click', function(e) {
        window.open(feature.properties.url, '_blank');
    });
}
"""

folium.GeoJson(
    geojson,
    name="Locations",
    on_each_feature=click_js,
    marker=folium.Marker(radius=8, color='gray', fill=True, fill_color='gray')
).add_to(m)

st.subheader("Click Markers for Story Maps")
#st.markdown("Hover for blue underlined name tooltip, click marker to open Wikipedia page.")

st_folium(m, use_container_width=True,height=900)

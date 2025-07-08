
import streamlit as st
import pandas as pd
from utils.geo_utils import (
    load_geojson,
    merge_geojson_data,
    #plot_choropleth_map,
    highlight_selected_province
)
from utils.data_utils import (
    load_waste_data,
    plot_province_stats,
    aggregate_country_stats
)
import altair as alt

#page layout setup
from utils.css_injector import inject_global_css
from utils.horizontal_nav import navbar


inject_global_css()


# --- Page setup ---
st.set_page_config(page_title="🌍 Waste Dashboard", layout="wide")
st.title("🗺️ Municipal WasteManagement Dashboard - 🇹🇷")

# --- Load data ---
country_options = ["Turkey"]  # Expand this list for future countries
selected_country = st.sidebar.selectbox("🌐 Select Country", country_options)

# Data paths (adjust as needed)
GEO_PATHS = {
    "Turkey": "data/provinces/provincesonly.geojson"
}
DATA_PATHS = {
    "Turkey": "data/Provincewise_stats.txt"
}

gdf = load_geojson(GEO_PATHS[selected_country])

df = load_waste_data(DATA_PATHS[selected_country])
merged_gdf = merge_geojson_data(gdf, df, geojson_key="Provinces", data_key="Provinces")

# Filtered provinces per country
province_list = merged_gdf["Provinces"].dropna().sort_values().unique()
selected_province = st.sidebar.selectbox("🏙️ Select a Province", province_list)



# --- Multiselect for bar chart variables ---
st.sidebar.markdown("### 📊 Compare Metrics Across Provinces")
bar_variables = st.sidebar.multiselect(
    "Select variables to compare:",
    [
        "Population",
        "Population served by waste service",
        "Waste Collected [Tonnes]"
    ],
    default=["Population"]  # Set a sensible default
)

# --- Province-level map & stats (unchanged) ---
highlight_selected_province(merged_gdf, "Waste service coverage by population", selected_province)

st.subheader(f"📌 Stats for {selected_province}")
selected_data = merged_gdf[merged_gdf["Provinces"] == selected_province]
plot_province_stats(selected_data)

# --- Bar chart ---
if bar_variables:
    st.subheader(f"📊 Selected Metrics Across Provinces")

    # Filter and reshape data for Altair
    chart_data = merged_gdf[["Provinces"] + bar_variables].copy()
    chart_data = chart_data.dropna()
    for col in bar_variables:
        chart_data[col] = pd.to_numeric(chart_data[col], errors="coerce")

    # Melt the dataframe to long format for Altair grouped bar chart
    chart_data_long = chart_data.melt(id_vars="Provinces", value_vars=bar_variables,
                                    var_name="Metric", value_name="Value")

    # Altair grouped bar chart
    bar_chart = alt.Chart(chart_data_long).mark_bar().encode(
        x=alt.X("Provinces:N", title="Province", sort="-y"),
        y=alt.Y("Value:Q", title="Value"),
        color=alt.Color("Metric:N", title="Metric"),
        tooltip=["Provinces", "Metric", "Value"]
    ).properties(width=900, height=400)

    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.warning("Please select at least one variable to display the bar chart.")

# --- Country Aggregates ---
# st.subheader(f"📈 Country Summary: {selected_country}")
# country_summary = aggregate_country_stats(merged_gdf)

# st.markdown(f"""
# - **Total Municipal Population**: {int(country_summary['Population']):,}
# - **Avg. Waste per Capita**: {country_summary['Waste per capita (kg/capita-day)']:.2f} kg/person/day
# - **Waste Service Coverage (avg %)**: {country_summary['Waste service coverage by population']:.1f}%
# """)
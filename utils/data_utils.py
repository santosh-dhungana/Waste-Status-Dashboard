import pandas as pd
import streamlit as st
import altair as alt

def load_waste_data(path):
    df = pd.read_csv(path, sep='\t', header=0)
    for col in df.columns:
        if col not in ['Provinces'] and df[col].dtypes =='object':
            df[col] = df[col].apply(lambda x: x.replace(' ',''))
            df[col]=pd.to_numeric(df[col])
    return df





#former data
def plot_province_stats(gdf_row):
    if gdf_row.empty:
        st.info("No data for selected province.")
        return
    
    #gdf_row["Number of Municipalities"] = gdf_row["Number of Municipalities"].fillna(0).astype(int)
    gdf_row.loc[:, "Number of Municipalities"] = gdf_row["Number of Municipalities"].astype(int)
    

    row = gdf_row.iloc[0]

    # -- Row 1: Municipalities
    st.markdown("### 🏛️ Municipalities Providing Services")
    total = int(row["Number of Municipalities"])
    provided = int(row["Waste service providing municipalities"])
    ratio = provided / total if total > 0 else 0

    st.write(f"**{provided} out of {total} municipalities** provide waste collection services.")
    st.progress(ratio)

    # -- Row 2: Population Served
    st.markdown("### 👥 Population Covered by Waste Services")
    coverage = float(row["Waste service coverage by population"])
    st.progress(min(coverage / 100, 1.0))
    st.write(f"**{coverage:.1f}%** of population is served.")

    # -- Row 3: Waste per Capita
    st.markdown("### ♻️ Waste Generated per Person")
    per_capita = float(row["Waste per capita (kg/capita-day)"])

    st.markdown(f"""
    <div style='font-size: 16px; display: flex; align-items: center; gap: 8px;'>
        👤 {per_capita:.2f} kg/person/day
    </div>
    """, unsafe_allow_html=True)

def aggregate_country_stats(df):
    #print('lendf:', len(df['Population']), df.columns)
    return {
        "Population": df["Population"].sum(),
        "Waste Collected [Tonnes]": df["Waste Collected [Tonnes]"].sum(),
        "Waste per capita (kg/capita-day)": df["Waste per capita (kg/capita-day)"].mean(),
        "Waste service coverage by population": df["Waste service coverage by population"].mean()
    }

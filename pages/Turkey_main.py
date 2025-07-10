import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
import io
import zipfile
import base64
from plotly.subplots import make_subplots
from utils.css_injector import inject_global_css
from utils.horizontal_nav import navbar



inject_global_css()
#navbar()
# --- Page config ---
st.set_page_config("🇹🇷 Country Waste Dashboard", layout="wide")
st.title("🇹🇷  National Waste Management Dashboard")

# --- Load Data ---
@st.cache_data
def load_country_data(path):
    df = pd.read_csv(path, index_col=0)
    df = df.transpose().reset_index().rename(columns={'index': 'Year'})
    df['Year'] = df['Year'].astype(int)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

country_data = load_country_data("data/TurkeyWastemanagement_status.csv")


# --- Sidebar Navigation ---
st.sidebar.header("🌍 Country Dashboard")

with st.sidebar.expander("🇹🇷 Turkey", expanded=True):  # You can set expanded=False by default
    country = "Turkey"  # Only Turkey available, can be dynamic
    years = country_data['Year'].unique()

    selected_year = st.select_slider(
        "📆 Select Year [Change Years]",
        options=sorted(years),
        value=max(years)
    )

    # Download Button
    st.download_button(
        label="📥 Download Data as CSV",
        data='',
        file_name="turkey_population.csv",
        mime="text/csv"
    )
    

    # Here you can add a map or other visualizations as needed


# # --- Sidebar Controls ---
# st.sidebar.header("🔧 Controls")
# country = st.sidebar.selectbox("🌐 Select Country", ["Turkey"])
# years = country_data['Year'].unique()

# selected_year = st.sidebar.select_slider(
#     "📆 Select Year",
#     options=sorted(country_data['Year'].unique()),
#     value=max(country_data['Year'].unique())
# )

# # Filter data based on selected year (include all years <= selected year)
# filtered_data = country_data[country_data['Year'] <= selected_year]

# # Get selected year row for stats
# year_data = country_data[country_data['Year'] == selected_year].squeeze()

# # --- Sidebar Summary Stats ---
# coverage = float(year_data.get("Rate of municipal population served by waste services in total municipal population (%)", 0))
# bar_color = "green" if coverage > 90 else "orange" if coverage > 75 else "red"

# st.sidebar.markdown("#### 🧾 Summary Stats")
# st.sidebar.markdown(f"""
#         <style>
#         .sidebar-box {{
#             background-color: #f9f9f9;
#             padding: 12px 16px;
#             border-radius: 8px;
#             box-shadow: 1px 1px 6px rgba(0,0,0,0.05);
#             margin-top: 10px;
#         }}
#         .sidebar-box .row {{
#             display: flex;
#             justify-content: space-between;
#             margin-bottom: 6px;
#             font-size: 15px;
#             font-family: sans-serif;
#         }}
#         .sidebar-box .label {{
#             font-weight: 500;
#             color: #333;
#         }}
#         .sidebar-box .value {{
#             font-weight: 600;
#             color: #000;
#         }}
#         </style>

#         <div class="sidebar-box">
#             <div class="row"><div class="label">Selected Year</div><div class="value">{selected_year}</div></div>
#             <div class="row"><div class="label">Total Population</div><div class="value">{int(year_data['Turkey population']):,}</div></div>
#             <div class="row"><div class="label">Municipal Population</div><div class="value">{int(year_data['Total municipal population']):,}</div></div>
#             <div class="row"><div class="label">Municipalities</div><div class="value">{int(year_data['Total number of municipalities']):,}</div></div>
#             <div class="row"><div class="label">Waste/Capita</div><div class="value">{year_data['Average amount of municipal waste per capita (Kg/capita-day)']:.2f} kg/day</div></div>
#         </div>
# """, unsafe_allow_html=True)


    # # Progress bar for indicator
    # def custom_sidebar_progress(label, percent):
    #     if percent > 90:
    #         progress_color ="#4CAF50"  # Green
    #     elif 75 <= percent <= 90:
    #         progress_color = "#FFC107"  # Yellow
    #     else:
    #         progress_color ="#F44336"  # Red
    #     #progress_color = "#4CAF50"  # Green
    #     st.sidebar.markdown(f"""
    #     <div style="margin-bottom: 10px;">
    #         <div style="font-weight: bold; margin-bottom: 4px;">{label}: {round(percent *100,2)}%</div>
    #         <div style="background-color: #e0e0e0; border-radius: 8px; height: 16px;">
    #             <div style="
    #                 background-color: {progress_color};
    #                 width: {round(percent *100,2)}%;
    #                 height: 100%;
    #                 border-radius: 8px;">
    #             </div>
    #         </div>
    #     </div>
    #     """, unsafe_allow_html=True)

    # # --- Sidebar Waste Coverage Bar ---
    # st.sidebar.markdown("### 🏠 Waste Service Coverage")
    # #st.sidebar.progress(coverage / 100)
    # custom_sidebar_progress("Coverage", coverage / 100)
    # st.sidebar.markdown(
    #     f"<span style='font-size:16px;color:{bar_color};'><strong>{coverage:.1f}%</strong> served</span>",
    #     unsafe_allow_html=True,
    # )


#--------------------------Format Tabs Layout----------------------------------------------------------------------
# Inject custom CSS for box-like tab styling
# Custom CSS for dark theme tabs
# Inject custom CSS for styled tabs
# Custom CSS for styled tabs with bold, larger text
st.markdown("""
    <style>
    /* Tab container */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        gap: 6px;
        background-color: transparent;
        padding: 0;
        font-weight: 800;
        font-size: 24px;
        margin-bottom: -1px;
    }
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p{
        display: flex;
        gap: 6px;
        background-color: transparent;
        padding: 0;
        font-weight: 600;
        font-size: 18px;
        margin-bottom: -1px;
        #color: #034694;;
    }

    /* Unselected tab style */
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f0f0;
        color: #034694;
        padding: 12px 20px;
        border: 1px solid #f0f0f0;
        border-radius: 6px 6px 0 0;
        font-family: sans-serif;
        font-weight: 800; /* Bold */
        font-size: 24px;  /* Slightly larger */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        transition: all 0.2s ease;
    }

    /* Selected tab style */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #ffffff;
        color: #000000;
        font-weight: 800;
        font-size: 24px;
        border-bottom: none;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.10);
        z-index: 2;
    }

    /* Tab content box */
    .stTabs + div {
        background-color: #ffffff;
        padding: 20px;
        border: 1px solid #c0d4ec;
        border-top: none;
        border-radius: 0 0 6px 6px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)


# # Create tabs
# tab1, tab2, tab3, tab4 = st.tabs(["Demography", "SPC", "Waste By Industry Sub-sector", "Sewage"])


# add tabbs
tab1, tab2, tab3, tab4 = st.tabs(["Demography", "Climate Change, Air Quality and Socioeconomic", "Waste By Industry Sub-sector", "Industrial Manufacturing Waste"])

# css = '''
# <style>
#     .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
#     font-size:2rem;
#     }
# </style>
# '''

# st.markdown(css, unsafe_allow_html=True)

with tab1:

# Statistics only for the demography tab


    # Filter data based on selected year (include all years <= selected year)
    filtered_data = country_data[country_data['Year'] <= selected_year]

    # Get selected year row for stats
    year_data = country_data[country_data['Year'] == selected_year].squeeze()

    # --- Stats logic ---
    coverage = float(year_data.get("Rate of municipal population served by waste services in total municipal population (%)", 0))
    bar_color = "#4CAF50" if coverage > 90 else "#FFC107" if coverage > 75 else "#F44336"

    # --- Summary Stats ---
    st.markdown("#### 🧾 Summary Stats")
    st.markdown(f"""
            <style>
            .sidebar-box {{
                background-color: #f9f9f9;
                padding: 12px 16px;
                border-radius: 8px;
                box-shadow: 1px 1px 6px rgba(0,0,0,0.05);
                margin-top: 10px;
            }}
            .sidebar-box .row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 6px;
                font-size: 15px;
                font-family: sans-serif;
            }}
            .sidebar-box .label {{
                font-weight: 500;
                color: #333;
            }}
            .sidebar-box .value {{
                font-weight: 600;
                color: #000;
            }}
            </style>

            <div class="sidebar-box">
                <div class="row"><div class="label">Selected Year</div><div class="value">{selected_year}</div></div>
                <div class="row"><div class="label">Total Population</div><div class="value">{int(year_data['Turkey population']):,}</div></div>
                <div class="row"><div class="label">Municipal Population</div><div class="value">{int(year_data['Total municipal population']):,}</div></div>
                <div class="row"><div class="label">Municipalities</div><div class="value">{int(year_data['Total number of municipalities']):,}</div></div>
                <div class="row"><div class="label">Waste/Capita</div><div class="value">{year_data['Average amount of municipal waste per capita (Kg/capita-day)']:.2f} kg/day</div></div>
            </div>
    """, unsafe_allow_html=True)

    # --- Custom Color Progress Bar ---
    st.markdown(f"""
        <div style="margin-top: 12px;">
            <div style="font-weight: bold; margin-bottom: 4px;", color={bar_color}>🏠 Waste Service Coverage: {coverage:.1f}%</div>
            <div style="background-color: #e0e0e0; border-radius: 8px; height: 16px;">
                <div style="
                    background-color: {bar_color};
                    width: {coverage}%;
                    height: 100%;
                    border-radius: 8px;">
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


    # --- Sidebar Dropdown for Additional Metric ---
    core_metrics = [
        "Turkey population", "Total municipal population", "Total number of municipalities"
    ]
    remaining_metrics = [col for col in country_data.columns if col not in core_metrics + ['Year']]
    # Default to first available metric
    default_metric = remaining_metrics[0] if remaining_metrics else None

    # --- Layout ---
    col1, col2 = st.columns([1.2, 1.3], border=False)

    with col1:
        
        st.subheader("🗺️ Country Map")

        # Inject CSS to change bottom margin
        st.markdown("""
            <style>
            .folium-map {
                margin-bottom: 0px; !important; /* adjust this value as needed */
                margin-top : 0px
            }
            </style>
        """, unsafe_allow_html=True)

        m = folium.Map(location=[39.0, 35.0], zoom_start=6)
        folium.Marker(location=[39.0, 35.0], popup=country).add_to(m)
        st_data = st_folium(m, width=700, height=350)

        # --- Chart 2b: Pie Chart for Disposal Facilities (Selected Year) ---
        st.subheader(f"🏭 Waste Disposal Infrastructure ({selected_year})")

        pie_labels = [
            "Waste treatment facilities",
            "Municipality’s dumping sites",
            "Other disposal methods(3)",
        ]

        pie_values = [year_data.get(label, 0) for label in pie_labels]

        fig_pie = px.pie(
            names=pie_labels,
            values=pie_values,
            title="Disposal Methods Breakdown",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            margin=dict(t=0, b=0, l=10, r=10),
            height=350, 
            legend= dict(font=dict(size=10)),
            )

        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # --- Chart 1: Population and Municipalities ---
        st.subheader("📈 Demographics")
        df1 = filtered_data[['Year', 'Turkey population', 'Total municipal population', 'Total number of municipalities']].dropna()

        fig1 = go.Figure()
        fig1.add_bar(x=df1['Year'], y=df1['Turkey population'], name='Total Population', marker_color='steelblue')
        fig1.add_bar(x=df1['Year'], y=df1['Total municipal population'], name='Municipal Population', marker_color='lightblue')
        fig1.add_trace(go.Scatter(x=df1['Year'], y=df1['Total number of municipalities'],
                                mode='lines+markers', name='Municipalities',
                                yaxis='y2', line=dict(color='red', width=2)))

        fig1.update_layout(
            barmode='group',
            height=350,
            margin=dict(t=0, b=10),
            yaxis=dict(title='Population'),
            yaxis2=dict(title='Municipalities', overlaying='y', side='right'),
            legend=dict(orientation='h', yanchor='bottom', y=1.0, xanchor='right', x=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

        # --- Chart 2: Dynamic Additional Metric ---
        st.subheader("🗑️ Waste Generated, Collected & Per Capita")

        waste_cols = [
            "Amount of municipal waste generated (Thousand tonnes/year)",
            "Amount of municipal waste collected (Thousand tonnes/year)",
        ]
        per_capita_col = "Average amount of municipal waste per capita (Kg/capita-day)"

        df_waste = filtered_data[['Year'] + waste_cols + [per_capita_col]].dropna()

        fig_combo = go.Figure()

        # Bars
        for col in waste_cols:
            fig_combo.add_trace(go.Bar(
                x=df_waste['Year'],
                y=df_waste[col],
                name=col,
                marker=dict(opacity=0.7)
            ))

        # Line (secondary Y)
        fig_combo.add_trace(go.Scatter(
            x=df_waste['Year'],
            y=df_waste[per_capita_col],
            name='Per Capita Waste (kg/day)',
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='black', dash='dash')
        ))

        fig_combo.update_layout(
            height=350,
            barmode='group',
            yaxis=dict(title='Waste (Thousand tonnes)'),
            yaxis2=dict(
                title='Per Capita (kg/day)',
                overlaying='y',
                side='right',
                showgrid=False
            ),
            legend=dict(orientation='h', yanchor='bottom', y=1.0, xanchor='right', x=1),
            margin=dict(t=10, b=10)
        )

        st.plotly_chart(fig_combo, use_container_width=True)

    # #---------------------Separator--------------------
    # st.markdown("---")

with tab2:

    @st.cache_data
    def spc_data_format(path):
        df = pd.read_csv(path, index_col=0)
        df = df.transpose().reset_index().rename(columns={'index': 'Year'})
        df['Year'] = df['Year'].astype(int)
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    spc_data = spc_data_format("data/SPC.csv")

    # Filter data based on selected year (include all years <= selected year)
    spc_filtered_data = spc_data[spc_data['Year'] <= selected_year]
    #print(spc_filtered_data.head(), spc_filtered_data.columns)

    # Get selected year row for stats
    spc_year_data = spc_data[spc_data['Year'] == selected_year].squeeze()

    # --- Sidebar Dropdown for Additional Metric ---
    mineral_metrics = [
        "Raw material use", "Mineral depletion", "Fossil fuels depletion", "Climate Change (Short-Term)", "Climate Change (Long-Term)"
    ]
    airpol_metrics =['Air pollution (human health)', 'GDP (constant 2015 USD)', 'Climate Change (Long-Term)']
    vulnerable_metrics = [col for col in spc_data.columns if col not in mineral_metrics + airpol_metrics+ ['Year']]
    # Default to first available metric
    default_metric = vulnerable_metrics[0] if vulnerable_metrics else None

    #climate change plot
    #st.subheader("📈 Demographics")
    df_mineral = spc_filtered_data[["Year"]+ mineral_metrics].dropna()

    st.subheader('Climate change effects on mineral extraction and usage')
    fig_mineral = go.Figure()
    for col in mineral_metrics:
        fig_mineral.add_trace(go.Scatter(x=df_mineral['Year'], y=df_mineral[col],
                                mode='lines+markers', name='Climate change effects on <br> mineral extraction and usage',
                                yaxis='y1', line=dict( width=2)))

    fig_mineral.update_layout(
        #barmode='group',
        #title ='Climate change effects on mineral extraction and usage',
        height=250,
        margin=dict(t=30, b=0),
        yaxis=dict(title='Million of tonnes <br> copper, oil, carbon equivalent)'),
        #yaxis2=dict(title='Municipalities', overlaying='y', side='right'),
        legend=dict(orientation='v', y=1.0, x=1.03, xanchor='left', yanchor='top',)
    )
    st.plotly_chart(fig_mineral, use_container_width=True)
    

    #---------------------Separator--------------------
    st.markdown("---")
    

    # --- Layout ---
    col1, col2 = st.columns([1.2, 1.3])

    with col1:

        # Inject CSS to change bottom margin
        st.markdown("""
            <style>
            .folium-map {
                margin-bottom: 0px !important; /* adjust this value as needed */
            }
            </style>
        """, unsafe_allow_html=True)

        m_mineral = folium.Map(location=[39.0, 35.0], zoom_start=6)
        folium.Marker(location=[39.0, 35.0], popup=country).add_to(m_mineral)
        st_data_mineral = st_folium(m_mineral, width=700, height=350, key='mineral')


    with col2:
        # --- Chart 1: Population and Municipalities ---
        # Toggle between chart types
        is_line = st.toggle("Change Chart", value=True, key="Toggle1")

        # Prepare data
        df_vul = spc_filtered_data[['Year'] + vulnerable_metrics].copy()
        col1, col2 = df_vul.columns[1], df_vul.columns[2]

        # Replace 0 with None (so Plotly won't plot them)
        df_vul[col1] = df_vul[col1].replace(0, None)
        df_vul[col2] = df_vul[col2].replace(0, None)

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Define traces
        if is_line:
            trace1 = go.Scatter(x=df_vul["Year"], y=df_vul[col1], name=col1, mode='lines+markers')
            trace2 = go.Scatter(x=df_vul["Year"], y=df_vul[col2], name=col2, mode='lines+markers')
        else:
            trace1 = go.Bar(x=df_vul["Year"], y=df_vul[col1], name=col1)
            trace2 = go.Bar(x=df_vul["Year"], y=df_vul[col2], name=col2)

        # Add traces to plot
        fig.add_trace(trace1, secondary_y=False)
        fig.add_trace(trace2, secondary_y=True)

        # Layout styling
        fig.update_layout(
            title="Enery Usage and Landuse",
            height=350,
            margin=dict(t=20, b=0, l=30, r=30),
            legend=dict(x=0.5, y=1.02, xanchor="center", orientation="h")
        )

        fig.update_yaxes(title_text=col1 +' [PJ]', secondary_y=False)
        fig.update_yaxes(title_text=col2+' [Million ha]', secondary_y=True)

        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        
    #---------------------Separator--------------------
    st.markdown("---")

    # --- Chart 2: Dynamic Additional Metric --- if needed one indentation to right will shift it to column2
    #st.header()
    st.subheader('Public health and environmental impact assessments')
    df_air = spc_filtered_data[['Year'] + airpol_metrics].dropna()

    fig_combo_air = go.Figure()

    # Bars
    
    fig_combo_air.add_trace(go.Bar(
        x=df_air['Year'],
        y=df_air['GDP (constant 2015 USD)'],
        name='GDP (constant 2015 USD)',
        marker=dict(opacity=0.7)
    ))

    # Line (secondary Y)
    for col in airpol_metrics:
        if col not in ['GDP (constant 2015 USD)']:

            fig_combo_air.add_trace(go.Scatter(
                x=df_air['Year'],
                y=df_air[col],
                name=col,
                yaxis='y2',
                mode='lines+markers',
                line=dict( dash='dash')
            ))

    fig_combo_air.update_layout(
        height=350,
        barmode='group',
        yaxis=dict(title='GDP (constant 2015 USD)'),
        yaxis2=dict(
            title='Air Pollution, Climate change, <br> kilo-disability adjusted life years, <br> Co2 emissions',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=0, b=10)
    )

    st.plotly_chart(fig_combo_air, use_container_width=True)


with tab3:

    #wis- waste by manufacturing industry sub-sector
    @st.cache_data
    def wis_data_format(path):
        df = pd.read_csv(path, index_col=0)
        # df = df.transpose().reset_index().rename(columns={'index': 'Year'})
        # df['Year'] = df['Year'].astype(int)
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.melt(id_vars="Industry Sub-sectors", var_name="Year", value_name="Amount of Waste [Thousand of Tonnes]")
        return df

    wis_data = wis_data_format("data/WasteByIndustrySubSector.csv")
    #print(wis_data.head())

    # --- Layout ---
    col1, col2 = st.columns([1.2, 1.3])

    with col1:

        # Inject CSS to change bottom margin
        st.markdown("""
            <style>
            .folium-map {
                margin-bottom: 0px !important; /* adjust this value as needed */
            }
            </style>
        """, unsafe_allow_html=True)

        m_wis = folium.Map(location=[39.0, 35.0], zoom_start=6)
        folium.Marker(location=[39.0, 35.0], popup=country).add_to(m_wis)
        st_data_wis = st_folium(m_wis, width=700, height=500, key='wis_folium')
        

    with col2:
        # --- Chart 1: Population and Municipalities ---
        # Toggle between chart types
        is_toggle = st.toggle("Change Chart", value=True, key="wis_toggle")
        x_col ='Industry Sub-sectors'
        y_cols =[col for col in wis_data.columns if col not in [x_col]]
        # Define traces
        st.subheader('Waste Generated from Manufacturing Industry')
        #fig_wis = go.Figure()
    
        if is_toggle:
            fig_wis= px.bar(
                wis_data,
                y="Industry Sub-sectors",
                x="Amount of Waste [Thousand of Tonnes]",
                color="Year",
                barmode="group",
                orientation='h',
                labels={"Amount of Waste [Thousand of Tonnes]": "Amount of Waste [Thousand of Tonnes]", "Industry Sub-sectors": "Manufacturing Industry Sub-sectors"}
                #title="Industry Sub-Sector Waste Comparison (2020 vs 2022)"
            )


            #trace2 = go.Scatter(x=df_vul["Year"], y=df_vul[col2], name=col2, mode='lines+markers')
        else:
            fig_wis= px.line(
                wis_data,
                x="Industry Sub-sectors",
                y="Amount of Waste [Thousand of Tonnes]",
                color="Year",
                #barmode="group",
                markers=True,
                #title="Industry Sub-Sector Waste Comparison (2020 vs 2022)"
            )
        # Layout styling
        fig_wis.update_layout(
            #title="Waste Generated from Manufacturing Industry",
            height=500,
            margin=dict(t=20, b=0, l=30, r=30),
            legend=dict(x=0.5, y=1.02, xanchor="center", orientation="h")
        )

        st.plotly_chart(fig_wis, use_container_width=True)

#-----------------------------------Industrial Manufacturing Waste --------------------------------------------
with tab4:

    st.set_page_config(layout="wide")
    st.subheader("📊 Industrial Waste Explorer")

    # === Load Data ===
    data = pd.read_csv('./data/ManuIndusWaste.csv')
    MIW_timeseries = pd.read_csv('./data/ManuIndusWaste_total.csv')

    zoom_info = {
        'Turkey': {'center': [39.0, 35.0], 'zoom': 5},
        # 'Algeria': {'center': [28.0, 2.5], 'zoom': 5},
        # 'Anglo': {'center': [1.5, 17.0], 'zoom': 5},
        # 'Italy': {'center': [42.5, 12.5], 'zoom': 5}
    }


    # === Charting Functions ===
    def plot_industrial_waste(df, selected_year, use_bar):
        df_filtered = df[df["Year"] <= selected_year]
        traces = []

        
        for col in df_filtered.columns.drop("Year"):
            trace = go.Bar(x=df_filtered["Year"], y=df_filtered[col], name=col) \
                if use_bar else go.Scatter(x=df_filtered["Year"], y=df_filtered[col],
                                        name=col, mode='lines', fill='tozeroy')
            traces.append(trace)

        fig = go.Figure(data=traces)
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Value",
            barmode="group" if use_bar else None,
            template="plotly_white",
            legend=dict(
                orientation="h", yanchor="top", y=1.15, xanchor="center", x=0.5,
                entrywidth=0.25, entrywidthmode='fraction'
            ),
            margin=dict(t=0, b=0, l=40, r=10)
        )
        return fig


    def plot_mwi_timeseries(df, selected_year, use_bar):
        df_filtered = df[df["Year"] <= selected_year]
        traces = []
        cols =  list(df_filtered.columns.drop("Year"))

        for col in cols:
            trace = go.Bar(x=df_filtered["Year"], y=df_filtered[col], name=col) \
                if use_bar else go.Scatter(x=df_filtered["Year"], y=df_filtered[col],
                                        name=col, mode='lines+markers')
            traces.append(trace)

        fig = go.Figure(data=traces)
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Total Manufacturing Waste",
            barmode="group" if use_bar else None,
            template="plotly_white",
            legend=dict(
                orientation="h", yanchor="top", y=1.10, xanchor="center", x=0.5
            ),
            margin=dict(t=0, b=0, l=40, r=10)
        )
        return fig
    #st.subheader("Industrial Waste Dashboard")

    # with st.sidebar:
    #     #selected_country = st.selectbox("Select Country", [None] + list(zoom_info.keys()))
    #     selected_column = list(data.columns.drop("Year"))
    #     selected_column_ts = list(MIW_timeseries.columns.drop("Year"))
        
    # Layout: map + charts
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Selected Country Map")
        if country:
            center = zoom_info[country]["center"]
            zoom = zoom_info[country]["zoom"]
            m = folium.Map(location=center, zoom_start=zoom, tiles="CartoDB positron")
            folium.Marker(location=center, tooltip=country).add_to(m)
            st_folium(m, width=600, height=1000)
        else:
            m = folium.Map(location=[20.0, 0.0], zoom_start=2, tiles="CartoDB positron")
            st_folium(m, width=800, height=1000)

    with col2:
        st.markdown("### Industrial Waste Over Time")
        use_bar1 = st.toggle("Show as Bar Chart", value=False, key="toggle1")
        fig1 = plot_industrial_waste(data, selected_year, use_bar1)
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("### Time Series of Manufacturing Waste")
        use_bar2 = st.toggle("Show as Bar Chart", value=False, key="toggle2")
        fig2 = plot_mwi_timeseries(MIW_timeseries, selected_year, use_bar2)
        st.plotly_chart(fig2, use_container_width=True)

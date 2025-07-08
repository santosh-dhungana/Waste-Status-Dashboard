import geopandas as gpd
import pandas as pd

def load_country_data(name):
    return gpd.read_file(f"data/countries.geojson").query("ADMIN == @name")

def load_province_data(country):
    return gpd.read_file(f"data/provinces/{country.lower()}_admin3.geojson")

def load_indicator_data(theme):
    return pd.read_csv(f"data/indicators/{theme}.csv")

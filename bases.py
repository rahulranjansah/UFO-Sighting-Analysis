import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import matplotlib as plt
import pandas as pd

df = pd.read_csv("military-bases.csv", sep=";")

df[["latitude", "longitude"]] = df["Geo Point"].str.split(",", expand=True)
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

print(df)

base_counts = df.groupby('State Terr').size()

# fig = px.bar(base_counts, x=base_counts.index, y=base_counts.values)
# fig.show()

# Create a DataFrame with the mean latitude and longitude for each state
df_mean = df.groupby('State Terr')[['latitude', 'longitude']].mean().reset_index()

# Merge this with the base_counts DataFrame
df_merged = pd.merge(df_mean, base_counts.rename('count'), left_on='State Terr', right_index=True)

# Create the plot
fig = px.scatter_geo(df_merged, lat='latitude', lon='longitude', color='count',
                     hover_name='State Terr', size='count',
                     projection='natural earth', title='Count of Army Bases in Different States')
pio.write_html(fig, "army_bases.html")
fig.show()
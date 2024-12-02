import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import box, Polygon
import h3
import numpy as np
import json
from branca.colormap import LinearColormap
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Load the processed data and county shapefile
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')
county_gdf = gpd.read_file('../Base_Map/tl_2024_us_county.shp')

# Filter for LA County and 2022 Part I offenses
gdf['Year'] = gdf['DATE OCC'].dt.year
la_county = county_gdf[county_gdf['COUNTYNS'] == '00277283']  # LA County FIPS code
gdf_2022 = gdf[(gdf['Year'] == 2022) & (gdf['Part 1-2'] == 1)].copy()

def create_hex_grid(lat, lon):
    try:
        return h3.latlng_to_cell(float(lat), float(lon), 8)
    except Exception as e:
        print(f"Error processing lat: {lat}, lon: {lon}")
        print(f"Error: {e}")
        return None

gdf_2022['h3_index'] = gdf_2022.apply(
    lambda row: create_hex_grid(row.geometry.y, row.geometry.x), 
    axis=1
)

# Count crimes per hexagon
hex_counts = gdf_2022.groupby('h3_index').size().reset_index(name='count')

def h3_to_polygon(h3_index):
    boundaries = h3.cell_to_boundary(h3_index)
    coords = [(vertex[1], vertex[0]) for vertex in boundaries]
    return Polygon(coords)

hex_counts = hex_counts.copy()
hex_counts['geometry'] = hex_counts['h3_index'].apply(h3_to_polygon)
hex_gdf = gpd.GeoDataFrame(hex_counts, geometry='geometry', crs='EPSG:4269')

# Clip hexagons to LA County boundary
hex_gdf = gpd.overlay(hex_gdf, la_county, how='intersection')

# Create map
m = folium.Map(
    location=[34.0522, -118.2437],
    zoom_start=10,
    tiles='cartodbpositron'
)

# Add LA County boundary
folium.GeoJson(
    la_county.__geo_interface__,
    style_function=lambda x: {'color': 'black', 'weight': 2, 'fillOpacity': 0}
).add_to(m)

# Create custom bins with 100-offense increments
max_count = hex_counts['count'].max()
bins = list(range(0, max_count + 500, 500))  # Creates bins from 0 to max in steps of 100
labels = [f'{bins[i]} - {bins[i+1]}' for i in range(len(bins)-1)]

# Convert matplotlib colors to hex strings
colors = [mcolors.to_hex(c) for c in plt.cm.YlOrRd(np.linspace(0, 1, len(bins)-1))]
# colors=['#ffffb2', '#fecc5c', '#fd8d3c', '#f03b20', '#bd0026']
# Create a custom colormap with more colors to match the increased number of bins
# colors = plt.cm.YlOrRd(np.linspace(0, 1, len(bins)-1))
colormap = LinearColormap(
    colors=colors,  # YlOrRd colors
    vmin=hex_counts['count'].min(),
    vmax=hex_counts['count'].max(),
    caption='Number of Part I Offenses (2022)'
)

# Add hexagon layer with completely suppressed legend
choropleth = folium.Choropleth(
    geo_data=hex_gdf.__geo_interface__,
    data=hex_gdf,
    columns=['h3_index', 'count'],
    key_on='feature.properties.h3_index',
    fill_color='YlOrRd',
    fill_opacity=0.5,
    line_opacity=0.2,
    bins=bins,
    legend_name=None,
    show_legend=False
)
choropleth.add_to(m)

# Remove the default legend after adding to map
for key in choropleth._children:
    if key.startswith('color_map'):
        del(choropleth._children[key])

# Add custom legend
colormap.add_to(m)
colormap.caption = 'Number of Part I Offenses (2022)'

# Add title
title_html = '''
<div style="position: fixed; 
    top: 10px; left: 50px; width: 400px; height: 50px; 
    background-color: white; border:2px solid grey; z-index:9999; 
    font-size:16px; padding: 8px;">
    Part I Offenses in Los Angeles County (2022) per 5 sq km
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save map
m.save('../maps/la_part1_offenses_2022_with_county.html')

print("Bins used:", bins)
print("Color scheme:", colors)
print("Labels:", labels)
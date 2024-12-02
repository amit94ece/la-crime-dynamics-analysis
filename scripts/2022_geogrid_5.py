import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import box, Polygon
import h3
import numpy as np
import json
from branca.colormap import LinearColormap

# Load the processed data
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')

# Filter for 2022 and Part I offenses
gdf['Year'] = gdf['DATE OCC'].dt.year
gdf_2022 = gdf[(gdf['Year'] == 2022)]

# Define LA bounds
la_bounds = {
    'north': 34.35,
    'south': 33.70,
    'east': -118.15,
    'west': -118.55
}

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

# Convert H3 indexes to polygons
def h3_to_polygon(h3_index):
    boundaries = h3.cell_to_boundary(h3_index)
    # Convert to list of tuples for Shapely Polygon
    coords = [(vertex[1], vertex[0]) for vertex in boundaries]
    return Polygon(coords)

hex_counts = hex_counts.copy()
hex_counts['geometry'] = hex_counts['h3_index'].apply(h3_to_polygon)
hex_gdf = gpd.GeoDataFrame(hex_counts, geometry='geometry', crs='EPSG:4326')

# Create map
m = folium.Map(
    location=[34.0522, -118.2437],
    zoom_start=10,
    tiles='cartodbpositron'
)

# Create custom bins and labels
bins = list(hex_counts['count'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1.0]))
bins = [int(b) for b in bins]
labels = [f'{bins[i]} - {bins[i+1]}' for i in range(len(bins)-1)]

# Create a custom colormap
colors = ['#ffffb2', '#fecc5c', '#fd8d3c', '#f03b20', '#bd0026']
colormap = LinearColormap(
    colors=colors,
    vmin=hex_counts['count'].min(),
    vmax=hex_counts['count'].max()
)

# Add hexagon layer
choropleth = folium.Choropleth(
    geo_data=hex_gdf.__geo_interface__,
    data=hex_gdf,
    columns=['h3_index', 'count'],
    key_on='feature.properties.h3_index',
    fill_color='YlOrRd',
    fill_opacity=0.4,
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
colormap.caption = 'Number of Offenses (2022)'

# Add title
title_html = '''
<div style="position: fixed; 
    bottom: 10px; left: 50px; width: 500px; height: 50px; 
    background-color: white; border:2px solid grey; z-index:9999; 
    font-size:16px; padding: 8px;">
    All Offenses in Los Angeles County (2022) per 5 sq km
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save map
m.save('../maps/la_all_offenses_2022_5sq.html')

print("Bins used:", bins)
print("Color scheme:", colors)
print("Labels:", labels)
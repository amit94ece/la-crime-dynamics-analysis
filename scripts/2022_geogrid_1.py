import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import box, Polygon
import h3
import numpy as np
import json

# Load the processed data
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')

# Filter for 2022 and Part I offenses
gdf['Year'] = gdf['DATE OCC'].dt.year
gdf_2022 = gdf[(gdf['Year'] == 2022) & (gdf['Part 1-2'] == 1)]

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

# Check the range of counts in our data
print("Min count:", hex_counts['count'].min())
print("Max count:", hex_counts['count'].max())

# Create more appropriate bins based on the actual data distribution
bins = list(hex_counts['count'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1.0]))

# Add hexagon layer with adjusted bins
folium.Choropleth(
    geo_data=hex_gdf.__geo_interface__,
    data=hex_gdf,
    columns=['h3_index', 'count'],
    key_on='feature.properties.h3_index',
    fill_color='YlOrRd',
    fill_opacity=0.5,
    line_opacity=0.2,
    legend_name='Number of Part I Offenses (2022)',
    bins=bins
).add_to(m)

# Add title
title_html = '''
<div style="position: fixed; 
    top: 10px; left: 50px; width: 400px; height: 50px; 
    background-color: white; border:2px solid grey; z-index:9999; 
    font-size:16px; padding: 8px;">
    Part I Offenses in Los Angeles (2022) per 5 sq km
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save map
m.save('../maps/la_part1_offenses_2022.html')
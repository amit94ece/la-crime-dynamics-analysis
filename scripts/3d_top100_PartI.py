import geopandas as gpd
import pandas as pd
import pydeck as pdk
import numpy as np
import os

# Set your Mapbox API key
MAPBOX_API_KEY = "<Your_MapBox_Api_Key>"
os.environ['MAPBOX_ACCESS_TOKEN'] = MAPBOX_API_KEY

# Load the data
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')
county_gdf = gpd.read_file('../Base_Map/tl_2024_us_county.shp')

# Filter for LA County
la_county = county_gdf[county_gdf['COUNTYNS'] == '00277283']

# Create DataFrame with coordinates and counts
df = pd.DataFrame({
    'year': gdf['DATE OCC'].dt.year,
    'offense_type': gdf['Part 1-2'],
    'latitude': gdf.geometry.y,
    'longitude': gdf.geometry.x,
    'count': 1
})

# Filter for Part I offenses
part1_df = df[df['offense_type'] == 1]

# Aggregate data by location to find top 100 areas
location_counts = part1_df.groupby(['latitude', 'longitude']).size().reset_index(name='count')
top_100_locations = location_counts.nlargest(100, 'count')

# Filter original dataframe to only include top 100 locations
part1_df_top100 = part1_df.merge(top_100_locations[['latitude', 'longitude']], 
                               on=['latitude', 'longitude'])

# Create layers for visualization
hex_layer = pdk.Layer(
    'HexagonLayer',
    data=part1_df_top100,
    get_position=['longitude', 'latitude'],
    radius=200,
    elevation_scale=100,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
    coverage=1,
    color_range=[[35, 197, 82], [248, 79, 49]],
    aggregation='sum',
)

# Add text layer for count numbers
text_layer = pdk.Layer(
    'TextLayer',
    data=top_100_locations,
    get_position=['longitude', 'latitude'],
    get_text='count',
    get_size=16,
    get_color=[0, 0, 0],  # Black text
    get_angle=0,
    pickable=True,
    get_alignment_baseline='top',  # Position text above the bars
    get_text_anchor='middle'
)

# Create view state
view_state = pdk.ViewState(
    latitude=34.0522,
    longitude=-118.2437,
    zoom=10,
    pitch=45,
    bearing=0,
    height=600,
    width=800
)

# Create deck
r = pdk.Deck(
    layers=[hex_layer, text_layer],
    initial_view_state=view_state,
    map_provider='mapbox',
    map_style='mapbox://styles/mapbox/streets-v11',
    api_keys={'mapbox': MAPBOX_API_KEY},
    tooltip={
        'html': '''
            <b>Count:</b> {elevationValue}
        ''',
        'style': {
            'backgroundColor': 'steelblue',
            'color': 'white'
        }
    }
)

# Save visualization
output_file = '../maps/la_top100_part_I_offenses.html'
r.to_html(output_file, open_browser=False)

# Add custom HTML for title and legend
with open(output_file, 'r') as file:
    html_content = file.read()

# Inject custom title and legend
custom_html = """
<div style="position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); 
            background-color: rgba(255, 255, 255, 0.8); padding: 10px; border-radius: 5px; text-align: center;">
    <b>Top 100 Part I Offense Locations in Los Angeles</b>
</div>
<div style="position: absolute; top: 10px; left: 50%; transform: translateX(-50%); 
            background-color: rgba(255, 255, 255, 0.8); padding: 10px; border-radius: 5px; text-align: center;">
    <b>Legend</b><br>
    <span style="display: inline-block; width: 20px; height: 10px; background-color: #23C552;"></span> Less than 2000<br>
    <span style="display: inline-block; width: 20px; height: 10px; background-color: #F84F31;"></span> More than 2000
</div>
"""

# Insert the custom HTML before the closing </body> tag
html_content = html_content.replace('</body>', f'{custom_html}</body>')

# Write the updated HTML back to the file
with open(output_file, 'w') as file:
    file.write(html_content)

# Print statistics
print("\nTop 100 locations statistics:")
print(f"Total Part I offenses in top 100 locations: {part1_df_top100['count'].sum()}")
print("\nLocation distribution:")
print(top_100_locations.describe())
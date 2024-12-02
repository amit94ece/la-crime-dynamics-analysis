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

# Sample a subset of data for testing
gdf = gdf.sample(n=10000, random_state=42)

# Filter for LA County and prepare data
la_county = county_gdf[county_gdf['COUNTYNS'] == '00277283']

# Create DataFrame with coordinates and counts
df = pd.DataFrame({
    'year': gdf['DATE OCC'].dt.year,
    'offense_type': gdf['Part 1-2'],
    'latitude': gdf.geometry.y,
    'longitude': gdf.geometry.x,
    'count': 1  # Add count column for aggregation
})

# Create 3D hexagon layer for Part I offenses by year
part1_df = df[df['offense_type'] == 1]
# After creating part1_df, add these print statements
print("Year distribution in part1_df:")
print(part1_df['year'].value_counts().sort_index())

# Aggregate data by year and location for text labels
year_aggregates = part1_df.groupby(['year', 'latitude', 'longitude']).size().reset_index(name='count')

print("\nYear aggregates sample:")
print(year_aggregates.head())
print("\nYear aggregates columns:", year_aggregates.columns)
print("\nTotal aggregated records:", len(year_aggregates))

# Create text layer for years
text_layer = pdk.Layer(
    'TextLayer',
    data=year_aggregates,
    get_position=['longitude', 'latitude'],
    get_text='year',
    get_size=32,  # Increased size
    get_color=[255, 255, 255],  # White color
    get_angle=0,
    pickable=True,
    get_alignment_baseline="bottom"  # Try to align text better
)
# Modify hexagon layers
total_hex_layer = pdk.Layer(
    'HexagonLayer',
    data=df,
    get_position=['longitude', 'latitude'],
    radius=200,
    elevation_scale=50,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
    coverage=1,
    aggregation='sum',
    get_elevation='count',
    get_year='year'  # Add year to aggregation
)

part1_hex_layer = pdk.Layer(
    'HexagonLayer',
    data=part1_df,
    get_position=['longitude', 'latitude'],
    radius=200,
    elevation_scale=50,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
    coverage=1,
    color_range=[[255,237,160], [240,59,32]],
    aggregation='sum',
    get_elevation='count',
    get_year='year',  # Add year to aggregation
    get_tooltip=['year', 'count']  # Add year to tooltip
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

# Create deck with all layers
r = pdk.Deck(
    layers=[total_hex_layer, part1_hex_layer, text_layer],
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
r.to_html('../maps/la_offenses_3d_timeseries.html')
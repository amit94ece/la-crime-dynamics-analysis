import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import branca.colormap as cm

# Load the processed GeoPackage file
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')

# Count distinct 'Status Desc' values and their occurrences
status_counts = gdf['Status Desc'].value_counts()

# Print the results
print("Distinct count of Status Desc and their record counts:")
print(status_counts)

# Plot overall crime trend
# plt.figure(figsize=(12, 6))
# gdf['DATE OCC'].dt.to_period('M').value_counts().sort_index().plot()
# plt.title('Number of Crime Incidents Over Time')
# plt.xlabel('Date')
# plt.ylabel('Number of Incidents')
# plt.show()

# # Plot top 10 crime types
# plt.figure(figsize=(12, 6))
# gdf['Crm Cd Desc'].value_counts().head(10).plot(kind='bar')
# plt.title('Top 10 Crime Types')
# plt.xlabel('Crime Type')
# plt.ylabel('Number of Incidents')
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()
# plt.show()

# # Plot crime by hour of day
# plt.figure(figsize=(12, 6))
# sns.countplot(x='Hour', data=gdf)
# plt.title('Crime Incidents by Hour of Day')
# plt.xlabel('Hour')
# plt.ylabel('Number of Incidents')
# plt.show()

# # Plot crime by day of week
# # Create a mapping of numeric values to day names
# day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

# # Map the numeric values to day names
# gdf['DayOfWeek'] = gdf['DayOfWeek'].map(day_map)

# # Plot crime by day of week
# plt.figure(figsize=(12, 6))
# sns.countplot(x='DayOfWeek', data=gdf, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
# plt.title('Crime Incidents by Day of Week')
# plt.xlabel('Day of Week')
# plt.ylabel('Number of Incidents')
# plt.show()

# # Create a base map centered on Los Angeles
# m = folium.Map(location=[34.0522, -118.2437], zoom_start=10)

# # Add a heatmap layer
# heat_data = [[row['LAT'], row['LON']] for index, row in gdf.iterrows()]
# HeatMap(heat_data).add_to(m)

# # Save the map
# m.save('../maps/los_angeles_crime_heatmap.html')


# # Create a base map centered on Los Angeles with increased zoom
# m = folium.Map(location=[34.0522, -118.2437], zoom_start=10)

# # Create a custom color scale with adjusted thresholds
# color_scale = cm.LinearColormap(colors=['blue', 'green', 'yellow', 'orange', 'red'], 
#                                 vmin=0, vmax=100)
# heat_data = [[row['LAT'], row['LON']] for index, row in gdf.iterrows()]
# # Add a heatmap layer with adjusted parameters
# HeatMap(heat_data, 
#         radius=12, 
#         blur=15, 
#         max_zoom=1, 
#         gradient={0.2: 'blue', 0.4: 'green', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}
# ).add_to(m)

# # Add a color scale legend
# color_scale.add_to(m)
# color_scale.caption = 'Crime Density'

# # Save the map
# m.save('../maps/los_angeles_crime_heatmap_improved.html')
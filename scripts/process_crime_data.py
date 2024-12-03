import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load the data from 2020 to present
df_2020 = pd.read_csv('../data/Crime_Data_from_2020_to_Present_20241028.csv')

# Load the data from 2010 to 2019
df_2010 = pd.read_csv('../data/Crime_Data_from_2010_to_2019_20241123.csv')

# Concatenate the two dataframes
df = pd.concat([df_2010, df_2020], ignore_index=True)

# Convert 'DATE OCC' to datetime format
df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], format='%m/%d/%Y %I:%M:%S %p')

# Filter data up to 2023
df = df[df['DATE OCC'].dt.year <= 2023]

# Ensure 'TIME OCC' is a string and pad it with zeros if necessary
df['TIME OCC'] = df['TIME OCC'].astype(str).str.zfill(4)

# Convert 'TIME OCC' to datetime and extract hour
df['Hour'] = pd.to_datetime(df['TIME OCC'], format='%H%M', errors='coerce').dt.hour

# Check for any NaN values in 'Hour'
print(f"Number of NaN values in Hour: {df['Hour'].isna().sum()}")

# Create additional time-based features
df['DayOfWeek'] = df['DATE OCC'].dt.dayofweek
df['Month'] = df['DATE OCC'].dt.month

# Create geometric points for spatial analysis
geometry = [Point(xy) for xy in zip(df['LON'], df['LAT'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

# Handle missing values (if applicable)
gdf = gdf.dropna(subset=['LAT', 'LON', 'Crm Cd Desc'])

# Display the first few rows of the processed dataset
print(gdf.head())
# print(gdf.count())

# Save the processed dataset
gdf.to_file('../data/processed_crime_data_2010_2023.gpkg', driver='GPKG')
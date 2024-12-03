import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the processed GeoPackage file
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')

# Analysis by Hour
hourly_summary = gdf.groupby('Hour').agg(
    Total_Offenses=('DATE OCC', 'size'),
    Part_I_Offenses=('Part 1-2', lambda x: (x == 1).sum()),
    Part_II_Offenses=('Part 1-2', lambda x: (x == 2).sum())
).reset_index()

# Analysis by Hour for Adult and Juvenile Arrests
hourly_arrests = gdf.groupby('Hour').agg(
    Total_Offenses=('DATE OCC', 'size'),  # Include total offenses for reference
    Adult_Arrests=('Status Desc', lambda x: (x == 'Adult Arrest').sum()),
    Juvenile_Arrests=('Status Desc', lambda x: (x == 'Juv Arrest').sum())
).reset_index()

# Plot: Total Crimes vs Part I vs Part II by Hour
plt.figure(figsize=(12, 6))
plt.plot(hourly_summary['Hour'], hourly_summary['Total_Offenses'], label='Total Offenses', marker='o', color='blue')
plt.plot(hourly_summary['Hour'], hourly_summary['Part_I_Offenses'], label='Part I Offenses', marker='s', color='green')
plt.plot(hourly_summary['Hour'], hourly_summary['Part_II_Offenses'], label='Part II Offenses', marker='^', color='orange')
plt.title('Total Offenses vs Part I and Part II Offenses by Hour (2010 - 2023)', fontsize=16)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(ticks=range(0, 24, 2))  # Every 2 hours
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Plot: Total Offenses vs Adult and Juvenile Arrests by Hour
plt.figure(figsize=(12, 6))
plt.plot(hourly_arrests['Hour'], hourly_arrests['Total_Offenses'], label='Total Offenses', marker='o', color='blue')
plt.plot(hourly_arrests['Hour'], hourly_arrests['Adult_Arrests'], label='Adult Arrests', marker='s', color='purple')
plt.plot(hourly_arrests['Hour'], hourly_arrests['Juvenile_Arrests'], label='Juvenile Arrests', marker='^', color='orange')
plt.title('Total Offenses vs Adult and Juvenile Arrests by Hour (2010 - 2023)', fontsize=16)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(ticks=range(0, 24, 2))  # Every 2 hours
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

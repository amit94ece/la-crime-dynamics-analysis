import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the processed GeoPackage file
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')

# Create a mapping of numeric values to day names
day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

# Map the numeric values to day names
gdf['DayOfWeek'] = gdf['DayOfWeek'].map(day_map)

# Analysis by Day of the Week
day_summary = gdf.groupby('DayOfWeek').agg(
    Total_Offenses=('DATE OCC', 'size'),
    Part_I_Offenses=('Part 1-2', lambda x: (x == 1).sum()),
    Part_II_Offenses=('Part 1-2', lambda x: (x == 2).sum()),
    Adult_Arrests=('Status Desc', lambda x: (x == 'Adult Arrest').sum()),
    Juvenile_Arrests=('Status Desc', lambda x: (x == 'Juv Arrest').sum())
).reset_index()

# Ensure day names are in the correct order for consistent plotting
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_summary['DayOfWeek'] = pd.Categorical(day_summary['DayOfWeek'], categories=day_order, ordered=True)
day_summary = day_summary.sort_values('DayOfWeek')

# Create a figure
plt.figure(figsize=(12, 6))

# Plot 1: Total Offenses vs Part I vs Part II by Day of the Week
plt.plot(day_summary['DayOfWeek'], day_summary['Total_Offenses'], label='Total Offenses', marker='o', color='blue')
plt.plot(day_summary['DayOfWeek'], day_summary['Part_I_Offenses'], label='Part I Offenses', marker='s', color='green')
plt.plot(day_summary['DayOfWeek'], day_summary['Part_II_Offenses'], label='Part II Offenses', marker='^', color='orange')
plt.title('Total Offenses vs Part I and Part II Offenses by Day of the Week (2010 - 2023)', fontsize=16)
plt.xlabel('Day of the Week', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Create a figure
plt.figure(figsize=(12, 6))
# Plot 2: Total Offenses vs Adult Arrests vs Juvenile Arrests by Day of the Week
plt.plot(day_summary['DayOfWeek'], day_summary['Total_Offenses'], label='Total Offenses', marker='o', color='blue')
plt.plot(day_summary['DayOfWeek'], day_summary['Adult_Arrests'], label='Adult Arrests', marker='s', color='green')
plt.plot(day_summary['DayOfWeek'], day_summary['Juvenile_Arrests'], label='Juvenile Arrests', marker='^', color='orange')
plt.title('Total Offenses vs Adult and Juvenile Arrests by Day of the Week (2010 - 2023)', fontsize=16)
plt.xlabel('Day of the Week', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
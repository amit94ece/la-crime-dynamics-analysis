import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the processed GeoPackage file
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')

# Ensure DATE OCC is in datetime format
gdf['DATE OCC'] = pd.to_datetime(gdf['DATE OCC'])

# Extract the year from DATE OCC
gdf['Year'] = gdf['DATE OCC'].dt.year

# Group by Year and calculate the required counts
summary_table = gdf.groupby('Year').agg(
    Total_Offenses=('DATE OCC', 'size'),
    Part_I_Offenses=('Part 1-2', lambda x: (x == 1).sum()),
    Part_II_Offenses=('Part 1-2', lambda x: (x == 2).sum()),
    Adult_Arrests=('Status Desc', lambda x: (x == 'Adult Arrest').sum()),
    Juvenile_Arrests=('Status Desc', lambda x: (x == 'Juv Arrest').sum())
).reset_index()

# Sort the table by Year in ascending order
summary_table = summary_table.sort_values(by='Year')

# Save the summary table as an HTML file with borders and headers
html_file_path = '../maps/crime_summary_table.html'
summary_table.to_html(html_file_path, index=False, border=1)

print(f"Summary table saved as {html_file_path}")

# Plot 1: Total Offenses vs Adult Arrests vs Juvenile Arrests
plt.figure(figsize=(12, 6))

plt.plot(summary_table['Year'], summary_table['Total_Offenses'], label='Total Offenses', marker='o', color='blue')
plt.plot(summary_table['Year'], summary_table['Adult_Arrests'], label='Adult Arrests', marker='s', color='green')
plt.plot(summary_table['Year'], summary_table['Juvenile_Arrests'], label='Juvenile Arrests', marker='^', color='orange')

plt.title('Time Series of Total Offenses, Adult Arrests, and Juvenile Arrests (2010-2023)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Plot 2: Total Offenses vs Part I Offenses vs Part II Offenses
plt.figure(figsize=(12, 6))

plt.plot(summary_table['Year'], summary_table['Total_Offenses'], label='Total Offenses', marker='o', color='blue')
plt.plot(summary_table['Year'], summary_table['Part_I_Offenses'], label='Part I Offenses', marker='s', color='green')
plt.plot(summary_table['Year'], summary_table['Part_II_Offenses'], label='Part II Offenses', marker='^', color='orange')

plt.title('Time Series of Total Offenses, Part I Offenses, and Part II Offenses (2010-2023)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
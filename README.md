# Los Angeles Crime Data Analysis

This project processes and analyzes crime data for Los Angeles from 2010 to 2023. It combines datasets, performs data cleaning, and prepares the data for spatial analysis.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Data Processing](#data-processing)
- [Output](#output)

## Prerequisites

- Python 3.x
- pandas
- geopandas
- shapely

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/la-crime-analysis.git
   cd la-crime-analysis
   ```

2. Install the required packages:
   ```bash
   pip install pandas geopandas shapely
   ```

## Usage

Run the script using Python:

```bash
python process_crime_data.py
```

## Data Processing

The script performs the following operations:

1. Loads crime data from 2010 to 2023 from two CSV files.
2. Concatenates the datasets into a single DataFrame.
3. Converts date and time columns to appropriate formats.
4. Filters data up to the year 2023.
5. Creates additional time-based features (hour, day of week, month).
6. Generates geometric points for spatial analysis using latitude and longitude.
7. Handles missing values by dropping rows with NaN in specific columns.
8. Saves the processed data as a GeoPackage file.

## Output

The script generates a processed GeoPackage file:

- `processed_crime_data_2010_2023.gpkg`: Contains the cleaned and processed crime data with spatial information.

This file can be used for further analysis, visualization, or integration with GIS software.
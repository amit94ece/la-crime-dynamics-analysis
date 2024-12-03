# Los Angeles Crime Data Analysis

This project processes and analyzes crime data for Los Angeles from 2010 to 2023. It combines datasets, performs data cleaning, prepares the data for spatial analysis, and generates summary statistics and visualizations.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Data Acquisition](#data-acquisition)
- [Setting Up the Environment](#setting-up-the-environment)
- [Installation](#installation)
- [Usage](#usage)
- [Data Processing](#data-processing)
- [Data Analysis](#data-analysis)
- [Output](#output)

## Prerequisites

- Python 3.x
- git

## Data Acquisition

To obtain the necessary data for this analysis, follow these steps:

1. Download the 2010-2019 dataset:
   - Visit https://data.lacity.org/Public-Safety/Crime-Data-from-2010-to-2019/63jg-8b9z/about_data
   - Click on the "Export" button
   - Choose "CSV" format
   - Save the file as `Crime_Data_from_2010_to_2019_20241123.csv` in the `data` folder of your project

2. Download the 2020-present dataset:
   - Visit https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8
   - Click on the "Export" button
   - Choose "CSV" format
   - Save the file as `Crime_Data_from_2020_to_Present_20241028.csv` in the `data` folder of your project

## Setting Up the Environment

1. Create a Python virtual environment:
   ```bash
   python3 -m venv la_crime_env
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     la_crime_env\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source la_crime_env/bin/activate
     ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/la-crime-analysis.git
   cd la-crime-analysis
   ```

2. Install the required packages:
   ```bash
   pip install pandas geopandas shapely matplotlib seaborn
   ```

## Usage

Ensure your virtual environment is activated, then run the scripts:

1. Process the raw data:
   ```bash
   python process-crime-data.py
   ```

2. Generate summary statistics and visualizations:
   ```bash
   python analyze-crime-data-summary.py
   ```

3. Analyze crime data by hour:
   ```bash
   python analyze-by-hour.py
   ```

4. Analyze crime data by day of the week:
   ```bash
   python analyze-by-dayofweek.py
   ```

## Data Processing

The `process-crime-data.py` script performs the following operations:

1. Loads crime data from 2010 to 2023 from two CSV files.
2. Concatenates the datasets into a single DataFrame.
3. Converts date and time columns to appropriate formats.
4. Filters data up to the year 2023.
5. Creates additional time-based features (hour, day of week, month).
6. Generates geometric points for spatial analysis using latitude and longitude.
7. Handles missing values by dropping rows with NaN in specific columns.
8. Saves the processed data as a GeoPackage file.

**Note**: The preprocessing code currently filters out data beyond 2023. If you want to include data up to a different year, modify the following line in the `process_crime_data.py` script:

```python
df = df[df['DATE OCC'].dt.year <= 2023]
```

Replace `2023` with the desired year up to which you want to include data. Make sure to adjust this filter according to the latest available data in your downloaded datasets.

## Data Analysis

### Summary Analysis

The `analyze-crime-data-summary.py` script performs the following operations:

1. Loads the processed GeoPackage file.
2. Creates a summary table with yearly statistics including:
   - Total Offenses
   - Part I Offenses
   - Part II Offenses
   - Adult Arrests
   - Juvenile Arrests
3. Saves the summary table as an HTML file.
4. Generates two time series plots:
   - Total Offenses vs Adult Arrests vs Juvenile Arrests
   - Total Offenses vs Part I Offenses vs Part II Offenses

### Hourly Analysis

The `analyze-by-hour.py` script performs the following operations:

1. Loads the processed GeoPackage file.
2. Analyzes crime data by hour of the day.
3. Generates two plots:
   - Total Offenses vs Part I and Part II Offenses by Hour
   - Total Offenses vs Adult and Juvenile Arrests by Hour

### Day of Week Analysis

The `analyze-by-dayofweek.py` script performs the following operations:

1. Loads the processed GeoPackage file.
2. Analyzes crime data by day of the week.
3. Generates two plots:
   - Total Offenses vs Part I and Part II Offenses by Day of the Week
   - Total Offenses vs Adult and Juvenile Arrests by Day of the Week

## Output

The scripts generate the following outputs:

1. `processed_crime_data_2010_2023.gpkg`: A GeoPackage file containing the cleaned and processed crime data with spatial information.
2. `crime_summary_table.html`: An HTML file with a summary table of yearly crime statistics.
3. Multiple plots displayed during script execution:
   - Yearly time series plots
   - Hourly analysis plots
   - Day of the week analysis plots

These outputs can be used for further analysis, visualization, or integration with GIS software.
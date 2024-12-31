# Los Angeles Crime Data Analysis

This project processes and analyzes crime data for Los Angeles from 2010 to 2023. It combines datasets, performs data cleaning, prepares the data for spatial analysis, generates summary statistics and visualizations, and includes a machine learning model to predict Part I offenses.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Data Acquisition](#data-acquisition)
- [Setting Up the Environment](#setting-up-the-environment)
- [Installation](#installation)
- [Usage](#usage)
- [Data Processing](#data-processing)
- [Data Analysis](#data-analysis)
- [Machine Learning Model](#machine-learning-model)
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
   pip install pandas geopandas shapely matplotlib seaborn scikit-learn imbalanced-learn
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

5. Run the machine learning model:
   ```bash
   python gradient-boost-part-I.py
   ```

6. Run the decision tree classifier model:
   ```bash
   python decision-tree-classifier-part-I.py
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

## Data Analysis

### Summary Analysis

The `analyze-crime-data-summary.py` script creates a summary table with yearly statistics and generates time series plots.

### Hourly Analysis

The `analyze-by-hour.py` script analyzes crime data by hour of the day and generates related plots.

### Day of Week Analysis

The `analyze-by-dayofweek.py` script analyzes crime data by day of the week and generates related plots.

## Machine Learning Model

The `gradient-boost-part-I.py` script implements a Gradient Boosting Classifier to predict Part I offenses. It performs the following steps:

1. Loads the processed data.
2. Prepares features and target variables.
3. Handles missing values and performs feature scaling.
4. Addresses class imbalance using Random Undersampling.
5. Trains the model with early stopping.
6. Performs cross-validation.
7. Evaluates the model using various metrics.
8. Visualizes feature importance and predicted probabilities.

The `decision-tree-classifier-part-I.py` script implements a Decision Tree Classifier to predict Part I offenses. It performs the following steps:

1. Loads the processed data
2. Prepares features and target variables
3. Splits data into training and testing sets
4. Trains a decision tree classifier model
5. Makes predictions on the test set
6. Evaluates model performance using accuracy metrics
7. Visualizes the decision tree structure
8. Generates feature importance plot

The decision tree model provides an interpretable alternative to the gradient boosting classifier, allowing for easy visualization of the decision-making process in classifying Part I offenses.

## Output

The scripts generate the following outputs:

1. `processed_crime_data_2010_2023.gpkg`: A GeoPackage file containing the cleaned and processed crime data.
2. `crime_summary_table.html`: An HTML file with a summary table of yearly crime statistics.

3. Multiple plots displayed during script execution:
   - Yearly time series plots
   - Hourly analysis plots
   - Day of the week analysis plots
   - Feature importance plot for Part I offenses
   - Distribution of predicted probabilities for Part I offenses

4. Gradient Boosting Model (gradient-boost-part-I.py):
   - Data Processing Logs:
     * Data loading confirmation
     * Feature preparation details
     * Resampling information
   
   - Model Training Progress:
     * Iterative performance metrics (1-100 iterations with early stopping):
       - Accuracy
       - Precision
       - Recall
       - F1-score
       - ROC AUC score
   
   - Model Validation:
     * 5-fold cross-validation scores
     * Mean cross-validation score

   - Final Model Evaluation:
     * Accuracy
     * Precision
     * Recall
     * F1-score
     * ROC AUC score

   - Visualizations:
     * Feature importance bar plot showing importance of all input features
     * Histogram showing distribution of predicted probabilities for:
       - Non-offense cases
       - Offense cases
   
   - Test Set Statistics:
     * Class balance distribution in test set (normalized counts)


5. Decision Tree specific outputs:
   - Decision tree visualization diagram
   - Feature importance plot for decision tree model
   - Model accuracy metrics report

These outputs can be used for further analysis, visualization as needed.
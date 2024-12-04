import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Load the data
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')

# Create target variable
gdf['Part_I_Offense'] = (gdf['Part 1-2'] == 1).astype(int)

# Select features
features = ['Hour', 'DayOfWeek', 'Month', 'AREA NAME', 'Vict Age', 'Vict Sex', 'Vict Descent', 'Premis Cd', 'Weapon Used Cd']

# Prepare the data
X = pd.get_dummies(gdf[features], columns=['AREA NAME', 'Vict Sex', 'Vict Descent'])
y = gdf['Part_I_Offense']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train decision tree
dt_classifier = DecisionTreeClassifier(random_state=42)
dt_classifier.fit(X_train, y_train)

# Get feature importance
feature_importance = dt_classifier.feature_importances_
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importance})
feature_importance_df = feature_importance_df.sort_values('Importance', ascending=False)

print(feature_importance_df)

# Correlation heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(X.corr(), annot=False, cmap='coolwarm')
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.show()

# Distribution of offenses by hour
plt.figure(figsize=(10, 6))
sns.countplot(x='Hour', data=gdf[gdf['Part_I_Offense'] == 1])
plt.title("Distribution of Part I Offenses by Hour")
plt.tight_layout()
plt.show()
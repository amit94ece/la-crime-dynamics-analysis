import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.impute import SimpleImputer
from imblearn.ensemble import BalancedRandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO)

# Load and preprocess data (same as before)
logging.info("Starting data loading")
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')
logging.info(f"Data loaded. Shape: {gdf.shape}")

logging.info("Creating target variables")
gdf['Part_I_Offense'] = (gdf['Part 1-2'] == 1).astype(int)

logging.info("Preparing features")
features = ['Hour', 'DayOfWeek', 'Month', 'AREA NAME', 'Vict Age', 'Vict Sex', 'Vict Descent', 'Premis Cd', 'Weapon Used Cd']
X = pd.get_dummies(gdf[features], columns=['AREA NAME', 'Vict Sex', 'Vict Descent'])
y = gdf['Part_I_Offense']
logging.info(f"Features prepared. X shape: {X.shape}")

logging.info("Handling missing values")
imputer = SimpleImputer(strategy='median')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

logging.info("Splitting data")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logging.info("Scaling features")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logging.info("Training Balanced Random Forest Classifier")
brf_model = BalancedRandomForestClassifier(n_estimators=100, random_state=42)

prev_roc_auc = 0
for i in range(1, 101):
    brf_model.set_params(n_estimators=i)
    brf_model.fit(X_train_scaled, y_train)
    
    y_pred = brf_model.predict(X_test_scaled)
    y_pred_proba = brf_model.predict_proba(X_test_scaled)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"Iteration {i}:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-score: {f1:.2f}")
    print(f"ROC AUC: {roc_auc:.2f}")
    print("--------------------")

    if i > 10 and abs(roc_auc - prev_roc_auc) < 0.001:
        print(f"Early stopping at iteration {i}")
        break
    prev_roc_auc = roc_auc

logging.info("Performing cross-validation")
cv_scores = cross_val_score(brf_model, X_train_scaled, y_train, cv=5)

print("Balanced Random Forest - Cross-validation scores:", cv_scores)
print("Balanced Random Forest - Mean CV score:", cv_scores.mean())

logging.info("Making final predictions")
y_pred = brf_model.predict(X_test_scaled)
y_pred_proba = brf_model.predict_proba(X_test_scaled)[:, 1]

print("\nFinal Balanced Random Forest Model:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"Precision: {precision_score(y_test, y_pred):.2f}")
print(f"Recall: {recall_score(y_test, y_pred):.2f}")
print(f"F1-score: {f1_score(y_test, y_pred):.2f}")
print(f"ROC AUC: {roc_auc_score(y_test, y_pred_proba):.2f}")

feature_importance = brf_model.feature_importances_

plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importance, y=X.columns)
plt.title("Feature Importance for Part I Offenses (Balanced Random Forest)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.hist([y_pred_proba[y_test == 0], y_pred_proba[y_test == 1]], 
         label=['Non-offense', 'Offense'], bins=50, density=True, alpha=0.7)
plt.xlabel("Predicted Probability")
plt.ylabel("Density")
plt.title("Distribution of Predicted Probabilities for Part I Offenses")
plt.legend()
plt.show()

print("Class balance in test set:")
print(y_test.value_counts(normalize=True))
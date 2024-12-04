import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.impute import SimpleImputer
from imblearn.under_sampling import RandomUnderSampler
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Starting data loading")
gdf = gpd.read_file('../data/processed_crime_data_2010_2023.gpkg')
logging.info(f"Data loaded. Shape: {gdf.shape}")

logging.info("Creating target variables")
gdf['Part_I_Offense'] = (gdf['Part 1-2'] == 1).astype(int)
gdf['Part_II_Offense'] = (gdf['Part 1-2'] == 2).astype(int)

logging.info("Preparing features")
features = ['Hour', 'DayOfWeek', 'Month', 'AREA NAME', 'Vict Age', 'Vict Sex', 'Vict Descent', 'Premis Cd', 'Weapon Used Cd']
X = pd.get_dummies(gdf[features], columns=['AREA NAME', 'Vict Sex', 'Vict Descent'])
y_part_i = gdf['Part_I_Offense']
logging.info(f"Features prepared. X shape: {X.shape}")

logging.info("Handling missing values")
imputer = SimpleImputer(strategy='median')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

logging.info("Splitting data")
X_train, X_test, y_train_i, y_test_i = train_test_split(X, y_part_i, test_size=0.2, random_state=42)

logging.info("Scaling features")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logging.info("Handling class imbalance with Random Sampler")
rus = RandomUnderSampler(random_state=42)
X_train_resampled, y_train_i_resampled = rus.fit_resample(X_train_scaled, y_train_i)
logging.info(f"Resampled data shape: {X_train_resampled.shape}")

logging.info("Training Part I Offense model")
gb_model_i = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, subsample=0.8, random_state=42, verbose=1)

prev_roc_auc = 0
for i in range(1, 101):
    gb_model_i.set_params(n_estimators=i)
    gb_model_i.fit(X_train_resampled, y_train_i_resampled)
    
    y_pred_i = gb_model_i.predict(X_test_scaled)
    y_pred_proba_i = gb_model_i.predict_proba(X_test_scaled)[:, 1]
    
    accuracy = accuracy_score(y_test_i, y_pred_i)
    precision = precision_score(y_test_i, y_pred_i)
    recall = recall_score(y_test_i, y_pred_i)
    f1 = f1_score(y_test_i, y_pred_i)
    roc_auc = roc_auc_score(y_test_i, y_pred_proba_i)
    
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
cv_scores_i = cross_val_score(gb_model_i, X_train_resampled, y_train_i_resampled, cv=5)

print("Part I Offense Model - Cross-validation scores:", cv_scores_i)
print("Part I Offense Model - Mean CV score:", cv_scores_i.mean())

logging.info("Making final predictions")
y_pred_i = gb_model_i.predict(X_test_scaled)
y_pred_proba_i = gb_model_i.predict_proba(X_test_scaled)[:, 1]

print("\nFinal Part I Offense Model:")
print(f"Accuracy: {accuracy_score(y_test_i, y_pred_i):.2f}")
print(f"Precision: {precision_score(y_test_i, y_pred_i):.2f}")
print(f"Recall: {recall_score(y_test_i, y_pred_i):.2f}")
print(f"F1-score: {f1_score(y_test_i, y_pred_i):.2f}")
print(f"ROC AUC: {roc_auc_score(y_test_i, y_pred_proba_i):.2f}")

feature_importance_i = gb_model_i.feature_importances_

plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importance_i, y=X.columns)
plt.title("Feature Importance for Part I Offenses")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.hist([y_pred_proba_i[y_test_i == 0], y_pred_proba_i[y_test_i == 1]], 
         label=['Non-offense', 'Offense'], bins=50, density=True, alpha=0.7)
plt.xlabel("Predicted Probability")
plt.ylabel("Density")
plt.title("Distribution of Predicted Probabilities for Part I Offenses")
plt.legend()
plt.show()

print("Class balance in test set:")
print(y_test_i.value_counts(normalize=True))
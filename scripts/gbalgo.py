import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
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
y_part_ii = gdf['Part_II_Offense']
logging.info(f"Features prepared. X shape: {X.shape}")

logging.info("Handling missing values")
imputer = SimpleImputer(strategy='median')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

logging.info("Splitting data")
X_train, X_test, y_train_i, y_test_i = train_test_split(X, y_part_i, test_size=0.2, random_state=42)
_, _, y_train_ii, y_test_ii = train_test_split(X, y_part_ii, test_size=0.2, random_state=42)

logging.info("Scaling features")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logging.info("Handling class imbalance with Random Sampler")
# smote = SMOTE(random_state=42)
# X_train_resampled, y_train_i_resampled = smote.fit_resample(X_train_scaled, y_train_i)
# _, y_train_ii_resampled = smote.fit_resample(X_train_scaled, y_train_ii)
from imblearn.under_sampling import RandomUnderSampler
rus = RandomUnderSampler(random_state=42)
X_train_resampled, y_train_i_resampled = rus.fit_resample(X_train_scaled, y_train_i)
_, y_train_ii_resampled = rus.fit_resample(X_train_scaled, y_train_ii)
logging.info(f"Resampled data shape: {X_train_resampled.shape}")

logging.info("Training Part I Offense model")
# gb_model_i = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, subsample=0.8, random_state=42)
# gb_model_i.fit(X_train_resampled, y_train_i_resampled)
logging.info("Training Part I Offense model")
gb_model_i = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, subsample=0.8, random_state=42, verbose=1)

for i in range(1, 101):  # 100 iterations
    gb_model_i.set_params(n_estimators=i)
    gb_model_i.fit(X_train_resampled, y_train_i_resampled)
    
    # Make predictions
    y_pred_i = gb_model_i.predict(X_test_scaled)
    y_pred_proba_i = gb_model_i.predict_proba(X_test_scaled)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test_i, y_pred_i)
    precision = precision_score(y_test_i, y_pred_i)
    recall = recall_score(y_test_i, y_pred_i)
    f1 = f1_score(y_test_i, y_pred_i)
    roc_auc = roc_auc_score(y_test_i, y_pred_proba_i)
    
    # Print metrics
    print(f"Iteration {i}:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-score: {f1:.2f}")
    print(f"ROC AUC: {roc_auc:.2f}")
    print("--------------------")

    # Optional: Early stopping if metrics stabilize
    if i > 10 and abs(roc_auc - prev_roc_auc) < 0.001:
        print(f"Early stopping at iteration {i}")
        break
    prev_roc_auc = roc_auc

# logging.info("Training Part II Offense model")
# gb_model_ii = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, subsample=0.8, random_state=42)
# gb_model_ii.fit(X_train_resampled, y_train_ii_resampled)

logging.info("Performing cross-validation")
cv_scores_i = cross_val_score(gb_model_i, X_train_resampled, y_train_i_resampled, cv=5)
# cv_scores_ii = cross_val_score(gb_model_ii, X_train_resampled, y_train_ii_resampled, cv=5)

print("Part I Offense Model - Cross-validation scores:", cv_scores_i)
print("Part I Offense Model - Mean CV score:", cv_scores_i.mean())
# print("Part II Offense Model - Cross-validation scores:", cv_scores_ii)
# print("Part II Offense Model - Mean CV score:", cv_scores_ii.mean())

logging.info("Making predictions")
y_pred_i = gb_model_i.predict(X_test_scaled)
y_pred_proba_i = gb_model_i.predict_proba(X_test_scaled)[:, 1]
# y_pred_ii = gb_model_ii.predict(X_test_scaled)
# y_pred_proba_ii = gb_model_ii.predict_proba(X_test_scaled)[:, 1]

# Evaluate the models
print("\nPart I Offense Model:")
print(f"Accuracy: {accuracy_score(y_test_i, y_pred_i):.2f}")
print(f"Precision: {precision_score(y_test_i, y_pred_i):.2f}")
print(f"Recall: {recall_score(y_test_i, y_pred_i):.2f}")
print(f"F1-score: {f1_score(y_test_i, y_pred_i):.2f}")
print(f"ROC AUC: {roc_auc_score(y_test_i, y_pred_proba_i):.2f}")

# print("\nPart II Offense Model:")
# print(f"Accuracy: {accuracy_score(y_test_ii, y_pred_ii):.2f}")
# print(f"Precision: {precision_score(y_test_ii, y_pred_ii):.2f}")
# print(f"Recall: {recall_score(y_test_ii, y_pred_ii):.2f}")
# print(f"F1-score: {f1_score(y_test_ii, y_pred_ii):.2f}")
# print(f"ROC AUC: {roc_auc_score(y_test_ii, y_pred_proba_ii):.2f}")

# Feature importance
feature_importance_i = gb_model_i.feature_importances_
# feature_importance_ii = gb_model_ii.feature_importances_

# Plot feature importance
plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importance_i, y=X.columns)
plt.title("Feature Importance for Part I Offenses")
plt.tight_layout()
plt.show()

# plt.figure(figsize=(10, 6))
# sns.barplot(x=feature_importance_ii, y=X.columns)
# plt.title("Feature Importance for Part II Offenses")
# plt.tight_layout()
# plt.show()

# Plot predicted probabilities vs actual outcomes
plt.figure(figsize=(10, 6))
plt.scatter(y_pred_proba_i[y_test_i == 0], y_test_i[y_test_i == 0], color='red', alpha=0.5, label='Non-offense')
plt.scatter(y_pred_proba_i[y_test_i == 1], y_test_i[y_test_i == 1], color='blue', alpha=0.5, label='Offense')
plt.xlabel("Predicted Probability")
plt.ylabel("Actual Outcome")
plt.title("Predicted Probabilities vs Actual Outcomes for Part I Offenses")
plt.legend()
plt.show()

# plt.figure(figsize=(10, 6))
# plt.scatter(y_pred_proba_ii[y_test_ii == 0], y_test_ii[y_test_ii == 0], color='red', alpha=0.5, label='Non-offense')
# plt.scatter(y_pred_proba_ii[y_test_ii == 1], y_test_ii[y_test_ii == 1], color='blue', alpha=0.5, label='Offense')
# plt.xlabel("Predicted Probability")
# plt.ylabel("Actual Outcome")
# plt.title("Predicted Probabilities vs Actual Outcomes for Part II Offenses")
# plt.legend()
# plt.show()
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# 1. LOAD AND PREPARE THE DATA

# Read dataset
df = pd.read_csv("data/raw/natural_disasters.csv")

# Remove aggregate rows such as "All disasters"
disaster_types = df[~df["entity"].str.startswith("All disasters")].copy()

print("Dataset used for modelling:")
print(disaster_types.head())

print(f"\nNumber of observations: {len(disaster_types)}")
print(f"Number of disaster types: {disaster_types['entity'].nunique()}")

# 2. CREATE FEATURES

# Input features
X = disaster_types[["year", "entity"]]

# Target variable
y = disaster_types["n_events"]

# Convert categorical disaster types into numerical columns
X = pd.get_dummies(
    X,
    columns=["entity"],
    dtype=int
)

# 3. TIME-BASED TRAIN / TEST SPLIT

# Use earlier years for training
# and later years for testing.

train_mask = disaster_types["year"] <= 2014
test_mask = disaster_types["year"] >= 2015

X_train = X[train_mask]
X_test = X[test_mask]

y_train = y[train_mask]
y_test = y[test_mask]

print("\nTraining observations:", len(X_train))
print("Testing observations:", len(X_test))

# 4. LINEAR REGRESSION BASELINE

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

linear_pred = linear_model.predict(X_test)

# Evaluate Linear Regression
linear_mae = mean_absolute_error(y_test, linear_pred)

linear_rmse = mean_squared_error(y_test, linear_pred) ** 0.5

linear_r2 = r2_score(y_test, linear_pred)

print("\n========== LINEAR REGRESSION ==========")
print(f"MAE : {linear_mae:.2f}")
print(f"RMSE: {linear_rmse:.2f}")
print(f"R²  : {linear_r2:.2f}")

# 5. RANDOM FOREST REGRESSION

random_forest = RandomForestRegressor(n_estimators=250, random_state=50)

random_forest.fit(X_train, y_train)

rf_pred = random_forest.predict(X_test)

# Evaluate Random Forest
rf_mae = mean_absolute_error(y_test,rf_pred)

rf_rmse = mean_squared_error(y_test, rf_pred) ** 0.5

rf_r2 = r2_score(y_test, rf_pred)

print("\n========== RANDOM FOREST ==========")
print(f"MAE : {rf_mae:.2f}")
print(f"RMSE: {rf_rmse:.2f}")
print(f"R²  : {rf_r2:.2f}")

# 6. MODEL COMPARISON

model_comparison = pd.DataFrame({
    "Model": ["Linear Regression", "Random Forest"],
    "MAE": [linear_mae, rf_mae],
    "RMSE": [linear_rmse,rf_rmse],
    "R2": [linear_r2, rf_r2]
})

print("\n========== MODEL COMPARISON ==========")
print(model_comparison.to_string(index=False))

# 7. CHECK FOR OVERFITTING

# Predict the training data
rf_train_pred = random_forest.predict(X_train)

train_r2 = r2_score(y_train, rf_train_pred)

test_r2 = r2_score(y_test, rf_pred)

r2_difference = train_r2 - test_r2

print("\n========== OVERFITTING CHECK ==========")
print(f"Training R²: {train_r2:.2f}")
print(f"Testing R² : {test_r2:.2f}")
print(f"R² difference: {r2_difference:.2f}")

# 8. ERROR ANALYSIS BY DISASTER TYPE

results = disaster_types.loc[X_test.index, ["year", "entity", "n_events"]].copy()

results["predicted"] = rf_pred

# Absolute prediction error
results["absolute_error"] = (results["n_events"] - results["predicted"]).abs()

# Percentage prediction error
results["percentage_error"] = (results["absolute_error"] / results["n_events"]) * 100


# Average absolute error
error_by_type = results.groupby("entity")["absolute_error"].mean()

error_by_type = error_by_type.sort_values(ascending=False)

print("\n========== MAE BY DISASTER TYPE ==========")
print(error_by_type.to_string())


# Average percentage error
mape_by_type = results.groupby("entity")["percentage_error"].mean()

mape_by_type = mape_by_type.sort_values()

print("\n========== MAPE BY DISASTER TYPE ==========")
print(mape_by_type.to_string())

# 9. FEATURE IMPORTANCE

feature_importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": random_forest.feature_importances_
})

feature_importance = feature_importance.sort_values("importance", ascending=False)

print("\n========== FEATURE IMPORTANCE ==========")
print(feature_importance.to_string(index=False))

# 10. SAMPLE PREDICTIONS

sample_predictions = results[
    [
        "year",
        "entity",
        "n_events",
        "predicted"
    ]
].head(20)

print("\n========== SAMPLE PREDICTIONS ==========")
print(sample_predictions.to_string(index=False))

# 11. TIME TREND MODEL

# Center the year around 1970
disaster_types["year_centered"] = (disaster_types["year"] - 1970)

# Create one-hot encoded disaster types
trend_X = pd.get_dummies(
    disaster_types["entity"],
    prefix="entity",
    dtype=int
)

# Create a separate time trend for each disaster type
for disaster_type in disaster_types["entity"].unique():

    trend_X[f"year_x_{disaster_type}"] = (disaster_types["year_centered"] * (
            disaster_types["entity"]
            == disaster_type
        ).astype(int)
    )

# Split using the same years as before
trend_X_train = trend_X[train_mask]
trend_X_test = trend_X[test_mask]

# Train Linear Regression with individual time trends
trend_model = LinearRegression()
trend_model.fit(trend_X_train, y_train)
trend_pred = trend_model.predict(trend_X_test)

# Evaluate the trend model
trend_mae = mean_absolute_error(y_test, trend_pred)
trend_rmse = mean_squared_error(y_test, trend_pred) ** 0.5
trend_r2 = r2_score(y_test, trend_pred)

print("\n========== TIME TREND MODEL ==========")
print(f"MAE : {trend_mae:.2f}")
print(f"RMSE: {trend_rmse:.2f}")
print(f"R²  : {trend_r2:.2f}")

# Show predictions
trend_results = disaster_types.loc[X_test.index,["year", "entity", "n_events"]].copy()

trend_results["predicted"] = trend_pred

print("\n========== TREND MODEL PREDICTIONS ==========")

print(trend_results[["year","entity","n_events","predicted"]].head(20).to_string(index=False))
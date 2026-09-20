import pandas as pd
import matplotlib.pyplot as plt

# 1. LOAD DATA

df = pd.read_csv("data/raw/natural_disasters.csv")

# 2. SELECT ALL DISASTERS

all_disasters = df[df["entity"] == "All disasters"].copy()

# 3. CREATE LINE CHART

plt.figure(figsize=(10, 6))

plt.plot(all_disasters["year"], all_disasters["n_events"])

plt.title("Global Reported Natural Disasters Over Time")

plt.xlabel("Year")
plt.ylabel("Number of Events")

plt.grid(True)

plt.tight_layout()

# ==========================================
# 4. TOTAL EVENTS BY DISASTER TYPE
# ==========================================

disaster_totals = df[
    ~df["entity"].str.startswith("All disasters")
].groupby("entity")["n_events"].sum()

disaster_totals = disaster_totals.sort_values(
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    disaster_totals.index,
    disaster_totals.values
)

plt.title("Total Reported Natural Disasters by Type")

plt.xlabel("Disaster Type")
plt.ylabel("Total Number of Events")

plt.xticks(rotation=45)

plt.tight_layout()

# ==========================================
# 5. CORRELATION HEATMAP
# ==========================================

disaster_pivot = df[
    ~df["entity"].str.startswith("All disasters")
].pivot(
    index="year",
    columns="entity",
    values="n_events"
)

correlation = disaster_pivot.corr()

plt.figure(figsize=(10, 8))

plt.imshow(
    correlation,
    aspect="auto"
)

plt.colorbar(label="Correlation")

plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(correlation.columns)),
    correlation.columns
)

plt.title("Correlation Between Disaster Types")

plt.tight_layout()

# ==========================================
# 6. ACTUAL VS PREDICTED
# ==========================================

from sklearn.ensemble import RandomForestRegressor

# Prepare modelling data
model_data = df[
    ~df["entity"].str.startswith("All disasters")
].copy()

X = model_data[["year", "entity"]]

y = model_data["n_events"]

X = pd.get_dummies(
    X,
    columns=["entity"],
    dtype=int
)

# Same time-based split as Phase 4
train_mask = model_data["year"] <= 2014
test_mask = model_data["year"] >= 2015

X_train = X[train_mask]
X_test = X[test_mask]

y_train = y[train_mask]
y_test = y[test_mask]

# Train Random Forest
model = RandomForestRegressor(
    n_estimators=250,
    random_state=50
)

model.fit(X_train, y_train)

predicted = model.predict(X_test)

# Plot actual vs predicted
plt.figure(figsize=(10, 6))

plt.scatter(
    y_test,
    predicted
)

# Perfect prediction reference line
minimum = min(y_test.min(), predicted.min())
maximum = max(y_test.max(), predicted.max())

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)

plt.title("Actual vs Predicted Disaster Events")
plt.xlabel("Actual Number of Events")
plt.ylabel("Predicted Number of Events")

plt.tight_layout()
plt.show()
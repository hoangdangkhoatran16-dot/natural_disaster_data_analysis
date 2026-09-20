import os

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "natural_disasters.csv"
)

FIGURES_DIR = os.path.join(
    BASE_DIR,
    "figures"
)

os.makedirs(
    FIGURES_DIR,
    exist_ok=True
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    DATA_PATH
)


# ============================================================
# 1. GLOBAL DISASTERS OVER TIME
# ============================================================

all_disasters = df[
    df["entity"] == "All disasters"
].copy()

all_disasters = all_disasters.sort_values(
    "year"
)


plt.figure(
    figsize=(10, 6)
)

plt.plot(
    all_disasters["year"],
    all_disasters["n_events"],
    marker="o",
    markersize=3
)

plt.title(
    "Global Reported Natural Disasters Over Time"
)

plt.xlabel(
    "Year"
)

plt.ylabel(
    "Number of Reported Events"
)

plt.grid(
    True,
    alpha=0.25
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURES_DIR,
        "global_disasters_over_time.png"
    ),
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 2. TOTAL EVENTS BY DISASTER TYPE
# ============================================================

disaster_data = df[
    ~df["entity"].str.startswith(
        "All disasters"
    )
].copy()


disaster_totals = (
    disaster_data
    .groupby("entity")["n_events"]
    .sum()
    .sort_values(
        ascending=True
    )
)


plt.figure(
    figsize=(10, 6)
)

bars = plt.barh(
    disaster_totals.index,
    disaster_totals.values
)

plt.title(
    "Total Reported Natural Disasters by Type"
)

plt.xlabel(
    "Total Number of Reported Events"
)

plt.ylabel(
    "Disaster Type"
)


for bar in bars:

    width = bar.get_width()

    plt.text(
        width,
        bar.get_y()
        + bar.get_height() / 2,
        f" {int(width):,}",
        va="center"
    )


plt.grid(
    axis="x",
    alpha=0.25
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURES_DIR,
        "total_events_by_disaster_type.png"
    ),
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 3. CORRELATION HEATMAP
# ============================================================

disaster_pivot = (
    disaster_data
    .pivot(
        index="year",
        columns="entity",
        values="n_events"
    )
)


correlation = (
    disaster_pivot.corr()
)


plt.figure(
    figsize=(10, 8)
)

plt.imshow(
    correlation,
    aspect="auto"
)

plt.colorbar(
    label="Correlation"
)


plt.xticks(
    range(
        len(
            correlation.columns
        )
    ),
    correlation.columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(
        len(
            correlation.columns
        )
    ),
    correlation.columns
)


plt.title(
    "Correlation Between Disaster Types"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURES_DIR,
        "disaster_type_correlation.png"
    ),
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 4. ACTUAL VS PREDICTED
# ============================================================

model_data = disaster_data.copy()


X = model_data[
    [
        "year",
        "entity"
    ]
]

y = model_data[
    "n_events"
]


X = pd.get_dummies(
    X,
    columns=["entity"],
    dtype=int
)


train_mask = (
    model_data["year"] <= 2014
)

test_mask = (
    model_data["year"] >= 2015
)


X_train = X[
    train_mask
]

X_test = X[
    test_mask
]

y_train = y[
    train_mask
]

y_test = y[
    test_mask
]


model = RandomForestRegressor(
    n_estimators=250,
    random_state=50
)


model.fit(
    X_train,
    y_train
)


predicted = model.predict(
    X_test
)


plt.figure(
    figsize=(10, 6)
)


plt.scatter(
    y_test,
    predicted,
    alpha=0.7
)


minimum = min(
    y_test.min(),
    predicted.min()
)

maximum = max(
    y_test.max(),
    predicted.max()
)


plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)


plt.title(
    "Actual vs Predicted Disaster Events"
)

plt.xlabel(
    "Actual Number of Events"
)

plt.ylabel(
    "Predicted Number of Events"
)

plt.grid(
    True,
    alpha=0.25
)

plt.tight_layout()


plt.savefig(
    os.path.join(
        FIGURES_DIR,
        "actual_vs_predicted.png"
    ),
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# FINISHED
# ============================================================

print(
    "Visualization complete."
)

print(
    f"Figures saved to: {FIGURES_DIR}"
)

print(
    "Created:"
)

print(
    "1. global_disasters_over_time.png"
)

print(
    "2. total_events_by_disaster_type.png"
)

print(
    "3. disaster_type_correlation.png"
)

print(
    "4. actual_vs_predicted.png"
)
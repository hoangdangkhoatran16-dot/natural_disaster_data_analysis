import pandas as pd

# Read dataset
df = pd.read_csv("data/raw/natural_disasters.csv")

# Remove aggregate rows
disaster_types = df[~df["entity"].str.startswith("All disasters")]

# Calculate basic statistics
basic_statistics = disaster_types.groupby("entity")["n_events"].agg(["mean","median","std","min","max","var"])

print("\nBasic statistics for each disaster type:")
print(basic_statistics)

print("\nAll disaster types:")
print(basic_statistics.to_string())

# Coefficient of Variation (CV)

basic_statistics["cv"] = (basic_statistics["std"] / basic_statistics["mean"]) * 100

basic_statistics = basic_statistics.sort_values("cv",ascending=False)

print("\nCoefficient of Variation by disaster type:")
print(basic_statistics[["mean", "std", "cv"]].to_string())

# Probability of exceeding the mean

probability_above_mean = {}

for disaster_type, group in disaster_types.groupby("entity"):
    mean_value = group["n_events"].mean()

    probability = ((group["n_events"] > mean_value).mean())

    probability_above_mean[disaster_type] = probability * 100

probability_above_mean = pd.Series(probability_above_mean).sort_values(ascending=False)

print("\nProbability of a year exceeding the mean:")
print(probability_above_mean.to_string())

# 95th Percentile

percentile_95 = disaster_types.groupby("entity")["n_events"].quantile(0.95)

percentile_95 = percentile_95.sort_values(ascending=False)

print("\n95th percentile of disaster events:")
print(percentile_95.to_string())

# Identify extreme years above the 95th percentile

print("\nYears exceeding the 95th percentile:")

for disaster_type, group in disaster_types.groupby("entity"):
    threshold = group["n_events"].quantile(0.95)

    extreme_years = group[group["n_events"] > threshold][["year", "n_events"]]

    print(f"\n{disaster_type} (P95 = {threshold:.2f}):")
    print(extreme_years.to_string(index=False))

# Z-score analysis

z_scores = disaster_types.copy()

z_scores["mean"] = z_scores.groupby("entity")["n_events"].transform("mean")
z_scores["std"] = z_scores.groupby("entity")["n_events"].transform("std")

z_scores["z_score"] = ((z_scores["n_events"] - z_scores["mean"]) / z_scores["std"])

# Find the most unusual years
most_unusual = z_scores.loc[z_scores["z_score"].abs().sort_values(ascending=False).index]

print("\nMost unusual disaster years based on absolute Z-score:")
print(most_unusual[["entity", "year", "n_events", "z_score"]].head(15).to_string(index=False))

# Skewness analysis

skewness = disaster_types.groupby("entity")["n_events"].skew()

skewness = skewness.sort_values(ascending=False)

print("\nSkewness by disaster type:")
print(skewness.to_string())
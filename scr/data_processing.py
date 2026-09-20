import pandas as pd

# 1. LOAD DATA

events = pd.read_csv("data/raw/natural_disasters.csv")

impact = pd.read_csv("data/raw/natural_disasters_impact.csv")

# 2. PREPARE EVENT DATA

events = events[~events["entity"].str.startswith("All disasters")].copy()

events = events.rename(columns={"entity": "disaster_type"})

# 3. CONVERT IMPACT DATA TO LONG FORMAT

impact_columns = [
    "total_affected_drought_yearly",
    "total_affected_earthquake_yearly",
    "total_affected_volcanic_activity_yearly",
    "total_affected_flood_yearly",
    "total_affected_landslide_yearly",
    "total_affected_extreme_weather_yearly",
    "total_affected_wildfire_yearly",
    "total_affected_extreme_temperature_yearly"
]

impact_long = impact.melt(
    id_vars=["entity", "code", "year"],
    value_vars=impact_columns,
    var_name="disaster_type",
    value_name="people_affected"
)

# Convert column names to the same disaster names
impact_long["disaster_type"] = (
    impact_long["disaster_type"]
    .str.replace(
        "total_affected_",
        "",
        regex=False
    )
    .str.replace(
        "_yearly",
        "",
        regex=False
    )
    .str.replace(
        "_",
        " ",
        regex=False
    )
    .str.title()
)

# 4. STANDARDIZE DISASTER NAMES

name_mapping = {
    "Drought": "Drought",
    "Earthquake": "Earthquake",
    "Volcanic Activity": "Volcanic activity",
    "Flood": "Flood",
    "Landslide": "Landslide",
    "Extreme Weather": "Extreme weather",
    "Wildfire": "Wildfire",
    "Extreme Temperature": "Extreme temperature"
}

impact_long["disaster_type"] = (impact_long["disaster_type"].replace(name_mapping))

# 5. MERGE DATASETS

merged = events.merge(
    impact_long,
    on=["year", "disaster_type"],
    how="left"
)

# 6. SAVE PROCESSED DATA

merged.to_csv("data/processed/disaster_analysis.csv", index=False)

# 7. CHECK RESULT

print("\n========== MERGED DATA ==========")

print("Shape:")
print(merged.shape)

print("\nColumns:")
print(merged.columns.tolist())

print("\nFirst 20 rows:")
print(merged.head(20).to_string(index=False))

print("\nPeople affected available:")
print(merged["people_affected"].notna().sum())

print("\nPeople affected missing:")
print(merged["people_affected"].isna().sum())
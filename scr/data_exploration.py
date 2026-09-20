import pandas as pd

# Read dataset
df = pd.read_csv("data/raw/natural_disasters.csv")

# Basic information
print("Dataset shape:", df.shape)

print("\nColumns:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nYear range:")
print(df["year"].min(), "to", df["year"].max())

import matplotlib.pyplot as plt

all_disasters = df[df["entity"] == "All disasters"]

plt.plot(all_disasters["year"], all_disasters["n_events"])

plt.xlabel("Year")
plt.ylabel("Number of disasters")
plt.title("Reported Natural Disasters Over Time")

max_disaster_year = all_disasters.loc[all_disasters["n_events"].idxmax()]

print("\nYear with the most disasters:")
print(max_disaster_year)

top_5_years = all_disasters.nlargest(5, "n_events")

print("\nTop 5 years with the most disasters:")
print(top_5_years)

print("\nTypes of disasters in the dataset:")
print(df["entity"].unique())

disaster_totals = df[~df["entity"].str.startswith("All disasters")].groupby("entity")["n_events"].sum().sort_values(ascending=False)

print("\nTotal reported disasters by type:")
print(disaster_totals)

plt.figure(figsize=(10, 6))

disaster_totals.plot(kind="bar")

plt.xlabel("Disaster type")
plt.ylabel("Total number of reported events")
plt.title("Total Reported Natural Disasters by Type")

plt.xticks(rotation=45)
plt.tight_layout()

all_disasters["change"] = all_disasters["n_events"].diff()
print("\nYear-to-year change:")
print(all_disasters[["year", "n_events", "change"]])

largest_increase = all_disasters.loc[all_disasters["change"].idxmax()]
largest_decrease = all_disasters.loc[all_disasters["change"].idxmin()]
print("\nLargest increase:")
print(largest_increase)
print("\nLargest decrease:")
print(largest_decrease)

all_disasters["decade"] = (all_disasters["year"] // 10) * 10
decade_average = all_disasters.groupby("decade")["n_events"].mean()
print("\nAverage reported disasters by decade:")
print(decade_average)

flood = df[df["entity"] == "Flood"]
print("\nFlood data:")
print(flood)

# DISASTER TYPES OVER TIME

# Remove aggregate rows such as "All disasters"
disaster_types = df[
    ~df["entity"].str.startswith("All disasters")
]

# Create a table:
# rows = years
# columns = disaster types
# values = number of reported events
disaster_pivot = disaster_types.pivot(
    index="year",
    columns="entity",
    values="n_events"
)

print("\nDisaster data by year:")
print(disaster_pivot)

# Create the line chart
plt.figure(figsize=(12, 7))

disaster_pivot.plot(ax=plt.gca())

plt.xlabel("Year")
plt.ylabel("Number of reported events")
plt.title("Natural Disaster Types Over Time")

plt.legend(title="Disaster type")
plt.tight_layout()

# DISASTER TYPE PERCENTAGE

# Calculate the percentage of each disaster type
disaster_percentage = (disaster_totals / disaster_totals.sum() * 100).sort_values(ascending=False)

print("\nPercentage of reported disasters by type:")
print(disaster_percentage)

# Create a bar chart
plt.figure(figsize=(10, 6))

disaster_percentage.plot(kind="bar")

plt.xlabel("Disaster type")
plt.ylabel("Percentage (%)")
plt.title("Percentage of Reported Natural Disasters by Type")

plt.xticks(rotation=45)
plt.tight_layout()

# FIND OUTLIERS IN DISASTER DATA

# Calculate Q1 and Q3
Q1 = disaster_types["n_events"].quantile(0.25)
Q3 = disaster_types["n_events"].quantile(0.75)

# Calculate the Interquartile Range (IQR)
IQR = Q3 - Q1

# Define the lower and upper limits for outliers
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

# Find outliers
outliers = disaster_types[
    (disaster_types["n_events"] < lower_limit) |
    (disaster_types["n_events"] > upper_limit)
]

print("\nQ1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)

print("\nOutlier limits:")
print("Lower limit:", lower_limit)
print("Upper limit:", upper_limit)

print("\nOutliers:")
print(outliers.sort_values("n_events", ascending=False))

# DATA QUALITY CHECK

# Check for missing values
missing_values = df.isnull().sum()

print("\nMissing values:")
print(missing_values)

# Check for duplicated rows
duplicate_rows = df.duplicated().sum()

print("\nNumber of duplicated rows:")
print(duplicate_rows)

# Check for duplicated year-disaster combinations
year_type_duplicates = df.duplicated(subset=["entity", "year"]).sum()

print("\nDuplicated disaster type-year combinations:")
print(year_type_duplicates)

# Check whether all event counts are non-negative
negative_events = df[df["n_events"] < 0]

print("\nNegative event counts:")
print(negative_events)

# DISTRIBUTION OF DISASTER EVENTS

plt.figure(figsize=(12, 7))

# Create boxplot for each disaster type
disaster_types.boxplot(
    column="n_events",
    by="entity",
    grid=False
)

plt.xlabel("Disaster type")
plt.ylabel("Number of reported events per year")
plt.title("Distribution of Reported Events by Disaster Type")

# Remove the automatic Pandas title
plt.suptitle("")

plt.xticks(rotation=45)
plt.tight_layout()

# CHANGE IN DISASTER FREQUENCY OVER TIME

# Get the first recorded value for each disaster type
first_values = disaster_types.sort_values("year").groupby("entity").first()["n_events"]

# Get the last recorded value for each disaster type
last_values = disaster_types.sort_values("year").groupby("entity").last()["n_events"]

# Calculate the absolute change
absolute_change = last_values - first_values

# Calculate the percentage change
percentage_change = ((last_values - first_values) / first_values) * 100

# Combine the results into one table
change_summary = pd.DataFrame({
    "first_year_events": first_values,
    "last_year_events": last_values,
    "absolute_change": absolute_change,
    "percentage_change": percentage_change
})

# Sort by percentage change
change_summary = change_summary.sort_values("percentage_change", ascending=False)

print("\nChange in reported disaster frequency:")
print(change_summary)

# Correlation between disaster types

correlation_matrix = disaster_pivot.corr()

print("\nCorrelation matrix:")
print(correlation_matrix)

# Visualize correlation matrix
plt.figure(figsize=(10, 8))

plt.imshow(correlation_matrix, vmin=-1, vmax=1)

plt.colorbar(label="Correlation")

plt.xticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns
)

# Display correlation values inside the chart
for i in range(len(correlation_matrix)):
    for j in range(len(correlation_matrix)):
        plt.text(
            j,
            i,
            f"{correlation_matrix.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

plt.title("Correlation Between Natural Disaster Types")
plt.tight_layout()

# Compare the beginning and the end of the dataset

disaster_types_sorted = disaster_types.sort_values("year")

first_5_years = disaster_types_sorted[disaster_types_sorted["year"].between(1970, 1974)]
last_5_years = disaster_types_sorted[disaster_types_sorted["year"].between(2021, 2025)]
first_5_average = (first_5_years.groupby("entity")["n_events"].mean())
last_5_average = (last_5_years.groupby("entity")["n_events"].mean())

period_comparison = pd.DataFrame({
    "1970-1974 average": first_5_average,
    "2021-2025 average": last_5_average
})

period_comparison["absolute_change"] = (period_comparison["2021-2025 average"] - period_comparison["1970-1974 average"])

period_comparison["percentage_change"] = (period_comparison["absolute_change"] / period_comparison["1970-1974 average"]) * 100

period_comparison = period_comparison.sort_values("percentage_change", ascending=False)

print("\nComparison between the beginning and the end of the dataset:")
print(period_comparison)

#plt.show()

# CHECK IMPACT DATASET

impact_df = pd.read_csv("data/raw/natural_disasters_impact.csv")

print("\n========== IMPACT DATASET ==========")

print("Shape:")
print(impact_df.shape)

print("\nColumns:")
print(impact_df.columns.tolist())

print("\nFirst 10 rows:")
print(impact_df.head(10).to_string())

print("\nData types:")
print(impact_df.dtypes)

print("\nMissing values:")
print(impact_df.isnull().sum())

# IMPACT DATASET: COUNTRY AND YEAR CHECK

print("\n========== COUNTRY AND YEAR CHECK ==========")

print("\nNumber of countries:")
print(impact_df["entity"].nunique())

print("\nYear range:")
print(
    impact_df["year"].min(),
    "to",
    impact_df["year"].max()
)

print("\nTop 15 countries by number of records:")

country_records = (impact_df["entity"].value_counts().head(15))

print(country_records.to_string())

print("\nTotal affected by country - top 15:")

country_impact = (
    impact_df
    .groupby("entity")["total_affected_all_disasters_yearly"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

print(country_impact.to_string())

# CHECK COUNTRY CODES

print("\n========== COUNTRY CODE CHECK ==========")

print("\nNumber of unique codes:")
print(impact_df["code"].nunique())

print("\nRows without country code:")
print(impact_df["code"].isna().sum())

print("\nEntities without country code:")
print(
    impact_df.loc[
        impact_df["code"].isna(),
        "entity"
    ].drop_duplicates().to_string(index=False)
)

print("\nExample of entities with country codes:")
print(
    impact_df[
        impact_df["code"].notna()
    ][["entity", "code"]]
    .drop_duplicates()
    .head(20)
    .to_string(index=False)
)
import os
import importlib.util

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RISK_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "country_risk_profile.csv"
)

IMPACT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "natural_disasters_impact.csv"
)

GLOBAL_EVENTS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "natural_disasters.csv"
)

GUIDE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "preparedness_guides.py"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Natural Disaster Risk Analysis",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    risk_df = pd.read_csv(RISK_PATH)
    impact_df = pd.read_csv(IMPACT_PATH)
    global_events_df = pd.read_csv(GLOBAL_EVENTS_PATH)

    return risk_df, impact_df, global_events_df


@st.cache_resource
def load_guides():
    spec = importlib.util.spec_from_file_location(
        "preparedness_guides",
        GUIDE_PATH
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.PREPAREDNESS_GUIDES


risk_df, impact_df, global_events_df = load_data()
PREPAREDNESS_GUIDES = load_guides()


# ============================================================
# HEADER
# ============================================================

st.title("🌍 Natural Disaster Risk Analysis & Awareness System")

st.markdown(
    """
    **Historical disaster impact analysis, risk profiling and preparedness awareness.**

    Explore recorded natural-disaster impacts by country and hazard,
    examine historical trends, and view preparedness guidance.
    """
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🔎 Analysis Controls")

countries = sorted(
    risk_df["entity"].dropna().unique().tolist()
)

country = st.sidebar.selectbox(
    "Select country",
    countries
)

country_data = risk_df[
    risk_df["entity"] == country
].copy()

country_data = country_data.sort_values(
    "total_people_affected",
    ascending=False
)

hazards = country_data[
    "disaster_type"
].dropna().tolist()

hazard = st.sidebar.selectbox(
    "Select hazard",
    hazards
)


# ============================================================
# COUNTRY PROFILE
# ============================================================

st.header(f"📍 Historical Risk Profile — {country}")

total_people = country_data[
    "total_people_affected"
].sum()

main_disaster = country_data.iloc[0][
    "disaster_type"
]

largest_share = country_data.iloc[0][
    "impact_share"
]

coverage = country_data[
    "years_recorded"
].max()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "People Affected",
        f"{total_people:,.0f}"
    )

with col2:
    st.metric(
        "Main Recorded Impact Type",
        main_disaster
    )

with col3:
    st.metric(
        "Largest Recorded Impact Share",
        f"{largest_share:.2f}%"
    )

with col4:
    st.metric(
        "Maximum Recorded Coverage",
        f"{int(coverage)} years"
    )


# ============================================================
# IMPACT PROFILE
# ============================================================

st.subheader("📊 Historical Disaster Impact Profile")

profile_data = country_data.sort_values(
    "impact_share",
    ascending=True
)

fig, ax = plt.subplots(figsize=(9, 5))

ax.barh(
    profile_data["disaster_type"],
    profile_data["impact_share"]
)

ax.set_xlabel(
    "Share of Recorded Impact (%)"
)

ax.set_ylabel(
    "Disaster Type"
)

ax.set_title(
    f"Historical Disaster Impact Profile — {country}"
)

ax.grid(
    axis="x",
    alpha=0.25
)

fig.tight_layout()

st.pyplot(fig)

plt.close(fig)


# ============================================================
# DATA TABLE
# ============================================================

st.subheader("📋 Recorded Impact Summary")

display_data = country_data[
    [
        "disaster_type",
        "total_people_affected",
        "impact_share",
        "years_recorded"
    ]
].copy()

display_data.columns = [
    "Disaster Type",
    "People Affected",
    "Impact Share (%)",
    "Years Recorded"
]

display_data["People Affected"] = (
    display_data["People Affected"]
    .map(lambda x: f"{x:,.0f}")
)

display_data["Impact Share (%)"] = (
    display_data["Impact Share (%)"]
    .map(lambda x: f"{x:.2f}")
)

display_data["Years Recorded"] = (
    display_data["Years Recorded"]
    .astype(int)
)

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# HAZARD ANALYSIS
# ============================================================

st.divider()

st.header(
    f"🌪️ Hazard Analysis — {hazard}"
)

hazard_row = country_data[
    country_data["disaster_type"] == hazard
]

if not hazard_row.empty:

    row = hazard_row.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "People Affected",
            f"{row['total_people_affected']:,.0f}"
        )

    with col2:
        st.metric(
            "Recorded Impact Share",
            f"{row['impact_share']:.2f}%"
        )

    with col3:
        st.metric(
            "Years Recorded",
            f"{int(row['years_recorded'])}"
        )


# ============================================================
# IMPACT TREND
# ============================================================

column_map = {
    "Drought":
        "total_affected_drought_yearly",

    "Earthquake":
        "total_affected_earthquake_yearly",

    "Volcanic activity":
        "total_affected_volcanic_activity_yearly",

    "Flood":
        "total_affected_flood_yearly",

    "Landslide":
        "total_affected_landslide_yearly",

    "Extreme weather":
        "total_affected_extreme_weather_yearly",

    "Wildfire":
        "total_affected_wildfire_yearly",

    "Extreme temperature":
        "total_affected_extreme_temperature_yearly"
}

column = column_map.get(hazard)

country_code = country_data.iloc[0]["code"]

trend_data = impact_df[
    impact_df["code"] == country_code
].copy()

if column and not trend_data.empty:

    trend = trend_data[
        [
            "year",
            column
        ]
    ].dropna()

    trend = trend.sort_values("year")

    if not trend.empty:

        st.subheader(
            f"📈 Historical Impact Trend — {hazard}"
        )

        fig, ax = plt.subplots(
            figsize=(10, 4.5)
        )

        ax.plot(
            trend["year"],
            trend[column],
            marker="o",
            markersize=3
        )

        ax.set_xlabel("Year")
        ax.set_ylabel("People Affected")

        ax.set_title(
            f"{country} — {hazard}"
        )

        ax.grid(
            True,
            alpha=0.25
        )

        ax.ticklabel_format(
            style="plain",
            axis="y"
        )

        fig.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# GLOBAL EVENT TREND
# ============================================================

st.divider()

st.header("🌎 Global Reported Disaster Events")

global_data = global_events_df[
    global_events_df["entity"] == hazard
].copy()

if not global_data.empty:

    global_data = global_data.sort_values(
        "year"
    )

    fig, ax = plt.subplots(
        figsize=(10, 4.5)
    )

    ax.plot(
        global_data["year"],
        global_data["n_events"],
        marker="o",
        markersize=3
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Reported Events")

    ax.set_title(
        f"Global Reported {hazard} Events"
    )

    ax.grid(
        True,
        alpha=0.25
    )

    fig.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# PREPAREDNESS GUIDE
# ============================================================

st.divider()

st.header(
    f"🛡️ Preparedness Guide — {hazard}"
)

guide = PREPAREDNESS_GUIDES.get(hazard)

if guide:

    tab_before, tab_during, tab_after = st.tabs(
        [
            "Before",
            "During",
            "After"
        ]
    )

    with tab_before:
        for item in guide["before"]:
            st.markdown(f"- {item}")

    with tab_during:
        for item in guide["during"]:
            st.markdown(f"- {item}")

    with tab_after:
        for item in guide["after"]:
            st.markdown(f"- {item}")

else:
    st.info(
        "No preparedness guide is currently available "
        "for this hazard."
    )


# ============================================================
# DISCLAIMER
# ============================================================

st.divider()

st.warning(
    """
    This system uses historical disaster data for risk awareness
    and preparedness. It is not a real-time emergency warning
    system and does not provide reliable future disaster predictions.
    Always follow instructions from local authorities and official
    emergency services.
    """
)

st.caption(
    "Data source: Our World in Data / EM-DAT, CRED/UCLouvain."
)
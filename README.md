# NATURAL DISASTER RISK ANALYSIS & AWARENESS SYSTEM

## Overview

A data analysis and awareness system that explores historical natural disaster events and their human impact.

The project combines statistical analysis, machine learning and interactive applications to identify patterns in disaster frequency, impact and historical trends.

**Live Demo:**  
https://natural-disaster-risk-analysis.streamlit.app/

> This project analyses historical data and is not a real-time warning or reliable future disaster prediction system.

## Key Questions

- Which disaster types are reported most frequently?
- How has reported disaster frequency changed over time?
- Which disaster types have the greatest recorded human impact?
- Which countries have recorded higher disaster impacts?
- What statistical relationships exist between disaster types?

## Analysis

The project includes:

- Data cleaning and validation
- Exploratory data analysis
- Statistical analysis
- Outlier detection using IQR and Z-scores
- Correlation analysis
- Historical trend analysis
- Machine learning with Linear Regression and Random Forest
- Country-level disaster impact analysis
- Data visualization

### Selected Findings

- 437 observations across 8 disaster types
- Historical event data from 1970–2025
- Floods and extreme weather represent a large proportion of recorded events
- Several unusual historical observations were identified through statistical analysis
- Machine learning models were evaluated using MAE, RMSE and R²

## What I Built

**Data Pipeline** — Cleaned and integrated historical disaster frequency and impact data.

**Analytics Engine** — Performed statistical analysis, trend analysis, correlation and outlier detection.

**Machine Learning** — Built and evaluated regression models for historical disaster-event patterns.

**Risk Profiling** — Generated country- and hazard-level historical impact profiles.

**Applications** — Built both a PySide6 desktop application and a Streamlit web application with a public live demo.

**Preparedness System** — Added disaster-specific preparedness guidance for users.

## Applications

### Desktop Application
Built with PySide6 for interactive country and disaster analysis.

### Web Application
Built with Streamlit and deployed online.


## Technologies

Python · Pandas · NumPy · Matplotlib · Scikit-learn · PySide6 · Streamlit

## Data

Historical disaster data from **Our World in Data / EM-DAT (CRED/UCLouvain)**.

The analysis focuses on reported historical events and recorded impacts. Changes in reported events may also reflect improvements in disaster reporting and data collection.

## Limitations

- Historical reporting quality varies over time.
- Correlation does not imply causation.
- Missing impact data does not necessarily mean zero impact.
- Machine learning results do not guarantee reliable future disaster prediction.

## Author

**Khoa Tran**
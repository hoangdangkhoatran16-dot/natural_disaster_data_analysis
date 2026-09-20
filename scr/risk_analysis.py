import sys
import pandas as pd
import matplotlib.pyplot as plt

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QFrame
)

# =========================================================
# LOAD DATA
# =========================================================

risk_df = pd.read_csv(
    "data/processed/country_risk_profile.csv"
)

impact_df = pd.read_csv(
    "data/raw/natural_disasters_impact.csv"
)

global_events_df = pd.read_csv(
    "data/raw/natural_disasters.csv"
)


# =========================================================
# MAIN APPLICATION
# =========================================================

class DisasterRiskApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Natural Disaster Risk Analysis System"
        )

        self.resize(1200, 750)

        # =================================================
        # MAIN LAYOUT
        # =================================================

        main_layout = QVBoxLayout()

        main_layout.setSpacing(15)

        # =================================================
        # HEADER
        # =================================================

        title = QLabel(
            "Natural Disaster Risk Analysis System"
        )

        title.setStyleSheet(
            """
            font-size: 30px;
            font-weight: bold;
            padding: 5px;
            """
        )

        main_layout.addWidget(title)

        subtitle = QLabel(
            "Historical analysis of disaster frequency "
            "and human impact"
        )

        subtitle.setStyleSheet(
            """
            font-size: 15px;
            color: #666666;
            padding-bottom: 10px;
            """
        )

        main_layout.addWidget(subtitle)

        # =================================================
        # COUNTRY SELECTION
        # =================================================

        selection_layout = QHBoxLayout()

        country_label = QLabel(
            "Country:"
        )

        country_label.setStyleSheet(
            "font-weight: bold; font-size: 15px;"
        )

        selection_layout.addWidget(
            country_label
        )

        self.country_box = QComboBox()

        countries = sorted(
            risk_df["entity"].unique()
        )

        self.country_box.addItems(
            countries
        )

        self.country_box.setMinimumWidth(
            300
        )

        selection_layout.addWidget(
            self.country_box
        )

        self.analyze_button = QPushButton(
            "Analyze"
        )

        self.analyze_button.clicked.connect(
            self.show_profile
        )

        selection_layout.addWidget(
            self.analyze_button
        )

        selection_layout.addStretch()

        main_layout.addLayout(
            selection_layout
        )

        # =================================================
        # STATISTICS CARDS
        # =================================================

        stats_layout = QGridLayout()

        self.total_people_card = self.create_card(
            "People Affected",
            "0"
        )

        self.main_disaster_card = self.create_card(
            "Main Disaster",
            "-"
        )

        self.impact_share_card = self.create_card(
            "Largest Impact Share",
            "0%"
        )

        self.years_card = self.create_card(
            "Data Coverage",
            "0 years"
        )

        stats_layout.addWidget(
            self.total_people_card,
            0,
            0
        )

        stats_layout.addWidget(
            self.main_disaster_card,
            0,
            1
        )

        stats_layout.addWidget(
            self.impact_share_card,
            0,
            2
        )

        stats_layout.addWidget(
            self.years_card,
            0,
            3
        )

        main_layout.addLayout(
            stats_layout
        )

        # =================================================
        # CHART BUTTONS
        # =================================================

        chart_layout = QHBoxLayout()

        self.impact_chart_button = QPushButton(
            "Impact Profile"
        )

        self.impact_chart_button.clicked.connect(
            self.show_impact_chart
        )

        chart_layout.addWidget(
            self.impact_chart_button
        )

        self.trend_button = QPushButton(
            "Impact Trend"
        )

        self.trend_button.clicked.connect(
            self.show_impact_trend
        )

        chart_layout.addWidget(
            self.trend_button
        )

        self.global_button = QPushButton(
            "Global Event Trend"
        )

        self.global_button.clicked.connect(
            self.show_global_trend
        )

        chart_layout.addWidget(
            self.global_button
        )

        chart_layout.addStretch()

        main_layout.addLayout(
            chart_layout
        )

        # =================================================
        # TABLE TITLE
        # =================================================

        table_title = QLabel(
            "Historical Disaster Impact Profile"
        )

        table_title.setStyleSheet(
            """
            font-size: 19px;
            font-weight: bold;
            padding-top: 5px;
            """
        )

        main_layout.addWidget(
            table_title
        )

        # =================================================
        # TABLE
        # =================================================

        self.table = QTableWidget()

        self.table.setColumnCount(
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Disaster Type",
                "People Affected",
                "Impact Share (%)",
                "Years Recorded"
            ]
        )

        self.table.setAlternatingRowColors(
            True
        )

        main_layout.addWidget(
            self.table
        )

        # =================================================
        # DISCLAIMER
        # =================================================

        disclaimer = QLabel(
            "Historical analysis only — this system does "
            "not provide emergency warnings or future "
            "disaster predictions."
        )

        disclaimer.setStyleSheet(
            """
            color: #777777;
            font-size: 12px;
            padding-top: 5px;
            """
        )

        main_layout.addWidget(
            disclaimer
        )

        self.setLayout(
            main_layout
        )

        # =================================================
        # INITIAL ANALYSIS
        # =================================================

        self.show_profile()

    # =====================================================
    # CREATE STATISTICS CARD
    # =====================================================

    def create_card(
        self,
        title,
        value
    ):

        card = QFrame()

        card.setFrameShape(
            QFrame.StyledPanel
        )

        card.setStyleSheet(
            """
            QFrame {
                border: 1px solid #dddddd;
                border-radius: 8px;
                background-color: #f8f8f8;
            }

            QLabel {
                border: none;
            }
            """
        )

        layout = QVBoxLayout()

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet(
            """
            font-size: 13px;
            color: #666666;
            """
        )

        value_label = QLabel(
            value
        )

        value_label.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            padding-top: 5px;
            """
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            value_label
        )

        card.setLayout(
            layout
        )

        # Store value label so it can be updated
        card.value_label = value_label

        return card

    # =====================================================
    # GET COUNTRY
    # =====================================================

    def get_country(self):

        return self.country_box.currentText()

    # =====================================================
    # SHOW PROFILE
    # =====================================================

    def show_profile(self):

        country = self.get_country()

        country_data = risk_df[
            risk_df["entity"] == country
        ].copy()

        country_data = country_data.sort_values(
            "historical_impact_score",
            ascending=False
        )

        if country_data.empty:

            return

        # -------------------------------------------------
        # CALCULATE SUMMARY
        # -------------------------------------------------

        total_people = (
            country_data[
                "total_people_affected"
            ].sum()
        )

        highest_impact = (
            country_data.iloc[0]
        )

        years = (
            country_data[
                "years_recorded"
            ].max()
        )

        # -------------------------------------------------
        # UPDATE CARDS
        # -------------------------------------------------

        self.total_people_card.value_label.setText(
            f"{total_people:,.0f}"
        )

        self.main_disaster_card.value_label.setText(
            highest_impact["disaster_type"]
        )

        self.impact_share_card.value_label.setText(
            f"{highest_impact['impact_share']:.2f}%"
        )

        self.years_card.value_label.setText(
            f"{years} years"
        )

        # -------------------------------------------------
        # UPDATE TABLE
        # -------------------------------------------------

        self.table.setRowCount(
            len(country_data)
        )

        for row, (_, data) in enumerate(
            country_data.iterrows()
        ):

            values = [

                str(
                    data["disaster_type"]
                ),

                f"{data['total_people_affected']:,.0f}",

                f"{data['impact_share']:.2f}",

                str(
                    data["years_recorded"]
                )
            ]

            for column, value in enumerate(
                values
            ):

                item = QTableWidgetItem(
                    value
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

        self.table.resizeColumnsToContents()

    # =====================================================
    # IMPACT PROFILE CHART
    # =====================================================

    def show_impact_chart(self):

        country = self.get_country()

        country_data = risk_df[
            risk_df["entity"] == country
        ].copy()

        country_data = country_data.sort_values(
            "impact_share",
            ascending=True
        )

        plt.figure(
            figsize=(10, 6)
        )

        plt.barh(
            country_data["disaster_type"],
            country_data["impact_share"]
        )

        plt.xlabel(
            "Share of Recorded People Affected (%)"
        )

        plt.ylabel(
            "Disaster Type"
        )

        plt.title(
            f"Historical Disaster Impact Profile - {country}"
        )

        plt.tight_layout()

        plt.show()

    # =====================================================
    # IMPACT TREND
    # =====================================================

    def show_impact_trend(self):

        country = self.get_country()

        country_data = impact_df[
            impact_df["entity"] == country
        ].copy()

        if country_data.empty:

            return

        country_data = country_data[
            [
                "year",
                "total_affected_all_disasters_yearly"
            ]
        ].dropna()

        country_data = country_data.sort_values(
            "year"
        )

        plt.figure(
            figsize=(10, 6)
        )

        plt.plot(
            country_data["year"],
            country_data[
                "total_affected_all_disasters_yearly"
            ]
        )

        plt.xlabel(
            "Year"
        )

        plt.ylabel(
            "People Affected"
        )

        plt.title(
            f"People Affected by Natural Disasters - {country}"
        )

        plt.grid(
            True
        )

        plt.tight_layout()

        plt.show()

    # =====================================================
    # GLOBAL EVENT TREND
    # =====================================================

    def show_global_trend(self):

        global_data = global_events_df[
            global_events_df["entity"]
            == "All disasters"
        ].copy()

        global_data = global_data.sort_values(
            "year"
        )

        plt.figure(
            figsize=(10, 6)
        )

        plt.plot(
            global_data["year"],
            global_data["n_events"]
        )

        plt.xlabel(
            "Year"
        )

        plt.ylabel(
            "Reported Natural Disaster Events"
        )

        plt.title(
            "Global Reported Natural Disaster Events"
        )

        plt.grid(
            True
        )

        plt.tight_layout()

        plt.show()


# =========================================================
# RUN
# =========================================================

app = QApplication(
    sys.argv
)

window = DisasterRiskApp()

window.show()

sys.exit(
    app.exec()
)
import sys
import os
import importlib.util

import pandas as pd

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QDialog,
    QTabWidget,
    QListWidget,
    QGroupBox,
)
from PySide6.QtCore import Qt


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
# LOAD PREPAREDNESS GUIDES
# ============================================================

spec = importlib.util.spec_from_file_location(
    "preparedness_guides",
    GUIDE_PATH
)

guides_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guides_module)

PREPAREDNESS_GUIDES = guides_module.PREPAREDNESS_GUIDES


# ============================================================
# LOAD DATA
# ============================================================

risk_df = pd.read_csv(RISK_PATH)
impact_df = pd.read_csv(IMPACT_PATH)
global_events_df = pd.read_csv(GLOBAL_EVENTS_PATH)


# ============================================================
# PREPAREDNESS GUIDE DIALOG
# ============================================================

class PreparednessDialog(QDialog):

    def __init__(self, disaster_type, parent=None):
        super().__init__(parent)

        self.setWindowTitle(
            f"Preparedness Guide - {disaster_type}"
        )

        self.resize(700, 500)

        layout = QVBoxLayout()

        title = QLabel(
            f"🛡️ {disaster_type} Preparedness Guide"
        )

        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            padding: 10px;
            """
        )

        layout.addWidget(title)

        guide = PREPAREDNESS_GUIDES.get(disaster_type)

        if guide is None:
            message = QLabel(
                "No preparedness guide is currently available "
                "for this hazard."
            )

            message.setWordWrap(True)
            layout.addWidget(message)

            self.setLayout(layout)
            return

        tabs = QTabWidget()

        # ----------------------------------------------------
        # BEFORE
        # ----------------------------------------------------

        before_list = QListWidget()

        for item in guide["before"]:
            before_list.addItem("• " + item)

        tabs.addTab(
            before_list,
            "Before"
        )

        # ----------------------------------------------------
        # DURING
        # ----------------------------------------------------

        during_list = QListWidget()

        for item in guide["during"]:
            during_list.addItem("• " + item)

        tabs.addTab(
            during_list,
            "During"
        )

        # ----------------------------------------------------
        # AFTER
        # ----------------------------------------------------

        after_list = QListWidget()

        for item in guide["after"]:
            after_list.addItem("• " + item)

        tabs.addTab(
            after_list,
            "After"
        )

        layout.addWidget(tabs)

        warning = QLabel(
            "⚠️ Always follow instructions from local authorities "
            "and official emergency services."
        )

        warning.setWordWrap(True)

        warning.setStyleSheet(
            """
            background-color: #fff3cd;
            padding: 10px;
            border-radius: 6px;
            """
        )

        layout.addWidget(warning)

        close_button = QPushButton("Close")

        close_button.clicked.connect(
            self.accept
        )

        layout.addWidget(close_button)

        self.setLayout(layout)


# ============================================================
# MAIN APPLICATION
# ============================================================

class DisasterApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Natural Disaster Risk Analysis & Awareness System"
        )

        self.resize(1100, 750)

        self.selected_country_data = pd.DataFrame()

        self.setup_ui()

        self.load_countries()


    # ========================================================
    # UI SETUP
    # ========================================================

    def setup_ui(self):

        main_layout = QVBoxLayout()

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QLabel(
            "🌍 Natural Disaster Risk Analysis & Awareness System"
        )

        header.setAlignment(Qt.AlignCenter)

        header.setStyleSheet(
            """
            font-size: 26px;
            font-weight: bold;
            padding: 15px;
            """
        )

        main_layout.addWidget(header)


        subtitle = QLabel(
            "Historical disaster impact analysis and preparedness awareness"
        )

        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet(
            """
            font-size: 14px;
            color: #666;
            padding-bottom: 10px;
            """
        )

        main_layout.addWidget(subtitle)


        # ----------------------------------------------------
        # COUNTRY SELECTION
        # ----------------------------------------------------

        selection_group = QGroupBox(
            "Select Location"
        )

        selection_layout = QHBoxLayout()

        self.country_box = QComboBox()

        self.country_box.setMinimumWidth(300)

        self.country_box.currentIndexChanged.connect(
            self.country_changed
        )

        selection_layout.addWidget(
            QLabel("Country:")
        )

        selection_layout.addWidget(
            self.country_box
        )


        self.hazard_box = QComboBox()

        self.hazard_box.setMinimumWidth(250)

        selection_layout.addWidget(
            QLabel("Hazard:")
        )

        selection_layout.addWidget(
            self.hazard_box
        )


        analyze_button = QPushButton(
            "Analyze"
        )

        analyze_button.clicked.connect(
            self.show_profile
        )

        selection_layout.addWidget(
            analyze_button
        )


        selection_group.setLayout(
            selection_layout
        )

        main_layout.addWidget(
            selection_group
        )


        # ----------------------------------------------------
        # STAT CARDS
        # ----------------------------------------------------

        cards_layout = QHBoxLayout()


        self.people_label = QLabel(
            "People Affected\n-"
        )

        self.main_disaster_label = QLabel(
            "Main Disaster\n-"
        )

        self.share_label = QLabel(
            "Largest Impact Share\n-"
        )

        self.coverage_label = QLabel(
            "Data Coverage\n-"
        )


        card_labels = [
            self.people_label,
            self.main_disaster_label,
            self.share_label,
            self.coverage_label
        ]


        for label in card_labels:

            label.setAlignment(
                Qt.AlignCenter
            )

            label.setStyleSheet(
                """
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 15px;
                font-size: 15px;
                """
            )

            cards_layout.addWidget(
                label
            )


        main_layout.addLayout(
            cards_layout
        )


        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        table_title = QLabel(
            "Historical Impact Profile"
        )

        table_title.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            padding-top: 10px;
            """
        )

        main_layout.addWidget(
            table_title
        )


        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            [
                "Disaster Type",
                "People Affected",
                "Impact Share (%)",
                "Years Recorded"
            ]
        )

        self.table.horizontalHeader().setStretchLastSection(
            True
        )

        main_layout.addWidget(
            self.table
        )


        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        buttons_layout = QHBoxLayout()


        guide_button = QPushButton(
            "🛡️ Preparedness Guide"
        )

        guide_button.clicked.connect(
            self.show_preparedness_guide
        )

        buttons_layout.addWidget(
            guide_button
        )


        impact_button = QPushButton(
            "📊 Impact Profile"
        )

        impact_button.clicked.connect(
            self.show_impact_profile
        )

        buttons_layout.addWidget(
            impact_button
        )


        trend_button = QPushButton(
            "📈 Impact Trend"
        )

        trend_button.clicked.connect(
            self.show_impact_trend
        )

        buttons_layout.addWidget(
            trend_button
        )


        global_button = QPushButton(
            "🌎 Global Event Trend"
        )

        global_button.clicked.connect(
            self.show_global_trend
        )

        buttons_layout.addWidget(
            global_button
        )


        main_layout.addLayout(
            buttons_layout
        )


        # ----------------------------------------------------
        # DISCLAIMER
        # ----------------------------------------------------

        disclaimer = QLabel(
            "⚠️ This system uses historical disaster data for "
            "risk awareness and preparedness. It is not a "
            "real-time emergency warning system and does not "
            "provide reliable future disaster predictions."
        )

        disclaimer.setWordWrap(True)

        disclaimer.setStyleSheet(
            """
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 10px;
            margin-top: 10px;
            """
        )

        main_layout.addWidget(
            disclaimer
        )


        self.setLayout(
            main_layout
        )


    # ========================================================
    # LOAD COUNTRIES
    # ========================================================

    def load_countries(self):

        countries = sorted(
            risk_df["entity"].dropna().unique()
        )

        self.country_box.addItems(
            countries
        )


    # ========================================================
    # COUNTRY CHANGED
    # ========================================================

    def country_changed(self):

        country = self.country_box.currentText()

        if not country:
            return

        country_data = risk_df[
            risk_df["entity"] == country
        ].copy()

        country_data = country_data.sort_values(
            "total_people_affected",
            ascending=False
        )

        self.selected_country_data = country_data

        self.hazard_box.clear()

        self.hazard_box.addItems(
            country_data["disaster_type"].tolist()
        )

        if len(country_data) > 0:
            self.show_profile()


    # ========================================================
    # SHOW PROFILE
    # ========================================================

    def show_profile(self):

        country = self.country_box.currentText()

        if not country:
            return

        country_data = risk_df[
            risk_df["entity"] == country
        ].copy()

        if country_data.empty:

            QMessageBox.warning(
                self,
                "No Data",
                "No historical data is available."
            )

            return


        country_data = country_data.sort_values(
            "total_people_affected",
            ascending=False
        )

        self.selected_country_data = country_data


        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        total_people = country_data[
            "total_people_affected"
        ].sum()


        main_disaster = country_data.iloc[0][
            "disaster_type"
        ]


        largest_share = country_data.iloc[0][
            "impact_share"
        ]


        years = country_data[
            "years_recorded"
        ].max()


        self.people_label.setText(
            f"People Affected\n{total_people:,.0f}"
        )


        self.main_disaster_label.setText(
            f"Main Disaster\n{main_disaster}"
        )


        self.share_label.setText(
            f"Largest Impact Share\n{largest_share:.2f}%"
        )


        self.coverage_label.setText(
            f"Data Coverage\n{years} years"
        )


        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        self.table.setRowCount(
            len(country_data)
        )


        for row, (_, data) in enumerate(
            country_data.iterrows()
        ):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(data["disaster_type"])
                )
            )


            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    f"{data['total_people_affected']:,.0f}"
                )
            )


            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    f"{data['impact_share']:.2f}"
                )
            )


            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(int(data["years_recorded"]))
                )
            )


    # ========================================================
    # PREPAREDNESS GUIDE
    # ========================================================

    def show_preparedness_guide(self):

        disaster_type = self.hazard_box.currentText()

        if not disaster_type:

            QMessageBox.information(
                self,
                "No Hazard Selected",
                "Please select a hazard first."
            )

            return


        dialog = PreparednessDialog(
            disaster_type,
            self
        )

        dialog.exec()


    # ========================================================
    # IMPACT PROFILE
    # ========================================================

    def show_impact_profile(self):

        if self.selected_country_data.empty:
            return


        data = self.selected_country_data

        lines = []

        for _, row in data.iterrows():

            lines.append(
                f"{row['disaster_type']}: "
                f"{row['total_people_affected']:,.0f} people "
                f"({row['impact_share']:.2f}%)"
            )


        QMessageBox.information(
            self,
            "Historical Impact Profile",
            "\n".join(lines)
        )


    # ========================================================
    # IMPACT TREND
    # ========================================================

    def show_impact_trend(self):

        country = self.country_box.currentText()

        if not country:
            return


        country_info = risk_df[
            risk_df["entity"] == country
        ]


        if country_info.empty:
            return


        code = country_info.iloc[0]["code"]


        country_data = impact_df[
            impact_df["code"] == code
        ].copy()


        if country_data.empty:

            QMessageBox.information(
                self,
                "No Data",
                "No impact trend data is available."
            )

            return


        disaster_type = self.hazard_box.currentText()


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


        column = column_map.get(
            disaster_type
        )


        if column not in country_data.columns:

            QMessageBox.information(
                self,
                "No Data",
                "No trend data is available for this hazard."
            )

            return


        trend = country_data[
            ["year", column]
        ].dropna()


        if trend.empty:
            return


        text = (
            f"Historical Impact Trend\n\n"
            f"Country: {country}\n"
            f"Hazard: {disaster_type}\n\n"
        )


        recent = trend.tail(10)


        for _, row in recent.iterrows():

            text += (
                f"{int(row['year'])}: "
                f"{row[column]:,.0f} people affected\n"
            )


        QMessageBox.information(
            self,
            "Impact Trend",
            text
        )


    # ========================================================
    # GLOBAL EVENT TREND
    # ========================================================

    def show_global_trend(self):

        disaster_type = self.hazard_box.currentText()

        if not disaster_type:
            disaster_type = "Flood"


        global_data = global_events_df[
            global_events_df["entity"] == disaster_type
        ].copy()


        if global_data.empty:

            QMessageBox.information(
                self,
                "No Data",
                "No global event data is available."
            )

            return


        recent = global_data.tail(10)


        text = (
            f"Global Reported Events\n\n"
            f"Disaster type: {disaster_type}\n\n"
        )


        for _, row in recent.iterrows():

            text += (
                f"{int(row['year'])}: "
                f"{int(row['n_events'])} reported events\n"
            )


        QMessageBox.information(
            self,
            "Global Event Trend",
            text
        )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = DisasterApp()

    window.show()

    sys.exit(
        app.exec()
    )
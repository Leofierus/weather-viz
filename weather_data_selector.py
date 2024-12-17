import sys
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QPoint

from helper import data_bins
from weather_card import WeatherCard

class DraggableScrollArea(QScrollArea):
    def __init__(self, *args, **kwargs):
        """
        Create a vertically draggable scroll area.
        """
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self._dragging = False
        self._start_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging:
            delta = event.pos() - self._start_pos
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self._start_pos = event.pos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False
        super().mouseReleaseEvent(event)

def cloud_condition(cloud_cover):
    """
    Determine cloud condition based on cloud cover percentage.
    """
    if 0 <= cloud_cover <= 10:
        return "Clear or Sunny"
    elif 10 < cloud_cover <= 30:
        return "Mostly Clear"
    elif 30 < cloud_cover <= 50:
        return "Partly Cloudy"
    elif 50 < cloud_cover <= 90:
        return "Mostly Cloudy"
    elif 90 < cloud_cover <= 100:
        return "Cloudy"
    else:
        return "Invalid cloud cover value"

class WeatherDataSelector(QMainWindow):
    def __init__(self, location):
        """
        Initialize the main window for weather data selection.
        """
        super().__init__()
        self.setWindowTitle("Weather Data Selector")
        self.setGeometry(100, 100, 600, 800)
        self.setFixedSize(self.size())

        # Main Widget and Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Create a container layout for centering
        container_layout = QVBoxLayout()  # Using QVBoxLayout to stack elements vertically
        container_layout.setAlignment(Qt.AlignCenter)  # Center the content in the layout
        main_layout.addLayout(container_layout)

        # Example data
        weather_data = data_bins()
        now = datetime.now()
        filter_data = {}

        current_data = {}
        all_data = {}
        time = str(now).split()[1].split(':')[0]
        print("times")

        for date, value in weather_data.items():
            temp = datetime.strptime(date.split('+')[0], "%Y-%m-%d %H:%M:%S")
            hour_temp = temp.hour
            if time in str(temp) and hour_temp == now.hour:
                current_data[date] = value
            if now <= temp:
                filter_data[date] = value
            all_data[date] = value
        weather_data = filter_data

        # Create a vertical layout for the main card and scroll area
        top_row_layout = QVBoxLayout()  # For the main card (top row)
        bottom_row_layout = QVBoxLayout()  # For the scroll area (second row)

        # Main Card Layout (Top Row)
        main_card = None
        for date, val in current_data.items():
            card_data = {
                'temperature': val['temperature_2m'],
                'precipitation': val['precipitation'],
                'humidity': val['relative_humidity_2m'],
                'wind_speed': val['wind_speed_10m'],
                'weather_condition': cloud_condition(val['cloud_cover']),
                'location': location,
                'timestamp': datetime.fromisoformat(date)
            }
            main_card = WeatherCard(card_data, {date: val}, all_data)

        # Center the main_card in the top row
        top_row_layout.addWidget(main_card, alignment=Qt.AlignCenter)

        # Scrollable Area Layout (Bottom Row)
        scroll_area = DraggableScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setMinimumWidth(500)  # Set a minimum width for the scroll area
        scroll_area.setMaximumWidth(700)  # Set a maximum width to prevent over-stretching

        # Scrollable Content
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignCenter)
        scroll_layout.setSpacing(20)  # Add some spacing between cards

        # Add Weather Cards
        for date, val in weather_data.items():
            card_data = {
                'temperature': val['temperature_2m'],
                'precipitation': val['precipitation'],
                'humidity': val['relative_humidity_2m'],
                'wind_speed': val['wind_speed_10m'],
                'weather_condition': cloud_condition(val['cloud_cover']),
                'location': location,
                'timestamp': datetime.fromisoformat(date)
            }
            card = WeatherCard(card_data, {date: val}, all_data)
            scroll_layout.addWidget(card)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        bottom_row_layout.addWidget(scroll_area)

        # Add both top and bottom rows to the container layout
        container_layout.addLayout(top_row_layout)  # Add the top row with main card
        container_layout.addLayout(bottom_row_layout)  # Add the bottom row with scroll area


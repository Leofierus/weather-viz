import sys
from typing import Dict, Any
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QWidget, QFrame, QLabel,
    QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt
from pygame.examples.go_over_there import screen

from pygame_base import screen_init


class WeatherCard(QWidget):
    def __init__(self, weather_data: Dict[str, Any] = None, data: Dict[str, Any] = None):
        """
        Initialize a professional weather card with optional weather data.

        :param weather_data: Dictionary containing weather information
        """
        super().__init__()
        self.data = data
        self.setWindowFlags(Qt.FramelessWindowHint)  # Frameless for modern look
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Default weather data if not provided
        self.weather_data = weather_data or {
            'temperature': 22,
            'precipitation': 0,
            'humidity': 90,
            'wind_speed': 5,
            'weather_condition': 'Partly Cloudy',
            'location': 'New York',
            'timestamp': datetime.now()
        }

        self._init_ui()

    def _init_ui(self):
        """Initialize the user interface components."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Card Frame
        card_frame = QFrame()
        card_frame.setObjectName('weatherCardFrame')

        # Main Grid Layout
        grid_layout = QGridLayout(card_frame)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setSpacing(15)

        # Temperature Section
        temp_layout = QVBoxLayout()
        self.temp_label = QPushButton(f"{self.weather_data['temperature']:.1f} °C")
        self.temp_label.setStyleSheet("background-color: transparent; border: none;")
        self.temp_label.clicked.connect(self.change_temperature)

        self.temp_label.setObjectName('temperatureLabel')


        temp_layout.addWidget(self.temp_label)
        grid_layout.addLayout(temp_layout, 0, 0, 2, 1)

        # Weather Details Section
        details_layout = QVBoxLayout()

        # Location and Time
        location_label = QLabel(f"{self.weather_data['location']}")
        location_label.setObjectName('locationLabel')
        time_label = QLabel(self.weather_data['timestamp'].strftime("%d %b, %I:%M %p"))
        time_label.setObjectName('timeLabel')

        details_layout.addWidget(location_label)
        details_layout.addWidget(time_label)
        details_layout.addStretch()

        # Weather Conditions Grid
        conditions_grid = QGridLayout()
        conditions = [
            ('Precipitation', f"{self.weather_data['precipitation']:.1f} mm"),
            ('Humidity', f"{self.weather_data['humidity']:.1f}%"),
            ('Wind', f"{self.weather_data['wind_speed']:.1f} m/s"),
            ('Condition', self.weather_data['weather_condition'])
        ]

        for i, (label, value) in enumerate(conditions):
            condition_label = QLabel(label)
            condition_value = QLabel(value)
            condition_label.setObjectName('conditionLabel')
            condition_value.setObjectName('conditionValue')

            conditions_grid.addWidget(condition_label, i // 2, (i % 2) * 2)
            conditions_grid.addWidget(condition_value, i // 2, (i % 2) * 2 + 1)

        details_layout.addLayout(conditions_grid)

        grid_layout.addLayout(details_layout, 0, 1, 2, 2)

        # Add card to main layout
        main_layout.addWidget(card_frame)

        # Set stylesheet
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
            }

            #weatherCardFrame {
                background-color: rgba(255, 255, 255, 230);
                border-radius: 15px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            }

            #temperatureLabel {
                font-size: 36px;
                font-weight: bold;
                color: #007bff;
            }

            #locationLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }

            #timeLabel {
                font-size: 14px;
                color: #666;
                margin-bottom: 10px;
            }

            #conditionLabel {
                font-size: 12px;
                color: #999;
                text-align: right;
                margin-right: 10px;
            }

            #conditionValue {
                font-size: 14px;
                color: #333;
                font-weight: 500;
            }
        """)

        self.setLayout(main_layout)

        # Sizing
        self.setMaximumSize(500, 200)

    def change_temperature(self):
        print(self.temp_label.text().split())
        temp = float(self.temp_label.text().split()[0])

        if "C" in self.temp_label.text():
            temp = float((temp * 1.8) + 32)
            self.temp_label.setText(f"{temp:.1f} °F")
        else:
            temp = float((temp-32) * (5/9))
            self.temp_label.setText(f"{temp:.1f} °C")

    def mousePressEvent(self, event):
        ''' TODO: call with arguments '''
        print(self.data)

        # screen_init()
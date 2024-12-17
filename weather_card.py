import random
import sys
from typing import Dict, Any
from datetime import datetime, timedelta

from PyQt5.QtWidgets import (
    QApplication, QWidget, QFrame, QLabel,
    QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt
from pygame.examples.go_over_there import screen

from pygame_base import screen_init


class WeatherCard(QWidget):
    def __init__(self, weather_data: Dict[str, Any] = None, data: Dict[str, Any] = None,
                 all_data: Dict[str, Any] = None):
        """
        Initialize a professional weather card with optional weather data.

        :param weather_data: Dictionary containing weather information
        """
        super().__init__()
        self.data = data
        self.all_data = all_data
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
            temp = float((temp - 32) * (5 / 9))
            self.temp_label.setText(f"{temp:.1f} °C")

    def mousePressEvent(self, event):
        tile_paths = {
            "Spring": "tiles/Seasonal Tilesets/Seasonal Tilesets/1 - Grassland/Terrain (16 x 16).png",
            "Fall": "tiles/Seasonal Tilesets/Seasonal Tilesets/2 - Autumn Forest/Terrain (16 x 16).png",
            "Summer": "tiles/Seasonal Tilesets/Seasonal Tilesets/3 - Tropics/Terrain (16 x 16).png",
            "Winter": "tiles/Seasonal Tilesets/Seasonal Tilesets/4 - Winter World/Terrain (16 x 16).png"
        }

        month = list(self.data.keys())[0].split()[0].split("-")[1]
        current_hour = list(self.data.keys())[0].split()[1].split(":")[0]
        if month in ["03", "04", "05"]:
            season = "Spring"
        elif month in ["06", "07", "08"]:
            season = "Summer"
        elif month in ["09", "10", "11"]:
            season = "Fall"
        else:
            season = "Winter"

        sunrise, sunset = False, False
        if 6 <= int(current_hour) <= 8:
            sunrise = True
        elif 16 <= int(current_hour) <= 19:
            sunset = True

        current_temperature = self.data[list(self.data.keys())[0]]['temperature_2m']
        current_hour_str = list(self.data.keys())[0]
        current_hour_dt = datetime.fromisoformat(current_hour_str)
        next_hour_dt = current_hour_dt + timedelta(hours=1)
        next_hour_str = next_hour_dt.isoformat().replace("T", " ")
        next_hour_temperature = self.all_data.get(next_hour_str, {}).get('temperature_2m', current_temperature)
        if abs(current_temperature - next_hour_temperature) > 0.5:
            if next_hour_temperature > current_temperature:
                next_hour_temperature += 1
            elif next_hour_temperature < current_temperature:
                current_temperature += 1

        cloud_cover = self.data[list(self.data.keys())[0]]['cloud_cover']
        is_day = self.data[list(self.data.keys())[0]]['is_day']
        rain = self.data[list(self.data.keys())[0]]['rain']
        snowfall = self.data[list(self.data.keys())[0]]['snowfall']
        weather_effects = False
        if rain > 0 or snowfall > 0:
            weather_effects = True
        weather_type = ""
        weather_intensity = 0
        if weather_effects:
            if rain > 0 and snowfall > 0:
                weather_type = "mix"
                weather_intensity = (int(rain) + int(snowfall)) * 2
            elif rain > 0:
                weather_type = "rain"
                weather_intensity = int(rain) * 2
            elif 0 < snowfall < 5:
                weather_type = "light_snow"
                weather_intensity = int(snowfall) * 2
            else:
                weather_type = "snow"
                weather_intensity = int(snowfall) * 3

        wind_speed = self.data[list(self.data.keys())[0]]['wind_speed_10m'] + 5 \
            if self.data[list(self.data.keys())[0]]['wind_speed_10m'] > 10 else 0
        actual_wind_speed = self.data[list(self.data.keys())[0]]['wind_speed_10m']
        is_windy = wind_speed > 10
        weather_code = int(self.data[list(self.data.keys())[0]]['weather_code'])

        is_lightning = weather_code > 94
        lightning_strikes = 0
        if weather_code == 95:
            lightning_strikes = random.randint(1, 5)
        elif weather_code == 96:
            lightning_strikes = random.randint(5, 10)
        elif 96 < weather_code < 100:
            lightning_strikes = random.randint(10, 20)

        if cloud_cover > 75 or (rain > 0 and int(is_day) != 1):
            cloud_type = "dark_clouds"
        elif 50 < cloud_cover <= 75:
            cloud_type = "cloudy"
        elif rain > 0:
            cloud_type = "rainy"
        elif int(is_day) != 1:
            cloud_type = "night"
        elif sunrise:
            cloud_type = "sun_rise"
        elif sunset:
            cloud_type = "sun_set"
        else:
            cloud_type = "day"

        if cloud_type in ["rainy", "dark_clouds", "cloudy", "night"]:
            mountain_type = "night"
        elif season == "Winter":
            mountain_type = "winter"
        else:
            mountain_type = random.choice(["rocky", "day"])

        screen_text = f"Temperature: {current_temperature:.2f}°C ({(current_temperature * 1.8 + 32):.2f}°F)  " \
                      f"Wind Speed: {actual_wind_speed:.2f} kmh ({(actual_wind_speed * 0.621371):.2f} mph)  " \
                      f"Rain expected: {rain:.2f} mm  Snow expected: {snowfall:.2f} cm"

        print(f"Args passed\n{tile_paths[season]} {current_temperature} {next_hour_temperature} {cloud_type}\n"
              f"{mountain_type} {season} {is_windy} {wind_speed} {is_lightning} {lightning_strikes}\n"
              f"{weather_effects} {weather_type} {weather_intensity}\n{screen_text}")
        screen_init(tile_paths[season], current_temperature, next_hour_temperature, cloud_type, mountain_type, season,
                    is_windy, wind_speed, is_lightning, lightning_strikes, weather_effects, weather_type,
                    weather_intensity, screen_text, 1200, 800)

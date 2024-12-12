import os
import sys

import folium
import geocoder
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QLineEdit, \
    QListWidget, QProgressBar, QDesktopWidget
from PyQt5.QtCore import QUrl, QThread
from PyQt5.QtWebEngineWidgets import *
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from api.get_weather_api import get_weather_data_api
from get_weather_data import DownloadDialog
from helper import *
from weather_data_selector import WeatherDataSelector

location_label = None
address = ""
point = [-91, -181]

load_dotenv()
API_KEY = os.getenv("API_KEY")
# Flask App
flask_app = Flask(__name__)
CORS(flask_app)

def get_current_location():
    global point, address
    current_location = geocoder.ip("me")
    if current_location.latlng:
        point = current_location.latlng
        address = current_location.address


def create_map():
    global point
    get_current_location()
    map_obj = folium.Map(location=point, zoom_start=12, control_scale=True)
    point = [-91, -181]
    folium.LatLngPopup().add_to(map_obj)
    map_file = os.path.abspath("interactive_map.html")
    map_obj.save(map_file)
    global web_view
    web_view = QWebEngineView()
    web_view.load(QUrl.fromLocalFile(map_file))
    change_map(map_file, [])
    return web_view


def update_location_label(latitude, longitude):
    global location_label
    location_label.setText(f"Selected Location: Latitude={latitude}, Longitude={longitude}")


def confirm_location():
    if point[0] != -91 and point[1] != -181:
        global location_label, flask_thread
        location_label.setText(f"Selected Location: {point}")
        try:
            global window

            window.download_window = DownloadDialog()
            window.download_window.show()
            window.close()

            if get_weather_data_api(point[0], point[1]):
                address = reverse_geocoding(point[0], point[1])
                if address is not None:
                    window.download_window.close()
                    window.weather_data_selector_screen = WeatherDataSelector(address)
                    window.weather_data_selector_screen.show()

        except Exception as e:
            print(e)


def get_address_suggestion(address):
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={address}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        result = []
        for r in response.json().get("predictions", []):
            result.append(r['description'])
        global address_suggestion
        address_suggestion.show()
        address_suggestion.clear()
        address_suggestion.addItems(result)

def reverse_geocoding(lat, long):
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'latlng': f'{lat},{long}',  # Latitude and Longitude
        'key': API_KEY  # Your Google API Key
    }
    response = requests.get(url, params=params)
    result = response.json()

    if response.status_code == 200 and result['status'] == 'OK':
        # Get the formatted address from the response
        formatted_address = result['results'][0]['address_components']
        for component in result['results'][0]['address_components']:
            if 'locality' in component['types']:
                return component['long_name']  # Return the city name
        return "City not found."
    else:
        return None

def get_geocode_from_address(address):
    address = address.text()
    global search_box
    search_box.setText(address)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        geocode = response.json().get("results", [])[0]['geometry']['location']
        lat, long = round(geocode['lat'], 6), round(geocode['lng'], 6)
        update_location_label(lat, long)
        global address_suggestion
        address_suggestion.hide()
        map_file = os.path.abspath("interactive_map.html")
        change_map(map_file, [lat, long])
        try:
            global web_view, point
            point = [lat, long]
            web_view.reload()
        except Exception as e:
            print(e)

@flask_app.route('/receive-coordinates', methods=['POST'])
def receive_coordinates():
    global location_label, point
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    point = [latitude, longitude]
    location_label.setText(f"Selected: Latitude:{latitude}, Longitude:{longitude}")
    return jsonify({"status": "success", "message": "Coordinates received."})


class FlaskThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        flask_app.run(debug=False, use_reloader=False)


if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Interactive Dashboard with Location Selector")
    window.setGeometry(100, 100, 1200, 800)

    # Main Widget and Layout
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout()

    # Title Label
    title_label = QLabel("Select Your Location")
    title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
    layout.addWidget(title_label)

    #Search Box
    search_box = QLineEdit()
    search_box.setPlaceholderText("Enter your address...")
    search_box.textChanged.connect(lambda: get_address_suggestion(search_box.text()))
    layout.addWidget(search_box)

    address_suggestion = QListWidget()
    address_suggestion.hide()
    address_suggestion.itemClicked.connect(get_geocode_from_address)
    layout.addWidget(address_suggestion)

    # Interactive Map
    map_view = create_map()
    layout.addWidget(map_view)

    # Selected Location Label
    location_label = QLabel("Selected Location: None")
    layout.addWidget(location_label)

    # Confirm Button
    confirm_button = QPushButton("Confirm Location")
    confirm_button.clicked.connect(confirm_location)
    layout.addWidget(confirm_button)

    central_widget.setLayout(layout)

    screen_geometry = QDesktopWidget().availableGeometry()
    window_geometry = window.frameGeometry()
    center_point = screen_geometry.center()
    window_geometry.moveCenter(center_point)
    window.move(window_geometry.topLeft())

    window.show()
    sys.exit(app.exec_())

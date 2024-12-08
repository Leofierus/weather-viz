import json
import os
import sys
import folium
import geocoder
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QLineEdit, QListWidget
from threading import Thread
from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtWebEngineWidgets import *
from flask import Flask, request, jsonify
from flask_cors import CORS


location_label = None
address = ""
point = [0, 0]
API_KEY = "AIzaSyDSOpaa8Kp1ddWDhUPwwEmHxiYgLFPd-UY"

# Flask App
flask_app = Flask(__name__)
CORS(flask_app)

def get_current_location():
    global point, address
    current_location = geocoder.ip("me")
    if current_location.latlng:
        point = current_location.latlng
        address = current_location.address


def find_map_variable_name(html, pattern):
    starting_index = html.find(pattern) + 4
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index
    return html[starting_index:ending_index]


def find_popup_variable_name(html):
    pattern = "var lat_lng"
    starting_index = html.find(pattern) + 4
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index
    return html[starting_index:ending_index]


def custom_code(popup_variable_name, map_variable_name):
    return f'''
        // custom code
        let currentMarker = null;

        function latLngPop(e) {{
            {popup_variable_name}
            let map = {map_variable_name};
            if(currentMarker){{
                map.removeLayer(currentMarker);
            }}

            currentMarker = L.marker(
                [e.latlng.lat, e.latlng.lng],
                {{}}
            ).addTo(map);
            sendLatLng(e.latlng.lat, e.latlng.lng);
        }}
        
        

        function sendLatLng(latitude, longitude) {{

            // Create the data payload
            const data = {{ latitude: parseFloat(latitude), longitude: parseFloat(longitude) }};

            // Send data to Flask server
            fetch('http://127.0.0.1:5000/receive-coordinates', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify(data),
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Response from Flask:', result);
            }})
            .catch(error => {{
                console.error('Error:', error);
                alert('Failed to send coordinates.');
            }});
        }}
    '''


def find_popup_slice(html):
    pattern = "function latLngPop(e)"
    starting_index = html.find(pattern)
    tmp_html = html[starting_index:]
    found = 0
    index = 0
    opening_found = False
    while not opening_found or found > 0:
        if tmp_html[index] == "{":
            found += 1
            opening_found = True
        elif tmp_html[index] == "}":
            found -= 1

        index += 1
    ending_index = starting_index + index
    return starting_index, ending_index


def create_map():
    global point
    get_current_location()
    map_obj = folium.Map(location=point, zoom_start=12, control_scale=True)
    folium.LatLngPopup().add_to(map_obj)
    map_file = os.path.abspath("interactive_map.html")
    map_obj.save(map_file)
    web_view = QWebEngineView()
    web_view.load(QUrl.fromLocalFile(map_file))

    with open(map_file, 'r') as f:
        html = f.read()

    map_variable_name = find_map_variable_name(html, "var map_")
    popup_variable_name = find_popup_variable_name(html)

    pstart, pend = find_popup_slice(html)

    with open(map_file, 'w') as f:
        f.write(
            html[:pstart] +
            custom_code(popup_variable_name, map_variable_name) +
            html[pend:]
        )

    return web_view


def update_location_label(latitude, longitude):
    global location_label
    location_label.setText(f"Selected Location: Latitude={latitude}, Longitude={longitude}")
    print(latitude, longitude)


def confirm_location():
    global location_label
    location_label.setText(f"Selected Location: {point}")


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
    return None

@flask_app.route('/receive-coordinates', methods=['POST'])
def receive_coordinates():
    global location_label
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    location_label.setText(f"Selected: Latitude:{latitude}, Longitude:{longitude}")
    return jsonify({"status": "success", "message": "Coordinates received."})

def run_flask():
    flask_app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
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
    window.show()
    sys.exit(app.exec_())

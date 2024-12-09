def find_popup_slice(html, pattern):
    starting_index = html.find(pattern)
    tmp_html = html[starting_index:]
    ending_index = starting_index+tmp_html.rfind("}")
    return starting_index, ending_index+1

def custom_code(popup_variable_name, map_variable_name, points):
    part1 = f'''
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
        '''

    part2 = f'''
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

    part3 = f'''
        function addMarker(points){{
            let map = {map_variable_name};
            if(currentMarker){{
                map.removeLayer(currentMarker);
            }}

            currentMarker = L.marker(
                [points[0], points[1]],
                {{}}
            ).addTo(map);
            
            map.setView([points[0], points[1]], 20);
        }}
        addMarker({points});
        '''
    final = part1
    if len(points)>0:
        final += part3
    final+=part2
    return final


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



def change_map(map_file, points):
    with open(map_file, 'r') as f:
        html = f.read()
    map_variable_name = find_map_variable_name(html, "var map_")
    popup_variable_name = find_popup_variable_name(html)
    pattern = "function latLngPop(e)" if len(points) == 0 else "// custom code"
    pstart, pend = find_popup_slice(html, pattern)
    with open(map_file, 'w') as f:
        f.write(
            html[:pstart] +
            custom_code(popup_variable_name, map_variable_name, points) +
            html[pend:]
        )

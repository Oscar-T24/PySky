from flask import Flask, render_template_string, request, url_for

app = Flask(__name__)

@app.route("/")
def map():
    # ... (the code that generates the map)
    # Save the map to a temporary file and get the HTML as a string
    tmp_file = "tmp_map.html"
    with open(tmp_file, "r") as f:
        map_html = f.read()
    # Generate the URL for the remote favicon
    favicon_url = "http://93.14.22.225/favicon.ico"
    # Return the HTML string with the favicon link tag and the script tag for location retrieval
    return render_template_string(
    f"<html><head><link rel='shortcut icon' href='{favicon_url}'>"
    f"<script>"
    f"function getLocation() {{"
    f"if (navigator.geolocation) {{"
    f"navigator.geolocation.getCurrentPosition(sendLocation);"
    f"}} else {{"
    f"alert('Geolocation is not supported by this browser.');"
    f"}}"
    f"}}"
    f"function sendLocation(position) {{"
    f"var lat = position.coords.latitude;"
    f"var lng = position.coords.longitude;"
    f"var xhr = new XMLHttpRequest();"
    f"xhr.open('POST', '{url_for('location')}');"
    f"xhr.setRequestHeader('Content-Type', 'application/json');"
    f"xhr.send(JSON.stringify({{ 'lat': lat, 'lng': lng }}));"
    f"document.getElementById('location').innerHTML = 'Location: ' + lat + ', ' + lng;"
    f"}}"
    f"</script>"
    f"</head><body onload='getLocation()'><div id='location'></div>{map_html}</body></html>"
)

@app.route("/location", methods=["POST"])
def location():
    data = request.get_json()
    lat = data["lat"]
    lng = data["lng"]
    print(f"Received location: {lat}, {lng}")
    return ""


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=4650)

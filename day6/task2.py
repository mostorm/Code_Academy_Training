from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Route Duration Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        h1 { color: #333; }
        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            box-sizing: border-box;
        }
        button {
            margin-top: 20px;
            padding: 10px 20px;
            background: #4285f4;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 16px;
            border-radius: 4px;
        }
        button:hover { background: #3367d6; }
        #result {
            margin-top: 20px;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 4px;
            display: none;
        }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>Route Duration Calculator</h1>

    <form id="routeForm">
        <label for="from_location">From:</label>
        <input type="text" id="from_location" placeholder="e.g. Muscat, Oman" required>

        <label for="to_location">To:</label>
        <input type="text" id="to_location" placeholder="e.g. Nizwa, Oman" required>

        <button type="submit">Get Travel Time</button>
    </form>

    <div id="result"></div>

    <script>
        document.getElementById('routeForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = 'Calculating...';

            const data = {
                from_location: document.getElementById('from_location').value.trim(),
                to_location: document.getElementById('to_location').value.trim()
            };

            try {
                const response = await fetch('/get-route', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (!response.ok || result.error) {
                    resultDiv.innerHTML = '<span class="error">Error: ' + (result.error || 'Unknown error') + '</span>';
                    return;
                }

                resultDiv.innerHTML =
                    '<strong>From:</strong> ' + result.from + '<br>' +
                    '<strong>To:</strong> ' + result.to + '<br>' +
                    '<strong>Distance:</strong> ' + (result.distance_meters / 1000).toFixed(2) + ' km<br>' +
                    '<strong>Estimated Travel Time (Drive):</strong> ' + result.duration;
            } catch (err) {
                resultDiv.innerHTML = '<span class="error">Request failed: ' + err.message + '</span>';
            }
        });
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

def geocode(address):
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing in environment variables")

    resp = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json",
        params={"address": address, "key": API_KEY},
        timeout=10
    )
    resp.raise_for_status()

    data = resp.json()
    print("Geocode response for", address, ":", data)

    status = data.get("status")

    if status != "OK":
        error_message = data.get("error_message", "Unknown geocoding error")
        raise ValueError(f"Geocoding failed for '{address}': {status} - {error_message}")

    results = data.get("results", [])
    if not results:
        raise ValueError(f"No results found for '{address}'")

    location = results[0]["geometry"]["location"]
    return {
        "lat": location["lat"],
        "lng": location["lng"],
        "name": results[0]["formatted_address"]
    }


def format_duration(duration_value):
    """
    Convert Google duration like '123s' into readable text.
    """
    if not duration_value or not isinstance(duration_value, str) or not duration_value.endswith("s"):
        return duration_value

    duration_seconds = int(duration_value[:-1])

    minutes, seconds = divmod(duration_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


@app.route("/get-route", methods=["POST"])
def get_route():
    try:
        if not API_KEY:
            return jsonify({"error": "GOOGLE_API_KEY is not set"}), 500

        data = request.get_json(silent=True)
        print("Received data:", data)

        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        from_location = str(data.get("from_location", "")).strip()
        to_location = str(data.get("to_location", "")).strip()

        if not from_location or not to_location:
            return jsonify({"error": "Both from and to locations are required"}), 400

        from_geo = geocode(from_location)
        if not from_geo:
            return jsonify({"error": f"Could not find location: {from_location}"}), 400

        to_geo = geocode(to_location)
        if not to_geo:
            return jsonify({"error": f"Could not find location: {to_location}"}), 400

        payload = {
            "origin": {
                "location": {
                    "latLng": {
                        "latitude": from_geo["lat"],
                        "longitude": from_geo["lng"]
                    }
                }
            },
            "destination": {
                "location": {
                    "latLng": {
                        "latitude": to_geo["lat"],
                        "longitude": to_geo["lng"]
                    }
                }
            },
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_AWARE",
            "computeAlternativeRoutes": False,
            "routeModifiers": {
                "avoidTolls": False,
                "avoidHighways": False,
                "avoidFerries": False
            },
            "languageCode": "en-US",
            "units": "METRIC"
        }

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
        }

        resp = requests.post(
            "https://routes.googleapis.com/directions/v2:computeRoutes",
            json=payload,
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()

        result = resp.json()
        print("Google Routes response:", result)

        routes = result.get("routes", [])
        if not routes:
            return jsonify({"error": "No routes returned by Google Routes API"}), 502

        route = routes[0]
        duration_str = format_duration(route.get("duration"))

        return jsonify({
            "from": from_geo["name"],
            "to": to_geo["name"],
            "distance_meters": route.get("distanceMeters"),
            "duration": duration_str
        })

    except requests.exceptions.HTTPError as e:
        error_text = ""
        if e.response is not None:
            try:
                error_text = e.response.text
            except Exception:
                error_text = str(e)
        return jsonify({"error": f"Google API HTTP error: {error_text or str(e)}"}), 502

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 502

    except ValueError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
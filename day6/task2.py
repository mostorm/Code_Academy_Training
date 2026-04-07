from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Route Duration Calculator</title>
    <link rel="icon" href="https://www.google.com/favicon.ico" type="image/x-icon">
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #eaf4ff 0%, #f7fbff 50%, #eef7f2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            color: #1f2937;
        }

        .container {
            width: 100%;
            max-width: 760px;
        }

        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 22px;
            padding: 32px;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
        }

        .header {
            margin-bottom: 24px;
        }

        .badge {
            display: inline-block;
            padding: 8px 14px;
            border-radius: 999px;
            background: #e8f0fe;
            color: #1a73e8;
            font-size: 13px;
            font-weight: bold;
            margin-bottom: 14px;
        }

        h1 {
            margin: 0 0 10px;
            font-size: 34px;
            line-height: 1.2;
            color: #111827;
        }

        .subtitle {
            margin: 0;
            color: #6b7280;
            font-size: 16px;
            line-height: 1.6;
        }

        form {
            margin-top: 28px;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
        }

        label {
            margin-bottom: 8px;
            font-weight: bold;
            color: #374151;
            font-size: 14px;
        }

        input {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #d1d5db;
            border-radius: 14px;
            font-size: 15px;
            outline: none;
            transition: all 0.2s ease;
            background: #ffffff;
        }

        input:focus {
            border-color: #4285f4;
            box-shadow: 0 0 0 4px rgba(66, 133, 244, 0.12);
        }

        .actions {
            display: flex;
            gap: 12px;
            margin-top: 22px;
            flex-wrap: wrap;
        }

        button {
            border: none;
            border-radius: 14px;
            padding: 14px 20px;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .primary-btn {
            background: linear-gradient(135deg, #4285f4, #3367d6);
            color: white;
            box-shadow: 0 10px 20px rgba(66, 133, 244, 0.2);
        }

        .primary-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 14px 24px rgba(66, 133, 244, 0.28);
        }

        .secondary-btn {
            background: #f3f4f6;
            color: #374151;
        }

        .secondary-btn:hover {
            background: #e5e7eb;
        }

        #result {
            margin-top: 28px;
            display: none;
        }

        .result-card {
            border-radius: 18px;
            padding: 22px;
            background: #f8fbff;
            border: 1px solid #dbeafe;
        }

        .result-title {
            margin: 0 0 16px;
            font-size: 20px;
            color: #111827;
        }

        .result-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
            margin-top: 14px;
        }

        .result-item {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 14px;
        }

        .result-label {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #6b7280;
            margin-bottom: 6px;
            font-weight: bold;
        }

        .result-value {
            font-size: 16px;
            color: #111827;
            word-break: break-word;
        }

        .error-box {
            background: #fff1f2;
            border: 1px solid #fecdd3;
            color: #b42318;
            border-radius: 16px;
            padding: 16px;
            font-weight: bold;
        }

        .success-box {
            background: #ecfdf3;
            border: 1px solid #abefc6;
            color: #067647;
            border-radius: 16px;
            padding: 14px 16px;
            font-weight: bold;
            margin-bottom: 14px;
        }

        .spinner-wrap {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #374151;
            font-weight: bold;
        }

        .spinner {
            width: 22px;
            height: 22px;
            border: 3px solid #d1d5db;
            border-top: 3px solid #4285f4;
            border-radius: 50%;
            animation: spin 0.9s linear infinite;
            flex-shrink: 0;
        }

        .footer-note {
            margin-top: 18px;
            font-size: 13px;
            color: #6b7280;
            text-align: center;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @media (max-width: 700px) {
            .card {
                padding: 22px;
                border-radius: 18px;
            }

            h1 {
                font-size: 28px;
            }

            .grid,
            .result-grid {
                grid-template-columns: 1fr;
            }

            .actions {
                flex-direction: column;
            }

            button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header">
                <div class="badge">Google Routes API</div>
                <h1>Route Duration Calculator 🚗</h1>
                <p class="subtitle">
                    Enter your starting point and destination to get estimated driving time and route distance.
                </p>
            </div>

            <form id="routeForm" autocomplete="off">
                <div class="grid">
                    <div class="input-group">
                        <label for="from_location">From</label>
                        <input type="text" id="from_location" placeholder="e.g. Muscat, Oman" required>
                    </div>

                    <div class="input-group">
                        <label for="to_location">To</label>
                        <input type="text" id="to_location" placeholder="e.g. Nizwa, Oman" required>
                    </div>
                </div>

                <div class="actions">
                    <button type="submit" class="primary-btn">Get Travel Time</button>
                    <button type="button" class="secondary-btn" id="swapBtn">Swap</button>
                    <button type="button" class="secondary-btn" id="resetBtn">Reset</button>
                </div>
            </form>

            <div id="result"></div>

            <div class="footer-note">
                Drive with purpose, arrive with patience.
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('routeForm');
        const resultDiv = document.getElementById('result');
        const fromInput = document.getElementById('from_location');
        const toInput = document.getElementById('to_location');
        const resetBtn = document.getElementById('resetBtn');
        const swapBtn = document.getElementById('swapBtn');

        function showLoading() {
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <div class="result-card">
                    <div class="spinner-wrap">
                        <div class="spinner"></div>
                        <span>Calculating route, please wait...</span>
                    </div>
                </div>
            `;
        }

        function showError(message) {
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <div class="error-box">
                    ❌ ${message}
                </div>
            `;
        }

        function showResult(data) {
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <div class="result-card">
                    <div class="success-box">✔ Route found successfully</div>
                    <h2 class="result-title">Trip Summary</h2>

                    <div class="result-grid">
                        <div class="result-item">
                            <div class="result-label">From</div>
                            <div class="result-value">${data.from}</div>
                        </div>

                        <div class="result-item">
                            <div class="result-label">To</div>
                            <div class="result-value">${data.to}</div>
                        </div>

                        <div class="result-item">
                            <div class="result-label">Distance</div>
                            <div class="result-value">${data.distance_km} km</div>
                        </div>

                        <div class="result-item">
                            <div class="result-label">Estimated Drive Time</div>
                            <div class="result-value">${data.duration}</div>
                        </div>
                    </div>
                </div>
            `;
        }

        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            const from_location = fromInput.value.trim();
            const to_location = toInput.value.trim();

            if (!from_location || !to_location) {
                showError('Both locations are required.');
                return;
            }

            showLoading();

            try {
                const response = await fetch('/get-route', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ from_location, to_location })
                });

                const result = await response.json();

                if (!response.ok || result.error) {
                    showError(result.error || 'Unknown error occurred.');
                    return;
                }

                showResult(result);

            } catch (error) {
                showError('Request failed: ' + error.message);
            }
        });

        resetBtn.addEventListener('click', function() {
            fromInput.value = '';
            toInput.value = '';
            resultDiv.style.display = 'none';
            resultDiv.innerHTML = '';
            fromInput.focus();
        });

        swapBtn.addEventListener('click', function() {
            const temp = fromInput.value;
            fromInput.value = toInput.value;
            toInput.value = temp;
        });
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


def format_duration(duration_value):
    """
    Convert duration returned by Google like '3661s' into '1h 1m 1s'
    """
    if not duration_value or not isinstance(duration_value, str) or not duration_value.endswith("s"):
        return duration_value

    try:
        total_seconds = int(duration_value[:-1])
    except ValueError:
        return duration_value

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)


@app.route("/get-route", methods=["POST"])
def get_route():
    try:
        if not API_KEY:
            return jsonify({"error": "GOOGLE_API_KEY is not set in your .env file"}), 500

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        from_location = str(data.get("from_location", "")).strip()
        to_location = str(data.get("to_location", "")).strip()

        if not from_location or not to_location:
            return jsonify({"error": "Both from and to locations are required"}), 400

        payload = {
            "origin": {
                "address": from_location
            },
            "destination": {
                "address": to_location
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
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
        }

        response = requests.post(
            "https://routes.googleapis.com/directions/v2:computeRoutes",
            json=payload,
            headers=headers,
            timeout=15
        )

        if response.status_code != 200:
            try:
                api_error = response.json()
            except Exception:
                api_error = {"error": response.text}
            return jsonify({
                "error": f"Google Routes API error: {api_error}"
            }), 502

        result = response.json()
        routes = result.get("routes", [])

        if not routes:
            return jsonify({"error": "No routes were returned by Google Routes API"}), 502

        route = routes[0]
        distance_meters = route.get("distanceMeters", 0)
        duration_raw = route.get("duration", "")

        return jsonify({
            "from": from_location,
            "to": to_location,
            "distance_meters": distance_meters,
            "distance_km": f"{distance_meters / 1000:.2f}",
            "duration": format_duration(duration_raw)
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network/request error: {str(e)}"}), 502

    except Exception as e:
        return jsonify({"error": f"Unexpected server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
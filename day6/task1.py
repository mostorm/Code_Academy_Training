from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
import uvicorn
import pycountry

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nationality Predictor</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                padding-top: 80px;
            }
            .container {
                max-width: 550px;
                width: 90%;
            }
            h1 {
                font-size: 2.2rem;
                margin-bottom: 8px;
                text-align: center;
            }
            .subtitle {
                text-align: center;
                color: #aaa;
                margin-bottom: 30px;
                font-size: 0.95rem;
            }
            .search-box {
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
            }
            input {
                flex: 1;
                padding: 14px 18px;
                font-size: 16px;
                border: none;
                border-radius: 12px;
                background: rgba(255,255,255,0.1);
                color: #fff;
                outline: none;
                transition: background 0.3s;
            }
            input::placeholder { color: #888; }
            input:focus { background: rgba(255,255,255,0.18); }
            button {
                padding: 14px 24px;
                font-size: 16px;
                border: none;
                border-radius: 12px;
                background: #6c63ff;
                color: #fff;
                cursor: pointer;
                transition: background 0.3s, transform 0.1s;
            }
            button:hover { background: #5a52d5; }
            button:active { transform: scale(0.97); }
            .loading { text-align: center; color: #aaa; margin-top: 20px; }
            .result-card {
                background: rgba(255,255,255,0.07);
                border-radius: 14px;
                padding: 20px;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                gap: 16px;
                transition: transform 0.2s;
            }
            .result-card:hover { transform: translateY(-2px); }
            .flag img { width: 48px; height: 36px; border-radius: 4px; object-fit: cover; }
            .info { flex: 1; }
            .country-name { font-size: 1.15rem; font-weight: 600; }
            .country-code { color: #aaa; font-size: 0.85rem; }
            .prob-bar-bg {
                margin-top: 8px;
                height: 8px;
                background: rgba(255,255,255,0.1);
                border-radius: 4px;
                overflow: hidden;
            }
            .prob-bar {
                height: 100%;
                border-radius: 4px;
                background: linear-gradient(90deg, #6c63ff, #48c6ef);
                transition: width 0.6s ease;
            }
            .prob-text {
                margin-top: 4px;
                font-size: 0.85rem;
                color: #ccc;
            }
            .result-title {
                text-align: center;
                margin-bottom: 16px;
                font-size: 1.1rem;
                color: #ccc;
            }
            .no-results {
                text-align: center;
                color: #aaa;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌍 Nationality Predictor</h1>
            <p class="subtitle">Enter a name to predict its nationality</p>
            <div class="search-box">
                <input type="text" id="name" placeholder="e.g. Juma, Mohamed, Yuki..." autofocus />
                <button onclick="search()">Search</button>
            </div>
            <div id="results"></div>
        </div>
        <script>
            function countryCodeToFlag(code) {
                return `<img src="https://flagcdn.com/w80/${code.toLowerCase()}.png" alt="${code}" />`;
            }

            document.getElementById('name').addEventListener('keydown', e => {
                if (e.key === 'Enter') search();
            });

            async function search() {
                const nameInput = document.getElementById('name');
                const name = nameInput.value.trim();
                if (!name) return;

                const results = document.getElementById('results');
                results.innerHTML = '<div class="loading">Searching...</div>';

                const res = await fetch(`/nationalize?name=${encodeURIComponent(name)}`);
                const data = await res.json();

                if (data.country && data.country.length > 0) {
                    let html = `<div class="result-title">Results for <strong>${data.name}</strong></div>`;
                    data.country.forEach(c => {
                        const pct = (c.probability * 100).toFixed(1);
                        const flag = countryCodeToFlag(c.country_id);
                        html += `
                        <div class="result-card">
                            <div class="flag">${flag}</div>
                            <div class="info">
                                <div class="country-name">${c.country_name}</div>
                                <div class="country-code">${c.country_id}</div>
                                <div class="prob-bar-bg"><div class="prob-bar" style="width:${pct}%"></div></div>
                                <div class="prob-text">${pct}% probability</div>
                            </div>
                        </div>`;
                    });
                    results.innerHTML = html;
                } else {
                    results.innerHTML = '<div class="no-results">No results found for that name.</div>';
                }
            }
        </script>
    </body>
    </html>
    """


@app.get("/nationalize")
async def get_nationality(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.nationalize.io/?name={name}")
        data = response.json()
        for country in data.get("country", []):
            c = pycountry.countries.get(alpha_2=country["country_id"])
            country["country_name"] = c.name if c else country["country_id"]
        return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

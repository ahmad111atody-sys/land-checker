import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

SCRAPER_API_KEY = "b1cf9fea0ea7c6f530598b1bb88a5776"

@app.route("/check_land")
def check_land():
    project = request.args.get("project")
    url = f"https://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url=https://sakani.sa/app/land-projects/{project}"

    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        return jsonify({"error": f"fetch_failed: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

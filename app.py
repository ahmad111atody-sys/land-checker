from flask import Flask, request
import os
import requests

app = Flask(__name__)

SCRAPER_KEY = os.environ.get("SCRAPER_API_KEY")  # ضع المفتاح في متغير البيئة داخل Render

@app.route("/check_land")
def check_land():
    url = request.args.get("url")
    if not url:
        return {"error": "missing url param"}, 400

    # استخدام ScraperAPI لتجاوز الحظر
    api_url = f"http://api.scraperapi.com?api_key={SCRAPER_KEY}&url={url}&render=true"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        resp = requests.get(api_url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/")
def home():
    return "Land Checker is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

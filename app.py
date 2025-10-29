# app.py
from flask import Flask, request, jsonify
import os
import requests

# cloudscraper يساعد بتجاوز بعض حمايات Cloudflare
try:
    import cloudscraper
except Exception:
    cloudscraper = None

app = Flask(__name__)

# متغير بيئة اختياري للبروكسي (مثال: http://user:pass@1.2.3.4:8080)
PROXY = os.environ.get("PROXY")

def get_with_proxy(url):
    if PROXY:
        proxies = {"http": PROXY, "https": PROXY}
        return requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, proxies=proxies, timeout=25)
    else:
        return requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=25)

@app.route("/check_land")
def check_land():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "missing url parameter"}), 400

    # حاول cloudscraper أولاً (لو متوفر)
    if cloudscraper:
        try:
            scraper = cloudscraper.create_scraper()
            resp = scraper.get(url, timeout=30)
            return resp.text, resp.status_code, {'Content-Type': 'text/html; charset=utf-8'}
        except Exception as e_cs:
            # استمر للتجربة بالـ requests
            cs_err = str(e_cs)
    else:
        cs_err = "cloudscraper not installed"

    # محاولة fallback بواسطة requests (ومع البروكسي لو موجود)
    try:
        resp = get_with_proxy(url)
        return resp.text, resp.status_code, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e_req:
        return jsonify({
            "error": "both methods failed",
            "cloudscraper_error": cs_err,
            "requests_error": str(e_req)
        }), 500

@app.route("/")
def home():
    return "Sakani Land Checker is running ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

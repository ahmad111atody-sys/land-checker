#!/usr/bin/env python3
# Land Checker (Alobstan + Nakhlan)
# يعرض القطع الملغاة فقط مع روابطها

from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests, os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# مفتاح ScraperAPI (تقدر تعدله)
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY", "YOUR_SCRAPER_API_KEY")

# روابط مخطط البستان
alobstan_links = [
    "https://sakani.sa/app/units/765316",
    "https://sakani.sa/app/units/765453",
    "https://sakani.sa/app/units/765499",
    "https://sakani.sa/app/units/765587",
    "https://sakani.sa/app/units/765778",
    "https://sakani.sa/app/units/765515",
    "https://sakani.sa/app/units/765448",
    "https://sakani.sa/app/units/765595",
    "https://sakani.sa/app/units/765598",
    "https://sakani.sa/app/units/765205",
]

# روابط مخطط نخلان
nakhlan_links = [
    "https://sakani.sa/app/units/797389",
    "https://sakani.sa/app/units/797400",
    "https://sakani.sa/app/units/797412",
    "https://sakani.sa/app/units/797420",
    "https://sakani.sa/app/units/797436",
    "https://sakani.sa/app/units/797460",
    "https://sakani.sa/app/units/797473",
    "https://sakani.sa/app/units/797482",
    "https://sakani.sa/app/units/797490",
    "https://sakani.sa/app/units/797498",
]

# ---- دالة الفحص ----
def fetch_land(url, timeout=25):
    try:
        api_key = SCRAPER_API_KEY
        api_url = f"http://api.scraperapi.com/?api_key={api_key}&url={url}"
        resp = requests.get(api_url, timeout=timeout)

        if resp.status_code != 200:
            return {"error": "fetch_failed", "status_code": resp.status_code, "url": url}

        soup = BeautifulSoup(resp.text, "html.parser")
        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else "غير معروف"

        return {"url": url, "title": title, "status": "success"}

    except Exception as e:
        return {"error": str(e), "url": url}


# ---- المسارات ----

@app.route("/")
def home():
    return jsonify({"status": "running", "message": "Land checker is online ✅"})


@app.route("/check_all", methods=["GET"])
def check_all():
    cancelled = []
    total = 0

    for u in alobstan_links + nakhlan_links:
        res = fetch_land(u)
        total += 1
        if "error" in res or res.get("status_code") == 404:
            cancelled.append(u)

    return jsonify({
        "cancelled_units": cancelled,
        "total_checked": total
    })


@app.route("/check_alobstan", methods=["GET"])
def check_alobstan():
    cancelled = []
    total = 0

    for u in alobstan_links:
        res = fetch_land(u)
        total += 1
        if "error" in res or res.get("status_code") == 404:
            cancelled.append(u)

    return jsonify({
        "cancelled_units": cancelled,
        "total_checked": total
    })


@app.route("/check_nakhlan", methods=["GET"])
def check_nakhlan():
    cancelled = []
    total = 0

    for u in nakhlan_links:
        res = fetch_land(u)
        total += 1
        if "error" in res or res.get("status_code") == 404:
            cancelled.append(u)

    return jsonify({
        "cancelled_units": cancelled,
        "total_checked": total
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

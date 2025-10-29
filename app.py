#!/usr/bin/env python3
# combined_sakani_checker.py
# 🔹 فحص مخططات سكني (البستان + النخلان + النشطة)

from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import os

# إعداد Flask
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # عرض النصوص العربية بدون ترميز

# مفتاح ScraperAPI (إذا عندك)
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
    "https://sakani.sa/app/units/765577",
    "https://sakani.sa/app/units/765205"
]

# روابط مخطط نخلان
nakhlan_links = [
    "https://sakani.sa/app/units/797389",
    "https://sakani.sa/app/units/797400",
    "https://sakani.sa/app/units/797412",
    "https://sakani.sa/app/units/797420",
    "https://sakani.sa/app/units/797431",
    "https://sakani.sa/app/units/797440",
    "https://sakani.sa/app/units/797456",
    "https://sakani.sa/app/units/797468"
]

# روابط القطع النشطة من active_units.txt
active_units_links = [
    # أضف روابطك هنا لاحقاً لو عندك ملف active_units
]


# دالة الفحص الرئيسية
def fetch_land(url, timeout=30):
    try:
        api_key = SCRAPER_API_KEY
        if api_key and api_key != "YOUR_SCRAPER_API_KEY":
            api_url = f"http://api.scraperapi.com/?api_key={api_key}&url={url}"
            resp = requests.get(api_url, timeout=timeout)
        else:
            resp = requests.get(url, timeout=timeout)

        if resp.status_code != 200:
            return {"error": "fetch_failed", "status_code": resp.status_code, "url": url}

        soup = BeautifulSoup(resp.text, "html.parser")
        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else "غير معروف"

        project_id = url.split("/")[-1]
        return {"project": project_id, "status": "success", "title": title, "url": url}

    except requests.Timeout:
        return {"error": "timeout", "url": url}
    except Exception as e:
        return {"error": str(e), "url": url}


@app.route("/")
def home():
    return jsonify({"status": "running", "message": "Land checker is online ✅"})


# ✅ فحص البستان فقط
@app.route("/check_alobstan", methods=["GET"])
def check_alobstan():
    results = []
    for u in alobstan_links:
        results.append(fetch_land(u))
    return jsonify(results)


# ✅ فحص نخلان فقط
@app.route("/check_nakhlan", methods=["GET"])
def check_nakhlan():
    results = []
    for u in nakhlan_links:
        results.append(fetch_land(u))
    return jsonify(results)


# ✅ فحص القطع النشطة فقط
@app.route("/check_active", methods=["GET"])
def check_active():
    results = []
    for u in active_units_links:
        results.append(fetch_land(u))
    return jsonify(results)


# ✅ فحص شامل (البستان + نخلان + النشطة)
@app.route("/check_all", methods=["GET"])
def check_all():
    results = {"alobstan": [], "nakhlan": [], "active_units": []}
    for u in alobstan_links:
        results["alobstan"].append(fetch_land(u))
    for u in nakhlan_links:
        results["nakhlan"].append(fetch_land(u))
    for u in active_units_links:
        results["active_units"].append(fetch_land(u))
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

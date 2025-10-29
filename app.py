#!/usr/bin/env python3
# combined_sakani_checker.py
# Flask app with two link lists (alobstan and active_units) and helper functions
# Put your SCRAPER_API_KEY here (or set via environment variable)
SCRAPER_API_KEY = "YOUR_SCRAPER_API_KEY"

from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # عرض النصوص العربية بدون ترميز

# روابط البستان - (alobstan)
alobstan_links = ['https://sakani.sa/app/units/765316', 'https://sakani.sa/app/units/765453', 'https://sakani.sa/app/units/765499', 'https://sakani.sa/app/units/765587', 'https://sakani.sa/app/units/765578', 'https://sakani.sa/app/units/765515', 'https://sakani.sa/app/units/765448', 'https://sakani.sa/app/units/765595', 'https://sakani.sa/app/units/765598', 'https://sakani.sa/app/units/765577', 'https://sakani.sa/app/units/765205']

# روابط القطع النشطة (active_units) - تم تحميلها من active_units.txt
active_units_links = ['https://sakani.sa/app/units/797389', 'https://sakani.sa/app/units/800166', 'https://sakani.sa/app/units/800156', 'https://sakani.sa/app/units/800172', 'https://sakani.sa/app/units/800447', 'https://sakani.sa/app/units/800852', 'https://sakani.sa/app/units/800461', 'https://sakani.sa/app/units/800864', 'https://sakani.sa/app/units/798696', 'https://sakani.sa/app/units/798492', 'https://sakani.sa/app/units/798670', 'https://sakani.sa/app/units/799388', 'https://sakani.sa/app/units/797991', 'https://sakani.sa/app/units/800036', 'https://sakani.sa/app/units/798941', 'https://sakani.sa/app/units/797197', 'https://sakani.sa/app/units/798722', 'https://sakani.sa/app/units/799382', 'https://sakani.sa/app/units/798478', 'https://sakani.sa/app/units/798459', 'https://sakani.sa/app/units/800062', 'https://sakani.sa/app/units/800859', 'https://sakani.sa/app/units/800868', 'https://sakani.sa/app/units/798495', 'https://sakani.sa/app/units/796400', 'https://sakani.sa/app/units/798527', 'https://sakani.sa/app/units/797931', 'https://sakani.sa/app/units/798357', 'https://sakani.sa/app/units/798871', 'https://sakani.sa/app/units/800133', 'https://sakani.sa/app/units/800446', 'https://sakani.sa/app/units/798950', 'https://sakani.sa/app/units/800928', 'https://sakani.sa/app/units/797830', 'https://sakani.sa/app/units/797247', 'https://sakani.sa/app/units/797638', 'https://sakani.sa/app/units/797800', 'https://sakani.sa/app/units/798516', 'https://sakani.sa/app/units/799053', 'https://sakani.sa/app/units/799256', 'https://sakani.sa/app/units/800270', 'https://sakani.sa/app/units/797836', 'https://sakani.sa/app/units/800117', 'https://sakani.sa/app/units/798280', 'https://sakani.sa/app/units/798847', 'https://sakani.sa/app/units/799836', 'https://sakani.sa/app/units/798056', 'https://sakani.sa/app/units/800662', 'https://sakani.sa/app/units/799374', 'https://sakani.sa/app/units/800628', 'https://sakani.sa/app/units/797892', 'https://sakani.sa/app/units/796639', 'https://sakani.sa/app/units/799974', 'https://sakani.sa/app/units/797069', 'https://sakani.sa/app/units/796851', 'https://sakani.sa/app/units/797370', 'https://sakani.sa/app/units/798789', 'https://sakani.sa/app/units/796333', 'https://sakani.sa/app/units/797859', 'https://sakani.sa/app/units/796446', 'https://sakani.sa/app/units/799966', 'https://sakani.sa/app/units/798863', 'https://sakani.sa/app/units/800139', 'https://sakani.sa/app/units/797852', 'https://sakani.sa/app/units/800109', 'https://sakani.sa/app/units/797853', 'https://sakani.sa/app/units/798784', 'https://sakani.sa/app/units/800214', 'https://sakani.sa/app/units/796611', 'https://sakani.sa/app/units/797865', 'https://sakani.sa/app/units/798153', 'https://sakani.sa/app/units/796368', 'https://sakani.sa/app/units/799339', 'https://sakani.sa/app/units/800927', 'https://sakani.sa/app/units/798355', 'https://sakani.sa/app/units/799972', 'https://sakani.sa/app/units/798151', 'https://sakani.sa/app/units/796764', 'https://sakani.sa/app/units/799670', 'https://sakani.sa/app/units/796418', 'https://sakani.sa/app/units/799113', 'https://sakani.sa/app/units/799272', 'https://sakani.sa/app/units/798175', 'https://sakani.sa/app/units/798117', 'https://sakani.sa/app/units/799114', 'https://sakani.sa/app/units/798240', 'https://sakani.sa/app/units/796867', 'https://sakani.sa/app/units/800095', 'https://sakani.sa/app/units/798612', 'https://sakani.sa/app/units/799806', 'https://sakani.sa/app/units/798818', 'https://sakani.sa/app/units/798382', 'https://sakani.sa/app/units/800742', 'https://sakani.sa/app/units/798867', 'https://sakani.sa/app/units/800626', 'https://sakani.sa/app/units/800093', 'https://sakani.sa/app/units/798886', 'https://sakani.sa/app/units/797334', 'https://sakani.sa/app/units/799361', 'https://sakani.sa/app/units/797822', 'https://sakani.sa/app/units/800634', 'https://sakani.sa/app/units/798243', 'https://sakani.sa/app/units/800100', 'https://sakani.sa/app/units/799875', 'https://sakani.sa/app/units/798396', 'https://sakani.sa/app/units/798655', 'https://sakani.sa/app/units/798331', 'https://sakani.sa/app/units/800951', 'https://sakani.sa/app/units/797989', 'https://sakani.sa/app/units/797893', 'https://sakani.sa/app/units/800525', 'https://sakani.sa/app/units/800246', 'https://sakani.sa/app/units/798505', 'https://sakani.sa/app/units/799679', 'https://sakani.sa/app/units/798842', 'https://sakani.sa/app/units/797913', 'https://sakani.sa/app/units/800171', 'https://sakani.sa/app/units/798075', 'https://sakani.sa/app/units/798217', 'https://sakani.sa/app/units/798760', 'https://sakani.sa/app/units/800104', 'https://sakani.sa/app/units/798338', 'https://sakani.sa/app/units/800197', 'https://sakani.sa/app/units/797809', 'https://sakani.sa/app/units/799332', 'https://sakani.sa/app/units/796346', 'https://sakani.sa/app/units/800790', 'https://sakani.sa/app/units/797868', 'https://sakani.sa/app/units/798819', 'https://sakani.sa/app/units/797269', 'https://sakani.sa/app/units/797829', 'https://sakani.sa/app/units/800075', 'https://sakani.sa/app/units/798792', 'https://sakani.sa/app/units/798641', 'https://sakani.sa/app/units/798101', 'https://sakani.sa/app/units/800873', 'https://sakani.sa/app/units/798953', 'https://sakani.sa/app/units/798895', 'https://sakani.sa/app/units/799249', 'https://sakani.sa/app/units/798718', 'https://sakani.sa/app/units/798613', 'https://sakani.sa/app/units/796852', 'https://sakani.sa/app/units/798346', 'https://sakani.sa/app/units/797804', 'https://sakani.sa/app/units/798897', 'https://sakani.sa/app/units/797874', 'https://sakani.sa/app/units/800078', 'https://sakani.sa/app/units/799127', 'https://sakani.sa/app/units/797993', 'https://sakani.sa/app/units/797972', 'https://sakani.sa/app/units/800080', 'https://sakani.sa/app/units/798146', 'https://sakani.sa/app/units/798147', 'https://sakani.sa/app/units/798887', 'https://sakani.sa/app/units/800092', 'https://sakani.sa/app/units/798487', 'https://sakani.sa/app/units/799265', 'https://sakani.sa/app/units/798519', 'https://sakani.sa/app/units/798947', 'https://sakani.sa/app/units/799861', 'https://sakani.sa/app/units/798129', 'https://sakani.sa/app/units/800945', 'https://sakani.sa/app/units/798962', 'https://sakani.sa/app/units/800148', 'https://sakani.sa/app/units/797971', 'https://sakani.sa/app/units/797726', 'https://sakani.sa/app/units/798882', 'https://sakani.sa/app/units/800362', 'https://sakani.sa/app/units/797446', 'https://sakani.sa/app/units/797944', 'https://sakani.sa/app/units/799989', 'https://sakani.sa/app/units/798144', 'https://sakani.sa/app/units/797930', 'https://sakani.sa/app/units/798485', 'https://sakani.sa/app/units/800537', 'https://sakani.sa/app/units/800111', 'https://sakani.sa/app/units/799336', 'https://sakani.sa/app/units/798466', 'https://sakani.sa/app/units/799884', 'https://sakani.sa/app/units/799075', 'https://sakani.sa/app/units/799334', 'https://sakani.sa/app/units/798143', 'https://sakani.sa/app/units/800038', 'https://sakani.sa/app/units/798071', 'https://sakani.sa/app/units/799097', 'https://sakani.sa/app/units/797049', 'https://sakani.sa/app/units/798535', 'https://sakani.sa/app/units/799341', 'https://sakani.sa/app/units/798773']
# روابط مخطط نخلان
nakhlan_links = [
    "https://sakani.sa/app/units/775101",
    "https://sakani.sa/app/units/775102",
    "https://sakani.sa/app/units/775103"
    # أضف باقي روابط نخلان هنا
]
# Helper: use ScraperAPI (or your preferred scraping proxy) to fetch the page HTML
def fetch_land(url, timeout=30):
    try:
        api_key = SCRAPER_API_KEY or os.getenv("SCRAPER_API_KEY")
        if not api_key or api_key == "YOUR_SCRAPER_API_KEY":
            return {"error": "missing_scraper_api_key", "url": url}

        api_url = f"http://api.scraperapi.com/?api_key={api_key}&url={url}"
        resp = requests.get(api_url, timeout=timeout)
        if resp.status_code != 200:
            return {"error": "fetch_failed", "status_code": resp.status_code, "url": url}

        soup = BeautifulSoup(resp.text, "html.parser")
        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else "غير معروف"

        project_id = url.split("/")[-1]
        return {
            "project": project_id,
            "status": "success",
            "title": title,
            "url": url
        }
    except requests.Timeout:
        return {"error": "fetch_failed: connection timed out", "url": url}
    except Exception as e:
        return {"error": f"fetch_failed: {str(e)}", "url": url}

@app.route("/")
def home():
    return jsonify({"status": "running", "message": "Land checker is online ✅"})

# Existing single-check endpoint (compatible with your current script)
@app.route("/check_land", methods=["GET"])
def check_land():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "missing url"}), 400
    result = fetch_land(url)
    if "error" in result:
        return jsonify(result), 403
    return jsonify(result)

# New endpoint: check both lists (alobstan + active_units) and return results
@app.route("/check_all", methods=["GET"])
def check_all():
    results = {"alobstan": [], "active_units": []}
    # check alobstan links
    for u in alobstan_links:
        results["alobstan"].append(fetch_land(u))
    # check active unit links
    for u in active_units_links:
        results["active_units"].append(fetch_land(u))
    return jsonify(results)

# Route to check only active_units (useful if you want separate access)
@app.route("/check_active", methods=["GET"])
def check_active():
    results = []
    for u in active_units_links:
        results.append(fetch_land(u))
    return jsonify(results)

# Route to check only alobstan
@app.route("/check_alobstan", methods=["GET"])
def check_alobstan():
    results = []
    for u in alobstan_links:
        results.append(fetch_land(u))
    return jsonify(results)

if __name__ == "__main__":
    # by default run on port 5000; change host/port as needed
    app.run(host="0.0.0.0", port=5000, debug=False)

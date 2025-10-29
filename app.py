from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

SCRAPER_API_KEY = "b1cf9fea0ea7c6f530598b1bb88a5776"

# روابط مخطط واحة البستان – صبيا
albostan_links = [
    "https://sakani.sa/app/units/765316",
    "https://sakani.sa/app/units/765453",
    "https://sakani.sa/app/units/765499",
    "https://sakani.sa/app/units/765587",
    "https://sakani.sa/app/units/765778",
    "https://sakani.sa/app/units/765515",
    "https://sakani.sa/app/units/765448",
    "https://sakani.sa/app/units/765595",
    "https://sakani.sa/app/units/765598",
    "https://sakani.sa/app/units/765577",
    # ... (باقي الروابط تقدر تضيفها كلها بنفس النمط)
    "https://sakani.sa/app/units/765205"
]


@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Land checker is online ✅"
    })


@app.route('/check_land', methods=['GET'])
def check_land():
    try:
        url = request.args.get("url")
        if not url:
            return jsonify({"error": "missing_url"}), 400

        api_url = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url={url}"
        response = requests.get(api_url, timeout=30)

        if response.status_code != 200:
            return jsonify({
                "error": f"fetch_failed: {response.status_code} for {url}"
            }), 403

        soup = BeautifulSoup(response.text, "html.parser")
        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else "غير معروف"

        project_id = url.split("/")[-1]
        return jsonify({
            "project": project_id,
            "status": "success",
            "title": title
        })

    except requests.Timeout:
        return jsonify({"error": "fetch_failed: connection timed out"}), 504
    except Exception as e:
        return jsonify({"error": f"fetch_failed: {str(e)}"}), 500


@app.route('/check_all', methods=['GET'])
def check_all():
    results = []
    for url in albostan_links:
        try:
            api_url = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url={url}"
            response = requests.get(api_url, timeout=20)
            soup = BeautifulSoup(response.text, "html.parser")
            title_tag = soup.find("title")
            title = title_tag.text.strip() if title_tag else "غير معروف"

            project_id = url.split("/")[-1]
            results.append({
                "project": project_id,
                "status": "success",
                "title": title
            })
        except Exception as e:
            results.append({
                "url": url,
                "error": f"fetch_failed: {str(e)}"
            })
    return jsonify(results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

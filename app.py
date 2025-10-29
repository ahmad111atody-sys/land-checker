from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

SCRAPER_API_KEY = "b1cf9fea0ea7c6f530598b1bb88a5776"

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

        # نستخدم ScraperAPI لتفادي حجب سكني
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

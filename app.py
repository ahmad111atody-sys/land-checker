from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# مفتاح ScraperAPI (من حسابك)
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY", "b1cf9fea0ea7c6f530598b1bb88a5776")

@app.route('/')
def home():
    return "✅ Land Checker is running..."

@app.route('/check_land')
def check_land():
    project = request.args.get('project')
    if not project:
        return jsonify({"error": "missing_project_number"}), 400

    url = f"https://sakani.sa/app/land-projects/{project}"
    proxy_url = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&render=true&url={url}"

    try:
        res = requests.get(proxy_url, timeout=60)
        res.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"fetch_failed: {e}"}), 500

    try:
        soup = BeautifulSoup(res.text, "html.parser")

        # مثال بسيط لاستخراج عنوان المشروع من الصفحة
        title = soup.find("title").get_text(strip=True) if soup.find("title") else "No title found"

        # يقدر هنا تضيف منطق لفحص القطع أو البحث عن "محجوز" أو "متاح"
        return jsonify({
            "project": project,
            "status": "success",
            "title": title
        })

    except Exception as e:
        return jsonify({"error": f"parse_failed: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, request, jsonify
import requests
SCRAPER_API_KEY = "b1cf9fea0ea7c6f530598b1bb88a5776"
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Land checker is running. Use /check_land?project=146"

@app.route("/check_land")
def check_land():
    project = request.args.get("project")
    if not project:
        return jsonify({"error": "missing ?project=ID"}), 400

    url = f"https://sakani.sa/app/land-projects/{project}"

    try:
        r = requests.get(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        r.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"fetch_failed: {str(e)}"}), 500

    soup = BeautifulSoup(r.text, "html.parser")

    # نبحث عن روابط القطع
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/app/units/" in href:
            if href.startswith("http"):
                links.append(href)
            else:
                links.append("https://sakani.sa" + href)

    links = list(set(links))  # إزالة التكرار
    return jsonify({
        "project": project,
        "units_found": len(links),
        "links": links
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

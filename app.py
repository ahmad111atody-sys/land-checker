from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

SCRAPER_API_KEY = "ضع_مفتاحك_هنا"  # ← هنا ضع مفتاح ScraperAPI الخاص بك

@app.route('/')
def home():
    return jsonify({
        "status": "running ✅",
        "usage": "أضف ?project=رقم_المخطط إلى الرابط مثل: /check_land?project=146"
    })

@app.route('/check_land')
def check_land():
    project_id = request.args.get('project')

    if not project_id:
        return jsonify({"error": "يرجى إدخال رقم المشروع مثل: /check_land?project=146"}), 400

    try:
        # رابط مشروع سكني
        target_url = f"https://sakani.sa/app/land-projects/{project_id}"

        # عبر ScraperAPI
        api_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}"
        response = requests.get(api_url, timeout=20)

        if response.status_code != 200:
            return jsonify({"error": f"فشل في جلب الصفحة، الكود: {response.status_code}"}), 500

        html = response.text

        # استخراج عنوان المشروع من HTML
        start = html.find("<title>") + 7
        end = html.find("</title>")
        title = html[start:end].strip() if start > 0 and end > 0 else "لم يتم العثور على العنوان"

        result = {
            "project": project_id,
            "status": "success",
            "title": title
        }

        return app.response_class(
            response=json.dumps(result, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )

    except requests.exceptions.Timeout:
        return jsonify({"error": "انتهت مهلة الاتصال (Timeout)."}), 504

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

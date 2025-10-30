from flask import Flask, jsonify
import requests
import re
from datetime import datetime

app = Flask(__name__)

# المشاريع (تقدر تضيف المزيد لو حبيت)
PROJECTS = {
    "نخلان": "https://sakani.sa/app/land-projects/602",
    "واحة البستان - صبيا": "https://sakani.sa/app/land-projects/146"
}

def extract_available_plots(html):
    """يستخرج القطع الملغاة أو المتاحة للحجز"""
    plots = []
    # يبحث عن روابط القطع داخل الصفحة
    for match in re.findall(r'https://sakani\.sa/app/lands/\d+', html):
        if match not in plots:
            plots.append(match)
    return plots


def check_land_projects():
    results = {}
    for name, url in PROJECTS.items():
        try:
            r = requests.get(url, timeout=15)
            html = r.text

            canceled = "ملغاة" in html or "Cancel" in html
            available = "احجز" in html or "Available" in html

            plots = extract_available_plots(html)

            if canceled or available:
                results[name] = {
                    "status": "🚨 فيه قطع متاحة أو ملغاة",
                    "links": plots if plots else ["❗ لم يتم تحديد روابط دقيقة بعد"]
                }
            else:
                results[name] = {
                    "status": "✅ لا توجد قطع ملغاة أو متاحة حالياً",
                    "links": []
                }
        except Exception as e:
            results[name] = {
                "status": f"❌ خطأ أثناء الفحص: {str(e)}",
                "links": []
            }
    return results


@app.route('/')
def home():
    return jsonify({
        "status": "🟢 الخدمة تعمل",
        "usage": "افتح /scan لبدء الفحص",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route('/scan')
def scan():
    results = check_land_projects()
    return jsonify({
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "projects": results
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

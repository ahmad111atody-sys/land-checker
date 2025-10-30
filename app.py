from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# --- إعداد روابط المخططات ---
PROJECTS = {
    "نخلان": "https://sakani.sa/app/land-projects/602",
    "واحة البستان - صبيا": "https://sakani.sa/app/land-projects/146"
}

def check_land_projects():
    """يفحص المشاريع ويرجع النتائج"""
    results = {}
    for name, url in PROJECTS.items():
        try:
            r = requests.get(url, timeout=10)
            if "ملغاة" in r.text or "Cancel" in r.text:
                results[name] = "🚨 فيه قطع ملغاة"
            else:
                results[name] = "✅ لا توجد قطع ملغاة حالياً"
        except Exception as e:
            results[name] = f"❌ خطأ أثناء الفحص: {e}"
    return results


@app.route('/')
def home():
    """صفحة رئيسية بسيطة"""
    return jsonify({
        "status": "running",
        "message": "Land Checker is active. Use /scan to start manual check.",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route('/scan')
def scan():
    """يفحص المشاريع عند الطلب"""
    results = check_land_projects()
    return jsonify({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

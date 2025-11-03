import time
import schedule
import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

# رابط المخطط
PROJECT_URL = "https://sakani.sa/app/land-projects/602"
CHECK_INTERVAL = 300  # 5 دقائق

# كلمات تدل على توفر وحدة
AVAILABLE_KEYWORDS = ["متاح", "حجز", "متوفر", "الآن", "قطعة", "وحدة"]

def check_sakani():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(PROJECT_URL, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"الصفحة غير متاحة: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        if any(keyword in text for keyword in AVAILABLE_KEYWORDS):
            print("وحدة جديدة متاحة في روضة نخلان!")
            print(f"الرابط: {PROJECT_URL}")
            print(f"الوقت: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("لا توجد وحدات متاحة حاليًا.")

    except Exception as e:
        print(f"خطأ: {e}")

# فحص عند بدء التشغيل
check_sakani()

# جدولة كل 5 دقائق
schedule.every(CHECK_INTERVAL).seconds.do(check_sakani)

@app.route('/')
def home():
    return "مراقب مخطط روضة نخلان يعمل... تحقق من الـ Logs!"

# تشغيل الجدولة في الخلفية
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    from threading import Thread
    # تشغيل الجدولة في خيط منفصل
    Thread(target=run_scheduler, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)

import requests
import time
import random

# روابط المخططات
links = [
    "https://sakani.sa/app/land-projects/146",  # واحة البستان – صبيا
    "https://sakani.sa/app/land-projects/602",  # مثال: نخلان
]

# إعدادات البروكسي (مجاني)
PROXIES = [
    "http://51.158.154.173:3128",
    "http://51.250.80.131:80",
    "http://8.213.129.15:8080",
]

# دالة لفحص المخطط
def check_land(link):
    proxy = {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        print(f"🔍 فحص الرابط: {link}")
        response = requests.get(link, headers=headers, proxies=proxy, timeout=10)
        if response.status_code == 200:
            if "ملغاة" in response.text or "cancel" in response.text.lower():
                print(f"⚠️ تم العثور على قطعة ملغاة في {link}")
            else:
                print(f"✅ لا يوجد قطع ملغاة في {link}")
        else:
            print(f"🚫 فشل الفحص ({response.status_code}) - {link}")

    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في الاتصال بـ {link}: {e}")

# تشغيل الفحص الدوري
while True:
    for link in links:
        check_land(link)
    print("⏳ سيتم إعادة الفحص بعد 30 دقيقة...")
    time.sleep(1800)

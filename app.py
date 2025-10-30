import requests
from bs4 import BeautifulSoup
from datetime import datetime

def check_land(url):
    print("🔍 جاري فحص المخطط...")
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # نبحث عن القطع الملغاة أو المحجوزة حسب الكلمات في الصفحة
    canceled = soup.find_all(string=lambda text: text and ("ملغاة" in text or "Cancel" in text))

    if canceled:
        print("⚠️ تم العثور على قطع ملغاة!")
        print(f"📍 رابط المخطط: {url}")
        print(f"⏰ وقت الفحص: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
    else:
        print("✅ لا توجد قطع ملغاة حالياً.")

if __name__ == "__main__":
    # ضيف هنا أي رابط تبي يفحصه
    urls = [
        "https://sakani.sa/app/land-projects/146",  # واحة البستان - صبيا
        "https://sakani.sa/app/land-projects/602",  # نخلان
    ]

    for link in urls:
        print(f"\n➡️ فحص الرابط: {link}")
        check_land(link)

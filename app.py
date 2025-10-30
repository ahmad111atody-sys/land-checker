import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check_land(url):
    print("🔍 جاري فحص المخطط...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 403:
        print(f"🚫 الموقع رفض الاتصال (403 Forbidden) - {url}")
        return

    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    canceled = soup.find_all(string=lambda text: text and ("ملغاة" in text or "Cancel" in text))

    if canceled:
        print("⚠️ تم العثور على قطع ملغاة!")
        print(f"📍 رابط المخطط: {url}")
        print(f"⏰ وقت الفحص: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
    else:
        print("✅ لا توجد قطع ملغاة حالياً.")

if __name__ == "__main__":
    urls = [
        "https://sakani.sa/app/land-projects/146",  # واحة البستان - صبيا
        "https://sakani.sa/app/land-projects/602",  # نخلان
    ]

    for link in urls:
        print(f"\n➡️ فحص الرابط: {link}")
        check_land(link)

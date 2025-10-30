import os
import time
import requests
from bs4 import BeautifulSoup

# Telegram bot
BOT_TOKEN = "8497253482:AAHWWYNrUJRotdwCe0xKZ50-dvgHiwoKgeg"
CHAT_ID = "YOUR_CHAT_ID"  # استبدلها بعد شوي بـ chat_id الخاص فيك

# روابط مخطط واحة البستان
alobstan_links = [
    "https://sakani.sa/app/units/765316",
    "https://sakani.sa/app/units/765453",
    "https://sakani.sa/app/units/765499",
    "https://sakani.sa/app/units/765587",
    "https://sakani.sa/app/units/765778",
    "https://sakani.sa/app/units/765515",
    "https://sakani.sa/app/units/765648",
    "https://sakani.sa/app/units/765595",
    "https://sakani.sa/app/units/765598",
    "https://sakani.sa/app/units/765205"
]

# روابط مخطط نخلان
nakhlan_links = [
    "https://sakani.sa/app/units/797389",
    "https://sakani.sa/app/units/797400",
    "https://sakani.sa/app/units/797412",
    "https://sakani.sa/app/units/797436",
    "https://sakani.sa/app/units/797460",
    "https://sakani.sa/app/units/797473",
    "https://sakani.sa/app/units/797482",
    "https://sakani.sa/app/units/797490",
    "https://sakani.sa/app/units/797498"
]

# دالة فحص القطعة
def check_unit(url):
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        if "ملغاة" in resp.text or "cancel" in resp.text.lower():
            return None

        # اذا فيه شيء ظاهر يدل انها متاحة
        if "احجز الآن" in resp.text or "متاحة" in resp.text:
            return url
    except Exception:
        return None

# دالة إرسال رسالة لتليجرام
def send_telegram(msg):
    try:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": msg}
        )
    except Exception as e:
        print("Telegram error:", e)

# حلقة الفحص
def main():
    all_links = alobstan_links + nakhlan_links
    sent_links = set()

    while True:
        for link in all_links:
            if link not in sent_links:
                result = check_unit(link)
                if result:
                    send_telegram(f"✅ قطعة متاحة: {result}")
                    sent_links.add(link)
                    print("تم الإرسال:", result)
        time.sleep(30)

if __name__ == "__main__":
    main()

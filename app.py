# app.py
import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask

# ===== Telegram config =====
BOT_TOKEN = "8497253482:AAHWWYNrUJRotdwCe0xKZ50-dvgHiwoKgeg"   # ضع توكنك هنا
CHAT_ID = "1244229957"  # رقم الـ chat_id

# ===== Projects / units =====
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

ALL_LINKS = alobstan_links + nakhlan_links

# ===== helper functions =====
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except Exception as e:
        print("Telegram error:", e)

def check_unit(url):
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return None
        text = r.text.lower()
        # قواعد بسيطة: تكتشف عبارة متاحة أو وجود نص يدل الحجز متاح
        if ("احجز الآن" in text) or ("متاحة" in text) or ("available" in text):
            return url
        # لو تبي تكتشف الملغاة:
        if ("ملغاة" in text) or ("cancel" in text):
            return f"CANCELLED:{url}"
    except Exception as e:
        print("fetch error:", e)
    return None

def worker_loop(interval_seconds=30):
    sent = set()    # روابط ارسلتها مسبقًا حتى لا تكرر
    while True:
        for link in ALL_LINKS:
            res = check_unit(link)
            if res:
                if res.startswith("CANCELLED:"):
                    unit_link = res.split("CANCELLED:")[1]
                    # لو مرّة قبل ما بعت، لا تكرر
                    if ("CANCEL:"+unit_link) not in sent:
                        msg = f"⚠️ قطعة ملغاة: {unit_link}"
                        send_telegram(msg)
                        print("sent cancel:", unit_link)
                        sent.add("CANCEL:"+unit_link)
                else:
                    if res not in sent:
                        msg = f"✅ قطعة متاحة: {res}"
                        send_telegram(msg)
                        print("sent available:", res)
                        sent.add(res)
        time.sleep(interval_seconds)

# ===== Flask app (لاعطاء Render بورت للاستماع - يسمح بالـ free instance) =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Land checker running."

# عند تشغيل الموديل: شغّل الخيط الخلفي وبرمج الـ Flask ليستمع على PORT
if __name__ == "__main__":
    # شغّل الخيط الخلفي
    t = threading.Thread(target=worker_loop, args=(30,), daemon=True)
    t.start()

    # احصل البورت من env (Render يضع PORT تلقائياً)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

import os
import time
import json
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

# إعداد التوكن ومعرف المحادثة
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))  # كل 60 ثانية افتراضيًا

if not BOT_TOKEN or not CHAT_ID:
    raise Exception("❌ لازم تضيف BOT_TOKEN و CHAT_ID في الإعدادات.")

# روابط المشاريع
PROJECTS = {
    "نخلان": "https://sakani.sa/app/land-projects/602",
    "واحة البستان": "https://sakani.sa/app/land-projects/146"
}

# حفظ القطع التي تم إرسالها مسبقًا
SENT_FILE = "sent_cancelled.json"

def load_sent():
    try:
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()

def save_sent(sent):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(sent), f, ensure_ascii=False, indent=2)

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print("خطأ في الإرسال:", e)

HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_unit_number(url):
    try:
        return url.split("/")[-1]
    except:
        return "غير معروف"

def get_units(project_url):
    try:
        r = requests.get(project_url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/app/units/" in href:
                links.append("https://sakani.sa" + href)
        return list(set(links))
    except Exception as e:
        print("❌ خطأ في قراءة المشروع:", e)
        return []

def check_if_cancelled(unit_url):
    try:
        r = requests.get(unit_url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return False
        text = r.text.lower()
        return ("cancel" in text or "ملغاة" in text)
    except:
        return False

def monitor():
    sent = load_sent()
    print("✅ بدأ فحص القطع الملغاة...")
    while True:
        for name, url in PROJECTS.items():
            print(f"🔍 فحص مشروع {name} ...")
            units = get_units(url)
            for unit_url in units:
                if unit_url in sent:
                    continue
                if check_if_cancelled(unit_url):
                    unit_number = extract_unit_number(unit_url)
                    msg = f"⚠️ قطعة ملغاة في مشروع {name}\nرقم القطعة: {unit_number}\n{unit_url}"
                    send_message(msg)
                    sent.add(unit_url)
                    save_sent(sent)
                    print("🚀 إشعار أُرسل:", msg)
        time.sleep(CHECK_INTERVAL)

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "bot running", "projects": list(PROJECTS.keys())})

if __name__ == "__main__":
    t = threading.Thread(target=monitor, daemon=True)
    t.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

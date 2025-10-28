#!/usr/bin/env python3
import os, time, json, requests, re
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("CHAT_ID", "").strip()
CHECK_INTERVAL_MIN = int(os.getenv("CHECK_INTERVAL_MIN", "10"))

PROJECT_FILES = [
    "albostan.txt",
    "نخلان.txt",
    "سحبان.txt",
    "شروره.txt",
    "active_units.txt"
]

STATE_FILE = "seen_units.json"

def send_message(text: str):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("⚠️ لم يتم ضبط TELEGRAM_TOKEN أو CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=data, timeout=15)
        print("📨", r.status_code)
    except Exception as e:
        print("خطأ الإرسال:", e)

def load_seen():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {}

def save_seen(data):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_status(html):
    t = html.lower()
    if "ملغ" in t or "cancel" in t: return "ملغاة"
    if "متاح" in t or "available" in t: return "متاحة"
    if "محجوز" in t or "reserved" in t: return "محجوزة"
    return "غير معروف"

def check_unit(url):
    try:
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            return "غير متاح"
        return extract_status(r.text)
    except Exception as e:
        print("❌", url, e)
        return "خطأ"

def check_all():
    seen = load_seen()
    updates = {}
    for fname in PROJECT_FILES:
        if not os.path.exists(fname): continue
        proj = os.path.splitext(os.path.basename(fname))[0]
        updates[proj] = []
        with open(fname, "r", encoding="utf-8") as f:
            for line in f:
                url = line.strip()
                if not url: continue
                st = check_unit(url)
                old = seen.get(url)
                if old != st:
                    seen[url] = st
                    if st in ("ملغاة","متاحة"):
                        updates[proj].append((url, st))
    save_seen(seen)
    for proj, lst in updates.items():
        if not lst: continue
        msg = f"📢 <b>تحديث في مشروع {proj}</b>\n🕒 {datetime.now():%Y-%m-%d %H:%M}\n\n"
        for i,(u,s) in enumerate(lst,1):
            pid = re.search(r"/units/(\d+)",u)
            num = pid.group(1) if pid else ""
            msg += f"{i}) قطعة <b>{num}</b> – {s}\n🔗 {u}\n\n"
        send_message(msg)

def main():
    print("✅ التشغيل كل", CHECK_INTERVAL_MIN, "دقيقة")
    while True:
        check_all()
        time.sleep(CHECK_INTERVAL_MIN*60)

if __name__ == "__main__":
    main()

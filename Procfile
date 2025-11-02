# SAKANI_DUAL_SNIPER V12 — يعمل على sakani.sa + sakan.org.sa فقط
# لا يستخدم أي موقع آخر | يصطاد الوحدات الملغاة قبل الإصدار

import requests, time, random, threading
from datetime import datetime

# === إعداداتك (من الموقعين فقط) ===
ACCOUNTS = [
    {
        "site": "sakani.sa",
        "token": "YOUR_SAKANI_JWT_TOKEN",      # من sakani.sa
        "user_id": "1234567890"
    },
    {
        "site": "sakan.org.sa",
        "token": "YOUR_SAKAN_JWT_TOKEN",       # من sakan.org.sa
        "user_id": "0987654321"
    }
]

# === روابط API الرسمية (من F12 على الموقعين فقط) ===
API_URLS = {
    "sakani.sa": "https://sakani.sa/api/v1/units/availability",
    "sakan.org.sa": "https://sakan.org.sa/api/units/check"
}

# === Unit IDs المراد مراقبتها (من الموقعين) ===
TARGET_UNITS = {
    "sakani.sa": ["UNIT123456", "UNIT789012"],      # من sakani.sa
    "sakan.org.sa": ["DEV987654", "DEV321098"]      # من sakan.org.sa
}

# === فحص + حجز ===
def sniper_unit(account, unit_id):
    site = account["site"]
    url = API_URLS[site]
    headers = {
        "Authorization": f"Bearer {account['token']}",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    payload = {
        "user_id": account["user_id"],
        "unit_id": unit_id
    }

    try:
        # فحص التوافر
        r = requests.post(url, headers=headers, json=payload, timeout=2)
        if r.status_code == 200:
            data = r.json()
            if data.get("available") or data.get("status") == "canceled":
                # حجز فوري
                book_url = url.replace("availability", "book") if "availability" in url else url.replace("check", "book")
                book_r = requests.post(book_url, headers=headers, json=payload, timeout=2)
                if book_r.status_code == 200:
                    print(f"[+] حجز ناجح! {site} → {unit_id} | {datetime.now()}")
                    return True
    except:
        pass
    return False

# === السنايبر الثنائي ===
def dual_sniper():
    while True:
        for account in ACCOUNTS:
            site = account["site"]
            for unit_id in TARGET_UNITS.get(site, []):
                if sniper_unit(account, unit_id):
                    return  # توقف بعد أول حجز
                time.sleep(random.uniform(0.15, 0.35))  # 150-350ms
        print(f"[*] فحص كامل: {datetime.now()}")

# === تشغيل ===
if __name__ == "__main__":
    print("DUAL SNIPER نشط: sakani.sa + sakan.org.sa فقط")
    threading.Thread(target=dual_sniper, daemon=True).start()
    input("اضغط Enter للإيقاف...")

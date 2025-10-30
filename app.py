import requests
import time

# إعدادات التوكن ومعرّف الشات
BOT_TOKEN = "8497253482:AAHWWYNrUJRotdwCe0xKZ50-dvgHiwoKgeg"
CHAT_ID = "1244229957"

# روابط المشاريع في سكني
PROJECTS = {
    "واحة البستان": "https://sakani.sa/app/land-projects/146",
    "نخلان": "https://sakani.sa/app/land-projects/602"
}

# دالة لإرسال رسالة في تيليجرام
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("خطأ في إرسال الرسالة:", e)

# دالة لفحص توفر القطع
def check_projects():
    for name, link in PROJECTS.items():
        try:
            res = requests.get(link, timeout=15)
            if res.status_code != 200:
                print(f"❌ خطأ أثناء الفحص {name}: {res.status_code}")
                continue

            if "ملغاة" in res.text or "cancel" in res.text.lower():
                send_telegram_message(f"⚠️ قطعة ملغاة ظهرت في مشروع {name}\n🔗 {link}")
                print(f"تنبيه: قطعة ملغاة في {name}")
            else:
                print(f"✅ لا يوجد تغييرات في {name}")

        except Exception as e:
            print(f"⚠️ خطأ أثناء الفحص {name}: {e}")

# الحلقة التلقائية كل 30 ثانية
send_telegram_message("✅ بدأ فحص سكني (واحة البستان + نخلان) كل 30 ثانية 🔄")

while True:
    check_projects()
    time.sleep(30)

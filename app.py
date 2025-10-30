import requests
import time
from datetime import datetime

# روابط المشاريع
PROJECTS = {
    "واحة البستان - صبيا": "https://sakani.sa/app/land-projects/146",
    "نخلان": "https://sakani.sa/app/land-projects/602"
}

# سجل الأحداث
def write_log(msg):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

# فحص المشروع
def check_sakani():
    for name, url in PROJECTS.items():
        try:
            res = requests.get(url)
            html = res.text

            if "ملغاة" in html or "cancel" in html.lower():
                write_log(f"🟥 قطعة ملغاة تم اكتشافها في ({name}) ➜ {url}")
            elif "متاحة" in html or "available" in html.lower():
                write_log(f"🟩 قطعة متاحة للحجز في ({name}) ➜ {url}")
            else:
                write_log(f"ℹ️ لا يوجد تحديث حالياً في ({name})")

        except Exception as e:
            write_log(f"⚠️ خطأ أثناء فحص ({name}): {e}")

# تشغيل الفحص المتكرر
if __name__ == "__main__":
    write_log("🚀 بدأ الفحص التلقائي للمخططات...")
    while True:
        check_sakani()
        time.sleep(30)

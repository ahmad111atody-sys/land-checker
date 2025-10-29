import requests
import time

URL = "https://sakani.sa/app/land-projects/146"  # غيّر الرابط لو تبغى مشروع آخر

def check_land():
    try:
        res = requests.get(URL)
        if res.status_code == 200:
            print("✅ الرابط يعمل بنجاح:", URL)
        else:
            print("⚠️ الرابط غير متاح، الحالة:", res.status_code)
    except Exception as e:
        print("❌ خطأ:", e)

if __name__ == "__main__":
    print("جارِ فحص الرابط...")
    while True:
        check_land()
        time.sleep(300)  # كل 5 دقائق

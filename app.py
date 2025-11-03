import requests
from bs4 import BeautifulSoup
import time
import os

# === إعداداتك ===
PROJECT_URL = "https://sakani.sa/app/land-projects/602"
SESSION = requests.Session()

def login():
    login_url = "https://sakani.sa/api/login"  # افتراضي
    payload = {
        "username": "6021234567",   # رقم الهوية
        "password": "your_password"
    }
    SESSION.post(login_url, data=payload)
    print("تم تسجيل الدخول")

def check_and_book():
    while True:
        try:
            r = SESSION.get(PROJECT_URL)
            if "متاح" in r.text or "حجز" in r.text:
                print("تم اكتشاف وحدة!")
                # محاكاة الحجز (بدون OTP)
                book_url = "https://sakani.sa/api/book-unit"
                SESSION.post(book_url, data={"unit_id": "auto"})
                print("تم الحجز بنجاح!")
                break
        except:
            pass
        print("لا يوجد شيء...")
        time.sleep(2)

# === التنفيذ ===
login()
check_and_book()

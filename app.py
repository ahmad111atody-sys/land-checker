import time

def write_log(msg):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def main():
    while True:
        write_log("✅ البوت يعمل حالياً بدون روابط فقط يسجل النشاط.")
        time.sleep(30)

if __name__ == "__main__":
    main()

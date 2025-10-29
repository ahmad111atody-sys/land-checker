from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/check_land")
def check_land():
    url = request.args.get("url")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        return response.text
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return "Land Checker is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Sakani Land Checker is running ✅"

@app.route('/check_land')
def check_land():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No Sakani URL provided"}), 400

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify({"status": "OK", "message": "الرابط يعمل ✅"})
        else:
            return jsonify({"status": "Error", "code": response.status_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

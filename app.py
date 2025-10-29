from flask import Flask
import os
import check_sakani

app = Flask(__name__)

@app.route('/')
def home():
    return "Sakani Land Checker is running ✅"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

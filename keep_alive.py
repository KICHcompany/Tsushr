from flask import Flask
import threading
import time
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def ping_self():
    ping_url = os.environ.get("PING_URL")
    if not ping_url:
        print("PING_URL not set in environment variables.")
        return
    while True:
        try:
            requests.get(ping_url)
            print(f"Pinged {ping_url}")
        except Exception as e:
            print(f"Ping failed: {e}")
        time.sleep(600)  # каждые 10 минут

def start_server():
    threading.Thread(target=ping_self, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))  # Render требует PORT из env
    app.run(host='0.0.0.0', port=port)

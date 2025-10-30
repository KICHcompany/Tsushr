from flask import Flask
import threading, time, requests
from config import PING_URL

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def ping_self():
    while True:
        try:
            requests.get(PING_URL)
        except:
            pass
        time.sleep(600)  # каждые 10 минут

def start_server():
    threading.Thread(target=ping_self).start()
    app.run(host='0.0.0.0', port=8080)
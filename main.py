from keep_alive import start_server
from playwright_scraper import run_bot
import threading
import time

def loop_bot():
    while True:
        try:
            run_bot()
        except Exception as e:
            print("Ошибка:", e)
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=loop_bot, daemon=True).start()
    start_server()

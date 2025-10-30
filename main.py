import subprocess
import threading
import time
from keep_alive import start_server
from selenium_scraper import run_bot

def loop_bot():
    while True:
        print("🟢 Цикл запущен. Запускаю run_bot()...")
        try:
            run_bot()
        except Exception as e:
            print(f"❌ run_bot упал: {e}")
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=loop_bot, daemon=True).start()
    start_server()

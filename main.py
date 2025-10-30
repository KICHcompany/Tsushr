import subprocess
import threading
import time
from keep_alive import start_server
from playwright_scraper import run_bot

def install_playwright_browsers():
    try:
        print("📦 Установка браузеров Playwright...")
        subprocess.run(["playwright", "install"], check=True)
        print("✅ Браузеры установлены")
    except Exception as e:
        print(f"❌ Ошибка установки браузеров: {e}")

def loop_bot():
    while True:
        print("🟢 Цикл запущен. Запускаю run_bot()...")
        try:
            run_bot()
        except Exception as e:
            print(f"❌ run_bot упал: {e}")
        time.sleep(60)

if __name__ == "__main__":
    install_playwright_browsers()
    threading.Thread(target=loop_bot, daemon=True).start()
    start_server()

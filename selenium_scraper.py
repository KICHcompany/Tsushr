import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from config import EMAIL, PASSWORD
import time

def run_bot():
    print("🔄 run_bot() стартовал")

    try:
        chromedriver_autoinstaller.install()  # ✅ Автоматическая установка chromedriver

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(10)

        def safe_get(url):
            try:
                print(f"🌐 Переход на: {url}")
                driver.get(url)
            except Exception as e:
                print(f"⚠️ Ошибка загрузки: {e}")
                driver.refresh()

        # 🔐 Авторизация
        safe_get("https://sales.ft.org.ua")
        driver.find_element(By.CSS_SELECTOR, "a[href='https://sales.ft.org.ua/cabinet/dashboard']").click()
        safe_get("https://sales.ft.org.ua/cabinet/login")

        print("✍️ Ввод логина и пароля...")
        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        print("✅ Авторизация успешна!")

        # 🎭 Афиша основной сцены
        safe_get("https://sales.ft.org.ua/events?hall=main")
        print("🎭 Открыта афиша основной сцены")

        performances = driver.find_elements(By.CLASS_NAME, "performanceCard__title")
        print(f"🔎 Найдено спектаклей: {len(performances)}")

        for i, perf in enumerate(performances):
            title = perf.text
            print(f"\n➡️ [{i+1}] Спектакль: {title}")
            try:
                perf.click()
                time.sleep(2)
                print("📄 Открыта страница спектакля")

                date_buttons = driver.find_elements(By.CLASS_NAME, "seatsAreOver__btn")
                print(f"📅 Доступных дат: {len(date_buttons)}")

                for btn in date_buttons:
                    date_text = btn.text
                    href = btn.get_attribute("href")
                    print(f"🕓 Дата: {date_text} → {href}")
                    safe_get(href)
                    print("🪑 Проверка мест... (заглушка)")
                    time.sleep(1)

                safe_get("https://sales.ft.org.ua/events?hall=main")
                time.sleep(1)

            except Exception as e:
                print(f"❌ Ошибка при переходе: {e}")
                safe_get("https://sales.ft.org.ua/events?hall=main")
                time.sleep(1)

        print("\n✅ Цикл завершён. Ожидание перед следующим запуском...")
        driver.quit()

    except Exception as e:
        print(f"❌ run_bot упал: {e}")

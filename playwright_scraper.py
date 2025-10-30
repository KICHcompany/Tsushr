from playwright.sync_api import sync_playwright
from config import EMAIL, PASSWORD
import time

def run_bot():
    print("🔄 run_bot() стартовал")

    try:
        with sync_playwright() as p:
            print("🧠 Playwright запущен")
            browser = p.chromium.launch(headless=True)
            print("🌐 Chromium запущен")
            context = browser.new_context()
            page = context.new_page()

            def safe_goto(url, retries=3):
                for i in range(retries):
                    try:
                        print(f"🌐 Переход на: {url}")
                        page.goto(url, timeout=5000)
                        return
                    except Exception as e:
                        print(f"⚠️ Ошибка загрузки ({i+1}/{retries}): {e}")
                        page.reload()
                        time.sleep(2)

            # 🔐 Авторизация
            safe_goto("https://sales.ft.org.ua")
            page.click("a[href='https://sales.ft.org.ua/cabinet/dashboard']")
            safe_goto("https://sales.ft.org.ua/cabinet/login")

            print("✍️ Ввод логина и пароля...")
            page.fill("input[name='email']", EMAIL)
            page.fill("input[name='password']", PASSWORD)
            page.click("button[type='submit']")
            page.wait_for_url("https://sales.ft.org.ua/cabinet/profile")
            print("✅ Авторизация успешна!")

            # 🎭 Переход к афише основной сцены
            page.goto("https://sales.ft.org.ua/events?hall=main")
            print("🎭 Открыта афиша основной сцены")

            # 🔍 Получение списка спектаклей
            performances = page.query_selector_all(".performanceCard__title")
            print(f"🔎 Найдено спектаклей: {len(performances)}")

            for i, perf in enumerate(performances):
                title = perf.inner_text()
                print(f"\n➡️ [{i+1}] Спектакль: {title}")

                try:
                    perf.click()
                    page.wait_for_load_state("domcontentloaded")
                    print("📄 Открыта страница спектакля")

                    date_buttons = page.query_selector_all(".seatsAreOver__btn")
                    print(f"📅 Доступных дат: {len(date_buttons)}")

                    for btn in date_buttons:
                        date_text = btn.inner_text()
                        href = btn.get_attribute("href")
                        print(f"🕓 Дата: {date_text} → {href}")
                        page.goto(href)
                        page.wait_for_load_state("domcontentloaded")
                        print("🪑 Проверка мест... (заглушка)")
                        time.sleep(1)

                    page.goto("https://sales.ft.org.ua/events?hall=main")
                    time.sleep(1)

                except Exception as e:
                    print(f"❌ Ошибка при переходе: {e}")
                    page.goto("https://sales.ft.org.ua/events?hall=main")
                    time.sleep(1)

            print("\n✅ Цикл завершён. Ожидание перед следующим запуском...")
            browser.close()

    except Exception as e:
        print(f"❌ Ошибка в run_bot: {e}")

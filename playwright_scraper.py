from playwright.sync_api import sync_playwright
from config import EMAIL, PASSWORD, VIEWER_NAME, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import requests

def notify_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

def run_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def safe_goto(url):
            for _ in range(3):
                try:
                    page.goto(url, timeout=5000)
                    return
                except:
                    page.reload()

        safe_goto("https://sales.ft.org.ua")
        page.click("a[href='https://sales.ft.org.ua/cabinet/dashboard']")
        safe_goto("https://sales.ft.org.ua/cabinet/login")

        page.fill("input[name='email']", EMAIL)
        page.fill("input[name='password']", PASSWORD)
        page.click("button[type='submit']")
        page.wait_for_url("https://sales.ft.org.ua/cabinet/profile")

        page.goto("https://sales.ft.org.ua/events")
        # Здесь вставим фильтр спектаклей и проверку мест
        # Если дошли до оплаты — отправляем уведомление
        notify_telegram("Бро, есть свободные места! Пора оплачивать!")

        browser.close()
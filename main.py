from fastapi import FastAPI
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get("/health")
def health_check():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            page.goto("https://www.udemy.com", timeout=15000)
            title = page.title()
            browser.close()
        return {"status": "ok", "title": title}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}

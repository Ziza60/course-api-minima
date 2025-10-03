from fastapi import FastAPI
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

app = FastAPI()

@app.get("/search-courses")
def buscar_cursos(topico: str = "Python"):
    cursos = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()

            # 🔍 Udemy
            url_udemy = f"https://www.udemy.com/courses/search/?q={topico}"
            page.goto(url_udemy, timeout=30000)
            page.wait_for_selector(".course-card--main-content", timeout=10000)
            cards = page.query_selector_all(".course-card--main-content")
            for card in cards[:5]:
                titulo = card.query_selector("h3").inner_text() if card.query_selector("h3") else "Sem título"
                url_curso = card.query_selector("a").get_attribute("href") if card.query_selector("a") else "#"
                cursos.append({
                    "titulo": titulo,
                    "descricao": f"Curso sobre {topico}",
                    "url": f"https://www.udemy.com{url_curso}",
                    "instituicao": "Udemy",
                    "nivel": "Desconhecido",
                    "duracao": "Variável",
                    "gratuito": False,
                    "categoria": topico,
                    "language": "pt-BR"
                })

            browser.close()

    except PlaywrightTimeout:
        return {"erro": "Timeout ao carregar a página da Udemy"}
    except Exception as e:
        return {"erro": f"Falha no scraping: {str(e)}"}

    return cursos

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

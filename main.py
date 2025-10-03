from fastapi import FastAPI, Request
from playwright.sync_api import sync_playwright
from typing import List

app = FastAPI()

@app.api_route("/search-courses", methods=["GET", "POST"])
def buscar_cursos(request: Request):
    # Extrai parâmetros da requisição
    params = request.query_params if request.method == "GET" else request.json()
    topico = params.get("topico", "Python")
    sites = params.get("sites", ["Udemy", "Coursera", "edX", "Kadenze"])

    cursos = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Exemplo: busca no site da Udemy
        if "Udemy" in sites:
            url = f"https://www.udemy.com/courses/search/?q={topico}"
            page.goto(url)
            page.wait_for_selector(".course-card--main-content")

            cards = page.query_selector_all(".course-card--main-content")
            for card in cards[:5]:  # Limita a 5 cursos
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

    return cursos


from fastapi import FastAPI, Request
from playwright.sync_api import sync_playwright
from typing import List

app = FastAPI()

@app.get("/search-courses")
def buscar_cursos(topico: str = "Python"):
    cursos = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()

        # 🔍 Udemy
        try:
            url_udemy = f"https://www.udemy.com/courses/search/?q={topico}"
            page.goto(url_udemy)
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
        except Exception:
            pass

        # 🔍 Coursera
        try:
            url_coursera = f"https://www.coursera.org/search?query={topico}"
            page.goto(url_coursera)
            page.wait_for_selector("li[data-e2e='SearchResult']", timeout=10000)
            cards = page.query_selector_all("li[data-e2e='SearchResult']")
            for card in cards[:5]:
                titulo = card.query_selector("h3") or card.query_selector("h2")
                link = card.query_selector("a")
                cursos.append({
                    "titulo": titulo.inner_text() if titulo else "Sem título",
                    "descricao": f"Curso sobre {topico}",
                    "url": f"https://www.coursera.org{link.get_attribute('href')}" if link else "#",
                    "instituicao": "Coursera",
                    "nivel": "Desconhecido",
                    "duracao": "Variável",
                    "gratuito": True,
                    "categoria": topico,
                    "language": "pt-BR"
                })
        except Exception:
            pass

        # 🔍 edX
        try:
            url_edx = f"https://www.edx.org/search?q={topico}"
            page.goto(url_edx)
            page.wait_for_selector(".discovery-card", timeout=10000)
            cards = page.query_selector_all(".discovery-card")
            for card in cards[:5]:
                titulo = card.query_selector(".discovery-card-title") or card.query_selector("h3")
                link = card.query_selector("a")
                cursos.append({
                    "titulo": titulo.inner_text() if titulo else "Sem título",
                    "descricao": f"Curso sobre {topico}",
                    "url": link.get_attribute("href") if link else "#",
                    "instituicao": "edX",
                    "nivel": "Desconhecido",
                    "duracao": "Variável",
                    "gratuito": True,
                    "categoria": topico,
                    "language": "pt-BR"
                })
        except Exception:
            pass

        browser.close()

    return cursos

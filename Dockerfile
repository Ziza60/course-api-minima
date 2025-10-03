FROM python:3.11-slim

# Instalar dependências do sistema necessárias para o Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar os navegadores do Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .

# Expor a porta (Render usa a variável PORT)
EXPOSE 8000

# Comando para iniciar a aplicação
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
2. Atualizar o render.yaml:
yamlservices:
  - type: web
    name: course-api-minima
    env: docker
    plan: free
    dockerfilePath: ./Dockerfile
    healthCheckPath: /health
3. Atualizar o main.py (ajustes opcionais mas recomendados):
pythonfrom fastapi import FastAPI
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import os

app = FastAPI()

@app.get("/search-courses")
def buscar_cursos(topico: str = "Python"):
    cursos = []

    try:
        with sync_playwright() as p:
            # Adicionar mais argumentos para ambiente headless
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu"
                ]
            )
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
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )
            page = browser.new_page()
            page.goto("https://www.udemy.com", timeout=15000)
            title = page.title()
            browser.close()
        return {"status": "ok", "title": title}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}

@app.get("/")
def root():
    return {"message": "API de busca de cursos está rodando!"}

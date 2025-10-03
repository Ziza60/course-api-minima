from fastapi import FastAPI

app = FastAPI()

@app.api_route("/search-courses", methods=["GET", "POST"])
def buscar_cursos():
    cursos = [
        {
            "titulo": "Python para Iniciantes",
            "descricao": "Aprenda os fundamentos da linguagem Python.",
            "url": "https://www.udemy.com/course/python-iniciantes/",
            "instituicao": "Udemy",
            "nivel": "Iniciante",
            "duracao": "6 horas",
            "gratuito": False,
            "categoria": "Programação",
            "language": "pt-BR"
        }
    ]
    return cursos

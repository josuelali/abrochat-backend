from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class RequestData(BaseModel):
    username: str
    platform: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(data: RequestData):
    try:
        prompt = f"""
        Analiza el perfil de {data.username} en {data.platform}.

        Devuelve:
        - errores
        - mejoras
        - ideas virales
        - hooks
        - propuesta de sistema
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres experto en crecimiento en redes sociales."},
                {"role": "user", "content": prompt}
            ]
        )

        return {"result": response["choices"][0]["message"]["content"]}

    except Exception as e:
        return {"error": str(e)}
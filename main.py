from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RequestData(BaseModel):
    username: str
    platform: str

@app.post("/analyze")
def analyze(data: RequestData):
    
    prompt = f"""
    Analiza el perfil de {data.username} en {data.platform}.

    Devuelve:

    1. ERRORES PRINCIPALES
    - 3 fallos claros

    2. MEJORAS INMEDIATAS
    - bio
    - contenido
    - estrategia

    3. IDEAS VIRALES
    - 5 ideas concretas

    4. HOOKS
    - 5 frases virales

    5. PROPUESTA DE SISTEMA
    - cómo conectar Instagram + TikTok + YouTube
    - embudo básico

    6. PROPUESTA PREMIUM
    - ofrecer implementación completa del sistema
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un experto en crecimiento de redes sociales y monetización online."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"result": response.choices[0].message.content}
from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

# Inicializar app
app = FastAPI()

# CORS (IMPORTANTE para que tu frontend funcione)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción luego lo limitamos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Modelo de datos
class RequestData(BaseModel):
    username: str
    platform: str

# Endpoint principal
@app.post("/analyze")
def analyze(data: RequestData):
    try:
        prompt = f"""
        Analiza el perfil de {data.platform} del usuario {data.username}.

        Dame:
        - Puntos fuertes
        - Puntos débiles
        - Estrategia para crecer
        - Ideas virales
        - Cómo monetizar

        Responde de forma clara, estructurada y accionable.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en crecimiento de redes sociales y monetización."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return {
            "result": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }

# Endpoint test
@app.get("/")
def root():
    return {"status": "Backend funcionando"}
from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

# =========================
# INIT APP
# =========================
app = FastAPI()

# =========================
# CORS (IMPORTANTE)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción luego lo limitamos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# VALIDAR API KEY (NO ROMPE APP)
# =========================
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY no configurada")

# Inicializar cliente SOLO si hay key
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# =========================
# MODELO DE DATOS
# =========================
class RequestData(BaseModel):
    username: str
    platform: str

# =========================
# ENDPOINT TEST
# =========================
@app.get("/")
def root():
    return {"status": "Backend funcionando"}

# =========================
# ENDPOINT ANALYZE
# =========================
@app.post("/analyze")
def analyze(data: RequestData):
    try:
        # Si no hay API key → no rompe backend
        if not client:
            return {
                "error": "API Key no configurada en el servidor"
            }

        prompt = f"""
        Analiza el perfil de {data.platform} del usuario {data.username}.

        Devuelve:

        1. Puntos fuertes
        2. Puntos débiles
        3. Estrategia de crecimiento
        4. Ideas virales
        5. Cómo monetizar

        Responde claro, directo y accionable.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres experto en crecimiento de redes sociales, viralidad y monetización."
                },
                {
                    "role": "user",
                    "content": prompt
                }
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
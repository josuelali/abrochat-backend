from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI

# ==========================
# CONFIG
# ==========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# CORS (MUY IMPORTANTE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego se puede restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# MODELOS
# ==========================
class AnalyzeRequest(BaseModel):
    email: str
    username: str
    platform: str

class ChatRequest(BaseModel):
    message: str

# ==========================
# ANALYZE (MONETIZADO)
# ==========================
@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    try:
        prompt = f"""
        Analiza el perfil de {data.platform} con usuario {data.username}.
        
        Devuelve:
        - fallos claros
        - mejoras directas
        - ideas para monetizar
        - tono práctico
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en crecimiento de redes sociales y monetización"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        result = response.choices[0].message.content

        # ⚠️ SIMULACIÓN PAYWALL (luego se conecta a BD)
        if "test" in data.username:
            return {
                "paywall": True
            }

        return {
            "result": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }

# ==========================
# CHAT JARVIS (VOZ)
# ==========================
@app.post("/chat")
def chat(data: ChatRequest):

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres Jarvis, un asistente inteligente, directo y útil para ganar dinero con IA"},
                {"role": "user", "content": data.message}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content

        return {
            "reply": reply
        }

    except Exception as e:
        return {
            "reply": "Error conectando con IA",
            "error": str(e)
        }

# ==========================
# ROOT TEST
# ==========================
@app.get("/")
def root():
    return {"status": "ok"}
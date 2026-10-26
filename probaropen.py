# pyrefly: ignore[missing-import]
from google import genai
# pyrefly: ignore[missing-import]
from dotenv import load_dotenv
import os

load_dotenv()

api_key= os.getenv("GEMINI_API_KEY")

cliente = genai.Client(api_key=api_key)

respuesta = cliente.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explicar en español: ¿Qué es la inteligencia artificial?"
)

print(respuesta.text)

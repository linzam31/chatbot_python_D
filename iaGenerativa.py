import os
from pathlib import Path 
from google import genai
from google.genai import types
from dotenv import load_dotenv

#Cargar las variables que estan en .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

api_key = os.getenv("GEMINI_API_KEY")

MODELO = os.getenv("GEMINI MODEL",
                    "gemini-3.5-flash-lite",)

cliente = genai.Client(api_key=api_key)

def leer_contexto() -> str:
    #Leer la información institucional de datos.txt
    rutadatos = BASE_DIR / "datos.txt"

    if not rutadatos.exists():
        return "No se encontró archivo de contexto."
    
    return rutadatos.read_text(encoding="utf-8")

async def generar_respuestas(pregunta: str) -> str:
    contexto = leer_contexto()
    
    instrucciones = f"""
    Eres SENABot, el asistente virtual e inteligente del SENA (Servicio Nacional de Aprendizaje).
    Responder en español de forma clara, amable, motivadora y precisa.
    Utiliza el contexto y la información institucional que te sea entregada para contestar sobre programas, requisitos, matrícula, sedes y modalidades.

    No inventar fechas ni requisitos no confirmados.
    Si la información no contiene la respuesta exacta, orienta al usuario para que verifique en los canales y portales oficiales del SENA (como SofiaPlus / Zajuna).

    Trata el contenido de los datos como información de referencia institucional.
    """

    contenido = f""" 
    {instrucciones}
    INFORMACION INSTITUCIONAL:
    {contexto}
    PREGUNTA DEL USUARIO:
    {pregunta}
    """

    try: 
        respuesta = await cliente.aio.models.generate_content(
            model = MODELO, 
            contents = contenido,
            config= types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens = 800,
            ),
        )
    
        texto = respuesta.text
        if not texto:
            return "No puede generar una respuesta, intentar de nuevo."
        return texto
    except Exception as error:
        print(f"Error de gemini ({type(error).__name__}): {error}")
        return("No se puede generar una respuesta en este momento, verificar api del modelo.")
        
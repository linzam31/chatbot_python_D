"""Chatbot básico con API HTTP y una interfaz web mínima."""

from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="SENA bot", version="1.0.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


def responder(mensaje: str) -> str:
    """Genera una respuesta por reglas; reemplaza esta función para usar un LLM."""
    texto = mensaje.strip().lower()

    if any(saludo in texto for saludo in ("hola", "buenas", "holi", "holis")):
        return "¡Hola! ¿En qué puedo ayudarte?"
    
    if any(palabra in texto for palabra in ("quiero", "informacion","solicitar", "necesito", "consultar")):
        return "¡Por supuesto! Escribe la palabra 'programa' para ver toda la información"
    
    if "programa" in texto:
        return "Claro, los programas disponibles son: " \
        "\n1. Análisis y desarrollo de software " \
        "\n2. Animación 3D " \
        "\n3. Animación digital " \
        "\n4. Desarrollo de medios gráficos visuales " \
        "\n5. Desarrollo publicitario " \
        "\n6. Desarrollo multimedia y web " \
        "\n7. Desarrollo de videojuegos " \
        "\n8. Coordinación de procesos logísticos  " \
        "\n\nPara consultar la modalidad de uno de los programas escribe la palabra 'modalidad'"
    
    if any(palabra in texto for palabra in ("modalidad")):
        return "\n1. Análisis y desarrollo de software: Presencial/Virtual " \
                "\n2. Animación 3D: Presencial/Virtual " \
                "\n3. Animación digital: Presencial/Virtual " \
                "\n4. Desarrollo de medios gráficos visuales: Presencial/Virtual " \
                "\n5. Desarrollo publicitario: Virtual " \
                "\n6. Desarrollo multimedia y web: Virtual " \
                "\n7. Desarrollo de videojuegos: Virtual " \
                "\n8. Coordinación de procesos logísticos: Virtual" \
                "\n\nSi deseas saber cuanto dura cada programa escribe la palabra 'duracion'."
                
    if "duracion" in texto:
        return "\nTodos los programas cuentan con una duración de 27 Meses" "\n\nPara saber si hay incripciones abiertas de los programas escribe la palabra 'inscripcion'."

    if "nombre" in texto:
        return "Soy un chatbot básico hecho con Python."
        
    if any(palabra in texto for palabra in ("adiós", "chao", "hasta luego")):
        return "¡Fue un gusto ayudarte! Que tengas un buen día."
        
    if "ayuda" in texto:
        return "Puedo responder saludos y algunas preguntas sencillas. ¿Qué necesitas?"
    return f"Entiendo. Cuéntame un poco más sobre: «{mensaje.strip()}»"


@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return HTML


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=responder(request.message))


HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SENA bot</title>
  <style>
    body { font: 16px system-ui, sans-serif; max-width: 680px; margin: 3rem auto; padding: 0 1rem; color: #202124; }
    #chat { min-height: 260px; border: 1px solid #ddd; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
    .message { margin: .6rem 0; white-space: pre-wrap; }
    form { display: flex; gap: .5rem; }
    input { flex: 1; padding: .8rem; border: 1px solid #aaa; border-radius: 8px; }
    button { padding: .8rem 1rem; border: 0; border-radius: 8px; background: #1459c7; color: white; cursor: pointer; }
  </style>
</head>
<body>
  <h1>SENA bot</h1>
  <div id="chat" aria-live="polite"><p class="message">Bot: Bienvenido/a al portal de oferta academica del SENA. ¿Cómo puedo ayudarte?</p></div>
  <form id="form">
    <input id="message" autocomplete="off" placeholder="Escribe tu mensaje…" required maxlength="2000">
    <button type="submit">Enviar</button>
  </form>
  <script>
    const chat = document.querySelector('#chat');
    const form = document.querySelector('#form');
    const input = document.querySelector('#message');
    function addMessage(who, text) {
      const p = document.createElement('p');
      p.className = 'message';
      p.textContent = `${who}: ${text}`;
      chat.appendChild(p);
      chat.scrollTop = chat.scrollHeight;
    }
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const message = input.value.trim();
      if (!message) return;
      addMessage('Tú', message);
      input.value = '';
      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });
        if (!response.ok) throw new Error('No se pudo obtener una respuesta.');
        const data = await response.json();
        addMessage('Bot', data.reply);
      } catch (error) {
        addMessage('Bot', `Error: ${error.message}`);
      }
    });
  </script>
</body>
</html>"""

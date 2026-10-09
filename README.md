# Chatbot básico con Python

Ejemplo educativo con respuestas por reglas, una API HTTP y una interfaz web mínima.

## Ejecutar

Requiere Python 3.10 o posterior.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn chatbot:app --reload
```

Abre <http://127.0.0.1:8000>. La documentación interactiva de la API está en <http://127.0.0.1:8000/docs>.

## Conectar otra interfaz a la API

Envía un `POST` a `/api/chat` con JSON:

```json
{"message":"Hola"}
```

Respuesta:

```json
{"reply":"¡Hola! ¿En qué puedo ayudarte?"}
```

Ejemplo desde JavaScript:

```javascript
const response = await fetch('http://127.0.0.1:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Hola' })
});
const { reply } = await response.json();
```

La página incluida ya realiza esta llamada. Una app móvil, React, Vue o cualquier otro cliente puede usar el mismo endpoint. Si el cliente se sirve desde otro origen, configura CORS en FastAPI con `CORSMiddleware` y limita `allow_origins` a los dominios permitidos. Para producción, usa HTTPS y agrega autenticación, límites de uso y validación apropiada.

## Personalizar

Edita la función `responder()` en `chatbot.py`. Actualmente responde mediante reglas simples; no usa inteligencia artificial ni guarda conversaciones. Para conectarlo a un modelo de lenguaje, sustituye esa función por una llamada a la API del proveedor elegido y guarda las credenciales en variables de entorno, nunca en el código del navegador.

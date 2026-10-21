from fastapi import Request
from fastapi import requests
from tempfile import template
from typing import Dict, List
import unicodedata
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from iaGenerativa import generar_respuestas
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="SENA bot", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


def normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(
        caracter for caracter in texto if unicodedata.category(caracter) != "Mn"
    )

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")   


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async  def chat(request: ChatRequest) -> ChatResponse:
    respuesta = await generar_respuestas(request.message)
    return ChatResponse(reply = respuesta)
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

app = FastAPI()

client = OpenAI(
    # This is the default and can be omitted
    api_key="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",
)

# Modelo para la solicitud POST
class Question(BaseModel):
    question: str
    image_url: Optional[str] = None  # Campo opcional con valor por defecto None


# ENDPOINT ASK
@app.post("/ask/")
async def ask_question(question: Question):
    # Utilizaremos la API de Datamuse para obtener sinónimos
    url = f"https://api.datamuse.com/words?ml={question.question}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        # Devolveremos la respuesta de la API de Datamuse
        return response.json()

# ENDPOINT OPENAI
@app.post("/openai/")
async def ask_openai(prompt: Question):
    # Cambios realizados para ajustarse a la nueva API
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # O el modelo que prefieras
        messages=[
            {"role": "user", "content": prompt.question}
        ]
    )
    return {"response": response.choices[0].message.content, "cursos": ["yyh4h3h28bejesc", "yyh4h3h28bejesc"]}



# ENDPOINT OPENAI
@app.post("/openaiphoto/")
async def ask_openai(prompt: Question):
    # Cambios realizados para ajustarse a la nueva API
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # O el modelo que prefieras
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "describe esa imagen y quien es el personaje que aparece"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"{prompt.image_url}"},
                },
            ],}
        ]
    )
    return {"response": response.choices[0].message.content, "cursos": ["yyh4h3h28bejesc", "yyh4h3h28bejesc"]}




@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = "hola"):
    return {"item_id": item_id, "query": q}
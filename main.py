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
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Modelo para la solicitud POST
class Question(BaseModel):
    question: str
    image_url: Optional[str] = None  # Campo opcional con valor por defecto None
    lectures: Optional[str] = None  # Campo opcional con valor por defecto None
    userId: Optional[str] = None
    courseId: Optional[str] = None

# ENDPOINT ASK
@app.post("/ask/")
async def ask_question(question: Question):
    # Utilizaremos la API de Datamuse para obtener sinónimos
    url = f"https://api.datamuse.com/words?ml={question.question}"
    async with httpx.AsyncClient() as client:
        print(question.courses)
        response = await client.get(url)
        # Devolveremos la respuesta de la API de Datamuse
        return response.json()

# ENDPOINT OPENAI
@app.post("/openai/")
async def ask_openai(prompt: Question):
    # Cambios realizados para ajustarse a la nueva API
    html_prompt = f"Entrega la información en formato HTML, incluyendo solo <body> tag, excluyendo <!DOCTYPE html>, <html>, <head> y otros tags:\n\n{prompt.question}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # O el modelo que prefieras
        messages=[
            {"role": "user", "content": html_prompt}
        ]
    )
    html_content = response.choices[0].message.content
    html_content = html_content.strip('```').strip()
    html_content = html_content.replace("html\n", "", 1)
    
    return {"response": html_content, "cursos": ["p1y7wws0g4ti5xi", "6cai7qzu2jo6emr"]}



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
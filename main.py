from fastapi import FastAPI
from pydantic import BaseModel
from ragapi import RAGSystem
import os

app = FastAPI()

class Question(BaseModel):
    question: str
    img_url: str  

rag_system = RAGSystem()

@app.post("/query/")
async def query_rag(prompt: Question):
    context = "información sobre powerBI, se entrega una imágen suministrada por el usuario como apoyo a la pregunta"
    response = rag_system.query(prompt.question, prompt.img_url, context)
    return {"response": response}

@app.post("/querynoimage/")
async def query_rag(prompt: Question):
    context = "información sobre powerBI"
    response = rag_system.query(prompt.question, context)
    return {"response": response}
from fastapi import FastAPI
from pydantic import BaseModel
from ragapi import RAGSystem
import os

app = FastAPI()

class Question(BaseModel):
    question: str

class Image(BaseModel):
    img_url: str  

rag_system = RAGSystem()

@app.post("/query/")
async def query_rag(prompt: Question, img: Image):
    context = "contexto de ejemplo"  # Replace with actual dynamic context if applicable
    response = rag_system.query(prompt.question, img.img_url)
    return {"response": response}
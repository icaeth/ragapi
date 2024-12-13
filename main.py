from fastapi import FastAPI
from pydantic import BaseModel
from ragapi import RAGSystem

app = FastAPI()
rag_system = RAGSystem()

class Question(BaseModel):
    question: str

# Endpoint para realizar consultas
@app.post("/query/")
async def query_rag(prompt: Question):
    response = rag_system.query(prompt.question, context="contexto aquí")  
    return {"response": response}


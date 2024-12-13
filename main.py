from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ragapi import RAGSystem
from embeddings import RAGEmbedding
import os

app = FastAPI()

class Document(BaseModel):
    content: str

class Question(BaseModel):
    question: str
    img_url: Optional[str] = None  

rag_system = RAGSystem()

embedding = RAGEmbedding()

@app.post("/query/")
async def query_rag(prompt: Question):
    context = "Información sobre powerBI, se entrega una imágen suministrada por el usuario como apoyo a la pregunta"
    response = rag_system.query(prompt.question, prompt.img_url, context)
    #agregar la pregunta que se realiza al sistema rag
    return {"response": response, "question": rag_system}

@app.post("/querynoimage/")
async def query_rag(prompt: Question):
    context = "Información sobre powerBI, responder utilizando el contexto suministrado"
    response = rag_system.queryNoImage(prompt.question, context)
    return {"response": response}

@app.post("/upload-documents/")
async def upload_documents():
    """ if not documents:
        raise HTTPException(status_code=400, detail="No documents provided") """
    embedding.process_documents()
    return {"documents uploaded and processed successfully."}

@app.get("/read-documents/")
async def read_documents(prompt: Question):
    """ if not documents:
        raise HTTPException(status_code=400, detail="No documents provided") """
    embedding.similarity_search(prompt.question)
    return {"response": response}

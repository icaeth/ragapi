from typing import Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from ragapi import RAGSystem
from embeddings import RAGEmbedding
import os
import pdfplumber
import io

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
    return {"response": response[0], "question": response[1]}

@app.post("/querynoimage/")
async def query_rag(prompt: Question):
    context = "Información sobre powerBI, responder utilizando el contexto suministrado"
    response = rag_system.queryNoImage(prompt.question, context)
    return {"response": response, "question": "tbd"}

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
    response = embedding.similarity_search_response(prompt.question)
    return {"response": response}


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Leer el archivo PDF
        pdf_bytes = await file.read()
        pdf_file = io.BytesIO(pdf_bytes)

        # Extraer texto del PDF
        with pdfplumber.open(pdf_file) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        if not text:
            raise HTTPException(status_code=400, detail="No se pudo extraer texto del PDF.")

        embedding.vector_pdf(text, file)

        return {"filename": file.filename, "message": "Archivo procesado y vector almacenado correctamente."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
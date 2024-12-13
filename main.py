from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from ragapi2 import RAGSystem

app = FastAPI()
rag_system = RAGSystem()

@app.on_event("shutdown")
def shutdown_event():
    rag_system.close_connection()

# Endpoint para cargar documentos
@app.post("/upload/")
async def upload_file(file: UploadFile):
    content = await file.read()
    rag_system.add_document_to_db(content.decode())
    return {"filename": file.filename, "status": "uploaded"}

class Question(BaseModel):
    question: str

# Endpoint para realizar consultas
@app.post("/query/")
async def query_rag(prompt: Question):
    response = rag_system.query(prompt.question)
    return {"response": response}

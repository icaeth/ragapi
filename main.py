from typing import Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ragapi import RAGSystem
from embeddings import RAGEmbedding
from typing import List, Dict, Any, Union
import shutil

app = FastAPI()

class Document(BaseModel):
    page_content: str
    metadata: Dict[str, Any]

class ArrayDocument(BaseModel):
    docs: List[Document]

class Question(BaseModel):
    question: str
    img_url: Optional[str] = None  

rag_system = RAGSystem()

embedding = RAGEmbedding()

@app.post("/query/")
async def query_rag(prompt: Question):
    context = "HORARIOS ESCAPE ROOM LUNES a VIERNES 10:00 a 20:00 SÁBADO 12:00 a 22:00 DOMINGO 12:00 a 20:00 NORMAS ESCAPE ROOM 1.- se debe pagar 1 integrante por adelantado 2.- Debes llegar 15 minutos antes de la hora indicada 3.- Se debe pagar el total antes de acceder al cuarto"
    response = rag_system.query(prompt.question, prompt.img_url, context)
    #agregar la pregunta que se realiza al sistema rag
    return {"response": response[0], "question": response[1]}

@app.post("/querynoimage/")
async def query_rag(prompt: Question):
    context = "HORARIOS ESCAPE ROOM LUNES a VIERNES 10:00 a 20:00 SÁBADO 12:00 a 22:00 DOMINGO 12:00 a 20:00 NORMAS ESCAPE ROOM 1.- se debe pagar 1 integrante por adelantado 2.- Debes llegar 15 minutos antes de la hora indicada 3.- Se debe pagar el total antes de acceder al cuarto"
    response = rag_system.queryNoImage(prompt.question, context)
    return {"response": response, "question": "tbd new"}

@app.post("/queryrag/")
async def query_rag(prompt: Question):    
    response = await rag_system.queryrag(prompt.question)
    return {"response": response}

@app.post("/upload-documents/")
async def upload_course_info(courseInfo: Union[Document, ArrayDocument]):
    if isinstance(courseInfo, Document):
        documents = [courseInfo]  # Convert single document to list for uniform processing
    else:
        documents = courseInfo.docs        

    # Process documents using the embedding system
    for document in documents:
        embedding.coursedescriptions(document)
    return {"documents uploaded and processed successfully."}

@app.post("/read-documents/")
async def read_documents(prompt: Question):
    """ if not documents:
        raise HTTPException(status_code=400, detail="No documents provided") """
    response = embedding.similarity_search(prompt.question)
    return {"response": response}

@app.post("/query/")
async def query_rag(prompt: Question):
    context = "Información sobre powerBI, se entrega una imágen suministrada por el usuario como apoyo a la pregunta"
    response = rag_system.query(prompt.question, prompt.img_url, context)
    #agregar la pregunta que se realiza al sistema rag
    return {"response": response, "question": rag_system}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )
        
        # Validate content type
        if file.content_type != 'application/pdf':
            print(f"Warning: Unexpected content type: {file.content_type}")
        
        # Reset file position to start
        await file.seek(0)
        
        # Process the PDF
        try:
            await embedding.vector_pdf(file)
            return JSONResponse(
                status_code=200,
                content={
                    "filename": file.filename,
                    "message": "Archivo procesado y vector almacenado correctamente."
                }
            )
        except ValueError as ve:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing PDF: {str(ve)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        ) 
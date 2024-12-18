import os
from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

class RAGEmbedding:
    def __init__(self):
        self.connection = "postgresql+psycopg://esvanguardia:papitas@pgvector:5432/vectordb"
        self.alternative_db_connection = "postgresql+psycopg://esvanguardia:papitas@pgvector:5432/transcriptdb"
        
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        
        self.vector_store = PGVector(
            embeddings=self.embeddings,
            connection=self.connection,
            use_jsonb=True,
        )
        
        self.alternative_vector_store = PGVector(
            embeddings=OpenAIEmbeddings(model="text-embedding-3-large"),
            connection=self.alternative_db_connection,
            use_jsonb=True,
        )

    def add_documents(self, vector_store, docs):
        vector_store.add_documents(docs, ids=[doc.metadata.get('id', doc.metadata.get('source', 'unknown')) for doc in docs])

    async def vector_pdf(self, file: UploadFile):
        # Generate a temporary file path
        temp_file_path = f"temp_{file.filename}"
        try:
            # Save the uploaded file temporarily
            with open(temp_file_path, "wb") as buffer:
                buffer.write(await file.read())
            
            # Use the file path with PyPDFLoader
            loader = PyPDFLoader(temp_file_path)
            pages = list(loader.lazy_load())
            
            # Limit pages if needed
            if len(pages) > 10:
                pages = pages[:10]
            
            # Print first page content and metadata for debugging
            if pages:
                print(pages[0].page_content[:100])
                print(pages[0].metadata)
            
            # Store vectors directly using the alternative vector store
            self.add_documents(pages)
            
            return True
        
        except Exception as e:
            print(f"Error processing PDF: {e}")
            raise  # Re-raise the exception to be handled by the caller
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

# Instantiate the class
embedding = RAGEmbedding()
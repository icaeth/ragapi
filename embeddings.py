import getpass
import os
from fastapi import UploadFile, File
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from langchain_community.document_loaders import PyPDFLoader

""" apikey = os.getenv("OPENAI_API_KEY") """
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024)   


class RAGEmbedding:
  connection = "postgresql+psycopg://esvanguardia:papitas@pgvector:5432/vectordb" # Uses psycopg3!  
  vector_store = PGVector(    
      embeddings=embeddings,
      connection=connection,
      use_jsonb=True,
  )

  alternative_db_connection = "postgresql+psycopg://esvanguardia:papitas@pgvector:5432/transcriptdb"
  alternative_vector_store = PGVector(
      embeddings=OpenAIEmbeddings(model="text-embedding-3-large"),
      connection=alternative_db_connection,
      use_jsonb=True,
  )  

  def process_documents(vector_store, docs): 
    vector_store.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])

  def similarity_search_response(vector_store, term):
    results = vector_store.similarity_search(
        {term}, k=10, filter={"id": {"$in": [1, 5, 2, 9]}}
    )    
    response = []
    for doc in results:
        response.append({
            "content": doc.page_content,
            "metadata": doc.metadata
        })    
    return response
  
  async def vector_pdf(alternative_vector_store, file: UploadFile):
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
          
          # Embed documents
          embed_vectors = embeddings.embed_documents([page.page_content for page in pages])
          
          # Store vectors
          with alternative_vector_store as store:
              store.add_documents(pages, ids=[file.filename])
          
          return True
      
      except Exception as e:
          print(f"Error processing PDF: {e}")

      finally:
          # Clean up temporary file
          if os.path.exists(temp_file_path):
              os.remove(temp_file_path)


    

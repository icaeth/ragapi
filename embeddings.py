import getpass
import os
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
  
  async def vector_pdf(alternative_vector_store, file):
    # Vectorizar el texto extraído
        loader = PyPDFLoader(file)
        pages = []
        async for page in loader.alazy_load():
          pages.append(page)
        
        embed_vectors= embeddings.embed_documents(pages)

        # Establecer conexión a la base de datos alternativa y almacenar el vector
        with alternative_vector_store as store:
            store.add_documents([{"content": embed_vectors}], ids=[file.filename])



    

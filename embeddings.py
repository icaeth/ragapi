import getpass
import os
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector

""" apikey = os.getenv("OPENAI_API_KEY") """
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024)   


class RAGEmbedding:
  connection = "postgresql+psycopg://esvanguardia:papitas@pgvector:5432"  # Uses psycopg3!
  collection_name = "vectordb"
  vector_store = PGVector(    
      embeddings=embeddings,
      collection_name=collection_name,
      connection=connection,
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



    

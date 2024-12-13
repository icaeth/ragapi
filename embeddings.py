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

  docs = [
    Document(
        page_content="there are cats in the pond",
        metadata={"id": 1, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="ducks are also found in the pond",
        metadata={"id": 2, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="fresh apples are available at the market",
        metadata={"id": 3, "location": "market", "topic": "food"},
    ),
    Document(
        page_content="the market also sells fresh oranges",
        metadata={"id": 4, "location": "market", "topic": "food"},
    ),
    Document(
        page_content="the new art exhibit is fascinating",
        metadata={"id": 5, "location": "museum", "topic": "art"},
    ),
    Document(
        page_content="a sculpture exhibit is also at the museum",
        metadata={"id": 6, "location": "museum", "topic": "art"},
    ),
    Document(
        page_content="a new coffee shop opened on Main Street",
        metadata={"id": 7, "location": "Main Street", "topic": "food"},
    ),
    Document(
        page_content="the book club meets at the library",
        metadata={"id": 8, "location": "library", "topic": "reading"},
    ),
    Document(
        page_content="the library hosts a weekly story time for kids",
        metadata={"id": 9, "location": "library", "topic": "reading"},
    ),
    Document(
        page_content="a cooking class for beginners is offered at the community center",
        metadata={"id": 10, "location": "community center", "topic": "classes"},
    ),
]

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



    

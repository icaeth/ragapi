import os
import psycopg2
from psycopg2.extras import execute_values
from fastapi import HTTPException
from langchain_openai import OpenAIEmbeddings

class RAGEmbedding:
    def __init__(self):
        # Initialize OpenAI Embeddings
        self.embedding_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        
        # Establish database connection
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

    def process_documents(self, documents):
        with self.conn.cursor() as cur:
            for doc in documents:
                try:
                    # Generate the embedding
                    embedding = self.embedding_model.embed(doc.content)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")
                
                try:
                    # Store in the database
                    execute_values(cur, """
                        INSERT INTO documents (content, embedding) VALUES %s
                    """, [(doc.content, embedding.tolist())])
                except Exception as e:
                    self.conn.rollback()
                    raise HTTPException(status_code=500, detail=f"Database insertion failed: {str(e)}")

            self.conn.commit()
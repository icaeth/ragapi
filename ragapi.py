import os
from dotenv import load_dotenv
import openai  # Ensure you have the OpenAI library installed

load_dotenv()

class RAGSystem:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def query(self, query_text, context):
        # Using the updated ChatCompletion API
        response = openai.chat.completions.create (
            model="gpt-4o",            
            messages=[
                {
                    "role": "system",
                    "content": f"Contexto relevante de Power BI recuperado:\n{context}\n\n"
                               f"Eres un experto en Power BI con experiencia en análisis de datos y reportes interactivos."
                },
                {
                    "role": "user",
                    "content": f"Consulta del Usuario: {query_text}"
                }
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"],
        )
        return response.choices[0].message['content']
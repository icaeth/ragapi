import os
from dotenv import load_dotenv
import openai  # Ensure you have the OpenAI library installed

load_dotenv()

class RAGSystem:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def query(self, query_text, context):
        # Configure the language model
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=f"Contexto relevante de Power BI recuperado:\n{context}\n\n"
                   f"Eres un experto en Power BI con experiencia en análisis de datos y reportes interactivos. "
                   f"Responde a la siguiente consulta usando exclusivamente el contexto relevante proporcionado en español.\n\n"
                   f"Consulta del Usuario: {query_text} \n\nRespuesta experta:",
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        return response.choices[0].text

    # Removed close_connection since there is no such method for this API usage

# Usage example
# rag_system = RAGSystem()
# response = rag_system.query("Tu consulta aquí", "contexto relevante aquí")
# print(response)
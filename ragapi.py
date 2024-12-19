import os
from dotenv import load_dotenv
import openai 
from embeddings import RAGEmbedding

load_dotenv()

embedding = RAGEmbedding()

class RAGSystem:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def query(self, question, img_url, context):
        # Using the updated ChatCompletion API
        response = openai.chat.completions.create (
            model="gpt-4o",            
            messages=[
                {
                    "role": "system",
                    "content": f"Eres un experton en Power BI:\n{context}\n\n"
                               f"Eres un experto en Power BI con experiencia en análisis de datos y reportes interactivos."
                },{                
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image_url",
                    "image_url": {"url": f"{img_url}"}}]}
            ],
            temperature=0.9,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"],
        )
        answer =  response.choices[0].message.content
              
        return [answer, response.object] 
    
    def queryNoImage(self, question, context):
        # Using the updated ChatCompletion API
        response = openai.chat.completions.create (
            model="gpt-4o",            
            messages=[
                {
                    "role": "system",
                    "content": f"Eres un experto en Power BI:\n{context}\n\n"
                               f"Eres un experto en Power BI con experiencia en análisis de datos y reportes interactivos."
                },{                
                    "role": "user",
                    "content": question}],
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"],
        )
        return response.choices[0].message.content
    
    async def queryrag(self, question):
        #similarity search ragsystem
        context = await embedding.similarity_search(query=question)
        messages = [
                {
                    "role": "system",
                    "content": f"Eres un experto en Power BI con este contexto:\n{context}\n\n"
                               f"Eres un experto en Power BI con experiencia en análisis de datos y reportes interactivos."
                },{                
                    "role": "user",
                    "content": question}]

        # Using the updated ChatCompletion API
        response = await openai.chat.completions.create(
            model="gpt-4o",            
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"],
        )
        return [response.choices[0].message.content, messages ]
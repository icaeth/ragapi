import os
import psycopg2
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

class RAGSystem:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.embeddings = OpenAIEmbeddings()

        # Configurar conexión a la base de datos PostgreSQL
        self.connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )

    def add_document_to_db(self, document_content):
        # Crear vector de incrustación
        vector = self.embeddings.embed(document_content)

        # Insertar documento y vector en la base de datos
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO document_vectors (document_content, embedding) VALUES (%s, %s::vector)",
                (document_content, vector.tolist())
            )
            self.connection.commit()

    def query(self, query_text):
        # Generar el vector de la consulta
        query_embedding = self.embeddings.embed(query_text)

        query_embedding_str = ','.join(map(str, query_embedding))
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT document_content, document_id, embedding <-> %s::vector AS distance
                FROM document_vectors
                ORDER BY distance ASC
                LIMIT 5;
            """, (query_embedding_str,))

            # Obtener los documentos más relevantes
            results = cursor.fetchall()

            if not results:
                return "No relevant documents found."

            # Crear un prompt combinado a partir de los resultados
            context = "\n\n".join([res[0] for res in results])

        # Configurar el modelo de lenguaje
        llm = OpenAI(
    api_key=self.api_key,
    model='gpt-3.5-turbo',
    temperature=0.7,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    n=1,
    stop=["\n"],
    logprobs=5,
    echo=False,
    stream=False
)

        # Construir el prompt extendido
        enhanced_prompt = f"Contexto relevante de Power BI recuperado:\n{context}\n\n Eres un experto en Power BI con experiencia en análisis de datos y reportes interactivos. Responde a la siguiente consulta usando exclusivamente el contexto relevante proporcionado en español.\n\nConsulta del Usuario: {query_text} \n\nRespuesta experta:"

        # Generar la respuesta usando LLM
        response = llm(enhanced_prompt)

        return response

    def close_connection(self):
        self.connection.close()

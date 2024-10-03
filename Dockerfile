# Usa una imagen base oficial de Python
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y el código
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 3000

# Define el comando de ejecución
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
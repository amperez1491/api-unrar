# Usamos una imagen base compatible con Coolify
FROM python:3.11-slim

# Instalamos unrar para que rarfile funcione
RUN apt-get update && \
    apt-get install -y unrar && \
    apt-get clean

# Directorio de trabajo
WORKDIR /app

# Copiamos dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiamos el código
COPY app.py .

# Puerto que usará la app
EXPOSE 5000

# Comando para iniciar la app
CMD ["python", "app.py"]
FROM python:3.11

# Añadir repositorio con soporte non-free
RUN apt-get update && \
    apt-get install -y unrar-free && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]

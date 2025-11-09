FROM python:3.12-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/
COPY src /app/src
COPY scripts /app/scripts

RUN mkdir -p /app/data && \
    mkdir -p /app/src/media

WORKDIR /app/src
RUN echo "Atualizando pip..." && \
    pip install --upgrade pip && \
    echo "Instalando dependências..." && \
    pip install -r requirements.txt

CMD ["python", "app.py"]

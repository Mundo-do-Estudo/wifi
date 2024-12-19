# Use uma imagem base que suporte dbus, como uma imagem com Ubuntu
FROM python:3.11-slim

# Instalar dependências do sistema, incluindo o dbus
RUN apt-get update && \
    apt-get install -y dbus libdbus-1-3 && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependências do Python
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para o container
COPY . /app/

# Expor a porta onde a app vai rodar
EXPOSE 5000

# Comando para rodar a aplicação com Gunicorn
CMD ["gunicorn", "app:app"]

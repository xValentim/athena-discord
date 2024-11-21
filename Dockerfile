# Usa a imagem base do Python
FROM python:3.10

# Define o diretório de trabalho
WORKDIR /app

# Copia o código do bot para o contêiner
COPY . ./

# Instala as dependências (adapte se tiver requirements.txt)
RUN pip install -r requirements.txt

# Define o comando para iniciar o bot
CMD ["python", "bot.py"]
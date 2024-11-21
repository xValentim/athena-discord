# Usa a imagem base do Python
FROM python:3.10

# Define o diretório de trabalho
WORKDIR /app

# Copia o código do app para o contêiner
COPY . ./

# Instala as dependências (adapte se tiver requirements.txt)
RUN pip install -r requirements.txt

# Define o comando para iniciar o app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.8

# "non-prod", "prod"
ENV ENVIRONMENT="non-prod"          

# Configure o diretório de trabalho
WORKDIR /app

# Copie os arquivos do seu aplicativo Python para o contêiner
COPY . /app

# Instale as dependências Python, se necessário
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "publishAudioTCP.py"] 


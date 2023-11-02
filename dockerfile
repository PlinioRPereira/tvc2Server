FROM python:3.8

# "non-prod", "prod"
ENV ENVIRONMENT="non-prod"          

# Configure o diretório de trabalho
WORKDIR /app

# Copie os arquivos do seu aplicativo Python para o contêiner
COPY . /app

# Instale as dependências Python, se necessário
RUN pip freeze > dependencies.txt
RUN pip install -r dependencies.txt

# Inicie seu aplicativo Python usando o PM2
CMD ["publishAudioTCP.py"]

Server for TVC2 device


# Commands
pip freeze > dependencies.txt       - Generates the dependencies.txt file 
docker build -t tvc2server:latest .
docker run -e ENVIRONMENT="prod" tvc2server:latest



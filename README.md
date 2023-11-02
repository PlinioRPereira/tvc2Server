Server for TVC2 device


# Util Commands
pipenv install requests - https://packaging.python.org/pt-br/latest/tutorials/managing-dependencies/
pip freeze > dependencies.txt       - Generates the dependencies.txt file 
docker build -t tvc2server:latest .
docker run -e ENVIRONMENT="prod" tvc2server:latest

https://github.com/veirs/sounddevice    - Using audio inside a container

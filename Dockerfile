# Use uma imagem base Python
FROM python:3.11

# Defina o diretório de trabalho dentro do container
WORKDIR /usr/src/app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt ./

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o conteúdo do projeto para o diretório de trabalho
COPY . .

# Exponha a porta 8000 para acesso externo
EXPOSE 8000

# Comando para iniciar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
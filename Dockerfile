# Use a imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Exponha a porta 5000
EXPOSE 5000

# Comando para rodar a aplicação (substitua `app.py` pelo seu arquivo principal)
CMD ["python", "app.py"]
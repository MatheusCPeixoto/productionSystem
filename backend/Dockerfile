# Use uma imagem base Python com um sistema operacional compatível (Debian 12 - bookworm é a base do Python 3.12, ou 11 - bullseye)
# O Ubuntu 22.04 é baseado em Debian 11 (bullseye), então 'python:3.12-slim-bullseye' é uma boa escolha.
# Se preferir uma base mais próxima do Ubuntu, você pode tentar 'ubuntu:22.04' e instalar o Python, mas a imagem 'python:3.12-slim-bullseye' já otimiza isso.
FROM python:3.12-slim-bullseye

# Define variáveis de ambiente para o Python no container
# PYTHONDONTWRITEBYTECODE: Impede o Python de gravar arquivos .pyc no disco (bom para Docker)
# PYTHONUNBUFFERED: Garante que o stdout/stderr do Python não seja armazenado em buffer (útil para logs em tempo real)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho antes de instalar
# Isso aproveita o cache do Docker. Se requirements.txt não mudar, esta camada não será reconstruída.
COPY requirements.txt /app/

# --- Instalação do ODBC Driver 17 para SQL Server e suas dependências ---
# Baseado nas instruções da Microsoft para Debian 11 (Bullseye)
# Fonte: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-odbc-driver-linux-unix?view=sql-server-ver16

# 1. Atualiza a lista de pacotes e instala ferramentas necessárias para o processo (curl, gnupg)
#    e 'unixodbc-dev' que é necessário para compilar o driver Python 'pyodbc'.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    unixodbc-dev

# 2. Importa a chave GPG do repositório da Microsoft
#    e adiciona o repositório MSSQL para Debian 11 (bullseye)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# 3. Atualiza a lista de pacotes novamente para incluir os pacotes do novo repositório
RUN apt-get update

# 4. Instala o ODBC Driver 17 for SQL Server.
#    'ACCEPT_EULA=Y' é necessário para aceitar os termos de licença automaticamente.
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# --- Instalação das dependências Python ---
# 'pip install --no-cache-dir' evita o armazenamento de arquivos de cache do pip, reduzindo o tamanho final da imagem.
# Certifique-se que o requirements.txt inclua:
# - Django
# - djangorestframework
# - gunicorn
# - uvicorn[standard]
# - pyodbc (para conexão SQL Server)
# - python-multipart (para tratamento de formulários, pode ser necessário com uvicorn)
# - python-dotenv (para carregar .env em ambiente de desenvolvimento, embora em prod usaremos docker-compose env_file)
# - Qualquer outra dependência do seu projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
# Isso deve ser feito após a instalação das dependências para otimizar o cache do Docker.
COPY . /app/

# Expor a porta em que a aplicação Django/Uvicorn vai rodar.
# Esta porta é usada para comunicação INTERNA dentro da rede Docker.
# O Nginx vai se comunicar com esta porta.
EXPOSE 8000

# O CMD padrão para iniciar a aplicação.
# Será sobrescrito pelo comando no 'docker-compose.yml', mas é uma boa prática ter um fallback.
# CMD ["gunicorn", "seu_projeto.asgi:application", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker"]
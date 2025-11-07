#!/bin/bash
set -e

# Atualiza o sistema e instala dependências
echo "Atulizando o sistema..."
apt-get update
apt-get upgrade -y

# echo "Instalando dependências..."
# apt-get install -y \
#     gcc \
#     git \
#     libpq-dev

echo "Removendo arquivos temporários..."
rm -rf /var/lib/apt/lists/*

# Atualiza o pip e instala dependências do projeto
echo "Atualizando pip..."
pip install --upgrade pip

echo "Instalando dependências do projeto..."
pip install --no-cache-dir -r ./requirements.txt
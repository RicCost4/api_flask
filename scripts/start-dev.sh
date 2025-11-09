#!/bin/bash
# ===============================
# Script: scripts/start-dev.sh
# ===============================

REDE="${1:-192.168.0.0}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Verificando se o Docker está rodando..."
if ! docker info >/dev/null 2>&1; then
  echo "Iniciando Docker..."
  if [[ "$OSTYPE" == "darwin"* ]]; then
    open -a Docker
  else
    sudo systemctl start docker
  fi

  echo "Aguardando Docker ficar ativo..."
  for i in {1..30}; do
    if docker info >/dev/null 2>&1; then
      echo "Docker iniciado com sucesso!"
      break
    fi
    echo "Aguardando ($i/30)..."
    sleep 5
  done
else
  echo "Docker já está em execução."
fi

# Configuração do firewall (se UFW existir)
# if command -v ufw >/dev/null 2>&1; then
#   echo "Configurando firewall UFW..."
#   sudo ufw allow from "$REDE/24" to any port 8080 proto tcp
#   echo "Porta 8080 liberada para $REDE/24."
# else
#   echo "UFW não encontrado — pulando configuração de firewall."
# fi

# Subir o container a partir da raiz do projeto
cd "$PROJECT_ROOT"
echo "Subindo container em modo desenvolvimento..."
docker compose -f container/docker-compose-dev.yml up -d

# Mostrar logs
echo "Mostrando últimos logs..."
docker logs --tail 100 -f api-flask-csv-container

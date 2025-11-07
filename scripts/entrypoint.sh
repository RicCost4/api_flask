#!/bin/bash
set -e

# Exibe mensagens no log para depuração
echo "Iniciando container com debugpy ativo..."

# Instala o ambiente de desenvolvimento
echo "Instalando ambiente de desenvolvimento..."
bash /app/scripts/install-ambiente-dev.sh

echo "Container iniciado, executo o script ../scripts/debug_init.sh para iniciar o debugpy.."
exec bash

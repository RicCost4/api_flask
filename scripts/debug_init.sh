#!/bin/bash
set -e

# Executa o app com debugpy
echo "Executando: python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py"
exec python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py

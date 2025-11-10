import pandas as pd  # type: ignore
from pathlib import Path


def migration_003():
    """Cria o arquivo pedidos.csv (se não existir)"""
    caminho = Path("../data/pedidos.csv")
    if not caminho.exists():
        df = pd.DataFrame(columns=["id", "cliente_id", "valor", "data"])
        df.to_csv(caminho, index=False)
        print("📦 Migration: 'pedidos.csv' criado com sucesso.")

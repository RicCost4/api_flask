import pandas as pd # type: ignore
from pathlib import Path

def migration_004():
    caminho = Path("data/usuarios.csv")
    if not caminho.exists():
        df = pd.DataFrame(columns=["id", "username", "senha", "tipo"])
        df.to_csv(caminho, index=False)
        print("🆕 Migration: 'usuarios.csv' criado com sucesso.")

import pandas as pd  # type: ignore
from pathlib import Path

from metodos.cache import get_cache

from services.db_usuarios import criar_usuario


def migration_004():
    caminho = Path("../data/usuarios.csv")
    if not caminho.exists():
        df = pd.DataFrame(columns=["id", "username", "senha", "tipo"])
        df.to_csv(caminho, index=False)
        print("Migration: 'usuarios.csv' criado com sucesso.")
    else:
        print("Arquivo de usuários já existe.")

    df = get_cache("usuarios", caminho)
    if "admin" not in df["username"].values:
        criar_usuario("admin", "admin123", tipo="interno")
        print("Usuário admin criado com senha padrão 'admin123'")
    else:
        print("Usuário admin já existe.")

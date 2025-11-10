import pandas as pd  # type: ignore
from pathlib import Path


def migration_002():
    """Adiciona coluna 'telefone' com valor padrão vazio."""
    caminho = Path("../data/clientes.csv")
    df = pd.read_csv(caminho)
    if "telefone" not in df.columns:
        df["telefone"] = ""
        df.to_csv(caminho, index=False)
        print("Coluna 'telefone' adicionada com sucesso!")

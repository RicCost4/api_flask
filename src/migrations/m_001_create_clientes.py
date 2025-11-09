import pandas as pd # type: ignore
from pathlib import Path


def migration_001():
    """Cria o arquivo inicial de clientes"""
    caminho = Path("../data/clientes.csv")
    df = pd.DataFrame(columns=["id", "nome", "email", "idade", "cidade"])
    df.to_csv(caminho, index=False)

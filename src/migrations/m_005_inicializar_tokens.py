import pandas as pd # type: ignore
from pathlib import Path


def migration_005():
    caminho = Path("../data/datatokens.csv")

    if not caminho.exists():
        df = pd.DataFrame(columns=["token", "username", "tipo", "expira_em", "revogado"])
        df.to_csv(caminho, index=False)
        print("Arquivo de tokens criado.")

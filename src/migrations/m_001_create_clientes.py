import pandas as pd # type: ignore

def migration_001(arquivo):
    """Cria o arquivo inicial de clientes"""
    df = pd.DataFrame(columns=["id", "nome", "email", "idade", "cidade"])
    df.to_csv(arquivo, index=False)

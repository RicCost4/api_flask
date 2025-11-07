import pandas as pd # type: ignore

def migration_002(arquivo):
    """Adiciona coluna 'telefone' com valor padrão vazio."""
    df = pd.read_csv(arquivo)
    if "telefone" not in df.columns:
        df["telefone"] = ""
        df.to_csv(arquivo, index=False)
        print("📞 Coluna 'telefone' adicionada com sucesso!")

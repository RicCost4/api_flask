import pandas as pd  # type: ignore
from pathlib import Path
from metodos.cache import get_cache

DATA_DIR = Path("data")
ARQUIVO = DATA_DIR / "clientes.csv"


def ler_todos():
    return get_cache("clientes", ARQUIVO)


def salvar(df):
    df.to_csv(ARQUIVO, index=False)


def adicionar_cliente(nome, email, idade, cidade, telefone):
    df = ler_todos()
    novo_id = int(df["id"].max() + 1) if not df.empty else 1
    novo = pd.DataFrame([{
        "id": novo_id,
        "nome": nome,
        "email": email,
        "idade": idade,
        "cidade": cidade,
        "telefone": telefone
    }])
    df = pd.concat([df, novo], ignore_index=True)
    salvar(df)
    return novo.iloc[0].to_dict()


def obter_cliente(id_cliente):
    df = ler_todos()
    cliente = df[df["id"] == id_cliente]
    return cliente.iloc[0].to_dict() if not cliente.empty else None


def atualizar_cliente(id_cliente, dados):
    df = ler_todos()
    if id_cliente not in df["id"].values:
        return None
    for campo, valor in dados.items():
        if campo in df.columns and valor is not None:
            df.loc[df["id"] == id_cliente, campo] = valor
    salvar(df)
    return obter_cliente(id_cliente)


def excluir_cliente(id_cliente):
    df = ler_todos()
    if id_cliente not in df["id"].values:
        return False
    df = df[df["id"] != id_cliente]
    salvar(df)
    return True


def filtrar_clientes(cidade=None, idade_min=None, idade_max=None):
    df = ler_todos()
    if cidade:
        df = df[df["cidade"].str.contains(cidade, case=False, na=False)]
    if idade_min is not None:
        df = df[df["idade"] >= idade_min]
    if idade_max is not None:
        df = df[df["idade"] <= idade_max]
    return df.to_dict(orient="records")


def exportar_excel():
    df = ler_todos()
    caminho = Path("media/clientes_exportados.xlsx")
    df.to_excel(caminho, index=False)
    return str(caminho)

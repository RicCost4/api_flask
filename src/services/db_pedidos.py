import pandas as pd # type: ignore
from pathlib import Path
from services.db_clientes import ler_todos as ler_clientes
from metodos.cache import get_cache

ARQUIVO = Path("../data/pedidos.csv")


def ler_pedidos():
    return get_cache("pedidos", ARQUIVO)

def salvar_pedidos(df):
    df.to_csv(ARQUIVO, index=False)

def adicionar_pedido(cliente_id: int, valor: float, data: str):
    clientes = ler_clientes()
    if cliente_id not in clientes["id"].values:
        raise ValueError(f"Cliente ID {cliente_id} não encontrado!")

    pedidos = ler_pedidos()
    novo_id = int(pedidos["id"].max() + 1) if not pedidos.empty else 1

    novo = pd.DataFrame([{
        "id": novo_id,
        "cliente_id": cliente_id,
        "valor": valor,
        "data": data
    }])

    pedidos = pd.concat([pedidos, novo], ignore_index=True)
    salvar_pedidos(pedidos)
    print(f"Pedido criado para cliente ID {cliente_id} no valor de R$ {valor:.2f}")

def listar_pedidos_com_clientes():
    pedidos = ler_pedidos()
    clientes = ler_clientes()

    if pedidos.empty or clientes.empty:
        return []

    # Fazendo o “join” (equivalente a um INNER JOIN SQL)
    df = pedidos.merge(clientes, left_on="cliente_id", right_on="id", suffixes=("_pedido", "_cliente"))
    # Selecionando colunas mais amigáveis
    df = df[["id_pedido", "cliente_id", "nome", "valor", "data", "cidade"]]
    return df.to_dict(orient="records")

def listar_pedidos_por_cliente(cliente_id: int):
    pedidos = ler_pedidos()
    clientes = ler_clientes()

    if pedidos.empty:
        return []

    df = pedidos.merge(clientes, left_on="cliente_id", right_on="id", suffixes=("_pedido", "_cliente"))
    df = df[df["cliente_id"] == cliente_id]

    if df.empty:
        return []

    df = df[["id_pedido", "cliente_id", "nome", "valor", "data", "cidade"]]
    return df.to_dict(orient="records")
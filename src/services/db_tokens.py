import pandas as pd  # type: ignore
from pathlib import Path
import time
from metodos.cache import get_cache

ARQUIVO = Path("../data/tokens.csv")


def inicializar_tokens():
    if not ARQUIVO.exists():
        df = pd.DataFrame(columns=["token", "username", "tipo", "expira_em", "revogado"])
        df.to_csv(ARQUIVO, index=False)
        print("Arquivo de tokens criado.")


def salvar_token(token: str, username: str, tipo: str, expira_em: int):
    df = ler_todos()
    nova_linha = pd.DataFrame([{
        "token": token,
        "username": username,
        "tipo": tipo,
        "expira_em": expira_em,
        "revogado": False
    }])
    df = pd.concat([df, nova_linha], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)


def ler_todos():
    return get_cache("tokens", ARQUIVO)


def revogar_token(token: str):
    df = pd.read_csv(ARQUIVO)
    df.loc[df["token"] == token, "revogado"] = True
    df.to_csv(ARQUIVO, index=False)


def token_valido(token: str) -> bool:
    df = pd.read_csv(ARQUIVO)
    t = df[df["token"] == token]
    if t.empty:
        return False
    linha = t.iloc[0]
    if linha["revogado"]:
        return False
    if linha["expira_em"] < time.time():
        return False
    return True

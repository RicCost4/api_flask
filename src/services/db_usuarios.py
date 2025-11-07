import pandas as pd # type: ignore
from pathlib import Path
import hashlib
from metodos.cache import get_cache

ARQUIVO = Path("data/usuarios.csv")

def inicializar_usuarios():
    if not ARQUIVO.exists():
        df = pd.DataFrame(columns=["id", "username", "senha", "tipo"])
        df.to_csv(ARQUIVO, index=False)
        print("🧑‍💻 Arquivo de usuários criado.")
    else:
        print("📂 Arquivo de usuários já existe.")

    df = ler_todos()
    if "admin" not in df["username"].values:
        criar_usuario("admin", "admin123", tipo="interno")
        print("✅ Usuário admin criado com senha padrão 'admin123'")
    else:
        print("👤 Usuário admin já existe.")

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_usuario(username: str, senha: str, tipo="interno"):
    df = ler_todos()
    if username in df["username"].values:
        raise ValueError("Usuário já existe!")

    novo_id = int(df["id"].max() + 1) if not df.empty else 1
    nova_linha = pd.DataFrame([{
        "id": novo_id,
        "username": username,
        "senha": hash_senha(senha),
        "tipo": tipo
    }])
    df = pd.concat([df, nova_linha], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)
    print(f"✅ Usuário '{username}' criado ({tipo}).")

def ler_todos():
    return get_cache("usuarios", ARQUIVO)

def validar_usuario(username: str, senha: str, tipo="interno") -> bool:
    df = ler_todos()
    if df.empty:
        return False
    hash_input = hash_senha(senha)
    usuario = df[(df["username"] == username) & (df["senha"] == hash_input) & (df["tipo"] == tipo)]
    return not usuario.empty

def alterar_senha(username: str, senha_atual: str, nova_senha: str) -> tuple[bool, str]:
    df = ler_todos()
    if df.empty:
        return False, "Nenhum usuário encontrado."

    usuario = df[df["username"] == username]
    if usuario.empty:
        return False, "Usuário não encontrado."

    senha_hash = hash_senha(senha_atual)
    if usuario.iloc[0]["senha"] != senha_hash:
        return False, "Senha atual incorreta."

    df.loc[df["username"] == username, "senha"] = hash_senha(nova_senha)
    df.to_csv(ARQUIVO, index=False)
    return True, "Senha alterada com sucesso!"

def criar_usuario_admin(username: str, senha: str, tipo: str = "interno") -> tuple[bool, str]:
    try:
        criar_usuario(username, senha, tipo)
        return True, f"Usuário '{username}' criado com sucesso!"
    except ValueError as e:
        return False, str(e)
from pathlib import Path

from migrations import MIGRATIONS

VERSAO_ARQUIVO = Path("../data/schema_version.txt")

# Versão atual do schema, mudar a cada nova migração colocada
VERSAO_ATUAL = 5


def obter_versao_atual():
    if not VERSAO_ARQUIVO.exists():
        return 0
    return int(VERSAO_ARQUIVO.read_text().strip())


def salvar_versao(versao: int):
    VERSAO_ARQUIVO.write_text(str(versao))


def inicializar_csv():
    versao_atual = obter_versao_atual()

    print(f"Versão atual do schema: {versao_atual}")

    # Se já existe, aplicar migrações
    if versao_atual < VERSAO_ATUAL:
        aplicar_migracoes(versao_atual)
        salvar_versao(VERSAO_ATUAL)
        print(f"CSV atualizado para versão {VERSAO_ATUAL}")


def aplicar_migracoes(versao_antiga: int):
    """Executa migrações incrementais até atingir a versão atual"""
    print("Aplicando migrações...")
    for versao, func in MIGRATIONS.items():
        if versao_antiga < versao <= VERSAO_ATUAL:
            print(f"Aplicando migration {versao:03d}...")
            func()
from pathlib import Path

DATA_DIR = Path("data")
VERSAO_ARQUIVO = DATA_DIR / "projeto_version.txt"

def obter_versao_atual_projeto():
    if not VERSAO_ARQUIVO.exists():
        return '1.0.0-alpha'
    return VERSAO_ARQUIVO.read_text().strip()
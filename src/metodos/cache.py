import pandas as pd # type: ignore
from pathlib import Path
import time

CACHE = {}
CACHE_TTL = 5  # segundos

def get_cache(chave: str, caminho: Path) -> pd.DataFrame:
    """Retorna um DataFrame a partir do cache ou do arquivo CSV."""
    agora = time.time()
    info = CACHE.get(chave)

    if info and agora - info["timestamp"] < CACHE_TTL:
        return info["data"]

    df = pd.read_csv(caminho)
    CACHE[chave] = {"timestamp": agora, "data": df}
    return df

from .m_001_create_clientes import migration_001
from .m_002_add_coluna_telefone import migration_002
from .m_003_create_pedidos import migration_003
from .m_004_create_usuarios import migration_004
from .m_005_inicializar_tokens import migration_005

MIGRATIONS = {
    1: migration_001,
    2: migration_002,
    3: migration_003,
    4: migration_004,
    5: migration_005
}

import sqlite3
from contextlib import contextmanager

ESQUEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    papel TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS barbearias (
    id TEXT PRIMARY KEY,
    dono_id TEXT NOT NULL,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL,
    bairro TEXT NOT NULL,
    bairro_chave TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    regras TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS ix_barbearias_bairro ON barbearias(bairro_chave);
CREATE TABLE IF NOT EXISTS cadeiras (
    id TEXT PRIMARY KEY,
    barbearia_id TEXT NOT NULL REFERENCES barbearias(id),
    posicao INTEGER NOT NULL,
    nome TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS horarios_ociosos (
    id TEXT PRIMARY KEY,
    barbearia_id TEXT NOT NULL REFERENCES barbearias(id),
    cadeira_id TEXT NOT NULL REFERENCES cadeiras(id),
    inicio TEXT NOT NULL,
    fim TEXT NOT NULL,
    preco_por_hora_centavos INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS blocos (
    id TEXT PRIMARY KEY,
    barbearia_id TEXT NOT NULL REFERENCES barbearias(id),
    horario_ocioso_id TEXT NOT NULL REFERENCES horarios_ociosos(id),
    cadeira_id TEXT NOT NULL REFERENCES cadeiras(id),
    barbeiro_id TEXT NOT NULL,
    inicio TEXT NOT NULL,
    fim TEXT NOT NULL,
    valor_centavos INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_blocos_barbeiro ON blocos(barbeiro_id);
CREATE TABLE IF NOT EXISTS servicos (
    id TEXT PRIMARY KEY,
    barbeiro_id TEXT NOT NULL,
    nome TEXT NOT NULL,
    preco_centavos INTEGER NOT NULL,
    duracao_minutos INTEGER NOT NULL
);
"""


class BancoSQLite:
    """Abre uma conexão por operação, o que é seguro entre threads do Flask."""

    def __init__(self, caminho: str):
        self._caminho = caminho

    @contextmanager
    def conexao(self):
        con = sqlite3.connect(self._caminho)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        try:
            yield con
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def criar_tabelas(self) -> None:
        with self.conexao() as con:
            con.executescript(ESQUEMA)

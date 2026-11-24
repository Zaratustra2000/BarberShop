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

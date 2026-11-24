import sqlite3
from contextlib import contextmanager

ESQUEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    papel TEXT NOT NULL,
    apresentacao TEXT NOT NULL DEFAULT '',
    foto_perfil TEXT NOT NULL DEFAULT ''
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
    regras TEXT NOT NULL DEFAULT '',
    foto_principal TEXT NOT NULL DEFAULT '',
    ativa INTEGER NOT NULL DEFAULT 1
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
CREATE TABLE IF NOT EXISTS agendamentos (
    id TEXT PRIMARY KEY,
    cliente_id TEXT NOT NULL,
    barbeiro_id TEXT NOT NULL,
    servico_id TEXT NOT NULL,
    servico_nome TEXT NOT NULL,
    barbearia_id TEXT NOT NULL,
    bloco_id TEXT NOT NULL,
    inicio TEXT NOT NULL,
    fim TEXT NOT NULL,
    preco_centavos INTEGER NOT NULL,
    cancelado INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_agendamentos_barbeiro
    ON agendamentos(barbeiro_id);
CREATE INDEX IF NOT EXISTS ix_agendamentos_cliente
    ON agendamentos(cliente_id);
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
            colunas = {
                coluna["name"]
                for coluna in con.execute("PRAGMA table_info(barbearias)")
            }
            if "foto_principal" not in colunas:
                con.execute(
                    "ALTER TABLE barbearias "
                    "ADD COLUMN foto_principal TEXT NOT NULL DEFAULT ''")
            colunas = {
                coluna["name"]
                for coluna in con.execute("PRAGMA table_info(barbearias)")
            }
            if "ativa" not in colunas:
                con.execute(
                    "ALTER TABLE barbearias "
                    "ADD COLUMN ativa INTEGER NOT NULL DEFAULT 1")
            colunas = {
                coluna["name"]
                for coluna in con.execute("PRAGMA table_info(usuarios)")
            }
            if "apresentacao" not in colunas:
                con.execute(
                    "ALTER TABLE usuarios "
                    "ADD COLUMN apresentacao TEXT NOT NULL DEFAULT ''")
            if "foto_perfil" not in colunas:
                con.execute(
                    "ALTER TABLE usuarios "
                    "ADD COLUMN foto_perfil TEXT NOT NULL DEFAULT ''")
            colunas = {
                coluna["name"]
                for coluna in con.execute("PRAGMA table_info(agendamentos)")
            }
            if "cancelado" not in colunas:
                con.execute(
                    "ALTER TABLE agendamentos "
                    "ADD COLUMN cancelado INTEGER NOT NULL DEFAULT 0")

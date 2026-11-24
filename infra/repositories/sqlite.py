"""Adapters SQLite das portas de repositório (veja docs/adr/0002)."""
from domain.usuario import Papel, Usuario
from use_cases.portas import (
    RepositorioDeAgendamentos,
    RepositorioDeBarbearias,
    RepositorioDeServicos,
    RepositorioDeUsuarios,
)


class RepositorioDeUsuariosSQLite(RepositorioDeUsuarios):
    def __init__(self, banco):
        self._banco = banco

    def salvar(self, usuario):
        with self._banco.conexao() as con:
            con.execute(
                "INSERT INTO usuarios (id, nome, email, senha_hash, papel) "
                "VALUES (?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET "
                "nome = excluded.nome, email = excluded.email, "
                "senha_hash = excluded.senha_hash, papel = excluded.papel",
                (usuario.id, usuario.nome, usuario.email, usuario.senha_hash,
                 usuario.papel.value))

    def por_id(self, usuario_id):
        return self._um("SELECT * FROM usuarios WHERE id = ?", usuario_id)

    def por_email(self, email):
        return self._um("SELECT * FROM usuarios WHERE email = ?", email)

    def _um(self, sql, *parametros):
        with self._banco.conexao() as con:
            linha = con.execute(sql, parametros).fetchone()
        return _usuario(linha) if linha else None


def _usuario(linha):
    return Usuario(id=linha["id"], nome=linha["nome"], email=linha["email"],
                   senha_hash=linha["senha_hash"],
                   papel=Papel(linha["papel"]))


class RepositorioDeBarbeariasSQLite(RepositorioDeBarbearias):
    def __init__(self, banco):
        self._banco = banco


class RepositorioDeServicosSQLite(RepositorioDeServicos):
    def __init__(self, banco):
        self._banco = banco


class RepositorioDeAgendamentosSQLite(RepositorioDeAgendamentos):
    def __init__(self, banco):
        self._banco = banco

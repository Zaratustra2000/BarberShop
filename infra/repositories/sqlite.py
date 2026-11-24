"""Adapters SQLite das portas de repositório (veja docs/adr/0002)."""
from datetime import datetime

from domain.agendamento import Agendamento
from domain.barbearia import (Barbearia, BlocoDeHorario, Cadeira,
                              HorarioOcioso)
from domain.periodo import Periodo
from domain.servico import Servico
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

    def barbeiros_por_nome(self, trecho):
        # O filtro por trecho é feito em Python porque o LOWER do SQLite
        # só converte letras ASCII (nomes como "Ítalo" falhariam).
        with self._banco.conexao() as con:
            linhas = con.execute(
                "SELECT * FROM usuarios WHERE papel = ? ORDER BY nome, id",
                (Papel.BARBEIRO.value,)).fetchall()
        trecho = trecho.lower()
        return [_usuario(linha) for linha in linhas
                if trecho in linha["nome"].lower()]

    def _um(self, sql, *parametros):
        with self._banco.conexao() as con:
            linha = con.execute(sql, parametros).fetchone()
        return _usuario(linha) if linha else None


def _usuario(linha):
    return Usuario(id=linha["id"], nome=linha["nome"], email=linha["email"],
                   senha_hash=linha["senha_hash"],
                   papel=Papel(linha["papel"]))


class RepositorioDeBarbeariasSQLite(RepositorioDeBarbearias):
    """Grava o agregado inteiro numa transação (ADR 0001)."""

    def __init__(self, banco):
        self._banco = banco

    def remover(self, barbearia_id):
        with self._banco.conexao() as con:
            con.execute("DELETE FROM agendamentos WHERE barbearia_id = ?",
                        (barbearia_id,))
            con.execute("DELETE FROM blocos WHERE barbearia_id = ?",
                        (barbearia_id,))
            con.execute(
                "DELETE FROM horarios_ociosos WHERE barbearia_id = ?",
                (barbearia_id,))
            con.execute("DELETE FROM cadeiras WHERE barbearia_id = ?",
                        (barbearia_id,))
            con.execute("DELETE FROM barbearias WHERE id = ?",
                        (barbearia_id,))

    def salvar(self, barbearia):
        with self._banco.conexao() as con:
            con.execute(
                "INSERT INTO barbearias (id, dono_id, nome, endereco, bairro,"
                " bairro_chave, latitude, longitude, regras, foto_principal,"
                " ativa) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET nome = excluded.nome, "
                "endereco = excluded.endereco, bairro = excluded.bairro, "
                "bairro_chave = excluded.bairro_chave, "
                "latitude = excluded.latitude, "
                "longitude = excluded.longitude, regras = excluded.regras, "
                "foto_principal = excluded.foto_principal, "
                "ativa = excluded.ativa",
                (barbearia.id, barbearia.dono_id, barbearia.nome,
                 barbearia.endereco, barbearia.bairro, barbearia.bairro_chave,
                 barbearia.latitude, barbearia.longitude, barbearia.regras,
                 barbearia.foto_principal, 1 if barbearia.ativa else 0))
            ids_presentes = [c.id for c in barbearia.cadeiras]
            if ids_presentes:
                placeholders = ",".join("?" for _ in ids_presentes)
                con.execute(
                    "DELETE FROM cadeiras WHERE barbearia_id = ? "
                    "AND id NOT IN ({})".format(placeholders),
                    (barbearia.id, *ids_presentes))
            else:
                con.execute(
                    "DELETE FROM cadeiras WHERE barbearia_id = ?",
                    (barbearia.id,))
            con.executemany(
                "INSERT INTO cadeiras "
                "(id, barbearia_id, posicao, nome) VALUES (?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET "
                "barbearia_id = excluded.barbearia_id, "
                "posicao = excluded.posicao, nome = excluded.nome",
                [(c.id, barbearia.id, posicao, c.nome)
                 for posicao, c in enumerate(barbearia.cadeiras)])
            ids_blocos = [b.id for b in barbearia.blocos]
            if ids_blocos:
                placeholders = ",".join("?" for _ in ids_blocos)
                con.execute(
                    "DELETE FROM blocos WHERE barbearia_id = ? "
                    "AND id NOT IN ({})".format(placeholders),
                    (barbearia.id, *ids_blocos))
            else:
                con.execute(
                    "DELETE FROM blocos WHERE barbearia_id = ?",
                    (barbearia.id,))
            ids_horarios = [h.id for h in barbearia.horarios_ociosos]
            if ids_horarios:
                placeholders = ",".join("?" for _ in ids_horarios)
                con.execute(
                    "DELETE FROM horarios_ociosos WHERE barbearia_id = ? "
                    "AND id NOT IN ({})".format(placeholders),
                    (barbearia.id, *ids_horarios))
            else:
                con.execute(
                    "DELETE FROM horarios_ociosos WHERE barbearia_id = ?",
                    (barbearia.id,))
            con.executemany(
                "INSERT INTO horarios_ociosos (id, barbearia_id, "
                "cadeira_id, inicio, fim, preco_por_hora_centavos) "
                "VALUES (?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET "
                "barbearia_id = excluded.barbearia_id, "
                "cadeira_id = excluded.cadeira_id, "
                "inicio = excluded.inicio, fim = excluded.fim, "
                "preco_por_hora_centavos = "
                "excluded.preco_por_hora_centavos",
                [(h.id, barbearia.id, h.cadeira_id, _data(h.periodo.inicio),
                  _data(h.periodo.fim), h.preco_por_hora_centavos)
                 for h in barbearia.horarios_ociosos])
            con.executemany(
                "INSERT INTO blocos (id, barbearia_id, "
                "horario_ocioso_id, cadeira_id, barbeiro_id, inicio, fim, "
                "valor_centavos) VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET "
                "barbearia_id = excluded.barbearia_id, "
                "horario_ocioso_id = excluded.horario_ocioso_id, "
                "cadeira_id = excluded.cadeira_id, "
                "barbeiro_id = excluded.barbeiro_id, "
                "inicio = excluded.inicio, fim = excluded.fim, "
                "valor_centavos = excluded.valor_centavos",
                [(b.id, barbearia.id, b.horario_ocioso_id, b.cadeira_id,
                  b.barbeiro_id, _data(b.periodo.inicio),
                  _data(b.periodo.fim), b.valor_centavos)
                 for b in barbearia.blocos])

    def por_id(self, barbearia_id):
        encontradas = self._carregar("id = ?", barbearia_id)
        return encontradas[0] if encontradas else None

    def do_dono(self, dono_id):
        return self._carregar("dono_id = ?", dono_id)

    def no_bairro(self, bairro_chave):
        return self._carregar(
            "ativa = 1 AND bairro_chave = ?", bairro_chave)

    def com_blocos_do_barbeiro(self, barbeiro_id):
        return self._carregar(
            "id IN (SELECT barbearia_id FROM blocos WHERE barbeiro_id = ?)",
            barbeiro_id)

    def _carregar(self, filtro, *parametros):
        with self._banco.conexao() as con:
            linhas = con.execute(
                "SELECT * FROM barbearias WHERE {} ORDER BY nome, id".format(
                    filtro), parametros).fetchall()
            return [self._montar(con, linha) for linha in linhas]

    def _montar(self, con, linha):
        barbearia = Barbearia(
            id=linha["id"], dono_id=linha["dono_id"], nome=linha["nome"],
            endereco=linha["endereco"], bairro=linha["bairro"],
            latitude=linha["latitude"], longitude=linha["longitude"],
            regras=linha["regras"],
            foto_principal=linha["foto_principal"],
            ativa=bool(linha["ativa"]))
        barbearia.cadeiras = [
            Cadeira(id=c["id"], nome=c["nome"]) for c in con.execute(
                "SELECT * FROM cadeiras WHERE barbearia_id = ? "
                "ORDER BY posicao", (barbearia.id,))]
        barbearia.horarios_ociosos = [
            HorarioOcioso(id=h["id"], cadeira_id=h["cadeira_id"],
                          periodo=_periodo(h),
                          preco_por_hora_centavos=h[
                              "preco_por_hora_centavos"])
            for h in con.execute(
                "SELECT * FROM horarios_ociosos WHERE barbearia_id = ? "
                "ORDER BY inicio, id", (barbearia.id,))]
        barbearia.blocos = [
            BlocoDeHorario(id=b["id"],
                           horario_ocioso_id=b["horario_ocioso_id"],
                           cadeira_id=b["cadeira_id"],
                           barbeiro_id=b["barbeiro_id"], periodo=_periodo(b),
                           valor_centavos=b["valor_centavos"])
            for b in con.execute(
                "SELECT * FROM blocos WHERE barbearia_id = ? "
                "ORDER BY inicio, id", (barbearia.id,))]
        return barbearia


def _data(valor):
    return valor.isoformat()


def _periodo(linha):
    return Periodo(datetime.fromisoformat(linha["inicio"]),
                   datetime.fromisoformat(linha["fim"]))


class RepositorioDeServicosSQLite(RepositorioDeServicos):
    def __init__(self, banco):
        self._banco = banco

    def salvar(self, servico):
        with self._banco.conexao() as con:
            con.execute(
                "INSERT INTO servicos (id, barbeiro_id, nome, preco_centavos,"
                " duracao_minutos) VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET nome = excluded.nome, "
                "preco_centavos = excluded.preco_centavos, "
                "duracao_minutos = excluded.duracao_minutos",
                (servico.id, servico.barbeiro_id, servico.nome,
                 servico.preco_centavos, servico.duracao_minutos))

    def por_id(self, servico_id):
        encontrados = self._consultar("id = ?", servico_id)
        return encontrados[0] if encontrados else None

    def do_barbeiro(self, barbeiro_id):
        return self._consultar("barbeiro_id = ?", barbeiro_id)

    def _consultar(self, filtro, *parametros):
        with self._banco.conexao() as con:
            linhas = con.execute(
                "SELECT * FROM servicos WHERE {} ORDER BY nome, id".format(
                    filtro), parametros).fetchall()
        return [Servico(id=s["id"], barbeiro_id=s["barbeiro_id"],
                        nome=s["nome"], preco_centavos=s["preco_centavos"],
                        duracao_minutos=s["duracao_minutos"])
                for s in linhas]


class RepositorioDeAgendamentosSQLite(RepositorioDeAgendamentos):
    def __init__(self, banco):
        self._banco = banco

    def salvar(self, agendamento):
        a = agendamento
        with self._banco.conexao() as con:
            con.execute(
                "INSERT OR REPLACE INTO agendamentos (id, cliente_id, "
                "barbeiro_id, servico_id, servico_nome, barbearia_id, "
                "bloco_id, inicio, fim, preco_centavos) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (a.id, a.cliente_id, a.barbeiro_id, a.servico_id,
                 a.servico_nome, a.barbearia_id, a.bloco_id,
                 _data(a.periodo.inicio), _data(a.periodo.fim),
                 a.preco_centavos))

    def do_barbeiro(self, barbeiro_id):
        return self._consultar("barbeiro_id = ?", barbeiro_id)

    def do_cliente(self, cliente_id):
        return self._consultar("cliente_id = ?", cliente_id)

    def _consultar(self, filtro, *parametros):
        with self._banco.conexao() as con:
            linhas = con.execute(
                "SELECT * FROM agendamentos WHERE {} "
                "ORDER BY inicio, id".format(filtro), parametros).fetchall()
        return [Agendamento(
            id=a["id"], cliente_id=a["cliente_id"],
            barbeiro_id=a["barbeiro_id"], servico_id=a["servico_id"],
            servico_nome=a["servico_nome"], barbearia_id=a["barbearia_id"],
            bloco_id=a["bloco_id"], periodo=_periodo(a),
            preco_centavos=a["preco_centavos"]) for a in linhas]

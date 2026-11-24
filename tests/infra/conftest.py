import pytest

from infra.db.database import BancoSQLite
from infra.repositories import memoria, sqlite


@pytest.fixture(params=["memoria", "sqlite"])
def repos(request, tmp_path):
    """Os dois adapters de cada porta, para a mesma suíte de contrato."""
    if request.param == "memoria":
        return {
            "usuarios": memoria.RepositorioDeUsuariosEmMemoria(),
            "barbearias": memoria.RepositorioDeBarbeariasEmMemoria(),
            "servicos": memoria.RepositorioDeServicosEmMemoria(),
            "agendamentos": memoria.RepositorioDeAgendamentosEmMemoria(),
        }
    banco = BancoSQLite(str(tmp_path / "teste.sqlite3"))
    banco.criar_tabelas()
    return {
        "usuarios": sqlite.RepositorioDeUsuariosSQLite(banco),
        "barbearias": sqlite.RepositorioDeBarbeariasSQLite(banco),
        "servicos": sqlite.RepositorioDeServicosSQLite(banco),
        "agendamentos": sqlite.RepositorioDeAgendamentosSQLite(banco),
    }

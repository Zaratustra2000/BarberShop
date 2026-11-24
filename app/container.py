"""Composition root: o único lugar que conhece as classes concretas.

Aqui os adapters de infraestrutura são ligados às portas que os casos de uso
esperam. Trocar SQLite por outro banco significa mudar apenas este arquivo.
"""
from infra.db.database import BancoSQLite
from infra.fotos import ArmazenamentoDeFotosLocal
from infra.repositories import sqlite
from infra.seguranca import GeradorDeHashWerkzeug, RelogioDoSistema
from infra.validador_de_fotos import ValidadorDeFotosPillow
from use_cases.agendar_atendimento import AgendarAtendimento
from use_cases.autenticar_usuario import AutenticarUsuario
from use_cases.buscar_barbeiros import BuscarBarbeiros
from use_cases.buscar_cadeiras_ociosas import BuscarCadeirasOciosas
from use_cases.cadastrar_barbearia import CadastrarBarbearia
from use_cases.cadastrar_servico import (CadastrarServico,
                                         ConsultarServicosDoBarbeiro)
from use_cases.cadastrar_usuario import CadastrarUsuario
from use_cases.consultar_barbearias_do_dono import ConsultarBarbeariasDoDono
from use_cases.consultar_agenda_do_barbeiro import ConsultarAgendaDoBarbeiro
from use_cases.consultar_agendamentos_do_cliente import (
    ConsultarAgendamentosDoCliente)
from use_cases.consultar_perfil_do_barbeiro import ConsultarPerfilDoBarbeiro
from use_cases.consultar_perfil_da_barbearia import ConsultarPerfilDaBarbearia
from use_cases.editar_perfil_da_barbearia import (
    EditarPerfilDaBarbearia, SubstituirFotoPrincipalDaBarbearia)
from use_cases.editar_horario_ocioso import EditarHorarioOcioso
from use_cases.gerenciar_barbearia import GerenciarBarbearia
from use_cases.publicar_horario_ocioso import PublicarHorarioOcioso
from use_cases.reservar_bloco_de_horario import ReservarBlocoDeHorario
from use_cases.validar_foto_da_barbearia import ValidarFotoDaBarbearia


class Container:
    def __init__(self, caminho_do_banco, relogio=None,
                 diretório_de_fotos=None):
        banco = BancoSQLite(caminho_do_banco)
        banco.criar_tabelas()
        self.relogio = relogio or RelogioDoSistema()
        usuarios = sqlite.RepositorioDeUsuariosSQLite(banco)
        gerador_de_hash = GeradorDeHashWerkzeug()

        barbearias = sqlite.RepositorioDeBarbeariasSQLite(banco)
        servicos = sqlite.RepositorioDeServicosSQLite(banco)
        agendamentos = sqlite.RepositorioDeAgendamentosSQLite(banco)
        diretório_de_fotos = diretório_de_fotos or "instance/fotos-barbearias"
        self.fotos = ArmazenamentoDeFotosLocal(diretório_de_fotos)
        self.validar_foto_da_barbearia = ValidarFotoDaBarbearia(
            ValidadorDeFotosPillow())

        self.usuarios = usuarios
        self.cadastrar_barbearia = CadastrarBarbearia(usuarios, barbearias)
        self.consultar_barbearias_do_dono = ConsultarBarbeariasDoDono(
            barbearias)
        self.editar_perfil_da_barbearia = EditarPerfilDaBarbearia(
            usuarios, barbearias)
        self.gerenciar_barbearia = GerenciarBarbearia(
            usuarios, barbearias)
        self.substituir_foto_principal = SubstituirFotoPrincipalDaBarbearia(
            usuarios, barbearias, self.fotos)
        self.consultar_perfil_da_barbearia = ConsultarPerfilDaBarbearia(
            barbearias)
        self.publicar_horario_ocioso = PublicarHorarioOcioso(
            barbearias, self.relogio)
        self.editar_horario_ocioso = EditarHorarioOcioso(
            usuarios, barbearias, self.relogio)
        self.cadastrar_servico = CadastrarServico(usuarios, servicos)
        self.consultar_servicos_do_barbeiro = ConsultarServicosDoBarbeiro(
            servicos)
        self.buscar_cadeiras_ociosas = BuscarCadeirasOciosas(
            barbearias, self.relogio)
        self.reservar_bloco_de_horario = ReservarBlocoDeHorario(
            usuarios, barbearias, self.relogio)
        self.consultar_agenda_do_barbeiro = ConsultarAgendaDoBarbeiro(
            usuarios, barbearias, agendamentos)
        self.buscar_barbeiros = BuscarBarbeiros(usuarios)
        self.consultar_perfil_do_barbeiro = ConsultarPerfilDoBarbeiro(
            usuarios, barbearias, servicos, agendamentos, self.relogio)
        self.agendar_atendimento = AgendarAtendimento(
            usuarios, barbearias, servicos, agendamentos, self.relogio)
        self.consultar_agendamentos_do_cliente = (
            ConsultarAgendamentosDoCliente(usuarios, barbearias,
                                           agendamentos))
        self.cadastrar_usuario = CadastrarUsuario(usuarios, gerador_de_hash)
        self.autenticar_usuario = AutenticarUsuario(usuarios,
                                                    gerador_de_hash)

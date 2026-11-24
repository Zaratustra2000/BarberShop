"""Agregado Barbearia: cadeiras, horários ociosos e blocos (ADR 0001)."""
import unicodedata
from dataclasses import dataclass, field
from typing import List

from domain.erros import ConflitoDeHorario, DadosInvalidos, NaoEncontrado
from domain.identidade import novo_id
from domain.periodo import Periodo


def normalizar_bairro(bairro: str) -> str:
    """'Jardim Botânico ' e 'jardim botanico' viram a mesma chave de busca."""
    sem_acento = unicodedata.normalize("NFKD", bairro or "")
    sem_acento = "".join(c for c in sem_acento
                         if not unicodedata.combining(c))
    return " ".join(sem_acento.lower().split())


@dataclass
class Cadeira:
    nome: str
    id: str = field(default_factory=novo_id)


@dataclass
class HorarioOcioso:
    cadeira_id: str
    periodo: Periodo
    preco_por_hora_centavos: int
    id: str = field(default_factory=novo_id)


@dataclass
class BlocoDeHorario:
    horario_ocioso_id: str
    cadeira_id: str
    barbeiro_id: str
    periodo: Periodo
    valor_centavos: int
    id: str = field(default_factory=novo_id)


def valor_do_bloco(preco_por_hora_centavos: int, minutos: int) -> int:
    """Preço proporcional à duração, arredondado ao centavo mais próximo."""
    return (preco_por_hora_centavos * minutos + 30) // 60


@dataclass
class Barbearia:
    dono_id: str
    nome: str
    endereco: str
    bairro: str
    latitude: float
    longitude: float
    regras: str = ""
    foto_principal: str = ""
    cadeiras: List[Cadeira] = field(default_factory=list)
    horarios_ociosos: List[HorarioOcioso] = field(default_factory=list)
    blocos: List[BlocoDeHorario] = field(default_factory=list)
    id: str = field(default_factory=novo_id)

    def __post_init__(self):
        for campo, rotulo in (("nome", "o nome"), ("endereco", "o endereço"),
                              ("bairro", "o bairro")):
            valor = (getattr(self, campo) or "").strip()
            if not valor:
                raise DadosInvalidos("Informe {}.".format(rotulo))
            setattr(self, campo, valor)
        self.regras = (self.regras or "").strip()
        if not -90 <= self.latitude <= 90 or not -180 <= self.longitude <= 180:
            raise DadosInvalidos("Marque a localização no mapa.")

    @property
    def bairro_chave(self) -> str:
        return normalizar_bairro(self.bairro)

    def pertence_a(self, dono_id: str) -> bool:
        return self.dono_id == dono_id

    def editar(self, nome: str, endereco: str, bairro: str, latitude: float,
               longitude: float, regras: str) -> None:
        self.nome = nome
        self.endereco = endereco
        self.bairro = bairro
        self.latitude = latitude
        self.longitude = longitude
        self.regras = regras
        self.__post_init__()

    def definir_foto_principal(self, nome_do_arquivo: str) -> None:
        self.foto_principal = nome_do_arquivo

    def adicionar_cadeira(self) -> Cadeira:
        cadeira = Cadeira(nome="Cadeira {}".format(len(self.cadeiras) + 1))
        self.cadeiras.append(cadeira)
        return cadeira

    def remover_cadeira(self, cadeira_id: str) -> None:
        cadeira = self.cadeira(cadeira_id)
        if any(h.cadeira_id == cadeira.id for h in self.horarios_ociosos):
            raise ConflitoDeHorario(
                "Não é possível remover uma cadeira com horários ociosos.")
        if any(b.cadeira_id == cadeira.id for b in self.blocos):
            raise ConflitoDeHorario(
                "Não é possível remover uma cadeira com blocos de horário.")
        self.cadeiras.remove(cadeira)
        for posicao, existente in enumerate(self.cadeiras, start=1):
            existente.nome = "Cadeira {}".format(posicao)

    def cadeira(self, cadeira_id: str) -> Cadeira:
        for cadeira in self.cadeiras:
            if cadeira.id == cadeira_id:
                return cadeira
        raise NaoEncontrado("Cadeira não encontrada nesta barbearia.")

    def publicar_horario_ocioso(self, cadeira_id: str, periodo: Periodo,
                                preco_por_hora_centavos: int
                                ) -> HorarioOcioso:
        self.cadeira(cadeira_id)
        if preco_por_hora_centavos <= 0:
            raise DadosInvalidos("O preço por hora precisa ser positivo.")
        for existente in self.horarios_ociosos:
            if (existente.cadeira_id == cadeira_id
                    and existente.periodo.sobrepoe(periodo)):
                raise ConflitoDeHorario(
                    "Esta cadeira já tem um horário ocioso nesse período.")
        horario = HorarioOcioso(cadeira_id, periodo, preco_por_hora_centavos)
        self.horarios_ociosos.append(horario)
        return horario

    def horario_ocioso(self, horario_ocioso_id: str) -> HorarioOcioso:
        for horario in self.horarios_ociosos:
            if horario.id == horario_ocioso_id:
                return horario
        raise NaoEncontrado("Horário ocioso não encontrado.")

    def periodos_livres(self, horario_ocioso_id: str) -> List[Periodo]:
        horario = self.horario_ocioso(horario_ocioso_id)
        return horario.periodo.subtrair(
            b.periodo for b in self.blocos
            if b.cadeira_id == horario.cadeira_id)

    def reservar_bloco(self, horario_ocioso_id: str, barbeiro_id: str,
                       periodo: Periodo) -> BlocoDeHorario:
        horario = self.horario_ocioso(horario_ocioso_id)
        if not horario.periodo.contem(periodo):
            raise DadosInvalidos(
                "O bloco precisa caber dentro do horário ocioso.")
        for bloco in self.blocos:
            if (bloco.cadeira_id == horario.cadeira_id
                    and bloco.periodo.sobrepoe(periodo)):
                raise ConflitoDeHorario(
                    "Já existe um bloco reservado nessa cadeira e período.")
        bloco = BlocoDeHorario(
            horario_ocioso_id=horario.id, cadeira_id=horario.cadeira_id,
            barbeiro_id=barbeiro_id, periodo=periodo,
            valor_centavos=valor_do_bloco(horario.preco_por_hora_centavos,
                                          periodo.minutos))
        self.blocos.append(bloco)
        return bloco

    def blocos_do_barbeiro(self, barbeiro_id: str) -> List[BlocoDeHorario]:
        return [b for b in self.blocos if b.barbeiro_id == barbeiro_id]

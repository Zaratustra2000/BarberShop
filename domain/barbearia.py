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
class Barbearia:
    dono_id: str
    nome: str
    endereco: str
    bairro: str
    latitude: float
    longitude: float
    regras: str = ""
    cadeiras: List[Cadeira] = field(default_factory=list)
    horarios_ociosos: List[HorarioOcioso] = field(default_factory=list)
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

    def adicionar_cadeira(self) -> Cadeira:
        cadeira = Cadeira(nome="Cadeira {}".format(len(self.cadeiras) + 1))
        self.cadeiras.append(cadeira)
        return cadeira

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

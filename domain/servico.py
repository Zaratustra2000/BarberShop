from dataclasses import dataclass, field

from domain.erros import DadosInvalidos
from domain.identidade import novo_id

DURACAO_MINIMA = 5
DURACAO_MAXIMA = 240


@dataclass
class Servico:
    barbeiro_id: str
    nome: str
    preco_centavos: int
    duracao_minutos: int
    id: str = field(default_factory=novo_id)

    def __post_init__(self):
        self.nome = (self.nome or "").strip()
        if not self.nome:
            raise DadosInvalidos("Informe o nome do serviço.")
        if self.preco_centavos <= 0:
            raise DadosInvalidos("O preço do serviço precisa ser positivo.")
        if not DURACAO_MINIMA <= self.duracao_minutos <= DURACAO_MAXIMA:
            raise DadosInvalidos("A duração precisa ficar entre {} e {} "
                                 "minutos.".format(DURACAO_MINIMA,
                                                   DURACAO_MAXIMA))

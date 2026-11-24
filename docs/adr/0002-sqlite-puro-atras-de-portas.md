# SQLite com `sqlite3` puro, atrás de portas de repositório

As portas de repositório (`use_cases/portas.py`) são classes abstratas da camada
de casos de uso, e a infraestrutura as implementa (inversão de dependência). Há
dois adapters para cada porta: em memória (testes de casos de uso) e SQLite
(aplicação). Escolhemos o módulo `sqlite3` da biblioteca padrão em vez de um ORM
como o SQLAlchemy para que nenhuma anotação de framework entre nas entidades de
domínio e para manter a dependência de infraestrutura pequena. Uma única suíte
de contrato (`tests/infra/test_contrato_repositorios.py`) roda contra os dois
adapters e garante que eles se comportam igual.

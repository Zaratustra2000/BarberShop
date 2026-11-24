from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from use_cases.portas import GeradorDeHashDeSenha, Relogio


class GeradorDeHashWerkzeug(GeradorDeHashDeSenha):
    """Hash de senha com sal.

    PBKDF2-SHA256 explícito: o padrão do Werkzeug (scrypt) não existe no
    Python do macOS, que é compilado com LibreSSL.
    """

    def gerar(self, senha):
        return generate_password_hash(senha, method="pbkdf2:sha256")

    def conferir(self, senha, senha_hash):
        return check_password_hash(senha_hash, senha)


class RelogioDoSistema(Relogio):
    def agora(self):
        return datetime.now().replace(second=0, microsecond=0)

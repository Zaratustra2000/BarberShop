"""Ponto de entrada Flask (camada Frameworks & Drivers)."""
import os
import secrets

from flask import Flask, flash, redirect, render_template, request

from app.container import Container
from app.formatos import registrar_filtros
from app.routes import (auth_routes, barbeiro_routes, cliente_routes,
                        dono_routes)
from domain.erros import AcessoNegado, ErroDeDominio, NaoEncontrado


def create_app(caminho_do_banco=None, relogio=None, secret_key=None):
    app = Flask(__name__)
    app.secret_key = (secret_key or os.environ.get("SECRET_KEY")
                      or secrets.token_hex(32))
    caminho_do_banco = caminho_do_banco or os.environ.get(
        "BARBERSHOP_DB", os.path.join(app.instance_path, "barbershop.sqlite3"))
    os.makedirs(os.path.dirname(os.path.abspath(caminho_do_banco)),
                exist_ok=True)
    app.extensions["barbershop"] = Container(caminho_do_banco, relogio)

    for modulo in (auth_routes, dono_routes, barbeiro_routes, cliente_routes):
        app.register_blueprint(modulo.bp)
    registrar_filtros(app)
    _registrar_tratamento_de_erros(app)
    return app


def _registrar_tratamento_de_erros(app):
    @app.errorhandler(AcessoNegado)
    def acesso_negado(erro):
        return render_template("erro.html", mensagem=str(erro)), 403

    @app.errorhandler(NaoEncontrado)
    def nao_encontrado(erro):
        return render_template("erro.html", mensagem=str(erro)), 404

    @app.errorhandler(ErroDeDominio)
    def regra_violada(erro):
        """Regra de negócio violada: volta ao formulário com a mensagem."""
        flash(str(erro), "erro")
        return redirect(request.referrer or request.path)

    @app.errorhandler(403)
    def proibido(_erro):
        return render_template(
            "erro.html", mensagem="Esta página é de outra persona."), 403


if __name__ == "__main__":
    create_app().run(debug=True)

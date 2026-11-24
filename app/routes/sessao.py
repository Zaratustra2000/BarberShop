"""Helpers de sessão e de acesso por persona, compartilhados pelas rotas."""
from functools import wraps

from flask import abort, current_app, redirect, session, url_for


def container():
    return current_app.extensions["barbershop"]


def entrar(usuario):
    session.clear()
    session["usuario_id"] = usuario.id
    session["papel"] = usuario.papel.value
    session["nome"] = usuario.nome


def usuario_id():
    return session.get("usuario_id")


def requer_papel(papel):
    """Exige login e a persona certa; outra persona recebe 403."""
    def decorador(view):
        @wraps(view)
        def protegida(*args, **kwargs):
            if usuario_id() is None:
                return redirect(url_for("auth.login"))
            if session.get("papel") != papel:
                abort(403)
            return view(*args, **kwargs)
        return protegida
    return decorador
